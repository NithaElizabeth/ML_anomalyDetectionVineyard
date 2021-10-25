"""
Counts the number of trees in a video.
"""

# import necessary modules
from tracker.utils import utils
from tracker.utils import sort_updated as mot_tracker
from tracker.utils.line import Point, Line, intersect
import os, platform
import argparse
import logging
import coloredlogs
import datetime
import numpy as np
import cv2
import json

"""
detect_video: Detects the location(bounding box of the objects in an video)

Input:
------
    input_video: The input image for which we have to perform the detections

Output:
------
"""


def detect_video(input_video):

    # Read the configuration parameters from the config.json file
    with open('./tracker/data/config.json', 'r') as f:
        config_params = json.load(f)

    # Load the network
    net = cv2.dnn.readNetFromDarknet(config_params["detector"]["config"],
                                     config_params["detector"]["weights"])                 # Load the YOLOv4 detector with given config and weights
    net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
    net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)
    logging.info('Successfully loaded the network.')

    # Get the output layer from YOLO
    layers = net.getLayerNames()
    output_layers = [layers[i[0] - 1] for i in net.getUnconnectedOutLayers()]

    # Get the class names for the network
    with open(config_params["detector"]["labels"], 'r') as f:
        classes = [line.strip() for line in f.readlines()]

    # Confidence and NMS thresholds for filtering detections
    CONF_THRESH, NMS_THRESH = float(config_params["detector"]["confidence"]), float(
        config_params["detector"]["nms-thresh"])

    cap = cv2.VideoCapture(input_video)

    while True:
        ret, img = cap.read()

        if not ret:
            break

        # Resize the image to 800x600 resolution
        img = cv2.resize(img, (1280, 720))
        # Get the height and width of the image (Redundant for now, since we fix it)
        height, width = img.shape[:2]

        # A list containing the information about the detected objects
        detected_items = []

        logging.info(
            "{}: Generated the blob from the input image.".format(__name__))

        # Construct a blob from the given image
        blob = cv2.dnn.blobFromImage(
            img, 0.00392, (608, 608), swapRB=True, crop=False)
        # Set the blob as input to the network
        net.setInput(blob)
        # Perform a single forward pass to get the detections
        layer_outputs = net.forward(output_layers)
        logging.info(
            "{}: Performed the forward pass for the blob.".format(__name__))

        class_ids, confidences, b_boxes = [], [], []

        # Loop through each detection
        for output in layer_outputs:
            for detection in output:
                scores = detection[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]

                # Create the bounding box with the detection
                center_x, center_y, w, h = (
                    detection[0:4] * np.array([width, height, width, height])).astype('int')
                x = int(center_x - w / 2)
                y = int(center_y - h / 2)
                b_boxes.append([x, y, int(w), int(h)])
                confidences.append(float(confidence))
                class_ids.append(int(class_id))

        # Perform non-maxima suppression to filter the bounding boxes
        try:
            indices = cv2.dnn.NMSBoxes(
                b_boxes, confidences, CONF_THRESH, NMS_THRESH).flatten().tolist()
        except AttributeError:
            pass

        # Draw the filtered bounding boxes on the image
        for index in indices:
            x, y, w, h = b_boxes[index]

            text = "{}: {:.2f}".format(
                classes[class_ids[index]], confidences[index])
            detected_items.append([x, y, x+w, y+h, confidences[index]])
            cv2.rectangle(img, (x, y), (x+w, y+h),
                          (255, 0, 255), 1, cv2.LINE_AA)
            cv2.putText(img, text, (x, y), int(config_params["font"]["style"]),
                        float(config_params["font"]["scale"]),
                        (255, 0, 255),
                        int(config_params["font"]["thickness"]))

        cv2.imshow("Frame", img)

        logging.info("{}: {} objects were detected".format(
            __name__, len(indices)))
        logging.debug("{}: Detected Items: \n{}".format(
            __name__, detected_items))

        if cv2.waitKey(1) & 0xFF == 27:
            break

    cap.release()
    cv2.destroyAllWindows()


"""
track_video: Detects and tracks the position of the object in the video

Input:
------
    input_video: The input image for which we have to perform the detections

Output:
------
"""


def track_video(input_video, right_rank, left_rank):

    # Clean up the input filename for logging
    try:
        last_index = input_video.rindex('/')            # NOTE: This fails on Windows (throws ValueError)
    except ValueError as e:
        last_index = input_video.rindex('\\')
        logging.warn("Exception: {} occured".format(e))

    assert last_index > -4
    output_suffix = input_video[last_index+1:-4]

    parcelleName = output_suffix.split("_")[1] + "_" + output_suffix.split("_")[2]

    # Read the config.json file to extract the parameters
    with open('./tracker/data/config.json', 'r') as f:
        config_params = json.load(f)

 # Get information about the system for os-specific commands
    pf = platform.system()
    logging.info("System OS: {}".format(pf))

    frames_list = []
    # Load the network
    # Load the YOLOv4 detector with given config and weights
    net = cv2.dnn.readNetFromDarknet(
        config_params["detector"]["config"], config_params["detector"]["weights"])
    net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
    net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)
    logging.info('Successfully loaded the network.')

    # Get the output layer from YOLO
    layers = net.getLayerNames()
    output_layers = [layers[i[0] - 1] for i in net.getUnconnectedOutLayers()]

    # Get the class names for the network
    with open(config_params["detector"]["labels"], 'r') as f:
        classes = [line.strip() for line in f.readlines()]

    # Instantiate the SORT tracker
    tracker = mot_tracker.Sort(float(config_params["tracker"]["max-age"]),
                               float(config_params["tracker"]["min-hits"]),
                               float(config_params["tracker"]["iou-thresh"]))

    # Confidence and NMS thresholds for filtering detections
    CONF_THRESH, NMS_THRESH = float(config_params["detector"]["confidence"]), float(
        config_params["detector"]["nms-thresh"])

    # Frame counter
    i = 0

    # Initialise the VideoCapture object
    cap = cv2.VideoCapture(input_video)

    # Initialise the VideoWriter object (comment out if you do not want video)
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    video_filename = "output/" + output_suffix + ".mp4"

    # if pf == "Windows":
    #     video_name = input_video[input_video.rindex('\\')+1: -4]
    #     print(f"Video Name: {video_name}")
    #     video_filename = "output/" + video_name + ".mp4"
    # elif pf == "Linux":
    #     video_name = input_video[input_video.rindex('/')+1: -4]
    #     print(f"Video name: {video_name}")
    #     video_filename = "output/" + video_name + ".mp4"
    # else:
    #     video_filename = "output/generic-name.mp4"
    #     print(video_filename)

    out = cv2.VideoWriter(video_filename, fourcc, 25.0, (800, 600))

    while True:

        ret, img = cap.read()
        i += 1
        if not ret:
            break

        # Resize the image to 800x600 resolution
        img = cv2.resize(img, (800, 600), interpolation=cv2.INTER_AREA)
        # Get the height and width of the image (Redundant for now, since we fix it)
        height, width = img.shape[:2]

        # A list containing the information about the detected objects
        dets, tree_dets, wp_dets, mp_dets = [], [], [], []

        logging.info(
            "{}: Generated the blob from the input image.".format(__name__))
        # Construct a blob from the given image
        blob = cv2.dnn.blobFromImage(
            img, 0.00392, (416, 416), swapRB=True, crop=False)
        # Set the blob as input to the network
        net.setInput(blob)
        # Perform a single forward pass to get the detections
        layer_outputs = net.forward(output_layers)

        logging.info(
            "{}: Performed the forward pass for the blob.".format(__name__))

        class_ids, confidences, b_boxes = [], [], []

        # Loop through each detection
        for output in layer_outputs:
            for detection in output:

                scores = detection[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]

                # Create the bounding box with the detection
                center_x, center_y, w, h = (
                    detection[0:4] * np.array([width, height, width, height])).astype('int')
                x = int(center_x - (w / 2))
                y = int(center_y - (h / 2))
                b_boxes.append([x, y, int(w), int(h)])
                confidences.append(float(confidence))
                class_ids.append(int(class_id))

        # Perform non-maxima suppression to filter the bounding boxes
        try:
            indices = cv2.dnn.NMSBoxes(
                b_boxes, confidences, CONF_THRESH, NMS_THRESH).flatten().tolist()
        except AttributeError as e:
            logging.warning(f"Exception: {e}")
            pass

        try:
            # Draw the filtered bounding boxes on the image
            for index in indices:
                x, y, w, h = b_boxes[index]
                dets.append([x, y, x+w, y+h, confidences[index], class_ids[index]])
                text = classes[class_ids[index]]
                cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 1, cv2.LINE_AA)
                cv2.putText(img, text, (x, y+h), int(config_params["font"]["style"]), float(
                    config_params["font"]["scale"]), (255, 0, 255), int(config_params["font"]["thickness"]), cv2.LINE_AA)
            logging.info("{}: {} objects were detected".format(
            __name__, len(indices)))
        except UnboundLocalError as e:
            logging.warning(f"Exception: {e}")
            pass

        dets = np.asarray(dets).astype("int")

        # Keep a track of the previous frame for detections
        tree_dets = np.asarray(tree_dets).astype("int")
        logging.debug("{}: Detected trees: \n{}".format(__name__, tree_dets))

        tracks = tracker.update(dets)

        tracks_list = []

        # Tracker returns a numpy array in the format (x1, y1, x2, y2, score, class_id)
        for track in tracks:
            x1 = int(track[0])
            y1 = int(track[1])
            x2 = int(track[2])
            y2 = int(track[3])

            obj, dir = "", ""

            bb = [x1, y1, x2, y2]

            try:
                obj = classes[int(track[5])]
            except ValueError:
                pass

            # Find out the centroid of the object
            centroid_x, centroid_y = int(
                (track[0]+track[2])/2), int((track[1]+track[3])/2)

            # TODO Implement the weighted average
            # for determining the left and right
            if left_rank == "0" or left_rank == "00":         # Edge case: Only right rank
                dir = "right"
                rank = right_rank

            elif right_rank == "0" or right_rank == "00":     # Edge case: Only left rank
                dir = "left"
                rank = left_rank

            elif centroid_x < int(width/2):
                dir = "left"
                rank = left_rank
            else:
                dir = "right"
                rank = right_rank

            cv2.rectangle(img, (x1, y1), (x2, y2),
                          (255, 255, 255), 1, cv2.LINE_AA)

            text = "{}: {}".format(classes[int(track[5])], int(track[4]))
            cv2.putText(img, text, (centroid_x, centroid_y),
                        cv2.FONT_HERSHEY_DUPLEX, 0.5, (0, 0, 0), 1, cv2.LINE_AA)

            track_obj = {
                "id": str(int(track[4])),
                "class": obj,
                "rank": rank,
                "direction": dir,
                "centroid": "{},{}".format(centroid_x, centroid_y),
                "bbox": "{},{},{},{}".format(bb[0], bb[1], bb[2], bb[3])
            }

            tracks_list.append(track_obj)

        frame_obj = {
            "frame {}".format(i): tracks_list
        }
        tracks_list = []
        frames_list.append(frame_obj)

        cv2.putText(img, "Frame: {}".format(i), (2, 595),
                    cv2.FONT_HERSHEY_DUPLEX, 0.5, (255, 255, 255), 1, cv2.LINE_AA)
        cv2.imshow("Output", img)
        out.write(img)

        if cv2.waitKey(1) & 0xFF == 27:
            break

    # Release the VideoCapture object and destroy all windows
    cap.release()
    cv2.destroyAllWindows()

    # Write the json output

    if not os.path.exists('./tracker/data/test/{}'.format(parcelleName)):
        os.makedirs('./tracker/data/test/{}'.format(parcelleName))
    with open('./tracker/data/test/{}/detections-{}.json'.format(parcelleName , output_suffix), 'w') as f:
        json.dump(frames_list, f, indent=4)

    if frames_list is None:
        return False
    else:
        return True


"""
count_trees: Counts the number of vines in the vineyard

Input:
------
    input_video: The input image for which we have to perform the detections

Output:
------
"""


def count_trees(input_video, right_rank, left_rank):
    # Read the config.json file to extract the parameters
    with open('data/config.json', 'r') as f:
        config_params = json.load(f)

    frames_list = []
    # Load the network
    # Load the YOLOv4 detector with given config and weights
    net = cv2.dnn.readNetFromDarknet(
        config_params["detector"]["config"], config_params["detector"]["weights"])
    net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
    net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)
    logging.info('Successfully loaded the network.')

    # Get the output layer from YOLO
    layers = net.getLayerNames()
    print(layers)
    output_layers = [layers[i[0] - 1] for i in net.getUnconnectedOutLayers()]

    # Get the class names for the network
    with open(config_params["detector"]["labels"], 'r') as f:
        classes = [line.strip() for line in f.readlines()]

    # Instantiate the SORT tracker
    tracker = mot_tracker.Sort(float(config_params["tracker"]["max-age"]),
                               float(config_params["tracker"]["min-hits"]),
                               float(config_params["tracker"]["iou-thresh"]))

    # Confidence and NMS thresholds for filtering detections
    CONF_THRESH, NMS_THRESH = float(config_params["detector"]["confidence"]), float(
        config_params["detector"]["nms-thresh"])

    i, tree_count_left, tree_count_right = 0, 0, 0

    cap = cv2.VideoCapture(input_video)

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    video_filename = "output/" + input_video[-12:-4] + ".mp4"

    out = cv2.VideoWriter(video_filename, fourcc, 25.0, (800, 600))

    while True:

        ret, img = cap.read()
        i += 1
        if not ret:
            break

        # Resize the image to 800x600 resolution
        img = cv2.resize(img, (800, 600), interpolation=cv2.INTER_AREA)
        # Get the height and width of the image (Redundant for now, since we fix it)
        height, width = img.shape[:2]

        # A list containing the information about the detected objects
        dets, tree_dets, wp_dets, mp_dets = [], [], [], []

        logging.info(
            "{}: Generated the blob from the input image.".format(__name__))
        # Construct a blob from the given image
        blob = cv2.dnn.blobFromImage(
            img, 0.00392, (416, 416), swapRB=True, crop=False)
        # Set the blob as input to the network
        net.setInput(blob)
        # Perform a single forward pass to get the detections
        layer_outputs = net.forward(output_layers)

        # Left and Right lines for drawing
        left_line = Line(Point(0, 150), Point(250, 600))
        right_line = Line(Point(800, 150), Point(550, 600))

        logging.info(
            "{}: Performed the forward pass for the blob.".format(__name__))

        class_ids, confidences, b_boxes = [], [], []

        # Loop through each detection
        for output in layer_outputs:
            for detection in output:

                scores = detection[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]

                # Create the bounding box with the detection
                center_x, center_y, w, h = (
                    detection[0:4] * np.array([width, height, width, height])).astype('int')
                x = int(center_x - (w / 2))
                y = int(center_y - (h / 2))
                b_boxes.append([x, y, int(w), int(h)])
                confidences.append(float(confidence))
                class_ids.append(int(class_id))

        # Perform non-maxima suppression to filter the bounding boxes
        try:
            indices = cv2.dnn.NMSBoxes(
                b_boxes, confidences, CONF_THRESH, NMS_THRESH).flatten().tolist()
        except AttributeError:
            pass

        # Draw the filtered bounding boxes on the image
        for index in indices:
            x, y, w, h = b_boxes[index]

            if classes[class_ids[index]] == "tree":
                dets.append(
                    [x, y, x+w, y+h, confidences[index], class_ids[index]])
            #text = classes[class_ids[index]]
            #cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 1, cv2.LINE_AA)
            #cv2.putText(img, text, (x, y+h), int(config_params["font"]["style"]), float(config_params["font"]["scale"]), (255, 0, 255), int(config_params["font"]["thickness"]))

        logging.info("{}: {} objects were detected".format(
            __name__, len(indices)))

        dets = np.asarray(dets).astype("int")

        # Keep a track of the previous frame for detections
        tree_dets = np.asarray(tree_dets).astype("int")
        logging.debug("{}: Detected trees: \n{}".format(__name__, tree_dets))

        tracks = tracker.update(dets)

        tracks_list = []

        for track in tracks:
            x1 = int(track[0])
            y1 = int(track[1])
            x2 = int(track[2])
            y2 = int(track[3])

            obj, dir = "", ""

            bb = [x1, y1, x2, y2]

            try:
                obj = classes[int(track[5])]
            except ValueError:
                pass

            # Find out the centroid of the object
            centroid_x, centroid_y = int(
                (track[0]+track[2])/2), int((track[1]+track[3])/2)

            line_centroid = Line(
                Point(centroid_x, centroid_y - 5), Point(centroid_x, centroid_y + 5))

            # Draw a small line segment along the centroid
            cv2.line(img, line_centroid.start.get_point(),
                     line_centroid.end.get_point(), (0, 255, 0), 2, cv2.LINE_AA)

            cv2.rectangle(img, (x1, y1), (x2, y2),
                          (255, 255, 255), 1, cv2.LINE_AA)

            text = "{}: {}".format(classes[int(track[5])], int(track[4]))
            cv2.putText(img, text, (int(x1), int(
                y1)), cv2.FONT_HERSHEY_DUPLEX, 0.35, (255, 255, 0), 1, cv2.LINE_AA)

            # Add intersection of Line code here
            status_left, intersection_left = intersect(
                line_centroid, left_line)
            status_right, intersection_right = intersect(
                line_centroid, right_line)

            if status_left == True:
                tree_count_left += 1

            if status_right == True:
                tree_count_right += 1

        cv2.putText(img, "Frame: {}".format(i), (2, 25),
                    cv2.FONT_HERSHEY_DUPLEX, 0.5, (0, 0, 0), 1)
        cv2.putText(img, "Right: {}".format(tree_count_right), (704, 50),
                    cv2.FONT_HERSHEY_DUPLEX, 0.5, (255, 128, 64), 1, cv2.LINE_AA)
        cv2.putText(img, "Left: {}".format(tree_count_left), (4, 50),
                    cv2.FONT_HERSHEY_DUPLEX, 0.5, (64, 64, 128), 1, cv2.LINE_AA)

        cv2.line(img, left_line.start.get_point(),
                 left_line.end.get_point(), (0, 0, 255), 2)     # Left line
        cv2.line(img, right_line.start.get_point(),
                 right_line.end.get_point(), (0, 0, 255), 2)   # Right line
        cv2.imshow("Output", img)
        out.write(img)

        if cv2.waitKey(1) & 0xFF == 27:
            break

    # Release the VideoCapture object and destroy all windows
    cap.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    # Configure the argument parser
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-i', '--image', default='input/210216_Nouvel_0435_13_14_img-4311.jpg', help='Input Image')
    parser.add_argument(
        '-v', '--video', default='input/MVI_3192.MP4', help='Input Video')
    parser.add_argument(
        '-w', '--weights', default='models/yolov4/yolov4-custom_final.weights', help='YOLOv4 Weights file')
    parser.add_argument(
        '-c', '--config', default='models/yolov4/yolov4-custom.cfg', help='YOLOv4 Configuration file')
    parser.add_argument(
        '-l', '--labels', default='models/yolov4/classes-3.names', help='Class labels')
    args = parser.parse_args()

    # Configure the logger
    # Get the current system date and time
    d = datetime.datetime.now()
    log_filename = 'logs/{}_{}.log'.format(__name__,
                                           d.strftime("%d%m%y-%H%M%S"))
    # Create the logger object
    logging.basicConfig(filename=log_filename, level=logging.INFO)
    # Create the coloredlogs object
    coloredlogs.install(level='INFO')

    # Get the output layer from YOLO
    # Confidence and NMS thresholds for filtering detections

"""
Counts the number of trees in a video.
"""

# import necessary modules
from utils import utils 
from utils import sort as mot_tracker
import os, argparse
import logging, coloredlogs, datetime
import numpy as np 
import cv2, json
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from matplotlib import colors
import matplotlib.pyplot as plt

"""
detect_image: Detects the location(bounding box of the objects in an image)

Input:
------
    input_image: The input image for which we have to perform the detections

Output:
------
    img: The updated image (Mainly a resized image)
    detected_items: A list of the objects detected in the format <x, y, w, h, object_class, confidence>

"""
def detect_image(input_image, labels):
    img = input_image                                         # Read the input image
    img = cv2.resize(img, (800, 600))                                       # Resize the image to 800x600 resolution
    height, width = img.shape[:2]                                           # Get the height and width of the image (Redundant for now, since we fix it)

    detected_items = []                                                     # A list containing the information about the detected objects

    logging.info("Generated the blob from the input image.")
    # Construct a blob from the given image
    blob = cv2.dnn.blobFromImage(img, 0.00392, (416, 416), swapRB=True, crop=False)    
    net.setInput(blob)                                                      # Set the blob as input to the network
    layer_outputs = net.forward(output_layers)                              # Perform a single forward pass to get the detections
    logging.info("Performed the forward pass for the blob.")

    class_ids, confidences, b_boxes = [], [], []                            

    # Loop through each detection
    for output in layer_outputs:
        for detection in output:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            
            # Create the bounding box with the detection
            center_x, center_y, w, h = (detection[0:4] * np.array([width, height, width, height])).astype('int')
            x = int(center_x - w / 2)
            y = int(center_y - h / 2)
            b_boxes.append([x, y, int(w), int(h)])
            confidences.append(float(confidence))
            class_ids.append(int(class_id))

    # Perform non-maxima suppression to filter the bounding boxes
    indices = cv2.dnn.NMSBoxes(b_boxes, confidences, CONF_THRESH, NMS_THRESH).flatten().tolist()

    # Draw the filtered bounding boxes on the image
    for index in indices:
        x,y,w,h = b_boxes[index]
        
        # text = "{}: {:.2f}".format(classes[class_ids[index]], confidences[index])
        detected_items.append([x, y, w, h, labels[class_ids[index]], confidences[index]])
    #     cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 255), 1, cv2.LINE_AA)
    #     cv2.putText(img, text, (x-10, y-5), cv2.FONT_HERSHEY_COMPLEX_SMALL, 0.75, (255, 0, 255))
    # cv2.imshow("Frame", img)

    # if cv2.waitKey(0) & 0xFF == 27:
    #    cv2.destroyAllWindows()

    logging.info("{} objects were detected".format(len(indices)))
    return img, detected_items

"""
detect_video: Detects the location(bounding box of the objects in an video)

Input:
------
    input_video: The input image for which we have to perform the detections
    net_config : The YOLOv4 configuration file 
    net_weights: The YOLOv4 weights file
    net_labels : The class labels

Output:
------
"""
def detect_video(input_video):

    # Read the configuration parameters from the config.json file
    with open('data/config.json', 'r') as f:
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
    CONF_THRESH, NMS_THRESH = float(config_params["detector"]["confidence"]), float(config_params["detector"]["nms-thresh"])

    cap = cv2.VideoCapture(input_video)
    
    while True:
        ret, img = cap.read()

        if not ret:
            break

        img = cv2.resize(img, (1280, 720))                                      # Resize the image to 800x600 resolution
        height, width = img.shape[:2]                                           # Get the height and width of the image (Redundant for now, since we fix it)

        detected_items = []                                                     # A list containing the information about the detected objects

        logging.info("{}: Generated the blob from the input image.".format(__name__))
        
        # Construct a blob from the given image
        blob = cv2.dnn.blobFromImage(img, 0.00392, (608, 608), swapRB=True, crop=False)    
        net.setInput(blob)                                                      # Set the blob as input to the network
        layer_outputs = net.forward(output_layers)                              # Perform a single forward pass to get the detections
        logging.info("{}: Performed the forward pass for the blob.".format(__name__))

        class_ids, confidences, b_boxes = [], [], []                            

        # Loop through each detection
        for output in layer_outputs:
            for detection in output:
                scores = detection[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]
            
                # Create the bounding box with the detection
                center_x, center_y, w, h = (detection[0:4] * np.array([width, height, width, height])).astype('int')
                x = int(center_x - w / 2)
                y = int(center_y - h / 2)
                b_boxes.append([x, y, int(w), int(h)])
                confidences.append(float(confidence))
                class_ids.append(int(class_id))

        # Perform non-maxima suppression to filter the bounding boxes
        indices = cv2.dnn.NMSBoxes(b_boxes, confidences, CONF_THRESH, NMS_THRESH).flatten().tolist()

        # Draw the filtered bounding boxes on the image
        for index in indices:
            x,y,w,h = b_boxes[index]
        
            text = "{}: {:.2f}".format(classes[class_ids[index]], confidences[index])
            detected_items.append([x, y, x+w, y+h, confidences[index]])
            cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 255), 1, cv2.LINE_AA)
            cv2.putText(img, text, (x, y), int(config_params["font"]["style"]), 
                                                float(config_params["font"]["scale"]), 
                                                (255, 0, 255), 
                                                int(config_params["font"]["thickness"]))
        cv2.imshow("Frame", img)

        
        logging.info("{}: {} objects were detected".format(__name__, len(indices)))
        logging.debug("{}: Detected Items: \n{}".format(__name__, detected_items))

        if cv2.waitKey(1) & 0xFF == 27:
            break
        
    
    cap.release()
    cv2.destroyAllWindows()

def track_video(input_video):
    
    # Read the config.json file to extract the parameters
    with open('data/config.json', 'r') as f:
        config_params = json.load(f)

    # Load the network
    net = cv2.dnn.readNetFromDarknet(config_params["detector"]["config"], config_params["detector"]["weights"])                 # Load the YOLOv4 detector with given config and weights
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
    CONF_THRESH, NMS_THRESH = float(config_params["detector"]["confidence"]), float(config_params["detector"]["nms-thresh"])

    i = 0

    cap = cv2.VideoCapture(input_video)

    while True:
        
        ret, img = cap.read()
        i+= 1
        if not ret:
            break

        img = cv2.resize(img, (800, 600))                                       # Resize the image to 800x600 resolution
        height, width = img.shape[:2]                                           # Get the height and width of the image (Redundant for now, since we fix it)

        detected_items = []                                                     # A list containing the information about the detected objects

        logging.info("{}: Generated the blob from the input image.".format(__name__))
        # Construct a blob from the given image
        blob = cv2.dnn.blobFromImage(img, 0.00392, (416, 416), swapRB=True, crop=False)    
        net.setInput(blob)                                                      # Set the blob as input to the network
        layer_outputs = net.forward(output_layers)                              # Perform a single forward pass to get the detections
        logging.info("{}: Performed the forward pass for the blob.".format(__name__))

        class_ids, confidences, b_boxes, history = [], [], [], []                            

        # Loop through each detection
        for output in layer_outputs:
            for detection in output:
                scores = detection[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]
            
                # Create the bounding box with the detection
                center_x, center_y, w, h = (detection[0:4] * np.array([width, height, width, height])).astype('int')
                x = int(center_x - w / 2)
                y = int(center_y - h / 2)
                b_boxes.append([x, y, int(w), int(h)])
                confidences.append(float(confidence))
                class_ids.append(int(class_id))

        # Perform non-maxima suppression to filter the bounding boxes
        try:
            indices = cv2.dnn.NMSBoxes(b_boxes, confidences, CONF_THRESH, NMS_THRESH).flatten().tolist()
        except AttributeError:
            pass

        # Draw the filtered bounding boxes on the image
        for index in indices:
            x,y,w,h = b_boxes[index]
        
            text = "{}: {:.2f}".format(classes[class_ids[index]], confidences[index])
            detected_items.append([x, y, x+w, y+h, confidences[index]])
            history.append([x, y, x+w, y+h, confidences[index], class_ids[index]])

            cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 255), 1, cv2.LINE_AA)
            cv2.putText(img, text, (x, y), int(config_params["font"]["style"]), 
                                                float(config_params["font"]["scale"]), 
                                                (255, 0, 255), 
                                                int(config_params["font"]["thickness"]))
                    
        logging.info("{}: {} objects were detected".format(__name__, len(indices)))

        # Keep a track of the previous frame for detections
        detected_items = np.asarray(detected_items)
        logging.debug("{}: Detected Items: \n{}".format(__name__, detected_items))

        tracks = tracker.update(detected_items)
        logging.debug("{}: Tracked Items: \n{}".format(__name__, tracks))
        
        tracks_list = []

        for track in tracks:
            x, y, w, h = track[0:4]

            obj, dir = "", ""

            # Find out the centroid of the object
            centroid_x, centroid_y = int((x+w)/2), int((y+h)/2)

            if centroid_x < int(width/2):
                dir = "left"
            else:
                dir = "right"

            cv2.putText(img, str(int(track[4])),(centroid_x, centroid_y),cv2.FONT_HERSHEY_DUPLEX, 0.5, (255, 255, 0), 1 )

            track_obj = {
                "id"        : str(int(track[4])),
                "class"     : obj,
                "direction" : dir,
                "bbox"      : str(track[0:4])
            }
            
            tracks_list.append(track_obj)


        cv2.imshow("Output", img)

        if cv2.waitKey(1) & 0xFF == 27:
            break
        
    # Write the json output
    with open('data/detections.json', 'w') as f:
        json.dump(tracks_list, f, indent=4)

    # Release the VideoCapture object and destroy all windows
    cap.release()
    cv2.destroyAllWindows()
    

if __name__=='__main__':
    # Configure the argument parser
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--image', default='input/210216_Nouvel_0435_13_14_img-4311.jpg', help='Input Image')
    parser.add_argument('-v', '--video', default='input/MVI_3192.MP4', help='Input Video')
    parser.add_argument('-w', '--weights', default='models/yolov4/yolov4-custom_final.weights', help='YOLOv4 Weights file')
    parser.add_argument('-c', '--config', default='models/yolov4/yolov4-custom.cfg', help='YOLOv4 Configuration file')
    parser.add_argument('-l', '--labels', default='models/yolov4/classes-3.names', help='Class labels')
    args = parser.parse_args()

    # Configure the logger
    d = datetime.datetime.now()                                                 # Get the current system date and time
    log_filename = 'logs/{}_{}.log'.format(__name__, d.strftime("%d%m%y-%H%M%S"))       
    logging.basicConfig(filename=log_filename, level=logging.INFO)              # Create the logger object
    coloredlogs.install(level='INFO')                                           # Create the coloredlogs object

    # Load the network
    net = cv2.dnn.readNetFromDarknet(args.config, args.weights)                 # Load the YOLOv4 detector with given config and weights
    net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
    net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)
    logging.info('Successfully loaded the network.')

    # Get the output layer from YOLO
    layers = net.getLayerNames()
    output_layers = [layers[i[0] - 1] for i in net.getUnconnectedOutLayers()]

    # Confidence and NMS thresholds for filtering detections

    img = cv2.imread(args.image)

    CONF_THRESH, NMS_THRESH = 0.9, 0.1
    logging.info('Filename: {}'.format(args.image))
    #detections = detect_image(img)
    detect_video(args.video)
    #for det in detections:
    #   print(det)
    
    # Write to a JSON file
    # with open('data/detections.json', 'w+') as f:
        # json.dump(detections, f, indent=4)

    
import cv2, logging
import numpy as np

"""
get_centroid: Returns the centroid of the box

Input:
------
    box: A list containing the coordinates of the bounding box
    in the order [x, y, w, h]

Output:
--------
    centroid: A list containing the centroid in the order (c_x, c_y)
"""
def get_centroid(box):
    c_x = int((box[0] + box[0] + box[2])/2)
    c_y = int((box[1] + box[1] + box[3])/2)

    return [c_x, c_y]

"""
draw_bboxes: Draws the detections as bounding boxes around each object in
an image

Input:
------
    input_image: The input image on which the boxes need to be drawn
    detections: A list of dictionary elements containing information about 
                each detection.

Output:
-------
    status: True if everything goes well, False otherwise
"""
def draw_bboxes(input_image, detection, tracks):

    # Read the config.json file to extract the parameters
    with open('data/config.json', 'r') as f:
        config_params = json.load(f)

    # Read the image
    img = cv2.imread(input_image)
    logging.info("Loaded the image.")

    for det in detection:
        text = "{}: {}".format(det["class"], det["confidence"])
        x, y, w, h = det["bounding box"]
        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 255), 1, cv2.LINE_AA)
        logging.info("Drawing a rectangle with dimensions: [{},{},{},{}]".format(x, y, w, h))
        cv2.putText(img, text, (x, y), int(config_params["font"]["style"]), 
                                                float(config_params["font"]["scale"]), 
                                                (255, 0, 255), 
                                                int(config_params["font"]["thickness"]))

    return 

    return True

def draw_tracks(input_image, tracks_list):
    # Read the image
    img = cv2.imread(input_image)
    logging.info("Loaded the image.")

    for track in tracks_list:
        text = "ID: {}".format(track[-1])
        x, y, w, h = track[0:4]
        cv2.putText(img, text, (x-5, y-3), cv2.FONT_HERSHEY_COMPLEX_SMALL, 0.75, (255, 255, 255), bottomLeftOrigin=True)

    cv2.imshow("Predictions", img)

    if cv2.waitKey() & 0xFF == ord('q'):
        cv2.destroyAllWindows()

    return True



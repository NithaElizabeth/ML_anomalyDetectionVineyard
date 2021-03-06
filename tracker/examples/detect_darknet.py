import argparse

import cv2
import numpy as np

#cap = cv2.VideoCapture('video3.mp4')

parser = argparse.ArgumentParser(add_help=False)
parser.add_argument("--image", default='data/tree.jpg', help="image for prediction")
parser.add_argument("--config", default='models/yolov4/yolov4-custom.cfg', help="YOLO config path")
parser.add_argument("--weights", default='models/yolov4/yolov4-custom_final.weights', help="YOLO weights path")
parser.add_argument("--names", default='models/yolov4/classes-3.names', help="class names path")
args = parser.parse_args()

CONF_THRESH, NMS_THRESH = 0.1, 0.1

# Load the network
net = cv2.dnn.readNetFromDarknet(args.config, args.weights)
net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)

# Get the output layer from YOLO
layers = net.getLayerNames()
output_layers = [layers[i[0] - 1] for i in net.getUnconnectedOutLayers()]

# Read and convert the image to blob and perform forward pass to get the bounding boxes with their confidence scores
#while True:
#ret, frame = cap.read()
img = cv2.imread(args.image)
#img = frame
img = cv2.resize(img,(800, 600))
height, width= img.shape[:2]

blob = cv2.dnn.blobFromImage(img, 0.00392, (416, 416), swapRB=True, crop=False)
net.setInput(blob)
layer_outputs = net.forward(output_layers)

class_ids, confidences, b_boxes = [], [], []
for output in layer_outputs:
    for detection in output:
        scores = detection[5:]
        class_id = np.argmax(scores)
        confidence = scores[class_id]

        if confidence > CONF_THRESH:
            center_x, center_y, w, h = (detection[0:4] * np.array([width, height, width, height])).astype('int')

            x = int(center_x - w / 2)
            y = int(center_y - h / 2)
            b_boxes.append([x, y, int(w), int(h)])
            confidences.append(float(confidence))
            class_ids.append(int(class_id))

            # Perform non maximum suppression for the bounding boxes to filter overlapping and low confident bounding boxes
            #indices = cv2.dnn.NMSBoxes(b_boxes, confidences, CONF_THRESH, NMS_THRESH).flatten().tolist()
            indices = cv2.dnn.NMSBoxes(b_boxes, confidences, CONF_THRESH, NMS_THRESH).flatten().tolist()

            # Draw the filtered bounding boxes with their class to the image
            with open(args.names, "r") as f:
                classes = [line.strip() for line in f.readlines()]
                colors = np.random.uniform(0, 255, size=(len(classes), 3))

                for index in indices:
                    x, y, w, h = b_boxes[index]
                    cv2.rectangle(img, (x, y), (x + w, y + h), (255, 255, 255), 2)
                    cv2.putText(img, classes[class_ids[index]], (x - 10, y - 5), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (255, 255, 255), 2)
                    fname = "op/" + args.image
                    cv2.imshow(fname, img)
                    cv2.waitKey(1)
                    cv2.imwrite(fname, img)

                    #cap.release()
cv2.destroyAllWindows()

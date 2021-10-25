import argparse as ap
import numpy
import cv2
import os

# Configure the argument parser -------------------
parser = ap.ArgumentParser(description="Extracts the images to create an image dataset from a given video file.")
parser.add_argument("--input", "-i", required=True, help="The video file from which the images have to be extracted")
parser.add_argument("--output", "-o", required=True, help="The location where the images have to be extracted")
args = parser.parse_args()
# -------------------------------------------------

#Variables declared for miscellaneous use ---------
totalImg = 0                                                # Store the total count of images in the dataset
i = 0                                                       # Loop (frame) counter
dirContent = os.listdir(args.input)                         # Stores the list of the contents of the directory
frameskip = 25                                              # Number of frames to be skipped[Do not change unless very important]
# -------------------------------------------------

# Loop through all the videos in the directory ----
for vid in dirContent:
    videoFileName = str(args.input) + "/" + vid             # Recreate the video file names
    cap = cv2.VideoCapture(videoFileName)                   # Run VideoCapture on each file
# -------------------------------------------------

    while(cap.isOpened):
        ret, frame = cap.read()                             # Capture frame-by-frame
        i = i + 1                                           # Increment the loop counter

        try:
            frame = cv2.resize(frame, (800, 600))           # Resize the frame

            if (i % frameskip) == 0:
                cv2.imshow(videoFileName, frame)            # Show the image
                totalImg = totalImg + 1
                imgFileName = str(args.output) + "img-" + str(totalImg) + ".jpg"        # Generate the filename
                cv2.imwrite(imgFileName, frame)             # Store the frame as an image

        except cv2.error as e:                              # Handles the !ssize() error
            pass

        if cv2.waitKey(1) & 0xFF == ord('q'):               # Press `q` after the video to go to the next one
            break

    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()

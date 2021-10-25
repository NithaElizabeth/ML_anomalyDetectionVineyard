"""
Utility tool that helps to resize the images in a given folder.

Prerequisites:
--------------
Run the generate-train.py on the directory to be resized to have
the train.txt file

Returns:
--------
The files in the directory are resized in (800x600) resolution.

Usage:
------
    python scripts/resize-images.py -i <path-to-folder> 
"""
# Module imports and set up argument parser
import cv2, os, argparse, logging, datetime
from progress.bar import ChargingBar

parser = argparse.ArgumentParser()
parser.add_argument('--input', '-i', type=str,  help='')
args = parser.parse_args()

# Configure the log file
x = datetime.datetime.now()
log_file_name = 'data/resize_images_py_{}.log'.format(x.strftime("%d%m%y-%H%M%S"))
logging.basicConfig(filename=log_file_name, level=logging.INFO)
#coloredlogs.install(level='INFO')

# Open the train.txt file to read the image names
train_file_location = 'train.txt'

#Count the number of images processed
img_count = 0

# Change to the required directory
os.chdir(args.input)

#Check if the train.txt file exists or not
if not os.path.exists(train_file_location):
    logging.warning("The file {} was not found. Did you run the generate-train.py script on the parent directory?".format(train_file_location))

image_files = []
# Read the image filenames from filenames.txt
f = open(train_file_location, 'r')
for img in f:
    img = img.strip('\n')
    image_files.append(img)
f.close()

# Setup progress bar
bar = ChargingBar('Processing', max=len(image_files))
    
for img_file in image_files:
    img_file = img_file.strip('\n')
    logging.info("Reading file {}".format(img_file))
    frame = cv2.imread(img_file)
    frame = cv2.resize(frame, (800, 600))
    logging.info("Successfully resized the file: {}".format(img_file))
    logging.info("Saving file: {}".format(img_file))
    cv2.imwrite(img_file, frame)
    img_count += 1
    bar.next()

bar.finish()

print("Total images processed: {}".format(img_count))
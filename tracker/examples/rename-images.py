import argparse
import shutil
import pickle
import numpy
import cv2
import os

"""
rename-images.py: Renames the images in a directory according to our specified format.
----------------

Prerequisites: Run generate-train.py on the particular directory to create the filenames.txt
----------------
"""

parser = argparse.ArgumentParser()

parser.add_argument('--input', '-i', help='Input directory')
parser.add_argument('--date', '-d', help="Date taken")
parser.add_argument('--name', '-n', help='Customer Name')
parser.add_argument('--parcel', '-p', help='Parcel Number')
parser.add_argument('--left', '-l', help='Left rank ID')
parser.add_argument('--right', '-r', help='Right rank ID')
args = parser.parse_args()

#start = 11388
# print("start= {}".format(start))

dir_name = args.date + "_" + args.name + "_" + args.parcel + "_" + args.right + "_" + args.left + "_CanonEOS"
print(dir_name)

with open('last_num.pickle','rb') as f:
    start = pickle.load(f)
    print("start=" + str(start))

if not os.path.exists(dir_name):
    os.mkdir(dir_name)
    print("Successfully created the directory: " + dir_name)
else:
    option = input('[INFO] Directory already exists. Remove directory? y/n: ')
    if option == 'y':
        shutil.rmtree(dir_name)
        os.mkdir(dir_name)
    if option == 'n':
        pass

logFileName = dir_name + "/log.txt"

k = input('Press any key to begin:')

# Create a log file to store the location of the data
with open(logFileName, "w") as f:
    f.write("Location of Images: " + str(args.input))
f.close()

os.chdir(args.input)

# Read the image filenames from filenames.txt
f = open('filenames.txt', 'r')
    
for img_file in f:
    start += 1
    img_file = img_file.strip('\n')
    frame = cv2.imread(img_file)
    frame = cv2.resize(frame, (800, 600))
    cv2.imwrite(img_file, frame)
    dest_name = dir_name + "_img-" + str(start) + ".jpg"
    print(img_file, dest_name)
    os.rename(img_file, dest_name)
f.close()

print("Successfully renamed the files.")

with open('last_num.pickle', 'wb') as f:
    pickle.dump(start, f)

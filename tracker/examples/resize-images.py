"""
Renames and resizes the images to 800*600 in an input folder.
"""

import cv2, os
import argparse, pickle
from progress.bar import Bar

# load the last number of image
#start = pickle.load(open('data/last_num.p', 'r'))
# Configure the argument parser
parser = argparse.ArgumentParser()
parser.add_argument('-input','--i', required=False, default='E:/DeVines/210416_Nouvel_LOI01_00_00_CanonEOS', help='The input folder where all the images are')
args = parser.parse_args()

start = 13721
x = input('start={}. Continue?'.format(start))

# store the current working directory to come back to this later
pwd = os.getcwd()

# Go to the directory in question
os.chdir(args.i)

# Configure the progress bar
bar = Bar('Processing', max = len(os.listdir(os.getcwd())))

# open the file to write the name in
f = open('filenames.txt', 'w')

for filename in os.listdir(os.getcwd()):
    if filename.endswith(".jpg") or filename.endswith(".JPG"):
        img = cv2.imread(filename)
        copy = img.copy()
        cv2.imshow("Original", img)
        cv2.resize(img, (0, 0), fx=0.2, fy=0.15)
        start += 1
        fname = "210416_Nouvel_LOI01_00_00_CanonEOS_img-{}.jpg".format(start)
        cv2.imshow("Output", img)
        #cv2.imwrite(fname, img)
        #f.write(fname + '\n')
        #os.remove(filename)
        bar.next()

bar.finish()

# save the last number done till now
pickle.dump(start, open('data/last_num.p', 'w'))
f.close()
os.chdir(pwd)
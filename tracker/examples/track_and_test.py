"""
Test code to run the detections for each video in a folder
"""

# import necessary modules
from utils import utils
from utils import sort_updated as mot_tracker
import os, argparse
import logging, coloredlogs, datetime
import numpy as np
import cv2, json
from utils import detections as det

if __name__ == '__main__':
    # Configure the argument parser
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', default="input", help='Input Video Folder')
    args = parser.parse_args()

    # Configure the logger
    d = datetime.datetime.now()                                                             # Get the current system date and time
    log_filename = 'logs/{}_{}.log'.format(__name__, d.strftime("%d%m%y-%H%M%S"))
    logging.basicConfig(filename=log_filename, level=logging.DEBUG)                         # Create the logger object
    coloredlogs.install(level='INFO')                                                       # Create the coloredlogs object

    logging.info('Filename: {}'.format(args.input))

    for filename in os.listdir(args.input):

        os.system("python track_video.py -i {}".format(args.input + "/" + filename))

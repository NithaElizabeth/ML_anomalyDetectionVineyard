"""
Counts the number of objects in a video.
"""
# import necessary modules
# from utils import utils
# from tracker.utils import utils
import os, argparse
import logging, coloredlogs, datetime
import numpy as np
import cv2, json
from tracker.utils import detections as det
from distance_estimator import missdead_tree_detector as ad

if __name__ == '__main__':
    # Configure the argument parser
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', default='E:\\DeVines\\Nouvel\\0435\\210216\\210216_Nouvel_0435_01_02.mp4', help='Input Video')
    parser.add_argument('-r', '--right', default=1, help='The right rank number.')
    parser.add_argument('-l', '--left', default=2, help='The left rank number.')
    args = parser.parse_args()
    
    # Create the useful folders
    if not os.path.exists("logs"):
        os.mkdir("logs")
        print("[INFO] Successfully created the logs directory.")

    if not os.path.exists("output"):
        os.mkdir("output")
        print("[INFO] Successfully created the output directory.")

    # Configure the logger
    d = datetime.datetime.now()                                                             # Get the current system date and time
    log_filename = './tracker/logs/{}_{}.log'.format(__name__, d.strftime("%d%m%y-%H%M%S"))
    logging.basicConfig(filename=log_filename, level=logging.DEBUG)                         # Create the logger object
    coloredlogs.install(level='INFO')                                                       # Create the coloredlogs object

    logging.info('Filename: {}'.format(args.input))

    # tracker
    det.track_video(args.input, args.right, args.left)
    

    # distance_estimator
    ad.miss_tree(args.input)

"""
Uses the SORT tracker to track objects in a video
"""
# import necessary modules
from utils import utils
import os, argparse
import logging, coloredlogs, datetime
import numpy as np 
import cv2, json
import single_image as si

if __name__ == '__main__':
    # Configure the argument parser
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', default='input/MVI_3192.MP4', help='Input Video')
    args = parser.parse_args()

    # Configure the logger
    d = datetime.datetime.now()                                                 # Get the current system date and time
    log_filename = 'logs/main_{}.log'.format(d.strftime("%d%m%y-%H%M%S"))       
    logging.basicConfig(filename=log_filename, level=logging.DEBUG)              # Create the logger object
    coloredlogs.install(level='INFO')                                           # Create the coloredlogs object

    logging.info('Filename: {}'.format(args.input))

    #si.detect_video(args.input)
    #si.draw_hough_lines(args.input)

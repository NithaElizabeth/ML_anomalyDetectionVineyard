#/usr/bin/env python3
"""
    test_line_intersection:
        Test code for the intersection of two lines.
        Uses OpenCV and Python
"""
import cv2
import time
import utils
import numpy as np
from utils import line
from utils.line import Point, Line

def update_image(line: Line):
    # Get the current values of x and y (starting point)
    (start_x, start_y) =  line.start.get_point()

    # Get the current values of x and y (ending point)
    (end_x, end_y) =  line.end.get_point()

    start_x, start_y = np.random.randint(0, 800), np.random.randint(0, 600)
    end_x, end_y = np.random.randint(0, 800), np.random.randint(0, 600)

    line.start.set_point(start_x, start_y)
    line.end.set_point(end_x, end_y)

def main():
    # Create the stationary line:
    # point_start : Point
    # point_end   : Point
    line_stationary = Line(Point(np.random.randint(0, 800), np.random.randint(0, 600)), Point(np.random.randint(0, 800), np.random.randint(0, 600)))

    #Create the moving line:
    # point_start : Point
    # point_end   : Point
    line_moving = Line(Point(np.random.randint(0, 800), np.random.randint(0, 600)), Point(np.random.randint(0, 800), np.random.randint(0, 600)))

    while(True):
        
        # Load the background image
        img = cv2.imread('input/background.jpg')
    
        # Move the line downwards
        update_image(line_moving)
        update_image(line_stationary)

        # Show the stationary line on the image
        cv2.line(img, line_stationary.start.get_point(), line_stationary.end.get_point(), (255, 0, 0), 2, cv2.LINE_AA)

        # Show the stationary line on the image
        cv2.line(img, line_moving.start.get_point(), line_moving.end.get_point(), (0, 0, 255), 2, cv2.LINE_AA)

        # Check for intersection
        status, inter_point = utils.line.intersect(line_stationary, line_moving)

        if status is not False:
            cv2.circle(img, inter_point.get_point(), 2, (0, 255, 0), 2)
            text = "Intersection: ({:.4f}, {:.4f})".format(inter_point.get_point_x(), inter_point.get_point_y())
            cv2.putText(img, text, (5, 15), cv2.FONT_HERSHEY_COMPLEX_SMALL, 0.6, (0, 34, 128), 1, cv2.LINE_AA)

        # Show the image
        cv2.imshow("Image", img)

        if cv2.waitKey(0) & 0xFF == 27:
            break

    cv2.destroyAllWindows()

if __name__=='__main__':
    main()
from numba import jit
import numpy as np
import sys
from dataclasses import dataclass

@dataclass
class Point:
    x: int
    y: int

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def get_point(self):
        return (int(self.x), int(self.y))

    def get_point_x(self):
        return self.x

    def get_point_y(self):
        return self.y

    def set_point_x(self, x: int):
        self.x = x

    def set_point_y(self, y: int):
        self.y = y

    def set_point(self, x: int, y: int):
        self.x = x
        self.y = y

@dataclass
class HCoord:
    x      : int
    y      : int
    z      : int

    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    # Create a homogeneous point from a Point object
    def __init__(self, point: Point):
        self.x = point.x
        self.y = point.y
        self.z = 1

    # Return a numpy array representation of the homogeneous line/point
    @jit(forceobj=True)
    def get_coords(self):
        val = np.zeros(3)

        val[0] = self.x
        val[1] = self.y
        val[2] = self.z

        return val


@dataclass
class Line:
    start    : Point
    end      : Point
    slope    : float
    intercept: float

    def __init__(self, pointA: Point, pointB: Point):
        self.start = pointA
        self.end   = pointB

        try:
            self.slope = (self.end.y - self.start.y) / (self.end.x - self.start.x)
            self.intercept = self.start.y - (self.slope * self.start.x)
        except ZeroDivisionError:
            self.slope = 0.000001

    def get_coords(self):
        return [self.start.get_point(), self.end.get_point()]

    def set_coords(self, pointA: Point, pointB: Point):
        self.start = pointA
        self.end   = pointB

def ccw(A: Point, B: Point, C: Point):
    return (C.y - A.y) * (B.x - A.x) > (B.y - A.y) * (C.x - A.x)

"""
intersects  : Checks if another Line object intersects with the current Line
              object or not. If yes, then returns the point of intersection.

Input:
------
    line2   : A Line type object against which the intersection is to be checked.

Output:
-------
    status  : A Boolean value signifying whether the intersection point was found
              or not.
    inter_pt: A Point object returning the point of intersection of the two lines.
              Default value (-1, -1) is returned when the lines do not intersect. 
"""
@jit(forceobj=True)
def intersect(line1: Line, line2: Line):
    # Take current line and convert to homogeneous coordinates:
    # Cross product of two distinct points in homogeneous coordinate
    # system will give the line in homogeneous coordinate system.
    line1_start = HCoord(line1.start)
    line1_end   = HCoord(line1.end)
    line1_coords = np.cross(line1_start.get_coords(), line1_end.get_coords())

    # Similarly, take the other line and convert it into homogeneous
    # coordinate system.
    line2_start = HCoord(line2.start)
    line2_end = HCoord(line2.end)
    line2_coords = np.cross(line2_start.get_coords(), line2_end.get_coords())

    # The cross product of two lines will return the intersection point
    inter_pts = np.cross(line1_coords, line2_coords)

    inter_points = Point(inter_pts[0]/inter_pts[2], inter_pts[1]/inter_pts[2])

    status = ccw(line1.start, line2.start, line2.end) != ccw(line1.end, line2.start, line2.end) and ccw(line1.start, line1.end, line2.start) != ccw(line1.start, line1.end, line2.end)

    return status, inter_points
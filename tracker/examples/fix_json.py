"""
Takes the detections.json file and calculates the distance between each object
on a frame by frame basis.
"""

import cv2, json
import numpy as np
from scipy.spatial.distance import euclidean

detections, obj1 = [], []


def diff(li1, li2):
    return (list(list(set(li1)-set(li2)) + list(set(li2)-set(li1))))

# Load the json file
with open('data/detections.json', 'r') as f:
    detections = json.load(f)

# # Loop through each object and correlate the distance
for i in range(len(detections)):
    try:

        this_frame = "frame " + str(i+1)
        next_frame = "frame " + str(i+3)
        to_elements, no_elements, missing_elements = [], [], []

        print("{} and {}".format(this_frame, next_frame))

        this_objs = detections[i][this_frame]
        ref_objs = detections[i + 1]["frame " + str(i + 2)]
        next_objs = detections[i + 2][next_frame]

    except IndexError:
        pass

    for x in this_objs:
        if any(to_elements) is not x["id"]:
            to_elements.append(x["id"])
        
    for y in next_objs:
        if any(no_elements) is not y["id"]:
            no_elements.append(y["id"]) 


    missing_elements = diff(to_elements, no_elements)

    dif_json_object = 

    detections[i][this_frame].append(missing_elements)        

    print("Missing elements: {}".format(missing_elements))

print(detections)

def preprosessing ():

    detections = []
    # Load the JSON file
    with open('C:/Users/User/Downloads/treecounter-ML-main (1)/treecounter-ML-main/data/test/detections-MVI_3192.json', 'r') as f:
        detections = json.load(f)

    for i in range(len(detections)):

        tracks = detections[i]["frame {}".format(i+1)]
        frame = i+1
        tree_id_pre =[]
        centroid_pre = []
        for track_element in tracks:

            tree_id  = int(track_element['id'])
            rank = track_element['rank']
            centroid =  track_element['centroid']
            centroid =  convert_float(centroid)
            class_name = track_element['class']
            tree_id_pre.append(tree_id)
            centroid_pre.append(centroid)

        obj1.append(objectJson(frame, tree_id_pre, rank, centroid_pre, class_name))
    for i in range(len(obj1)) :
        print("**********************************************************************")
        print("-------------------------------------------------------------------")
        print("Frame",obj1[i].frame)

        if (i < (len(obj1)-1)):

            elements=common_member(obj1[i].ids & obj1[i+1].ids)
            if not len(elements):
                print("No common elements")
            else:
                check = True

            print("The common ID's :    ",elements)

            if check is True:
                for j in  range(len(obj1[i].ids)) :
                    for key in elements:

                        if obj1[i].ids[j] == key and obj1[i+1].ids[j] == key:
                            first=obj1[i].cent[j]
                            print("The chosen first frame is {} and ID is  {}".format(obj1[i].frame,obj1[i].ids[j]))
                            print("The chosen next frame is {} and ID is  {}".format(obj1[i+1].frame,obj1[i+1].ids[j]))

                            last=obj1[i+1].cent[j]

                            closest_dst = (euclidean(first, last))
                            if closest_dst > 15:
                                print("**********************************************************************")
                                print("New ID. Provide new tree ID")






preprosessing()
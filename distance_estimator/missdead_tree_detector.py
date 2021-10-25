import json
import numpy as np
from scipy.spatial.distance import euclidean
from scipy.interpolate import interp1d
import matplotlib.pyplot as plt
from matplotlib import pyplot
import math
import operator
import pandas as pd
import sys, getopt
from distance_estimator.utils import gaussian as util1
from distance_estimator.utils import plot_nominal as util2
from distance_estimator.utils import gaussian as util1
from distance_estimator.utils import distance_estimation as util3
import os

#All the global variables initialised here

obj1 = []                   # List to store the details extracted from the JSON. The object is of type objectJSON
store_Obj =[] 
tree_id_pre=[]              # Tree ID list
centroid_pre = []           # Centroid List before sending to the object
id_list_arranged = []       # ID'S after rearrangement and sorting
distance_list=[]            # Stores the closest distance. This variable is no longer in use
gaussian_list_left =[]      # Contains all the distance of entire left rank for the whole video
gaussian_list_right =[]     # Contains all the distance of entire right rank for the whole video
status_data=[]              # Object for writting the output into JSON
ranks_data = {}             # Rank details storede for output JSON
section_data = {}           # Section details stored for output JSON
frame_number_left =[]       # Stores the frame numbers of left rank objects
frame_number_right = []     # Stores the frame numbers of left rank objects
centroid_list_left = []     # Centroid List for centroids within a framne for left rank
centroid_list_right = []    # Centroid List for centroids within a framne for left rank
centroid_list_met_l = []    # Centroid List for centroids within a framne for left rank metal post
centroid_list_met_r = []    # Centroid List for centroids within a framne for right rank metal post
centroid_list_wood_r=[]     # Centroid List for centroids within a framne for right rank wooden post
centroid_list_wood_l=[]     # Centroid List for centroids within a framne for left rank wooden post
tree_left = []              # list of treee ids within a frame for left ranks
tree_right = []             # list of treee ids within a frame for left ranks
wood_left =[]               # list of wooden post ids within a frame for left ranks
wood_right=[]               # list of wooden post ids within a frame for right ranks
metal_left=[]               # list of metal post ids within a frame for left ranks
metal_right = []            # list of metal post ids within a frame for right ranks
id_list =[]                 # list of ids of all objects
ids_list=[]                 # list of ids of all objectsn within one frame
rank_list=[]                # list rank numbers of all the object in a JSON
centroids_general = []      # Centroids of objects of all three class within a frame
class_name_array =[]        # List of classes appearing wthin a frame
gaussian_now_Left=[]        # List of distance within left rank ( This argument is not used within this script but it is used for calculating the conditional parameter inside distance_estimation.py)
gaussian_now_Right=[]       # List of distance within right rank ( This argument is not used within this script but it is used for calculating the conditional parameter inside distance_estimation.py)
tree_right_num = 0          # Counter for trees on right rank
tree_left_num = 0           # Counter for trees on left rank
miss_right =0               # Counter for missing trees on right rank
miss_left =0                # Counter for missing trees on left rank
frame_left_current =[]      # List of current frame. ( Only used to display the points inside section plots. Uncomment line no 515 for generating the plots for left rank)
frame_right_current =[]     # List of current frame. ( Only used to display the points inside section plots. Uncomment line no 515 for generating the plots for right rank)
# gaussian_now = []
# centroid_list=[] 
# class_list_final=[]
#right_center= []
#left_center =[]
# frame_value=[]



'''
The class that is used to structure the entries extracted from JSON
@input - frame, ids, rank, cent, clas, ranknum
These are the attributes that correspond to values extracted from JSON
'''
class objectJson:
    ids=[]
    def __init__(self, frame, ids, rank, cent, clas, ranknum):

        self.frame = frame
        self.ids = ids
        self.rank = rank
        self.cent = cent
        self.clas = clas
        self.ranknum = ranknum

class objectIds_Cent():
    ids=[]
    def __init__(self,ids,cent):

        #self.frame = frame
        self.ids = ids
        #self.rank = rank
        self.cent = cent
        #self.clas = clas
        #self.ranknum = ranknum


    def __repr__(self):
        return "This is object of class A"

    def print_value(self):
        print("IDS inside=", self.ids)
        print("Centroids inside =", self.cent)



'''
The function used to calculate the distance between the first tree in a frame and all other trees
@input  : cent (The value of the centroid)
@output : distance_list (list of distances calculated)
**This is function is no longer in use
'''
def distance_calculation(cent):
    ref = cent[0]
    for elm in cent:
        closest_dst = (euclidean(ref, elm))
        ref=elm
        distance_list.append(closest_dst)
    return distance_list



'''
This function is used to convert the string value of centroid into float from JSON
@input  : inp (The value of the centroid of type string)
@output : splitted_data (The coordinates of the centroid of type float)
'''
def convert_float(inp):
    splitted_data = inp.split(",")
    return float(splitted_data[-2]), float(splitted_data[-1])



'''
The function used to calculate the distance between first two objects within a frame
@input  : cent (The value of the centroid)
        : rank (Rank direction of the object considered,i.e., either left or right)
        : treeids (ID of the object considered)
@output : gaussian_list_left,gaussian_list_right (list of distances calculated for each rank)
        : closest_dst_gaussian (distance copmputed within two trees)
'''
def distance_calculation_gaussian(rank,cent,treeids):
    ref = cent[0]
    elm = cent[1]
    closest_dst_gaussian = (euclidean(ref, elm))
    print("||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||")
    print("The distance",closest_dst_gaussian)
    print("The centroids ref and elm",ref, elm)
    print("The tree ids considered",treeids)
    print("||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||")
    if rank == "left":
        gaussian_list_left.append(closest_dst_gaussian)
        return closest_dst_gaussian,gaussian_list_left
    else:
        gaussian_list_right.append(closest_dst_gaussian)
        return closest_dst_gaussian,gaussian_list_right



'''
This function is used to create the output JSON
@input  : centr (The value of the centroid of type string)
        : tree_id (ID of every detected object)
        : rank (rank direction,either left or right)
        : status (status flag for trees, either present or absent)
        : class_name (class label of the detected object)
        : ranknumber (rank number of the detected)
        : section (section number in which the detected object is placed)
@output : splitted_data (The coordinates of the centroid of type float)
'''
def structure_op(tree_id,rank,centr,status,class_name,ranknumber,section):
    parcel = 435
    #section = int(section/2)
    treestatusObject = {
        #"frame": str(frame_id),
        "id": str(tree_id),
        "direction": rank,
        "rank": str(ranknumber),
        #"bbox": str(bbox_value),
        "coordinates": str(centr),
        #"confidence": str("{:.2f}".confidence)

        "status":status,
        "class":class_name,
        "parcel":str(parcel),
        "section":str(section)
    }

    status_string = treestatusObject["id"] + "," + treestatusObject["rank"] + "," + treestatusObject["coordinates"] + "," + treestatusObject["status"] + "," + treestatusObject["class"]+ "," + treestatusObject["parcel"]+ ","+ treestatusObject["section"]
    print(treestatusObject)
    status_data.append(treestatusObject)

    # print("============ranks_data===========",ranks_data)
    print("============section_data===========",section)

    if ranks_data:
        if str(ranknumber) in ranks_data:
            ranks_data[str(ranknumber)].append(treestatusObject)
        else:
            ranks_data[str(ranknumber)] = [treestatusObject]
    else:
        ranks_data[str(ranknumber)] = [treestatusObject]

    if section_data:
        if str(section) in section_data:
            section_data[str(section)].append(treestatusObject)
        else:
            section_data[str(section)] = [treestatusObject]
    else:
        section_data[str(section)] = [treestatusObject]

    # if ranks_data2:
    #     for l in range(len(ranks_data2)):
    #         if(ranknumber == ranks_data2[l]["ranknumber"]) :
    #             # print("============2===========",ranks_data2[l])
    #             ranks_data2[l]["objects"].append(treestatusObject)
    #         else :
    #             ranks_data2.append({
    #                 "ranknumber" : ranknumber,
    #                 "objects" : [treestatusObject]
    #             })
    # else :
    #     ranks_data2.append({
    #         "ranknumber" : ranknumber,
    #         "objects" : [treestatusObject]
    #     })

    # with open('./distance_estimator/tree_status_data/text_dump/tree_status_27-05-2021.txt', 'a') as f:
    #     f.write(status_string)
    #     f.write("\n")
    # f.close()

    # with open('output/tree_status_27-05-2021.json', 'w') as status_file:
    #     json.dump(status_data, status_file, indent=4)

    # status_file.close()



'''
This function is used to nest the output JSON with the keys like ranknumber,section and object
@input  : output_suffix (The string suffix derived from the input videos name)
        : parcelleName (Name of the parcel. A string quantity)
@output : splitted_data (The coordinates of the centroid of type float)
'''
def transform_obj(output_suffix, parcelleName):
    ranks = []
    sec=[]
    for key, value in ranks_data.items():
        for key_sec, value_sec in section_data.items():
            ranks.append({
                "ranknumber": key,
                "section": key_sec,
                "object": value_sec
            })

        # # noOfPresentTrees = sum(x["class"] == "tree" and x["status"] == "present" for x in value)

        # # noOfAbsentTrees = sum(x["class"] == "tree" and x["status"] == "absent" for x in value)
        # # noOfMetalPosts = sum(x["class"] == "metal post" for x in value)
        # # noOfWoodenPosts = sum(x["class"] == "wooden post" for x in value)
        # # ranks.append({
        # #     "ranknumber": key,
        # #     "objects": value,
        # #     "noOfPresentTrees" : noOfPresentTrees,
        # #     "noOfAbsentTrees" :noOfAbsentTrees,
        # #     "metalPosts" : noOfMetalPosts,
        # #     "woodenPosts" : noOfWoodenPosts
        # # })



    parcelleObj = {
        "parcelleName": "Cristophe Nouvelle",
        "parcelleCode": 435,
        "ranks": ranks

        #"section": sec
    }


    print("=====parcelleName====" , parcelleName)

    if not os.path.exists('output/{}'.format(parcelleName)):
        os.makedirs('output/{}'.format(parcelleName))

    with open('output/{}/parcelle_{}.json'.format(parcelleName , output_suffix), 'w') as output_json:
        json.dump(parcelleObj, output_json, indent=4)

    output_json.close()



'''
This is the main function. Execution of missdead_tree_detector.py starts at this function.
@input  : input_video (Name of the input video passed from the main script track_vedio.py)
'''

def miss_tree (input_video):

    detections = []          # Stores the data from the input JSON          
    section_right=0          # Counter for section numbers on right rank
    section_left=0           # Counter for section numbers on right rank
    tree_right_num = 0       # Tree counter fo right rank
    tree_left_num = 0        # Tree counter for left rank
    gaussian_now_Left=[]
    gaussian_now_Right=[]
    miss_right =0            # Missed Tree counter fo right rank
    miss_left =0             # Missed Tree counter fo right rank
    rank_l = 0               # Rank number for current object of consideration on left rank
    rank_r =0                # Rank number for current object of consideration on left rank
    list_section_right=[]
    #list_section_left=[]

    # Clean up the input filename for logging
    try:
        last_index = input_video.rindex('/')            # NOTE: This fails on Windows (throws ValueError)
    except ValueError as e:
        last_index = input_video.rindex('\\')

    assert last_index > -4
    output_suffix = input_video[last_index+1:-4]
    # Load the JSON file
    parcelleName = output_suffix.split("_")[1] + "_" + output_suffix.split("_")[2]

    with open('tracker/data/test/{}/detections-{}.json'.format(parcelleName , output_suffix), 'r') as f:

        detections = json.load(f)

    average_left,average_right,conditional_value_left,conditional_value_right = util3.conditional_parameter(detections)

    # Now that we have each "frame" object in our list, we can loop through each item in the list

    for i in range(len(detections)):
        # We store the every object in a temporary list
        tracks = detections[i]["frame {}".format(i+1)]
        frame = i+1                 # To store frame ids
        tree_id_pre =[]             # To store tree ids
        centroid_pre = []           # To store centroid values
        rank_list=[]                # To store rank direction
        class_list=[]               # To store class names
        ranknum_list=[]             # To store rank numbers
        section_list_left=[]        # To store section numbers left 
        section_list_right=[]       # To store section numbers right
        dist_list_left=[]           # To store distance on leftrank
        dist_list_right=[]          # To store distances on rightrank
        centroid_list_left=[]       # To store centroids after sorting on left rank
        centroid_list_right=[]      # To store centroids after sorting on right rank
        for track_element in tracks:

            tree_id  = int(track_element['id'])
            rank_number = track_element['rank']
            ranknum_list.append(rank_number)
            rank = track_element['direction']
            rank_list.append(rank)
            centroid_ =  track_element['centroid']
            centroid = list(map(float,centroid_.split(',')))
            #cntr=centroid_[centroid_.find("(")+1:centroid_.rfind(")")]
            #lat, long = convert_float(cntr)
            #centroid = (lat, long)
            class_name = track_element['class']
            class_list.append(class_name)
            tree_id_pre.append(tree_id)
            id_list_arranged.append(tree_id)
            id_list_arranged.sort()
            centroid_pre.append(centroid)

        #Define all the extracted details in a class variable

        obj1.append(objectJson(frame, tree_id_pre, rank_list, centroid_pre, class_list,ranknum_list))

    # Frame by frame processing starts at this point

    for i in range(len(obj1)) :
        print("**********************************************************************")
        print("-------------------------------------------------------------------")
        print("Frame",obj1[i].frame)


        for j in  range(len(obj1[i].ids)) :

            if obj1[i].rank[j] == "left" and obj1[i].clas[j] =="tree":
                rank_l = obj1[i].ranknum[j]
                print("TREE DETECTED ON LEFT RANK")
                if obj1[i].ids[j] not in tree_left:

                    # A new tree is found on the left rank hence its properties needs to be added on to different lists

                    class_name_array.append(obj1[i].clas[j])
                    centroids_general.append(obj1[i].cent[j])
                    frame_number_left.append(obj1[i].frame)
                    ids_list.append((obj1[i].ids))

                    if  obj1[i].ids[j] in tree_left :
                        print("Tree already available")
                        centroid_list_left.append(obj1[i].cent[j])
                        centroid_list_left.sort()
                    else:
                        print("New tree found")
                        tree_left.append( obj1[i].ids[j])
                        store_Obj.append(objectIds_Cent(obj1[i].ids[j], obj1[i].cent[j]))
                        centroid_list_left.append(obj1[i].cent[j])
                        centroid_list_left.sort()


                        if len(centroid_list_left) > 1 :
                            
                            # Compare the currently computed distance with the conditional parameter 
                            distanceBYframe,gaussian_now_Left = distance_calculation_gaussian("left",centroid_list_left,obj1[i].ids[j])
                            frame_left_current.append(obj1[i].frame)
                            dist_list_left.append(distanceBYframe)
                            if section_left > 0:
                                section_list_left.append(int(section_left/2))
                            else:
                                section_list_left.append(int(section_left))


                            centroid_list_left=[]
                            if (distanceBYframe/average_left) > conditional_value_left:

                                print("----------Missing tree detected----------")
                                miss_left = miss_left+1
                                status = "present"
                                structure_op( obj1[i].ids[j],obj1[i].rank[j],obj1[i].cent[j],status,obj1[i].clas[j],obj1[i].ranknum[j],section_left)
                                status = "absent"
                                structure_op("n/a",obj1[i].rank[j],"n/a",status,obj1[i].clas[j],obj1[i].ranknum[j],section_left)
                                index = frame_number_left[-1]
                                # frame_value.append(index)



                            else:
                                tree_left_num = tree_left_num + 1
                                print("Total trees on left",tree_left_num)
                                print("------No missing tree detected------")
                                status = "present"
                                structure_op( obj1[i].ids[j],obj1[i].rank[j],obj1[i].cent[j],status,obj1[i].clas[j],obj1[i].ranknum[j],section_left)

                else:

                    centroid_list_left.append(obj1[i].cent[j])

            elif obj1[i].rank[j] == "right" and obj1[i].clas[j] =="tree":
                rank_r = obj1[i].ranknum[j]
                print("TREE DETECTED ON RIGHT RANK")

                if obj1[i].ids[j] not in tree_right:
                    class_name_array.append(obj1[i].clas[j])
                    centroids_general.append(obj1[i].cent[j])
                    frame_number_right.append(obj1[i].frame)
                    ids_list.append((obj1[i].ids))

                    if obj1[i].ids[j] in tree_right :
                        print("Tree already available")
                        centroid_list_right.append(obj1[i].cent[j])
                        centroid_list_right.sort(reverse=True)
                    else:
                        print("New tree found")
                        tree_right.append(obj1[i].ids[j])
                        store_Obj.append(objectIds_Cent(obj1[i].ids[j], obj1[i].cent[j]))
                        centroid_list_right.append(obj1[i].cent[j])
                        centroid_list_right.sort(reverse=True)
                        if len(centroid_list_right) > 1 :

                            distanceBYframe,gaussian_now_Right = distance_calculation_gaussian("right",centroid_list_right,obj1[i].ids[j])
                            frame_right_current.append(obj1[i].frame)
                            dist_list_right.append(distanceBYframe)
                            if section_right > 0:
                                section_list_right.append(int(section_right/2))
                            else:
                                section_list_right.append(int(section_right))
                            centroid_list_right=[]
                            if (distanceBYframe/average_right) > conditional_value_right :

                                print("----------Missing tree detected----------")
                                miss_right = miss_right+1
                                status = "present"
                                structure_op( obj1[i].ids[j],obj1[i].rank[j],obj1[i].cent[j],status,obj1[i].clas[j],obj1[i].ranknum[j],section_right)
                                status = "absent"
                                structure_op("n/a",obj1[i].rank[j],"n/a",status,obj1[i].clas[j],obj1[i].ranknum[j],section_right)
                                index = frame_number_right[-1]
                                # frame_value.append(index)

                            else:
                                tree_right_num = tree_right_num + 1
                                print("Total trees on right",tree_right_num)
                                print("------No missing tree detected------")
                                status = "present"
                                structure_op(obj1[i].ids[j],obj1[i].rank[j],obj1[i].cent[j],status,obj1[i].clas[j],obj1[i].ranknum[j],section_right)
                else:

                    centroid_list_right.append(obj1[i].cent[j])

            elif obj1[i].rank[j] == "right" and obj1[i].clas[j] =="metal post":
                print("METAL POST DETECTED ON RIGHT RANK")
                if obj1[i].ids[j] not in metal_right:
                    centroid_list_met_r.append(obj1[i].cent[j])
                    centroid_list_met_r.sort()

                    if obj1[i].ids[j] in metal_right :
                        print("Metal Post already available")
                    else:
                        print("New Metal post found")
                        metal_right.append(obj1[i].ids[j])


                        if ((len(metal_right)) >1):
                            section_right = section_right + 1
                            print("Section Number on right",section_right)
                        structure_op( obj1[i].ids[j],obj1[i].rank[j],obj1[i].cent[j],"present",obj1[i].clas[j],obj1[i].ranknum[j],section_right)
            elif obj1[i].rank[j] == "left" and obj1[i].clas[j] =="metal post":
                print("METAL POST DETECTED ON LEFT RANK")
                if obj1[i].ids[j] not in metal_left:
                    centroid_list_met_l.append(obj1[i].cent[j])
                    centroid_list_met_l.sort()

                    if obj1[i].ids[j] in metal_left :
                        print("Metal post already available")
                    else:
                        print("New Metal post found")
                        metal_left.append(obj1[i].ids[j])


                        if ((len(metal_left)) > 1):
                            section_left = section_left + 1
                            print("Section Number on left",section_left)
                        structure_op( obj1[i].ids[j],obj1[i].rank[j],obj1[i].cent[j],"present",obj1[i].clas[j],obj1[i].ranknum[j],section_left)

            elif obj1[i].rank[j] == "left" and obj1[i].clas[j] =="wooden post":
                print("WOODEN POST DETECTED ON LEFT RANK")
                if obj1[i].ids[j] not in wood_left:
                    centroid_list_wood_l.append(obj1[i].cent[j])
                    centroid_list_wood_l.sort()
                    if obj1[i].ids[j] in wood_left :
                        print("Wooden post already available")
                    else:
                        print("New wooden post found")
                        wood_left.append(obj1[i].ids[j])

                        if ((len(wood_left))>1):
                            section_left = section_left + 1
                            print("Section Number",section_left)
                    structure_op( obj1[i].ids[j],obj1[i].rank[j],obj1[i].cent[j],"present",obj1[i].clas[j],obj1[i].ranknum[j],section_left)
            elif obj1[i].rank[j] == "right" and obj1[i].clas[j] =="wooden post":
                print("WOODEN POST DETECTED ON RIGHT RANK")
                if obj1[i].ids[j] not in wood_right:
                    centroid_list_wood_r.append(obj1[i].cent[j])
                    centroid_list_wood_r.sort()
                    if obj1[i].ids[j] in wood_right:
                        print("Wooden post already available")
                    else:
                        print("New wooden post found")
                        wood_right.append(obj1[i].ids[j])

                        if ((len(wood_right))>1 ):
                            section_right = section_right + 1
                            print("Section Number",section_right)
                    list_section_right.append(section_right/2)
                    structure_op( obj1[i].ids[j],obj1[i].rank[j],obj1[i].cent[j],"present",obj1[i].clas[j],obj1[i].ranknum[j],section_right)


    #util2.section_dist_plot(section_list_left,dist_list_left,frame_left_current,rank_l)
    #util2.section_dist_plot(section_list_right,dist_list_right,frame_right_current,rank_r)

    print("Total trees on rank {} ".format(rank_l),tree_left_num)
    print("Total trees on rank {} ".format(rank_r),tree_right_num)

    #print("Distance on rank {}".format(rank_r),gaussian_now_Right)
    #print("Distance on rank {}".format(rank_l),gaussian_now_Left)

    print("Missing tree on right rank {} ".format(rank_r),miss_right)
    print("Missing tree on left rank {} ".format(rank_l),miss_left)
    transform_obj(output_suffix, parcelleName)

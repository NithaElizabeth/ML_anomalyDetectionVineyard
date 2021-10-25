import json
import numpy as np
from scipy.spatial.distance import euclidean
from scipy.interpolate import interp1d
import matplotlib.pyplot as plt
from matplotlib import pyplot
from scipy.stats import norm
import math
import operator
from numpy import asarray
from numpy import savetxt
import pandas as pd
from distance_estimator.utils import gaussian as util1
from distance_estimator.utils import plot_nominal as util2
import os


# All the global variables initialised here
obj1 = []
tree_id_pre = []
centroid_pre = []
id_list_arranged = []
distance_list = []
gaussian_list_left = []
gaussian_list_right = []
status_data = []
ranks_data = {}
section_data = {}


centroid_list_left = []
centroid_list_right = []
centroid_list_met_l = []
centroid_list_met_r = []
left = []
right = []
overall_left = []
tree_left = []
tree_right = []
distance_list = []
gaussian_list_right = []
overall_right = []
gaussian_list_left = []
gaussian_now = []
frame_ref = 0

global section_left
global section_right
section_left = 1
section_right = 1

frame_list = []
centroid_list_wood_r = []
centroid_list_wood_l = []
wood_left = []
wood_right = []
metal_left = []
metal_right = []
id_list = []
rank_list = []
centroid_list = []


right_center = []
left_center = []

centroids_general = []
class_name_array =[]
tree_right_num =0
tree_left_num = 0
frame_left_current=[]
frame_right_current=[]
#The class that is used to structure the entries extracted from JSON
class objectJson:
    ids = []

    def __init__(self, frame, ids, rank, cent, clas, ranknum):

        self.frame = frame
        self.ids = ids
        self.rank = rank
        self.cent = cent
        self.clas = clas
        self.ranknum = ranknum


# The function used to calculate the distance between all the objects objects
def distance_calculation(cent):
    ref = cent[0]
    for elm in cent:
        closest_dst = (euclidean(ref, elm))
        ref = elm
        distance_list.append(closest_dst)
    return distance_list

# This function is used to convert the string value of centroid into float from JSON


def convert_float(inp):
    splitted_data = inp.split(",")
    return float(splitted_data[-2]), float(splitted_data[-1])

# The function used to calculate the distance between first two objects


def distance_calculation_gaussian(rank, cent):
    ref = cent[0]
    elm = cent[1]
    closest_dst_gaussian = (euclidean(ref, elm))
    
    #print("|||||||||||||||||||||||||||||||||||||||||||||")
    #print("The distance",closest_dst_gaussian)
    if rank == "left":
        gaussian_list_left.append(closest_dst_gaussian)
        return closest_dst_gaussian, gaussian_list_left
    else:
        gaussian_list_right.append(closest_dst_gaussian)
        return closest_dst_gaussian, gaussian_list_right

# This function is used to create the output JSON


#This function is used to create the output JSON 
def structure_op(tree_id,rank,centr,status,class_name,ranknumber,section):
    if section > 1:
        section = int(section/2)
    parcel = 435
    treestatusObject = {
        # "frame": str(frame_id),
        "id": str(tree_id),
        "direction": rank,
        "rank": str(ranknumber),
        # "bbox": str(bbox_value),
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


def miss_tree(input_video):
   
    detections = []
    section_right=1
    section_left=1
    tree_right_num =0
    tree_left_num = 0
    gaussian_now_Left=[]
    gaussian_now_Right=[]
    miss_right =0
    miss_left =0

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
    #with open('tracker/data/test/Nouvel_GAM01/detections-210416_Nouvel_GAM01_04_05.json'.format(output_suffix), 'r') as f:
        
    

        detections = json.load(f)

    # Now that we have each "frame" object in our list, we can loop through each item in the list
    for i in range(len(detections)):
        # We store the every object in a temporary list
        tracks = detections[i]["frame {}".format(i+1)]
        frame = i+1
        tree_id_pre = []
        centroid_pre = []
        rank_list = []
        ranknum_list = []
        class_list = []
        section_list_left=[]
        section_list_right=[]
        dist_list_left=[]
        dist_list_right=[]
        for track_element in tracks:

            tree_id = int(track_element['id'])
            rank_number = track_element['rank']
            ranknum_list.append(rank_number)
            rank = track_element['direction']
            rank_list.append(rank)
            centroid = track_element['centroid']
            centroid = list(map(float, centroid.split(',')))
            class_name = track_element['class']
            class_list.append(class_name)
            tree_id_pre.append(tree_id)
            id_list_arranged.append(tree_id)
            id_list_arranged.sort()

            centroid_pre.append(centroid)
        # Define all the extracted details in a class variable
        obj1.append(objectJson(frame, tree_id_pre, rank_list,
                    centroid_pre, class_list, ranknum_list))

    for i in range(len(obj1)):
        print("**********************************************************************")
        print("-------------------------------------------------------------------")
        print("Frame",obj1[i].frame)
        
        for j in  range(len(obj1[i].ids)) :
            if obj1[i].rank[j] == "left" and obj1[i].clas[j] =="tree":
                print("TREE DETECTED ON LEFT RANK")
                rank_l = obj1[i].ranknum[j]
                if obj1[i].ids[j] not in tree_left:
                    class_name_array.append(obj1[i].clas[j])
                    centroids_general.append(obj1[i].cent[j])
                    centroid_list_left.append(obj1[i].cent[j])
                    print("Class Name", class_name_array)
                    left_center = centroid_list_left
                    # left.append(1)
                    centroid_list_left.sort()
                    if obj1[i].ids[j] in tree_left:
                        print("Tree already available")
                    else:
                        print("New tree found")
                        tree_left.append( obj1[i].ids[j])
                        tree_left_num = tree_left_num + 1
                    
                        if len(centroid_list_left) > 1 :
                            #print("tree_id", obj1[i].ids[j])
                            #print("tree centroids", centroid_list_left)
                            distanceBYframe,gaussian_now_Left = distance_calculation_gaussian("left",centroid_list_left)
                            frame_left_current.append(obj1[i].frame)
                            dist_list_left.append(distanceBYframe)
                            if section_left > 1:
                                section_list_left.append(int(section_left/2))
                            else:
                                section_list_left.append(int(section_left))
                            if distanceBYframe > 40:
                                print("----------Missing tree detected----------")
                                miss_left = miss_left+1
                                status = "present"
                                structure_op( obj1[i].ids[j],obj1[i].rank[j],obj1[i].cent[j],status,obj1[i].clas[j],obj1[i].ranknum[j],section_left)
                                status = "absent"
                                structure_op("n/a",obj1[i].rank[j],"n/a",status,obj1[i].clas[j],obj1[i].ranknum[j],section_left)
                                #index = obj1[i].frame
                                # frame_value.append(index)
                            else:

                                print("------No missing tree detected------")
                                
                                status = "present"
                                structure_op(obj1[i].ids[j],obj1[i].rank[j],obj1[i].cent[j],status,obj1[i].clas[j],obj1[i].ranknum[j],section_left)
            elif obj1[i].rank[j] == "right" and obj1[i].clas[j] =="tree":
                print("TREE DETECTED ON RIGHT RANK")
                rank_r = obj1[i].ranknum[j]
                if obj1[i].ids[j] not in tree_right:
                    class_name_array.append(obj1[i].clas[j])
                    centroids_general.append(obj1[i].cent[j])
                    centroid_list_right.append(obj1[i].cent[j])
                    #print("Cebtroid Right",centroid_list_right)
                    right_center = centroid_list_right
                    # right.append(1)
                    centroid_list_right.sort(reverse=True)
                    if obj1[i].ids[j] in tree_right:
                        print("Tree already available")
                    else:
                        print("New tree found")
                        tree_right.append(obj1[i].ids[j])
                        tree_right_num = tree_right_num + 1
                        
                        if len(centroid_list_right) > 1 :
                            #print("tree_id",obj1[i].ids[j])
                            distanceBYframe,gaussian_now_Right = distance_calculation_gaussian("right",centroid_list_right)
                            frame_right_current.append(obj1[i].frame)

                            dist_list_right.append(distanceBYframe)
                            if section_right > 1:
                                section_list_right.append(int(section_right/2))
                            else:
                                section_list_right.append(int(section_right))

                        
                            if distanceBYframe > 40 :
                                #if class_name_array[0] !="metal post" or class_name_array[1]!="metal post":
                                print("----------Missing tree detected----------")
                                miss_right = miss_right+1
                                status = "present"
                                structure_op( obj1[i].ids[j],obj1[i].rank[j],obj1[i].cent[j],status,obj1[i].clas[j],obj1[i].ranknum[j],section_right)
                                status = "absent"
                                structure_op("n/a",obj1[i].rank[j],"n/a",status,obj1[i].clas[j],obj1[i].ranknum[j],section_right)
                                
                            else:
                                
                                print("------No missing tree detected------")
                                status = "present"
                                structure_op( obj1[i].ids[j],obj1[i].rank[j],obj1[i].cent[j],status,obj1[i].clas[j],obj1[i].ranknum[j],section_right)
                            
            
            elif obj1[i].rank[j] == "right" and obj1[i].clas[j] =="metal post":
                print("METAL POST DETECTED ON RIGHT RANK")
                if obj1[i].ids[j] not in metal_right:
                    centroid_list_met_r.append(obj1[i].cent[j])
                    centroid_list_met_r.sort()
                    # right.append(0)
                    if obj1[i].ids[j] in metal_right:
                        print("Metal Post already available")
                    else:
                        print("New Metal post found")
                        metal_right.append(obj1[i].ids[j])
                        right.append(0)
                    
                        if ((len(metal_right)) > 2):
                            section_right = section_right + 1
                            print("Section Number on right",section_right)
                        structure_op( obj1[i].ids[j],obj1[i].rank[j],obj1[i].cent[j],"present",obj1[i].clas[j],obj1[i].ranknum[j],section_right)
            
            elif obj1[i].rank[j] == "left" and obj1[i].clas[j] =="metal post":
                print("METAL POST DETECTED ON LEFT RANK")
                if obj1[i].ids[j] not in metal_left:
                    centroid_list_met_l.append(obj1[i].cent[j])
                    centroid_list_met_l.sort()

                    if obj1[i].ids[j] in metal_left:
                        print("Metal post already available")
                    else:
                        print("New Metal post found")
                        metal_left.append(obj1[i].ids[j])
                        left.append(0)
                    
                        if ((len(metal_right)) > 2):
                            section_left = section_left + 1
                            print("Section Number on left",section_left)
                        structure_op( obj1[i].ids[j],obj1[i].rank[j],obj1[i].cent[j],"present",obj1[i].clas[j],obj1[i].ranknum[j],section_left)
            elif obj1[i].rank[j] == "left" and obj1[i].clas[j] =="wooden post":
                print("WOODEN POST DETECTED ON LEFT RANK")
                if obj1[i].ids[j] not in wood_left:
                    centroid_list_wood_l.append(obj1[i].cent[j])
                    centroid_list_wood_l.sort()
                    if obj1[i].ids[j] in wood_left:
                        print("Wooden post already available")
                    else:
                        print("New wooden post found")
                        wood_left.append(obj1[i].ids[j])

                        if ((len(wood_left)) > 2):
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

                        if ((len(wood_right)) > 2):
                            section_right = section_right + 1
                            print("Section Number",section_right)
                    structure_op( obj1[i].ids[j],obj1[i].rank[j],obj1[i].cent[j],"present",obj1[i].clas[j],obj1[i].ranknum[j],section_right)    
    # util1.gaussian_plot(gaussian_now_Left,gaussian_now_Right) 
    util2.section_dist_plot(section_list_left,dist_list_left,frame_left_current,rank_l)
    util2.section_dist_plot(section_list_right,dist_list_right,frame_right_current,rank_r) 
    print("Total trees on rank {} ".format(rank_l),tree_left_num)
    print("Total trees on rank {} ".format(rank_r),tree_right_num) 
    print("Total sections on rank {} ".format(rank_l),int(section_left/2))
    print("Total sections on rank {} ".format(rank_r),int(section_right/2) )
    #print("gaussian",gaussian_now_Left)
    #print("gaussian",gaussian_now_Right)
    # print("Missing trees on rank {} ".format(rank_r),miss_right)
    # print("Missing trees on rank {} ".format(rank_l),miss_left)   
    transform_obj(output_suffix, parcelleName)
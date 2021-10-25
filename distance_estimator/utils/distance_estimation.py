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

#All the global variables initialised here
obj1 = []
store_Obj =[]
tree_id_pre=[]
centroid_pre = []
id_list_arranged = []
distance_list=[]
gaussian_list_left =[]
gaussian_list_right =[]
status_data=[]
frame_number_left =[]
frame_number_right = []
centroid_list_left = []
centroid_list_right = []
centroid_list_met_l = []
centroid_list_met_r = []
tree_left = []
tree_right = []
distance_list = []
gaussian_list_right = []
gaussian_list_left =[]
gaussian_now = []
centroid_list_wood_r=[]
centroid_list_wood_l=[]
wood_left =[]
wood_right=[]
metal_left=[]
metal_right = []
id_list =[]
ids_list=[]
rank_list=[]
centroid_list=[]
class_list_final=[]
right_center= []
left_center =[]
centroids_general = []
class_name_array =[]
frame_value=[]
gaussian_now_Left=[]
gaussian_now_Right=[]
tree_right_num=0
tree_left_num=0
miss_right =0
miss_left =0
frame_left_current =[]
frame_right_current =[]



#The class that is used to structure the entries extracted from JSON
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
        


#The function used to calculate the distance between all the objects objects
def distance_calculation(cent):
    ref = cent[0]
    for elm in cent: 
        closest_dst = (euclidean(ref, elm))
        ref=elm
        distance_list.append(closest_dst)
    return distance_list

#This function is used to convert the string value of centroid into float from JSON
def convert_float(inp):
    splitted_data = inp.split(",")
    return float(splitted_data[-2]), float(splitted_data[-1])

#The function used to calculate the distance between first two objects
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

# This function is used to calculate the normalised average of all the distances calculated
def Average(lst):
    # Calcultaes the average
    if len(lst)!=0:

        avg= sum(lst) / len(lst)
    else :
         avg= sum(lst)
    print("--------------")
    print("Average",avg)
    print("--------------")
    # Normalises all the values in the distance list with the average
    quotients = []
    for number in lst:
        quotients.append(number / avg)

    print("Normalised distances ",quotients)
    if len(quotients)!=0:
        nominal_avg= sum(quotients) / len(quotients)
    else:
        nominal_avg= sum(quotients)
    print("--------------")
    print("Nominal Average",nominal_avg)
    print("--------------")
    return avg,nominal_avg,quotients


# This function checks for the number of missing trees using the current nominal value
def check(list1, val):
    return[item for item in list1 if item > val]


#This function is used to create the output JSON 
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

    with open('miss_tree.txt', 'a') as f:
        f.write(status_string)
        f.write("\n")
    f.close()

    with open('tree_status/status_210416_Nouvel_GAM01_test.json', 'w') as status_file:
        json.dump(status_data, status_file, indent=4)

    status_file.close()


def conditional_parameter (detect):
    
        
    detections = []
    section_right=0
    section_left=0
    index=0
    tree_right_num =0
    tree_left_num = 0
    gaussian_now_Left=[]
    gaussian_now_Right=[]
    miss_right =0
    miss_left =0
    rank_l =0
    rank_r =0
    list_section_right=[]
  
    #with open('C:/Users/nitha/3daerospace/src/tracker/multiple_for_lucie/detections-210216_Nouvel_0435_49_50.json', 'r') as f:
       
        #detections = json.load(f)
    detections=detect

    # Now that we have each "frame" object in our list, we can loop through each item in the list
    for i in range(len(detections)):
        # We store the every object in a temporary list
        tracks = detections[i]["frame {}".format(i+1)]
        frame = i+1
        tree_id_pre =[]
        centroid_pre = []
        rank_list=[]
        class_list=[]
        ranknum_list=[]
        section_list_left=[] 
        centroid_list_left=[]
        centroid_list_right=[]
        section_list_right=[]
        dist_list_left=[]
        dist_list_right=[]
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
        
    for i in range(len(obj1)) :
        #print("**********************************************************************")
        print("-------------------------------------------------------------------")
        print("Frame",obj1[i].frame)
        # centroid_list_left=[]
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
                        

                        # The distance will be only calculated if there is more than 1 object detected on the frame

                        if len(centroid_list_left) > 1  :

                            # The distance between the centroid of the trees in pixel unit will be calculated and the distance is pixel 
                            # unit will be stored in "distanceBYframe" and all the distances calculated will be stored in the list "gaussian_now_Left"

                            distanceBYframe,gaussian_now_Left = distance_calculation_gaussian("left",centroid_list_left,obj1[i].ids[j])
                            frame_left_current.append(obj1[i].frame)
                            dist_list_left.append(distanceBYframe)
                            if section_left > 0:
                                section_list_left.append(int(section_left/2))
                            else:
                                section_list_left.append(int(section_left))
                            
                            # The register list storing the value of centroid has to be cleared before every new frame
                            centroid_list_left=[]
                    
                            

                else:
                    # The tree was already registered but the value of its centroid must be updated
                    centroid_list_left.append(obj1[i].cent[j])
                    
            elif obj1[i].rank[j] == "right" and obj1[i].clas[j] =="tree":
                rank_r = obj1[i].ranknum[j]
                print("TREE DETECTED ON RIGHT RANK")
                if obj1[i].ids[j] not in tree_right:

                    # A new tree is found on the left rank hence its properties needs to be added on to different lists

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

                            # The distance between the centroid of the trees in pixel unit will be calculated and the distance is pixel 
                            # unit will be stored in "distanceBYframe" and all the distances calculated will be stored in the list "gaussian_now_Right"

                            distanceBYframe,gaussian_now_Right = distance_calculation_gaussian("right",centroid_list_right,obj1[i].ids[j])
                            frame_right_current.append(obj1[i].frame)
                            dist_list_right.append(distanceBYframe)
                            if section_right > 0:
                                section_list_right.append(int(section_right/2))
                            else:
                                section_list_right.append(int(section_right))

                            # The register list storing the value of centroid has to be cleared before every new frame
                            centroid_list_right=[]
                                  
                else:
                    # The tree was already registered but the value of its centroid must be updated
                    centroid_list_right.append(obj1[i].cent[j])


    # #util2.nominal_dist_plot_section(list_section_right,rank_r,"right",frame_right_current,gaussian_now_Right)
    # #util2.nominal_dist_plot(rank_l,rank_r,frame_left_current,frame_right_current,gaussian_now_Left,gaussian_now_Right)
    # # util2.section_dist_plot(section_right/2,rank,"right",frame_id,dist)
    # #util2.nominal_dist_plot_section(section_right,rank_r,"right",frame_right_current,gaussian_now_Right)
    util1.gaussian_plot(gaussian_now_Left,gaussian_now_Right)       
    print("Distance on rank {}".format(rank_l),gaussian_now_Left)
    average_l,nominal_value_left,normalised_list=Average(gaussian_now_Left) 
    print("The average of distance on rank {}".format(rank_l),nominal_value_left)
    print("The number of missing trees on rank {}".format(rank_l), len(check(normalised_list,nominal_value_left+4)))

    print("Distance on rank {}".format(rank_r),gaussian_now_Right)
    average_r,nominal_value_right,normalised_list=Average(gaussian_now_Right)
    print("The average of distance on rank {}".format(rank_r),nominal_value_right)
    print("The number of missing trees on rank {}".format(rank_r), len(check(normalised_list,nominal_value_right+4)))

    conditional_param_left = nominal_value_left + 4
    conditional_param_right = nominal_value_right + 4
    return average_l,average_r,conditional_param_left,conditional_param_right
                          
            
    
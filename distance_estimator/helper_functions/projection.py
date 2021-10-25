#!/usr/bin/env python3
import json
from scipy.spatial.distance import euclidean
import numpy as np
from scipy.interpolate import interp1d
import matplotlib.pyplot as plt

#All global variables defined and initialised
centroid_list_left=[]
centroid_list_right=[]
centroid_list_met_l = []
left=[]
distance_list=[]
frame_ref =1

#Function to convert the extracted centroids from json back to float
def convert_float(inp):
    splitted_data = inp.split(",")
    return float(splitted_data[-2]), float(splitted_data[-1])
    

#Calculated distance between every centroids
def distance_calculation(cent):
    ref = cent[0]
    for elm in cent: 
        closest_dst = (euclidean(ref, elm))
        ref=elm
        distance_list.append(closest_dst)
    return distance_list

#Projects the trees to 2d plane
def plot_projection(cent_l,cent_r):
 
    
    x=np.ones(len(cent_l))*-1
    y=np.arange(0,len(cent_l))

    x_r=np.ones(len(cent_r))
    y_r=np.arange(0,len(cent_r))
    
    # Linear length on the line
    distance = np.cumsum(np.sqrt( np.ediff1d(x, to_begin=0)**2 + np.ediff1d(y, to_begin=0)**2 ))
    distance = distance/distance[-1]

    fx, fy = interp1d( distance, x ), interp1d( distance, y )

    alpha = np.linspace(0, 1, 15)
    x_regular, y_regular = fx(alpha), fy(alpha)

    plt.plot(x, y, 'o-');
    plt.plot(x_r, y_r, 'o-');
    plt.axis('equal');
    plt.show()




with open('tracks.json', 'r') as f:
    tracks = json.load(f)

for track_element in tracks:
    frame = int(track_element['frame'])
    
    tree_id = int(track_element['id'])
    rank = track_element['direction']
    centroid_ = track_element['centroid']
    cntr=centroid_[centroid_.find("(")+1:centroid_.rfind(")")]
    lat, long = convert_float(cntr)
    centroid = (lat, long)

    class_name = track_element['class']

    
    #if rank == "left" and class_name =="tree":
        #print("-----------------------------LEFT RANK DETECTED-----------------------------")
    if frame_ref == frame:
        print("Frame ID : ",frame)
        if rank == "left" and class_name =="tree":
            print("-----------------------------LEFT RANK DETECTED-----------------------------")
            centroid_list_left.append(centroid)
            left.append(1)
            centroid_list_left.sort()
        elif rank == "right" and class_name =="tree":
            print("-----------------------------RIGHT RANK DETECTED-----------------------------")
            centroid_list_right.append(centroid)
            centroid_list_right.sort(reverse=True)

        
        
    else:
        print("Left centroids",centroid_list_left)
        print("Right centroids",centroid_list_right)
        plot_projection(centroid_list_left,centroid_list_right)
        #plot_projection(centroid_list_left,centroid_list_right)
        if len(centroid_list_left) <=0 or len(centroid_list_left) <=0:
            print("No enough trees to calculate distance")
        else:
            dist_rank=distance_calculation(centroid_list_left)
        
        frame_ref=frame_ref+1
        print("Frame ID after iteraring : ",frame)
        centroid_list_left=[]
        centroid_list_right=[]
        dist_rank=[]
        

    

            
        
centroid_list_left.sort()
print("Left centroids",centroid_list_left)
print("Right centroids",centroid_list_right)
print("distances",dist_rank)
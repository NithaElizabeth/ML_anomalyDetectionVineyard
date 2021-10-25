import json
import numpy as np
from scipy.spatial.distance import euclidean

obj1 = []
tree_id_pre=[]
centroid_pre = []
id_list_arranged = []
status_data = []

class objectJson:
    ids=[]
    def __init__(self, frame, ids, rank, cent, clas):
        
        self.frame = frame
        self.ids = ids
        self.rank = rank
        self.cent = cent
        self.clas = clas


def convert_float(inp):
    splitted_data = inp.split(",")
    return float(splitted_data[-2]), float(splitted_data[-1])

def common_member(a, b):
    #common_elm = []
    #a_set = set(a)
    #b_set = set(b)
    a_set = set(a.ids)
    b_set = set(b.ids)
  
    if (a_set & b_set):
        print("The Frame {} contains some elements of the Frame {}".format(a.frame, b.frame))    
        common_elm = a_set & b_set
        return True,common_elm
    else:
        print("No common elements between Frame {} and Frame {}".format(a.frame, b.frame)) 
        return False

def structure_op(tree_id,rank,centr,class_name):
    parcel = 435
    treestatusObject = {
        #"frame": str(frame_id),
        "id": str(tree_id),
        #"direction": rank,
        "rank": rank,
        #"bbox": str(bbox_value),
        "coordinates": str(centr),
        #"confidence": str("{:.2f}".confidence)
        "class":class_name,
        "parcel":str(parcel)
    }

    status_string = treestatusObject["id"] + "," + treestatusObject["rank"] + "," + treestatusObject["coordinates"] + "," + treestatusObject["class"]+ "," + treestatusObject["parcel"]
    print(treestatusObject)
    status_data.append(treestatusObject)

    with open('JSON_cleaned.txt', 'a') as f:
        f.write(status_string)
        f.write("\n")
    f.close()

    with open('JSON_cleaned.json', 'w') as status_file:
        json.dump(status_data, status_file, indent=4)

    status_file.close()

def preprosessing ():
    
    detections = []
    # Load the JSON file
    with open('C:/Users/User/Downloads/treecounter-ML-main (1)/treecounter-ML-main/data/test/detections-MVI_3192.json', 'r') as f:
        detections = json.load(f)

    # Now that we have each "frame" object in our list, we can loop through each item in the list
    for i in range(len(detections)):
        # We store the every object in a temporary list
        tracks = detections[i]["frame {}".format(i+1)]
        frame = i+1
        tree_id_pre =[]
        centroid_pre = []
        rank_list=[]
        class_list=[]
        for track_element in tracks:
            
            tree_id  = int(track_element['id'])
            rank = track_element['rank']
            rank_list.append(rank)
            centroid =  track_element['centroid']
            centroid = list(map(float,centroid.split(',')))
            class_name = track_element['class']
            class_list.append(class_name)
            tree_id_pre.append(tree_id)
            id_list_arranged.append(tree_id)
            id_list_arranged.sort()
            
            centroid_pre.append(centroid)
        #Define all the extracted details in a class variable
        obj1.append(objectJson(frame, tree_id_pre, rank_list, centroid_pre, class_list))
        
    for i in range(len(obj1)) :
        print("**********************************************************************")
        print("-------------------------------------------------------------------")
        print("Frame",obj1[i].frame)
        #print("ID",obj1[i].ids)
        #print("Centr",obj1[i].cent)
        
        if (i < (len(obj1)-1)):
            if i == 0:
                check,elements=common_member(obj1[0], obj1[1])
            
            check,elements=common_member(obj1[i], obj1[i+1])
            #check =  any(item in obj1[i].ids for item in obj1[i+1].ids)
            print("The common ID's :    ",elements)
            

            if check is True:
                for j in  range(len(obj1[i].ids)) :
                    for key in elements:
                        #print(key)
                        #print("obj",obj1[i].ids[j])
                        if obj1[i].ids[j] == key and obj1[i+1].ids[j] == key:
                            first=obj1[i].cent[j]
                            print("The chosen first frame is {} and ID is  {}".format(obj1[i].frame,obj1[i].ids[j]))
                            print("The chosen next frame is {} and ID is  {}".format(obj1[i+1].frame,obj1[i+1].ids[j]))
                            #print("The chosen first centroids",first)
                            #print("The chosen first id",obj1[i].ids[j])
                            last=obj1[i+1].cent[j]
                            #print("The chosen last centroids",last)
                            #print("The chosen last id",obj1[i+1].ids[j])
                            dist = tuple(map(lambda x, y: abs(x - y), first, last))
                            closest_dst = (euclidean(first, last))
                            print("The distance along x and y",dist) 
                            print("The closest distance",closest_dst) 
                            print("-------------------------------------------------------------------")
                            if closest_dst > 15 :
                                #obj1[i].ids[j] = obj1[i].ids[j] + 1
                                obj1[i+1].ids[j] = id_list_arranged[-1]+1
                                
                    structure_op(obj1[i].ids[j],obj1[i].rank[j],obj1[i].cent[j],obj1[i].clas[j])               
            else :
               print("No, frame {} doesn't have all elements of the frame {}.".format(obj1[i].frame, obj1[i+1].frame))
        
       

preprosessing()
        
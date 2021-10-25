import json
import numpy as np

detections = []
# Load the JSON file
with open('data/detections.json', 'r') as f:
    detections = json.load(f)

# We can store the id of the object we have seen here
objects_list = []
highest_track = 0

# Now that we have each "frame" object in our list, we can loop through each item in the list
for i in range(len(detections)):
    # We store the tracks in a temporary list
    tracks = detections[i]["frame {}".format(i+1)]

    for track in tracks:
        current_track = int(track["id"])
        if current_track > highest_track:
            highest_track = current_track
    
    for obj in objects_list:
        if current_track != obj:
            objects_list.append(current_track)
            
print(objects_list)



    
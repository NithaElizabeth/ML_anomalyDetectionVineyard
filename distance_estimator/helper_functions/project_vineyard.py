"""Script name :  Projection of vineyard
   Developer   :  Nitha Elizabeth John
   Company     : 3D Aerospace, Toulouse 
"""
import json
import matplotlib.pyplot as plt
import numpy as np
def ploting_tm(cent_l,cent_r,l,r):
    #Declaring the lists that will store values corresponding to the left and right ranks
    #List for storing projection coordinates of tree on left rank
    x = []
    y = []
    #List for storing projection coordinates of metal post on left rank
    x_m = []
    y_m = []
    #List for storing projection coordinates of wooden post on left rank
    x_w =[]
    y_w =[]
    #List for storing projection coordinates of trees on right rank
    rightx = []
    righty = []
    #List for storing projection coordinates of metal post on right rank
    rightx_m = []
    righty_m = []
    #List for storing projection coordinates of wooden post on right rank
    rightx_w = []
    righty_w = [] 
    for it,elm in enumerate(cent_l):
        
        if elm == 1:
            x.append(l)
            y.append(it)
            #plt.plot(x, y, 'o-');
        elif elm ==0:
            x_m.append(l)
            y_m.append(it)
            #plt.plot(x, y, 'x-');
        elif elm==2:
            x_w.append(l)
            y_w.append(it)
    for it,elm in enumerate(cent_r):
        if elm == 1:
            rightx.append(r)
            righty.append(it)
        elif elm ==0:
            rightx_m.append(r)
            righty_m.append(it)
        elif elm==2:
            rightx_w.append(r)
            righty_w.append(it)

    plt.plot(x, y, 'go',label='Trees');
    plt.plot(x_m, y_m, 'bo',label='Metal Post');
    plt.plot(x_w, y_w, 'yo',label='Wooden Post');
    plt.plot(rightx, righty, 'go');
    plt.plot(rightx_m, righty_m, 'bo');
    plt.plot(rightx_w, righty_w, 'yo');
    plt.xticks([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55 ])


#Load the tracking JSON for further use if needed
with open('projectionOverall.json', 'r') as f:
    tracks = json.load(f)

# Plot the projection rank by rank for every projected rank. 
# The dataframe corresponding to every rank are saved in the local system
left_read = np.load('data\array\outfile_4.npy')
right_read = np.load('data\array\outfile_3.npy')
ploting_tm(left_read,right_read,4,3)
left_read = np.load('data\array\outfile_5.npy')
right_read = np.load('data\array\outfile_6.npy')
ploting_tm(left_read,right_read,5,6)
left_read = np.load('data\array\outfile_8.npy')
right_read = np.load('data\array\outfile_7.npy')
ploting_tm(left_read,right_read,8,7)
left_read = np.load('data\array\outfile_9.npy')
right_read = np.load('data\array\outfile_10.npy')
ploting_tm(left_read,right_read,9,10)
left_read = np.load('data\array\outfile_12.npy')
right_read = np.load('data\array\outfile_11.npy')
ploting_tm(left_read,right_read,12,11)
left_read = np.load('data\array\outfile_13.npy')
right_read = np.load('data\array\outfile_14.npy')
ploting_tm(left_read,right_read,13,14)
left_read = np.load('data\array\outfile_16.npy')
right_read = np.load('data\array\outfile_15.npy')
ploting_tm(left_read,right_read,16,15)
left_read = np.load('data\array\outfile_17.npy')
right_read = np.load('data\array\outfile_18.npy')
ploting_tm(left_read,right_read,17,18)
left_read = np.load('data\array\outfile_20.npy')
right_read = np.load('data\array\outfile_19.npy')
ploting_tm(left_read,right_read,20,19)
left_read = np.load('data\array\outfile_21.npy')
right_read = np.load('data\array\outfile_22.npy')
ploting_tm(left_read,right_read,21,22)
left_read = np.load('data\array\outfile_24.npy')
right_read = np.load('data\array\outfile_23.npy')
ploting_tm(left_read,right_read,24,23)
left_read = np.load('data\array\outfile_25.npy')
right_read = np.load('data\array\outfile_26.npy')
ploting_tm(left_read,right_read,25,26)
left_read = np.load('data\array\outfile_28.npy')
right_read = np.load('data\array\outfile_27.npy')
ploting_tm(left_read,right_read,28,27)
left_read = np.load('data\array\outfile_29.npy')
right_read = np.load('data\array\outfile_30.npy')
ploting_tm(left_read,right_read,29,30)
left_read = np.load('data\array\outfile_32.npy')
right_read = np.load('data\array\outfile_31.npy')
ploting_tm(left_read,right_read,32,31)
left_read = np.load('data\array\outfile_33.npy')
right_read = np.load('data\array\outfile_34.npy')
ploting_tm(left_read,right_read,33,34)
left_read = np.load('data\array\outfile_36.npy')
right_read = np.load('data\array\outfile_35.npy')
ploting_tm(left_read,right_read,36,35)
left_read = np.load('data\array\outfile_37.npy')
right_read = np.load('data\array\outfile_38.npy')
ploting_tm(left_read,right_read,37,38)
left_read = np.load('data\array\outfile_40.npy')
right_read = np.load('data\array\outfile_39.npy')
ploting_tm(left_read,right_read,40,39)
left_read = np.load('data\array\outfile_41.npy')
right_read = np.load('data\array\outfile_42.npy')
ploting_tm(left_read,right_read,41,42)
left_read = np.load('data\array\outfile_45.npy')
right_read = np.load('data\array\outfile_46.npy')
ploting_tm(left_read,right_read,45,46)
left_read = np.load('data\array\outfile_44.npy')
right_read = np.load('data\array\outfile_43.npy')
ploting_tm(left_read,right_read,44,43)
left_read = np.load('data\array\outfile_48.npy')
right_read = np.load('data\array\outfile_47.npy')
ploting_tm(left_read,right_read,48,47)
left_read = np.load('data\array\outfile_49.npy')
right_read = np.load('data\array\outfile_50.npy')
ploting_tm(left_read,right_read,49,50)
left_read = np.load('data\array\outfile_53.npy')
right_read = np.load('data\array\outfile_54.npy')
ploting_tm(left_read,right_read,53,54)
left_read = np.load('data\array\outfile_52.npy')
right_read = np.load('data\array\outfile_51.npy')
ploting_tm(left_read,right_read,52,51)
plt.show()
import numpy as np
import matplotlib.pyplot as plt




def nominal_dist_plot(left,right,frame_id_l,frame_id_r,dist_l,dist_r):


        #plt.plot(frame_id_l, dist_l, marker='o', color = 'red',label='Left Rank')
        plt.plot(frame_id_l, dist_l,'rx',label='Left Rank {}'.format(left))
        plt.plot(frame_id_r, dist_r, 'bx',label='Right Rank {}'.format(right))
        plt.xlabel("Frame ID")
        plt.ylabel("Distances between centroids of first two trees in every frame")
        plt.legend(loc="upper left")
        plt.show()



    

def section_dist_plot(sec,dist,frame_id_l,rank) :
    print(". . . . . . . . . . . . . . . . . . Generating Plots . . . . . . . . . . . . . . . . . . ")
    distance=[]
    section_frame =[]
    
    for i in range(1,len(sec)) :
        distance.append(dist[i])
        section_frame.append(frame_id_l[i])
        if sec[i]!=sec[i-1] :
            
            plt.plot(section_frame, distance,'mx')
            plt.xlabel("Frame ID")
            plt.ylabel("Distances between centroids of first two trees in every frame")
            plt.title("Section {}, Rank {}".format(sec[i-1],rank))
            plt.ylim([0, 300])
            plt.xlim([0, 9000])
            plt.savefig('output/plot/plot - Rank {} - Section {}.png'.format(rank,sec[i-1]), dpi=300, bbox_inches='tight')
            plt.close()
            distance=[]
            section_frame =[]

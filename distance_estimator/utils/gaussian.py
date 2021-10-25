import numpy as np
import matplotlib.pyplot as plt
import math
import statistics



def gaussian_plot(frame_cents_left,frame_cents_right):


    X = frame_cents_left
    X = np.sort(X)
    mean = np.mean(X)
    sigma = 0

    for i in X:
        sigma += np.square(mean - i)

    sigma = np.std(X)


    def func(x):
        return np.exp(np.square(x - mean) / (2 * np.square(sigma))) / np.sqrt(2 * math.pi * sigma)

    def countOccurrences(dist):
        res = 0
        for i in range(len(X)):
            if dist == X[i]:
                res += 1
        return res

    Y = []
    Y_occ = []

    for i in X:
        Y.append(func(i))
        Y_occ.append(countOccurrences(i))

    



    X_right = frame_cents_right
    X_right = np.sort(X_right)
    mean_right = np.mean(X_right)
    

    sigma_right = 0

    for i in X_right:
        sigma_right += np.square(mean_right - i)

    #sigma = np.sqrt(sigma / (len(X_right) - 1))
    sigma_right = np.std(X_right)


    def func(x):
        return np.exp(np.square(x - mean_right) / (2 * np.square(sigma_right))) / np.sqrt(2 * math.pi * sigma_right)

    def countOccurrences(dist):
        res = 0
        for i in range(len(X_right)):
            if dist == X_right[i]:
                res += 1
        return res

    Y_right = []
    Y_occ_right = []

    for i in X_right:
        Y_right.append(func(i))
        Y_occ_right.append(countOccurrences(i))



    

    plt.hist(X, color = 'green',label='Left Rank')
    plt.hist(X_right, color = 'cyan',label='Right Rank')
    plt.xlabel("Distances between centroids of first two trees in every frame")
    plt.xlabel("Occurances of Distances")
    plt.legend(loc="upper left")
    plt.show()

    plt.plot(X, Y_occ, marker='o', color = 'red',label='Left Rank')
    plt.plot(X_right, Y_occ_right, marker='x', color = 'blue',label='Right Rank')
    plt.xlabel("Distances between centroids of first two trees in every frame")
    plt.ylabel("Occurrences")
    plt.legend(loc="upper left")
    plt.show()

    plt.plot(X, Y, marker='o',label='Left Rank')
    plt.plot(X_right, Y_right, marker='o',label='Right Rank')
    plt.xlabel("Distances between centroids of first two trees in every frame")
    plt.ylabel("Gaussian pdf")
    plt.legend(loc="upper left")
    plt.show()
    
    print("**************************************************")
    print("Distances",X)
    print("Distances",X_right)
    print("**************************************************")

    if len(Y_occ)>0:
        mean_lefttrank =statistics.mean(Y_occ)
        #print("Mean left",mean_lefttrank)
    elif len(Y_occ_right)>0:
        mean_rightrank =statistics.mean(Y_occ_right)
        #print("Mean right",mean_rightrank)
    
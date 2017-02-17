'''
Function to form clusters using weighted k-means algorithm
'''



import numpy as np
import copy

# finding the associated cluster for each data point
def nearestcenter(Global_Coreset1, centers2,ind):
    f_cost = 0
    for i in range(len(Global_Coreset1)):
        dist=[]
        for centeri in centers2:
            dist.append((np.sum((Global_Coreset1[i] - centeri) ** 2)))
        ind[i]=np.argmin(dist)
        f_cost=dist[np.argmin(dist)]+f_cost
    return(ind,f_cost)

# Recalculating centers based on new associations
def recalculate_centers(Global_Coreset1, Global_weigths , centers,ind,k,l):
    sumx=np.zeros((k,l))
    count = np.ones(k)
    for i in range(len(centers)):
        for j in range(len(Global_Coreset1)):
            if ind[j]==i:
                sumx[ind[j]]+= Global_Coreset1[j]*Global_weigths[j]
                count[i]=count[i]+Global_weigths[j]
            # print(count)
        centers[i]= sumx[i] / count[i]
    return centers


#main program to generate clusters and centers
def get_centers(Global_Coreset1,Global_weigths,k):
    l=len(Global_Coreset1[0])
    c=np.random.choice(np.arange(len(Global_Coreset1)),size = k,replace = False, p=None)
    centers=[]
    for i in range(len(c)):
        centers.append(Global_Coreset1[c[i]])
    ind = np.zeros(len(Global_Coreset1))
    ind ,f_cost =nearestcenter(Global_Coreset1,centers,ind)

    flag=1
    iteration =0
    while(flag):
        centers1=copy.deepcopy(centers)
        centers = recalculate_centers(Global_Coreset1, Global_weigths,centers,ind,k,l)
        ind,f_cost=nearestcenter(Global_Coreset1,centers,ind)

        iteration += 1
        zcount=0

        # stops when the centers does not change change or after 150 iterations
        for i in range(k):
            if all(centers[i] == centers1[i]):
                zcount+=1
        if zcount==k or iteration ==150:
            flag=0

    return centers


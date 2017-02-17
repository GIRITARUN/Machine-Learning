'''
The main chunk of the algorithm where coreset sample points are generated and calculates information needed to generate Global coresets.
'''


import numpy as np
import sklearn.cluster as skl
import math

class node:
    def __init__(self,data,n,k,all_t):
        # note that rows are data points
        self.data = np.array(data)
        # B is the set of centers
        self.B = []
        # labels for kmeans with B
        self.labels = []
        # n is the number of nodes in the graph
        self.n = n
        # k is the number of centers required
        self.k = k
        # S is the sample of pts
        self.S = []
        # wtsS are the weights on S
        self.wtsS = []
        # wtsB are the weghts for the centers
        self.wtsB = np.zeros(k)
        # costs are cost of points accoring to k-means
        self.costs = np.zeros(len(self.data))
        # total_costs is the sum of all costs
        self.total_cost  = []
        # all_cost is cost of the entire data set
        self.all_cost = []
        # t is the number of samples to be generated
        self.t = []
        # all_t refers to total number of samples to be taken
        self.all_t = all_t

    # An alpha aproximate algorithm(k-means)
    def k_means_algo(self):
        kmeans = skl.KMeans(n_clusters = self.k).fit(self.data)
        self.B = kmeans.cluster_centers_
        self.labels =  kmeans.labels_

    # Calcuating cost
    def cost_vecs(self):
        for i in range (len(self.data)):
            self.costs[i] =  math.sqrt(np.sum((self.data[i]-self.B[self.labels[i]])**2))
        self.total_cost = sum(self.costs)


    # Calculating number of points to be sampled from this node
    def set_post_transfer(self,all_cost):
        self.all_cost=all_cost
        self.t = self.all_t * self.total_cost/all_cost


    # Sampling of points from the node
    def sample(self):
        self.S = np.zeros((self.t,len(self.data[0])))
        self.wtsS = np.zeros(self.t)
        s = np.arange(len(self.data))
        s = np.random.choice(s,size = min(self.t,len(self.data)),replace = False, p=self.costs/self.total_cost)
        s = sorted(s)
        count = 0
        for i in range(len(self.data)):
            if count < len(s):
                if(s[count] == i):
                    self.S[count]=self.data[s[count]]
                    self.wtsS[count] = self.all_cost/ (self.t*self.costs[s[count]])
                    self.wtsB[self.labels[s[count]]] = self.wtsB[self.labels[s[count]]] - self.wtsS[-1]
                    count = count + 1
            self.wtsB[self.labels[i]] = self.wtsB[self.labels[i]]+1


    # Number of points to be sampled in Naive approach
    def naive_post_transfer(self):
        self.t = int(self.all_t / self.n)

    # Sampling of points using nao=ive approach
    def Naive_sample(self):
        self.S = np.zeros((self.t,len(self.data[0])))
        self.wtsS = np.zeros(self.t)
        s = np.arange(len(self.data))
        s = np.random.choice(s,size = min(self.t,len(self.data)),replace = False, p=self.costs/self.total_cost)
        s = sorted(s)
        count = 0
        for i in range(len(self.data)):
            if count < len(s):
                if(s[count] == i):
                    self.S[count]=self.data[s[count]]
                    self.wtsS[count] = self.total_cost/ (self.t*self.costs[s[count]])
                    self.wtsB[self.labels[s[count]]] = self.wtsB[self.labels[s[count]]] - self.wtsS[-1]
                    count = count + 1

            self.wtsB[self.labels[i]] = self.wtsB[self.labels[i]]+1




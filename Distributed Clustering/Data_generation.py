
'''
This class helps us generate distributed data from the centralized setting in 3 different ways.
'''

import random
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

class dataX:
    def __init__(self,dataF,n_nodes):
        self.data=dataF
        self.n_nodes=n_nodes
        self.length=len(dataF)
    def data_gen(self,type):
        self.type=type

        #Uniform distribution
        if (self.type == 1):
            for i in range(self.length):
                self.data[i].append(random.randint(0, self.n_nodes - 1))

        # Similarity based distribution
        if (self.type == 2):
            initial_points = random.sample(range(0, self.length), self.n_nodes)
            s = [i for i in range(self.n_nodes)]
            for i in range(self.length):
                pp = []
                if i not in initial_points:
                    for j in range(self.n_nodes):
                        try:
                            x = cosine_similarity(self.data[i], self.data[initial_points[j]])
                            pp.append(x[0][0])
                        except Exception:
                            pass
                    pp = pp / np.sum(pp)
                    index = np.random.choice(s, size=1, replace=False, p=pp)
                    self.data[i].append(index[0])
            w = 0
            for j in initial_points:
                self.data[j].append(w)
                w += 1

        # weighted distribution
        if (self.type == 3):
            s = [i for i in range(self.n_nodes)]
            pp = abs(np.random.normal(0.0, 1.0, size=self.n_nodes))
            pp = pp + 0.1
            pp = pp / np.sum(pp)
            for i in range(self.length):
                index = np.random.choice(s, size=1, replace=False, p=pp)
                self.data[i].append(index[0])

        return(self.data)





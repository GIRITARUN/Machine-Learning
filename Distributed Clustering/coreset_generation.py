'''
This module helps generate Global coresets for both the approaches.


'''

import node_code as nc
class coreset:
    def __init__(self,n_nodes,data,k,altt):
        self.A=[]
        self.B = []
        self.k=k
        self.altt=altt
        self.Naive_Global_Coreset = []
        self.Naive_Global_weights=[]
        self.t_cost=0
        self.Global_Coreset = []
        self.Global_weigths = []
        self.n_nodes=n_nodes
        self.data=data
        self.Global_Coreset1 = []
        self.Naive_Global_Coreset1 = []

    def gen_coreset(self):
        for i in range(self.n_nodes):
            data_n = self.data[self.data[:, len(self.data[0]) - 1] == i]
            self.A.append(nc.node(data_n, self.n_nodes, self.k, self.altt))
            self.A[i].k_means_algo()
            self.A[i].cost_vecs()
            self.t_cost = self.t_cost + self.A[i].total_cost
        for i in range(self.n_nodes):
            self.A[i].set_post_transfer(self.t_cost)
            self.A[i].sample()
            for j in self.A[i].S:
                self.Global_Coreset.append(j)
            for j in self.A[i].wtsS:
                self.Global_weigths.append(j)
            for j in self.A[i].B:
                self.Global_Coreset.append(j)
            for j in self.A[i].wtsB:
                self.Global_weigths.append(j)
        for i in range(len(self.Global_Coreset)):
            self.Global_Coreset1.append(self.Global_Coreset[i][:-1])
        return(self.Global_Coreset1,self.Global_weigths)

    def naive_gen_coreset(self):
        for i in range(self.n_nodes):
            data_n = self.data[self.data[:, len(self.data[0]) - 1] == i]
            self.B.append(nc.node(data_n, self.n_nodes, self.k, self.altt))
            self.B[i].k_means_algo()
            self.B[i].cost_vecs()
        for i in range(self.n_nodes):
            self.B[i].naive_post_transfer()
            self.B[i].Naive_sample()
            for j in self.B[i].S:
                self.Naive_Global_Coreset.append(j)
            for j in self.B[i].wtsS:
                self.Naive_Global_weights.append(j)
            for j in self.B[i].B:
                self.Naive_Global_Coreset.append(j)
            for j in self.B[i].wtsB:
                self.Naive_Global_weights.append(j)
        for i in range(len(self.Naive_Global_Coreset)):
            self.Naive_Global_Coreset1.append(self.Naive_Global_Coreset[i][:-1])
        return (self.Naive_Global_Coreset1,self.Naive_Global_weights)
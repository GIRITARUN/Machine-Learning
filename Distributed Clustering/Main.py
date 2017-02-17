# importing modules
import numpy as np
import sklearn.cluster as skl
import random
import warnings
import copy
import matplotlib.pyplot as plt
import node_code as nc
import weighted_k_means as wkm
import Data_generation
import Generate_graph
import coreset_generation
warnings.filterwarnings("ignore")

#Select how the data should be distributed from a centralized data (type 1= unifrom, 2= Similarity based 3= weighted based
type=3

# The algorithm is run tot_trails number of time, k is number of clusters needed, n_nodes is the number of nodes in the network
tot_trails=2;k=10;n_nodes=10

#select type of network should be generated (G_type 1= erdos_renyi_graph , 2=barabasi_albert_graph 3=grid network
G_type=1
G=Generate_graph.graph(G_type,n_nodes)

Y=[];X=[];dataF = []
#reading data
with open('C:/Users/tgiri2/Desktop/IE511/letter-recognition.txt', 'r') as data1:
    for line in data1:
        line = line.strip().split(',')
        dataF.append([int(x) for x in line[1:]])



# what would be the value if the data was centralized?
kmeans = skl.KMeans(n_clusters=k).fit(dataF)
cost_bad=kmeans.inertia_

# this is for ranging the number of points to be taken in forming the coreset
for i in range(4):
    altt =(i+1)*200
    ratio_plus,Naive_ratio_plus,communication_cost_plus,naive_communication_cost_plus= [0,0,0,0]
    for trail in range(tot_trails):
        dataq = copy.deepcopy(dataF)

        # generating distributed data from centralized data by calling Data_generation module
        new_data = Data_generation.dataX(dataq,n_nodes)
        data = new_data.data_gen(type)
        data = np.array(data)



        # generating coresets for 2 approaches by calling in coreset_generation
        cset=coreset_generation.coreset(n_nodes,data,k,altt)
        Global_Coreset1,Global_weigths=cset.gen_coreset()
        Naive_Global_Coreset1,Naive_Global_weights=cset.naive_gen_coreset()


        # calculating the centers by calling in a weighted kmeans module
        centers = wkm.get_centers(Global_Coreset1, Global_weigths,k)
        Naive_centers = wkm.get_centers(Naive_Global_Coreset1, Naive_Global_weights,k)

        # calculating costs for the 2 approaches
        the_cost = 0;the_Naive_cost = 0
        for i in range(len(dataF)):
            dist=[]
            for centeri in centers:
                dist.append((np.sum((dataF[i] - centeri) ** 2)))
            the_cost = dist[np.argmin(dist)] + the_cost

        for i in range(len(dataF)):
            Naive_dist=[]
            for centeri in Naive_centers:
                Naive_dist.append((np.sum((dataF[i] - centeri) ** 2)))
            the_Naive_cost = Naive_dist[np.argmin(Naive_dist)] + the_Naive_cost

        # calculating ratios of the costs from the 2 approaches with the cost in the centralized setting
        ratio_plus=(the_cost/cost_bad)+ratio_plus
        Naive_ratio_plus = (the_Naive_cost/cost_bad) + Naive_ratio_plus
        communication_cost_plus=(len(Global_Coreset1) * len(Global_Coreset1[0]) * G.number_of_edges())+communication_cost_plus
        naive_communication_cost_plus=naive_communication_cost_plus+(len(Naive_Global_Coreset1) * len(Naive_Global_Coreset1[0]) * G.number_of_edges())


    Y.append(ratio_plus/tot_trails)
    X.append(communication_cost_plus/tot_trails)
    print('For total number of points in coresets:',altt)
    print('Distributed ratio:',ratio_plus / tot_trails)
    print('Naive ratio:',Naive_ratio_plus / tot_trails)
    print('communication cost:',communication_cost_plus/tot_trails)
    print('naive communication cost:',naive_communication_cost_plus / tot_trails)


new_x, new_y = zip(*sorted(zip(X, Y)))
plt.plot(new_x, new_y)
plt.show()

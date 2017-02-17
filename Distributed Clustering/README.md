
This code was used to implement an advanced clusturing technique in distributed settings.
Paper can be found here:http://www.cs.princeton.edu/~yingyul/distributedClustering_full.pdf

Aim: This clustering method is designed to work btter than general algorithms when the data is spread
    across the network.I implemented the algorithm on the datasets which the authors have worked on and
    then on some new datasets to validate the results published in the paper.

Methodology:It uses a concept of corset generation for each node in the network.And based on these in a unique
            way points are sampled in the nodes.And only these few points which form the coresets are communicated
            across the network reducing the cost

Due to difficulty in obtaining a distributed data, the data was tranformed from a centralized one to a distributed one.
 This was done in three different ways(Unifrom, similarity and weighted).Network was simulated in three ways too.

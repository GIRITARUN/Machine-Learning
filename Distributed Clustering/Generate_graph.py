import networkx
def graph(G_type,n_nodes):
        if G_type==1:
            G=networkx.erdos_renyi_graph(n_nodes,0.3)
        if G_type==2:
            G=networkx.barabasi_albert_graph(n_nodes, 2, seed=None)
        if G_type ==3:
            G=networkx.grid_graph([3,3], periodic=False)
        return(G)
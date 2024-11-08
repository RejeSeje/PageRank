import matplotlib.pyplot as plt
import networkx as nx
import matplotlib

def construct_graph():
    with open('data/three.txt', 'rb') as fh:
        G = nx.read_adjlist(fh, create_using=nx.DiGraph())

    G = nx.relabel_nodes(G, {node: int(node) for node in G.nodes})

    return G

def get_size(G):
    return G.size()

def get_reverse(G):
    return G.reverse()

def get_branching_arr(G):
    max_node = max(G.nodes())
    branching = [0] * (max_node + 1)

    for node in range(max_node + 1):
        branching[node] = G.in_degree(node)

    return branching

def get_dangling_list(G):
    dangling_list = []
    branching_arr = get_branching_arr(G)

    for i, node in enumerate(branching_arr):
        if node == 0: dangling_list.append(i)

    return dangling_list

def get_initial_ranking_vector(G):
    n = max(G.nodes()) + 1
    ranking_vector = [(1/n)] * n

    return ranking_vector

if __name__ == '__main__':
    G = construct_graph()
    size = get_size(G)
    G_reversed = get_reverse(G)
    branching_arr = get_branching_arr(G)
    print(branching_arr)
    dangling_list = get_dangling_list(G)
    print(dangling_list)
    rv = get_initial_ranking_vector(G)
    print(rv)

    #nx.draw(G, with_labels=True)
    #plt.savefig("graph.png")
    #nx.draw(G_reversed, with_labels=True)
    #plt.savefig("graph_r.png")

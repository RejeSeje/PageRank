import matplotlib.pyplot as plt
import networkx as nx
import matplotlib

def construct_graph():
    with open('data/p2p-Gnutella08-mod.txt', 'rb') as fh:
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

def calculate_pagerank(G, damping_factor=0.85, max_iterations=100):
    # setup
    n = max(G.nodes()) + 1
    rv = get_initial_ranking_vector(G)  # x_0
    dangling_list = get_dangling_list(G)  # list of indices of dangling nodes (no outgoing edges)
    G_reversed = get_reverse(G)

    # outer loop
    for _ in range(max_iterations):
        x_next = [0] * n  # x_{k+1}

        dangling_sum = sum(rv[node] for node in dangling_list)
        dangling_contribution = (damping_factor * dangling_sum) / n  # Dx_k

        for i in range(n):
            x_next[i] = (1 - damping_factor) / n  # Sx_k
            x_next[i] += dangling_contribution

            for j in G_reversed[i]:  # Ax_k
                x_next[i] += damping_factor * rv[j] / G.out_degree(j)

        rv = x_next

    return rv


if __name__ == '__main__':
    G = construct_graph()
    pagerank_list = calculate_pagerank(G)

    sorted_pagerank = sorted(enumerate(pagerank_list), key=lambda x: x[1], reverse=True)
    print("the top 10 nodes:")
    for node, rank in sorted_pagerank[:10]:
        print(f"Node {node}: PageRank {rank}")
        #print(f"Node {node}: PageRank {rank:.4f}")  # limit floating digits
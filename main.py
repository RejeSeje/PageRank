import random

import matplotlib.pyplot as plt
import networkx as nx
import matplotlib
from networkx import pagerank


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

def calculate_pagerank(G, damping_factor=0.85, max_iterations=100, tolerance=1e-10):
    # setup
    n = max(G.nodes()) + 1
    rv = get_initial_ranking_vector(G)  # x_0
    dangling_list = get_dangling_list(G)  # list of indices of dangling nodes (no outgoing edges)
    G_reversed = get_reverse(G)

    previous_top_10 = None

    # outer loop
    for iter in range(max_iterations):
        x_next = [0] * n  # x_{k+1}

        dangling_sum = sum(rv[node] for node in dangling_list)
        dangling_contribution = (damping_factor * dangling_sum) / n  # Dx_k

        for i in range(n):
            x_next[i] = (1 - damping_factor) / n  # Sx_k
            x_next[i] += dangling_contribution

            for j in G_reversed[i]:  # Ax_k
                x_next[i] += damping_factor * rv[j] / G.out_degree(j)

        current_top_10 = sorted(enumerate(x_next), key=lambda x: x[1], reverse=True)[:10]

        # check for stability by the tolerance standard
        if previous_top_10:
            changes = [abs(current_top_10[i][1] - previous_top_10[i][1]) for i in range(10)]
            if all(change < tolerance for change in changes):
                # print(f"top 10 nodes stabilised after {iter} iterations.")
                return x_next, iter

        previous_top_10 = current_top_10
        rv = x_next

    print("max iterations reached without full stabilisation of top 10 nodes.")
    return rv, iter

def random_surfer(G, damping_factor=0.85, jumps=100000):
    n = max(G.nodes()) + 1
    visits = [0] * n  # list of visits for every site

    curr_node = random.choice(list(G.nodes()))

    for _ in range(jumps):
        visits[curr_node] += 1

        if random.random() < damping_factor and list(G.successors(curr_node)):
            curr_node = random.choice(list(G.successors(curr_node)))
        else:
            curr_node = random.choice(list(G.nodes()))

    rv = [visit_count / jumps for visit_count in visits]
    return rv

if __name__ == '__main__':
    G = construct_graph()
    random_surfer_list = random_surfer(G)
    pagerank_list_5th_digit, iter_5th = calculate_pagerank(G, tolerance=1e-5)
    pagerank_list_10th_digit, iter_10th = calculate_pagerank(G, tolerance=1e-10)

    sorted_random_surfer = sorted(enumerate(random_surfer_list), key=lambda x: x[1], reverse=True)
    sorted_pagerank_list_5th_digit = sorted(enumerate(pagerank_list_5th_digit), key=lambda x: x[1], reverse=True)
    sorted_pagerank_list_10th_digit = sorted(enumerate(pagerank_list_10th_digit), key=lambda x: x[1], reverse=True)
    print(f"the top 10 nodes for random surfing")
    for node, rank in sorted_random_surfer[:10]:
        print(f"Node {node}: PageRank {rank:.5f}")
    print("\n")

    print(f"the top 10 nodes for tolerance on 5th digit\nreached after {iter_5th} iterations:")
    for node, rank in sorted_pagerank_list_5th_digit[:10]:
        print(f"Node {node}: PageRank {rank:.5f}")
    print("\n")

    print(f"the top 10 nodes for tolerance on 10th digit\nreached after {iter_10th} iterations:")
    for node, rank in sorted_pagerank_list_10th_digit[:10]:
        print(f"Node {node}: PageRank {rank:.10f}")

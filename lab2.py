"""
Student's name: Duong Bui
Student's number: Y69125082
Student's email: thi.b.bui@student.oulu.fi
"""

import random
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import gzip
import powerlaw

def display_whole_graph(graph, title):
    plt.figure(figsize=(10,5))
    plt.title(title)
    nx.draw(graph, with_labels=True)
    plt.show()

def centrality_measures(graph):
    centrality_measures = [
        ("Degree Centrality", nx.degree_centrality(graph)),
        ("Eigenvector Centrality", nx.eigenvector_centrality(graph)),
        ("Katz Centrality", nx.katz_centrality(graph)),
        ("Page Rank Centrality", nx.pagerank(graph)),
        ("Closeness Centrality", nx.closeness_centrality(graph)),
        ("Betweenness Centrality", nx.betweenness_centrality(graph))
    ]
    return centrality_measures

def plot_centrality(graph):
    centralities = centrality_measures(graph)
    plt.figure(figsize=(15, 10))
    uniform_colors = ["blue", "green", "red", "purple", "cyan", "orange", "grey"]
    for i, (title, centrality) in enumerate(centralities, 1):
        plt.subplot(3, 2, i)
        node_color = [uniform_colors[i]] * len(graph.nodes())
        max_node = max(centrality, key=centrality.get)
        max_index = list(graph.nodes()).index(max_node)
        node_color[max_index] = "yellow"
        nx.draw(
            graph, 
            pos=nx.spring_layout(graph),
            node_color=node_color,
            with_labels=True
        )
        plt.title(title)
    plt.tight_layout()
    plt.show()
    
def centrality_histogram(graph):
    centralities= centrality_measures(graph)
    plt.figure(figsize=(15, 10))
    for i, (title, centrality) in enumerate(centralities, 1):
        plt.subplot(3, 2, i)
        plt.hist(list(centrality.values()), bins=20, alpha=0.75)
        plt.title(title)
    plt.tight_layout()
    plt.show()

def local_clustering_coefficient(graph):
    clustering_coefficients= nx.clustering(graph)
    # Displays the local clustering coefficient of each node
    print("Node\tClustering Coefficient")
    for node, cc, in clustering_coefficients.items():
        print(f"{node}\t{cc:.4f}")
    # Compare possible link between clustering coefficient values and some centrality measures
    centralities = nx.degree_centrality(graph)
    print("\nNode\tDegree Centrality\tClustering Coefficient")
    for node in graph.nodes():
        print(f"{node}\t{centralities[node]:.4f}\t\t{clustering_coefficients[node]:.4f}")
    # Draws the corresponding distribution function
    plt.figure(figsize=(10, 5))
    plt.hist(list(clustering_coefficients.values()), bins=20, alpha=0.75)
    plt.title("Local Clustering Coefficient Distribution")
    plt.xlabel("Clustering Coefficient")
    plt.ylabel("Frequency")
    plt.show()

def global_clustering_coefficient(graph):
    clustering_coefficient = nx.average_clustering(graph)
    print(f"Global Clustering Coefficient: {clustering_coefficient}")
    return clustering_coefficient

def smallest_global_coefficient_subgraph(graph):
    original_clustering_coefficient = nx.average_clustering(graph)
    smallest_subgraph = None
    smallest_subgraph_nodes = float('inf')
    subgraph = graph.copy()
    while len(subgraph.nodes()) > 1:
        node_to_remove = random.choice(list(subgraph.nodes()))
        subgraph.remove_node(node_to_remove)
        current_clustering_coefficient = nx.average_clustering(subgraph)
        coefficient_difference = abs(current_clustering_coefficient - original_clustering_coefficient)
        if coefficient_difference <= 0.2 and coefficient_difference > 0:
            if len(subgraph.nodes()) < smallest_subgraph_nodes:
                smallest_subgraph = subgraph
                smallest_subgraph_nodes = len(subgraph.nodes())
    return smallest_subgraph

def identify_bipartite_subgraph(graph):
    bipartite_subgraph = None
    subgraph = graph.copy()
    while (bipartite_subgraph == None) and (len(subgraph.nodes()) > 1):
        node_to_remove = random.choice(list(subgraph.nodes()))
        subgraph.remove_node(node_to_remove)
        if nx.is_bipartite(subgraph):
            bipartite_subgraph = subgraph
    return bipartite_subgraph

def load_facebook_dataset():
    with open("facebook_combined.txt", "r") as f:
        return nx.read_edgelist(f, create_using=nx.Graph(), nodetype=int)
    
def facebook_centrality_measures(graph):
    centrality_measures = [
        ("Degree Centrality", nx.degree_centrality(graph)),
        ("Closeness Centrality", nx.closeness_centrality(graph)),
        ("Betweenness Centrality", nx.betweenness_centrality(graph))
    ]
    return centrality_measures

def facebook_centrality_histogram(graph):
    centralities= facebook_centrality_measures(graph)
    plt.figure(figsize=(15, 10))
    for i, (title, centrality) in enumerate(centralities, 1):
        plt.subplot(3, 1, i)
        plt.hist(list(centrality.values()), bins=20, alpha=0.75)
        plt.title(title)
    plt.tight_layout()
    plt.show()

def shortest_distances(graph):
    centralities = facebook_centrality_measures(graph)
    for i, (title, centrality) in enumerate(centralities, 1):
        sorted_centrality = sorted(centrality.items(), key=lambda x: x[1], reverse=True)
        top_node, second_top_node = sorted_centrality[0][0], sorted_centrality[1][0]
        shortest_path = nx.shortest_path_length(graph, source=top_node, target=second_top_node)
        print(f"Shortest Distance with {title}: {shortest_path}")

def most_connected_subgraph(graph):
    degree_centrality = nx.degree_centrality(graph)
    max_degree_node = max(degree_centrality, key=degree_centrality.get)
    neighbors = list(graph.neighbors(max_degree_node))
    subgraph_nodes = [max_degree_node] + neighbors
    return graph.subgraph(subgraph_nodes)

def facebook_clustering_coefficient(graph):
    clustering_coefficients = nx.clustering(graph)
    sorted_coefficients = sorted(clustering_coefficients.items(), key=lambda x: x[1], reverse=True)
    top_node, second_top_node = sorted_coefficients[0][0], sorted_coefficients[1][0]
    shortest_path = nx.shortest_path_length(graph, source=top_node, target=second_top_node)
    print(f"Highest Clustering Coefficient: {clustering_coefficients[top_node]}")
    print(f"Second highest Clustering Coefficient: {clustering_coefficients[second_top_node]}")
    print(f"Shortest distance among highest and second highest clustering coefficient: {shortest_path}")

def check_power_law(graph):
    degrees = [d for n, d in graph.degree()]
    fit = powerlaw.Fit(degrees)
    print(f"Power-law fit parameters: {fit.power_law.alpha}")
    fit.plot_pdf(color='b', linewidth=2)
    fit.power_law.plot_pdf(color='b', linestyle='--')
    plt.hist(degrees, bins=10, density=True, color='g', alpha=0.5, label="Graph's Degree")
    # Add labels and legend
    plt.xlabel('Data')
    plt.ylabel('Probability Density')
    plt.legend()
    plt.show()

def main():
    # Section A
    karate_graph = nx.karate_club_graph()

    # a) Displays the whole graph 
    display_whole_graph(karate_graph, "Karate Graph")

    # b) Displays the degree centrality, eigenvector centrality, Katz centrality, page rank centrality
    # clossness centrality, betweenness centrality of each node of the network. Draw the network graph 
    # where the node with the highest centrality is highlighted (use different color for each centrality type)
    plot_centrality(karate_graph)

    # c) Draws the distribution (histogram) for each centrality measure
    centrality_histogram(karate_graph)

    # e) Displays the local clustering coefficient of each node, and draws the corresponding distribution function
    local_clustering_coefficient(karate_graph)
    """
    Through comparing the links between degree centrality and clustering coefficient, I see that the nodes with higher
    degree centrality tend to have lower clustering coefficients and vice versa
    """

    # f) Calculates the global clustering coefficient of the overall graph (or its largest connected componenty).
    global_clustering_coefficient(karate_graph)

    # g) Identify smallest subgraph that has a global clustering coefficient close to the one of the whole graph.
    subgraph = smallest_global_coefficient_subgraph(karate_graph)
    if subgraph != None:
        display_whole_graph(subgraph, "Smallest subgraph with global clusteirng coefficient")
    else:
        print("No subgraph meets requirement")

    # h) Identify a subgraph, which is bipartie graph
    bipartite_subgraph = identify_bipartite_subgraph(karate_graph)
    if bipartite_subgraph != None:
        display_whole_graph(bipartite_subgraph, "Bipartite subgraph")
    else:
        print("No subgraph meets requirement")
    # Section B
    facebook_graph = load_facebook_dataset()
    print(facebook_graph)

    # a) Calculates the degree, closeness and in-betweeness centrality of each node of the network, and displays the
    # corresponding distribution (histogram)
    facebook_centrality_histogram(facebook_graph)

    # b) Calculates the shortest distance between node (s) of highest centrality score and node (s) of second highest 
    # centrality score (for both degree, closeness, in-betweeness centraility measures)
    shortest_distances(facebook_graph)

    # c) Displays the subgraph where the nodes are most connected (in terms of degree centrality)
    facebook_subgraph = most_connected_subgraph(facebook_graph)
    print(facebook_subgraph)
    display_whole_graph(facebook_subgraph, "Facebook Subgraph")

    # d) Calculates the local clustering coefficients and the shortest distance among the nodes with highest and second 
    # highest clustering coefficient.
    facebook_clustering_coefficient(facebook_graph)

    # d) Checks whether Power-law distribution is fitted
    check_power_law(facebook_graph)
    # As indicated in the graph, the power law is fitted

if __name__ == "__main__":
    main()
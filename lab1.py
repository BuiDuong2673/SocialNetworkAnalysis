"""
Student's name: Duong Bui
Student's number: Y69125082
Student's email: thi.b.bui@student.oulu.fi
"""

import networkx as nx
import random
import matplotlib.pyplot as plt
import numpy as np
import pickle

def generate_random_graph(num_nodes, link_limit):
    """
    1) Write a full graph of 50 nodes where from each node, there is a link 
    (either in-going or out-going links) to one to 4 other nodes, taken at 
    random, of your choice. 
    Use a labelling of your choice to label each node of the network.
    """
    # Create graph
    graph = nx.Graph()
    # Add nodes
    for i in range(num_nodes):
         graph.add_node(f"Node {i+1}")
    # Add links
    for node in graph.nodes():
        # Get a list of nodes excluding the current node and
        # nodes that already has 4 connections
        available_nodes = []
        for n in graph.nodes():
            if (n != node) and (len(list(graph.neighbors(n))) < 4):
                available_nodes.append(n)
        # Randomly select up to the limitation of links from available nodes
        if len(available_nodes) > 0:
            max_links = min(link_limit, len(available_nodes))
            num_links = random.randint(1, max_links)
            linked_nodes = random.sample(available_nodes, num_links)
            for linked_node in linked_nodes:
                if len(list(graph.neighbors(node))) < 4:
                    graph.add_edge(node, linked_node)
        else:
            # In case when there is no node has less than 4 connection
            # the node is linked to itself
            if len(list(graph.neighbors(node))) == 0:
                graph.add_edge(node, node)
    return graph

def visualize_graph(graph):
    """
    a) Use a visualization tool to display the graph 
    """
    plt.figure(figsize=(8, 6))
    nx.draw(graph, with_labels=True)
    plt.title("Graph Visualization")
    plt.show()

def visualize_link(graph):
    """
    b) Use a visualization of your choice to display the nodes each node is linked to
    """
    for node in graph.nodes():
        linked_nodes = list(graph.neighbors(node))
        print(f"{node} is linked to {linked_nodes}.")

def calculate_degree_centrality(graph):
    """
    c) Calculate the degree centrality of each node and the average degree of the graph
    """
    degree_centrality = nx.degree_centrality(graph)
    average_degree = np.mean(list(degree_centrality.values()))
    return degree_centrality, average_degree

def plot_degree_distribution(graph):
    """
    d) Draw the degree distribution plot
    """
    degrees = [val for (node, val) in graph.degree()]
    plt.hist(degrees, bins=range(min(degrees), max(degrees) + 1), density=True)
    plt.xlabel("Degree")
    plt.ylabel("Frequency")
    plt.title("Degree distribution")
    plt.show()

def other_centrality(graph):
    """
    e) Test other centrality measures available in NetworkX and display their values, 
    and store the centrality values in a vector
    """
    betweenness_centrality = nx.betweenness_centrality(graph)
    closeness_centrality = nx.closeness_centrality(graph)

    betw_cen_values = list(betweenness_centrality.values())
    close_cen_values = list(closeness_centrality.values())

    return betw_cen_values, close_cen_values

def random_remove(graph):
    """
    f) write a script that randomly removes one node from the above graph
    until the number of nodes in the graph is equal to one.
    """
    while len(graph.nodes()) > 1:
        node_to_remove = random.choice(list(graph.nodes()))
        graph.remove_node(node_to_remove)
        print(f"Removed node: {node_to_remove}")
        # a) Display the graph
        visualize_graph(graph)

        # b) Display the nodes each node is linked to
        visualize_link(graph)

        # c) Calculate degree centrality and display the values
        degree_centrality, average_degree = calculate_degree_centrality(graph)
        print(f"Degree centrality: {degree_centrality}")
        print(f"Average degree: {average_degree}")

        # d) Draw the degree distribution plot and comment on whether the power-law distribution is fit
        plot_degree_distribution(graph)
    return graph

def remove_and_analyse(graph):
    """
    f) write a script that randomly removes one node from the above graph
    until the number of nodes in the graph is equal to one.

    g) Display a graph showing the variations of the various centrality measures as a function of the number of 
    edges in the graph.
    """
    # Create lists to store centrality measures
    degree_centralities = []
    betweenness_centralities = []
    closeness_centralitites = []
    num_edges = []
    while len(graph.nodes()) > 1:
        node_to_remove = random.choice(list(graph.nodes()))
        graph.remove_node(node_to_remove)
        print(f"Removed node: {node_to_remove}")
        # a) Display the graph
        visualize_graph(graph)

        # b) Display the nodes each node is linked to
        visualize_link(graph)

        # c) Calculate degree centrality and display the values
        degree_centrality, average_degree = calculate_degree_centrality(graph)
        print(f"Degree centrality: {degree_centrality}")
        print(f"Average degree: {average_degree}")

        # d) Draw the degree distribution plot and comment on whether the power-law distribution is fit
        plot_degree_distribution(graph)

        # e) Test other centrality measures available in NetworkX and display their values, and 
        #    store the centrality values in a vector
        degree_cen_values = list(degree_centrality.values())
        betw_cen_values, close_cen_values = other_centrality(graph)

        # Calculate average centrality values
        avg_degree_centrality = np.mean(degree_cen_values)
        avg_between_centrality = np.mean(betw_cen_values)
        avg_close_centrality = np.mean(close_cen_values)

        # Append average centrality of each graph to list
        degree_centralities.append(avg_degree_centrality)
        betweenness_centralities.append(avg_between_centrality)
        closeness_centralitites.append(avg_close_centrality)

        # Append the number of edges to the num_edges list
        num_edges.append(graph.number_of_edges())
    # Plot centrality measures as a function of the number of edges
    plt.plot(num_edges, degree_centralities, label='Degree Centrality')
    plt.plot(num_edges, betweenness_centralities, label='Betweenness Centrality')
    plt.plot(num_edges, closeness_centralitites, label='Closeness Centrality')
    plt.xlabel('Number of Edges')
    plt.ylabel('Centrality Measure')
    plt.legend()
    plt.title('Centrality Measures as Number of Edges function')
    plt.show()

def input_karate(file_name):
    """
    a) Write a program that input the karate_club_coords.pkl dataset
    """
    # Load the dataset
    with open(file_name, 'rb') as f:
        data = pickle.load(f, encoding='latin1')
    # Extract graph from the dataset
    graph = nx.karate_club_graph()
    graph = nx.convert_node_labels_to_integers(graph, first_label=1)
    graph = nx.relabel_nodes(graph, str)
    return graph

def display_adjacency_matrix(graph):
    """
    b) Displays the adjacency matrix of this graph and the network associated to this dataset
    """
    # Display adjacency matrix
    adjacency_matrix = nx.adjacency_matrix(graph).todense()
    print(f"Adjacency matrix {adjacency_matrix}")
    # Display network
    visualize_graph(graph)
    return adjacency_matrix

def identify_regular_graphs(graph):
    """
    d) Identifies potential regular graphs in the network.
    """
    degree_sequence = sorted([d for n, d in graph.degree()], reverse=True)
    if len(set(degree_sequence)) == 1:
        print("The graph is regular")
    else:
        print("The graph is not regular")

def identify_components(graph):
    """
    e) Uses appropriate NetworkX functions to identify the largest component of the graph, and smallest component.
    """
    largest_component = max(nx.connected_components(graph), key=len)
    smallest_component = min(nx.connected_components(graph), key=len)
    return largest_component, smallest_component

def compute_diameter(graph):
    """
    g) Use appropriate NetworkX functions to compute the diameter of the whole network and diameter of the largest 
    component
    """
    diameter = nx.diameter(graph)
    return diameter

def main():
    
    # Question 1:
    random_graph = generate_random_graph(50, 4)

    # a) Display the graph
    visualize_graph(random_graph)

    # b) Display the nodes each node is linked to
    visualize_link(random_graph)

    # c) Calculate degree centrality and display the values
    degree_centrality, average_degree = calculate_degree_centrality(random_graph)
    print(f"Degree centrality: {degree_centrality}")
    print(f"Average degree: {average_degree}")

    # d) Draw the degree distribution plot and comment on whether the power-law distribution is fit
    plot_degree_distribution(random_graph)
    """
    Through visualizing the degree distribution plot, I think the power-law distribution is fit.
    """

    # e) Test other centrality measures available in NetworkX and display their values, and 
    #    store the centrality values in a vector
    degree_cen_values = list(degree_centrality.values())
    betw_cen_values, close_cen_values = other_centrality(random_graph)
    print(f"Degree centrality: {degree_cen_values}")
    print(f"\nBetweenness centrality: {betw_cen_values}")
    print(f"\nCloseness centrality: {close_cen_values}")

    # f) Write a script that randomly removes one node from the above graph
    #   until the number of nodes in the graph is equal to one.
    # g) Display a graph showing the variations of the various centrality measures as a function of
    #   the number of edges in the graph.
    remove_and_analyse(random_graph)

    # Question 2
    # Use the provided dataset karate_club_coords.pkl.   
    # Write a program that 
    # a) Inputs the above dataset
    karate_graph = input_karate("karate_club_coords.pkl")

    # b) Displays the adjacency matrix of this graph and the network associated to this dataset
    adjacency_matrix = display_adjacency_matrix(karate_graph)

    # c) Calculates the degree centrality of each node and store them in an array vector
    degree_centrality, average_degree = calculate_degree_centrality(karate_graph)
    degree_centrality_values = np.array(list(degree_centrality.values()))
    print(degree_centrality_values)

    # d) Identifies potential regular graphs in the network. 
    identify_regular_graphs(karate_graph)

    # e) Uses appropriate NetworkX functions to identify the largest component of the graph, and
    # smallest component. 
    largest_component, smallest_component = identify_components(karate_graph)
    print("Nodes in the largest component:", largest_component)
    print("Nodes in the smallest component:", smallest_component)

    # f) Draw the degree distribution of this component (subgraph of d)).
    smallest_component_graph = karate_graph.subgraph(smallest_component)
    largest_component_graph = karate_graph.subgraph(largest_component)
    plot_degree_distribution(smallest_component_graph)
    plot_degree_distribution(largest_component_graph)

    # g) Use appropriate NetworkX functions to compute the diameter of the whole network and diameter
    # of the largest component
    diameter_whole_network = compute_diameter(karate_graph)
    diameter_largest_component = compute_diameter(largest_component_graph)
    print("Diameter of the whole network:", diameter_whole_network)
    print("Diameter of the largest component:", diameter_largest_component)

if __name__ == "__main__":
    main()
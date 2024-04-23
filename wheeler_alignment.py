import networkx as nx
import matplotlib.pyplot as plt

def create_wheeler_graph(strings):
    """Creates a Wheeler graph from a list of strings."""
    graph = nx.DiGraph()

    # Generate all rotations of each string and add them to the graph
    for s in strings:
        for i in range(len(s)):
            rotated = s[i:] + s[:i]
            graph.add_node(rotated)
            if i > 0:
                prev_rotated = s[i-1:] + s[:i-1]
                graph.add_edge(prev_rotated, rotated)

    # Sort nodes to visualize in Wheeler order
    sorted_nodes = sorted(graph.nodes(), key=lambda x: (x[-1], x))
    
    # Relabel nodes to show positions instead of content for clarity in visualization
    pos_labels = {node: f"{i}" for i, node in enumerate(sorted_nodes)}
    graph = nx.relabel_nodes(graph, pos_labels)
    
    return graph, pos_labels
import networkx as nx
import numpy as np
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

def smith_waterman(seq1, seq2, match_score=3, gap_cost=2, mismatch_cost=2):
    # Initialize the scoring matrix
    m, n = len(seq1), len(seq2)
    score_matrix = np.zeros((m+1, n+1))
    
    # Fill the scoring matrix
    max_score = 0
    max_pos = (0, 0)
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            match = score_matrix[i - 1][j - 1] + (match_score if seq1[i - 1] == seq2[j - 1] else -mismatch_cost)
            delete = score_matrix[i - 1][j] - gap_cost
            insert = score_matrix[i][j - 1] - gap_cost
            score = max(0, match, delete, insert)
            score_matrix[i][j] = score
            if score > max_score:
                max_score = score
                max_pos = (i, j)

    # Traceback to get the alignment
    align1, align2 = '', ''
    i, j = max_pos
    while score_matrix[i][j] > 0:
        score_current = score_matrix[i][j]
        score_diag = score_matrix[i - 1][j - 1]
        score_up = score_matrix[i][j - 1]
        score_left = score_matrix[i - 1][j]
        
        if score_current == score_diag + (match_score if seq1[i - 1] == seq2[j - 1] else -mismatch_cost):
            align1 += seq1[i - 1]
            align2 += seq2[j - 1]
            i -= 1
            j -= 1
        elif score_current == score_left - gap_cost:
            align1 += seq1[i - 1]
            align2 += '-'
            i -= 1
        else:
            align1 += '-'
            align2 += seq2[j - 1]
            j -= 1

    # Return the alignment and the score matrix
    return align1[::-1], align2[::-1], score_matrix


if __name__ == "__main__":
    with open('reference.txt', 'r') as file:
        reference = file.read().rstrip()
    with open('sample.txt', 'r') as file:
        sample = file.read().rstrip()
    graph, pos_labels = create_wheeler_graph([reference, sample])
    nx.draw(graph)
    plt.draw()  # pyplot draw()
    nodes = nx.draw_networkx_nodes(graph, pos=nx.spring_layout(graph))


# Plotting the scoring matrix
# plt.figure(figsize=(8, 6))
# plt.imshow(matrix, origin='upper', cmap='viridis')
# plt.colorbar()
# plt.xticks(np.arange(len(seq2)+1), '-' + seq2)
# plt.yticks(np.arange(len(seq1)+1), '-' + seq1)
# plt.title('Smith-Waterman Alignment Score Matrix')
# plt.show()


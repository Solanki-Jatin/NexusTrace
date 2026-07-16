"""
graph_engine.py

This is the same "brain" logic from analyze_graph.py, but rewritten as
reusable functions instead of a top-to-bottom script. This is what lets
our API call these functions on-demand, whenever a user uploads a file,
instead of only running once from the command line.
"""

import pandas as pd
import networkx as nx
import community as community_louvain
from io import StringIO


def build_graph_from_csv_text(csv_text: str) -> nx.Graph:
    """
    Takes the raw text content of an uploaded CSV file and builds a graph
    from it. Expects columns: caller, callee (at minimum).
    """
    df = pd.read_csv(StringIO(csv_text), dtype={"caller": str, "callee": str})

    G = nx.Graph()
    for _, row in df.iterrows():
        caller, callee = row["caller"], row["callee"]
        if G.has_edge(caller, callee):
            G[caller][callee]["weight"] += 1
        else:
            G.add_edge(caller, callee, weight=1)

    return G


def get_clusters(G: nx.Graph) -> dict:
    """Returns {phone_number: cluster_id} for every node in the graph."""
    return community_louvain.best_partition(G, weight="weight")


def get_centrality_scores(G: nx.Graph) -> dict:
    """Returns hub scores and bridge scores for every node."""
    degree_scores = nx.degree_centrality(G)
    betweenness_scores = nx.betweenness_centrality(G, weight="weight")
    return {"degree": degree_scores, "betweenness": betweenness_scores}


def get_shortest_path(G: nx.Graph, number_a: str, number_b: str):
    """Returns the connection path between two numbers, or None if no path exists."""
    try:
        return nx.shortest_path(G, source=number_a, target=number_b)
    except (nx.NetworkXNoPath, nx.NodeNotFound):
        return None


def graph_to_json(G: nx.Graph, partition: dict) -> dict:
    """Converts the graph into the {nodes, edges} format the frontend expects."""
    nodes = [{"id": n, "cluster": partition.get(n, -1)} for n in G.nodes()]
    edges = [{"source": u, "target": v, "weight": G[u][v]["weight"]} for u, v in G.edges()]
    return {"nodes": nodes, "edges": edges}

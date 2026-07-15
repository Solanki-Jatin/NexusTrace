"""
analyze_graph.py

This is the "brain" of NexusTrace. It reads the call records spreadsheet
and figures out:

1. Who calls who a lot (builds a graph / network out of the data)
2. Which groups of people call each other tightly and frequently
   (this is how we find suspect clusters, WITHOUT being told where to look)
3. Who the "important" / central people are in the network
   (the ones everyone calls, or the ones connecting different groups)

Think of this as the part that replaces hours of manual spreadsheet
staring with a few seconds of computation.
"""

import pandas as pd
import networkx as nx
import community as community_louvain  # this is the "python-louvain" library
import json

DATA_PATH = "data/call_records.csv"


def load_data():
    """Reads the CSV file into a table we can work with."""
    # dtype=str keeps phone numbers as text (e.g. "9876543210"), not as
    # actual numbers, since we never do math on them and treating them as
    # numbers can cause formatting bugs (like dropping leading digits)
    df = pd.read_csv(DATA_PATH, dtype={"caller": str, "callee": str})
    print(f"Loaded {len(df)} call records involving "
          f"{len(set(df['caller']) | set(df['callee']))} unique phone numbers.")
    return df


def build_graph(df):
    """
    Turns the spreadsheet into a graph.

    Every phone number becomes a NODE (a dot).
    Every call between two numbers becomes an EDGE (a line connecting two dots).

    If two people call each other multiple times, we don't draw multiple
    lines, instead we make ONE line but give it a "weight" = how many
    times they called. A weight of 15 means they called each other 15
    times, a weight of 1 means they only spoke once.
    """
    G = nx.Graph()  # undirected: we don't care who called who first, just that they're connected

    for _, row in df.iterrows():
        caller, callee = row["caller"], row["callee"]
        if G.has_edge(caller, callee):
            # they've called before, just increase the weight (call count)
            G[caller][callee]["weight"] += 1
        else:
            G.add_edge(caller, callee, weight=1)

    print(f"Graph built: {G.number_of_nodes()} nodes (people), "
          f"{G.number_of_edges()} unique connections (pairs who called each other).")
    return G


def find_clusters(G):
    """
    This is the key step: automatically groups nodes into clusters based
    on who talks to whom the most, using something called the "Louvain
    method" (a well-known, respected algorithm for this exact problem).

    People who call each other a LOT, relative to how much they call
    everyone else, get grouped into the same cluster. Our planted
    suspect group should show up as a small, dense cluster.
    """
    partition = community_louvain.best_partition(G, weight="weight")
    # partition is a dictionary: {phone_number: cluster_id}

    # Group numbers by their cluster id, so it's easier to read
    clusters = {}
    for number, cluster_id in partition.items():
        clusters.setdefault(cluster_id, []).append(number)

    print(f"\nFound {len(clusters)} clusters.")
    # Sort clusters by size, smallest first, tight suspect groups tend to be small and dense
    for cluster_id, members in sorted(clusters.items(), key=lambda x: len(x[1])):
        density_note = " <-- small & tight, worth investigating" if len(members) <= 8 else ""
        print(f"  Cluster {cluster_id} ({len(members)} people){density_note}: {members}")

    return partition, clusters


def find_important_people(G):
    """
    Figures out which phone numbers matter most in the network, using two
    different measures:

    - Degree centrality: how many DIFFERENT people this number talks to.
      High score = a "social hub" (could be a coordinator).
    - Betweenness centrality: how often this number sits BETWEEN two
      other people's shortest connection path. High score = this person
      bridges two otherwise separate groups (could be a middleman/broker).
    """
    degree_scores = nx.degree_centrality(G)
    betweenness_scores = nx.betweenness_centrality(G, weight="weight")

    top_degree = sorted(degree_scores.items(), key=lambda x: x[1], reverse=True)[:5]
    top_betweenness = sorted(betweenness_scores.items(), key=lambda x: x[1], reverse=True)[:5]

    print("\nTop 5 'social hub' numbers (talk to the most different people):")
    for number, score in top_degree:
        print(f"  {number}  (score: {score:.3f})")

    print("\nTop 5 'bridge/middleman' numbers (connect separate groups):")
    for number, score in top_betweenness:
        print(f"  {number}  (score: {score:.3f})")

    return degree_scores, betweenness_scores


def find_shortest_path(G, number_a, number_b):
    """
    Finds how two numbers are connected, even if they never called each
    other directly, e.g. A -> B -> C means A and C are connected THROUGH B.
    """
    try:
        path = nx.shortest_path(G, source=number_a, target=number_b)
        print(f"\nShortest connection path between {number_a} and {number_b}:")
        print("  " + " -> ".join(path))
        return path
    except nx.NetworkXNoPath:
        print(f"\nNo connection found between {number_a} and {number_b}.")
        return None


def save_results_for_frontend(G, partition):
    """
    Saves the graph + cluster results into a JSON file, this is the
    format our future website will read to draw the picture. Doing this
    now means the frontend work later just has to display this file.
    """
    nodes = [{"id": n, "cluster": partition[n]} for n in G.nodes()]
    edges = [{"source": u, "target": v, "weight": G[u][v]["weight"]} for u, v in G.edges()]

    output = {"nodes": nodes, "edges": edges}
    with open("data/graph_output.json", "w") as f:
        json.dump(output, f, indent=2)

    print(f"\nSaved graph data for the frontend to data/graph_output.json")


if __name__ == "__main__":
    df = load_data()
    G = build_graph(df)
    partition, clusters = find_clusters(G)
    find_important_people(G)

    # demo: pick two random numbers from the data and show how they connect
    sample_nodes = list(G.nodes())[:2]
    find_shortest_path(G, sample_nodes[0], sample_nodes[1])

    save_results_for_frontend(G, partition)

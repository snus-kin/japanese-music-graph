""" analyse the data """
import csv
import itertools
import networkx as nx

G = nx.Graph()

with open("../data/largest.csv", 'r') as creds:
    credit_reader = csv.reader(creds, delimiter=",", quotechar='"')
    for album in credit_reader:
        album_name = "%s - %s" % (album[0], album[1])
        credit_list = album[2][1:-1].replace("'", "").split(", ")
        if len(credit_list) > 50:
            continue

        G.add_nodes_from(credit_list)
        edges = itertools.combinations(credit_list, 2)
        G.add_edges_from(list(edges), album=album_name)

    G_smaller = nx.Graph()
    nodes = G.nodes()
    for node in nodes:
        print(node)
        edges = list(G.edges(node, data=True))
        if len(edges) <= 1:
            continue
        album = edges[0][2]["album"]
        for edge in edges:
            if edge[2]["album"] == album:
                pass
            else:
                G_smaller.add_node(node)
                G_smaller.add_edges_from(edges)

    nx.write_gexf(G_smaller, "uniquealbums.gexf")

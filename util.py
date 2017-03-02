import sys
import os.path
import networkx as nx
import matplotlib.pyplot as plt
import csv

AIRBNB_DATA_DIR = "/Users/kaho/projects/data_l109/airbnb/"

DATA_DIR = "/Users/kaho/projects/data_l109/small_foursquare_dataset"

def gen_fsq_edges():
    transit = []
    with open(os.path.join(DATA_DIR, "new_york_placenet_transitions.txt"), 'r') as f:
        r = csv.DictReader(f)
        for row in r:
            transit.append({"from": int(row["from"]),
                            "to": int(row["to"]),
                            "time_from": row["time_from"],
                            "time_to": row["time_to"]})
    return transit
def gen_fsq_nodes():
    locations = {}
    with open(os.path.join(DATA_DIR, "new_york_anon_locationData_newcrawl.txt"), 'r') as f:
        for row in f:
            id_ent = row.split("*;*")
            fields = map(lambda x: x.strip(), id_ent[1][1:-2].split(","))
            locations[int(id_ent[0])] = {"latitude": float(fields[0]),
                                    "longtitude": float(fields[1]),
                                    "type": fields[2][1:-1],
                                    "total_users": int(fields[3][1:-1]),
                                    "total_checkins": int(fields[4][1:-1]),
                                    "name": fields[5][1:-1]}
    return locations

def compute_distance(edge, nodes):
    from_node = nodes[edge["from"]]
    to_node = nodes[edge["to"]]
    return pow(pow((from_node["longtitude"] - to_node["longtitude"]), 2)
               + pow((from_node["latitude"] - to_node["latitude"]), 2), 0.5)

def gen_weighted_undirected_graph_fsq(weight):
    g = nx.MultiGraph()
    nodes = gen_fsq_nodes()
    edges = gen_fsq_edges()
    for k, v in nodes.iteritems():
        g.add_node(k, v)
    for e in edges:
        try:
            g.add_edge(e["from"], e["to"], weight=weight(e, g.node), time_from=e["time_from"],
                           time_to=e["time_to"])
        except ZeroDivisionError:
            continue
    return g


def gen_weighted_undirected_non_multi_graph_fsq(weight):
    g = nx.Graph()
    nodes = gen_fsq_nodes()
    edges = gen_fsq_edges()
    for k, v in nodes.iteritems():
        g.add_node(k, v)
    for e in edges:
        try:
            g.add_edge(e["from"], e["to"], weight=weight(e, g.node), time_from=e["time_from"],
                           time_to=e["time_to"])
        except ZeroDivisionError:
            continue
    return g

def gen_unweighted_undirected_graph_fsq():
    g = nx.Graph()
    nodes = gen_fsq_nodes()
    edges = gen_fsq_edges()
    for k, v in nodes.iteritems():
        g.add_node(k, v)
    for e in edges:
        if e["from"] != e["to"]:
            g.add_edge(e["from"], e["to"], weight=1, time_from=e["time_from"],
                       time_to=e["time_to"])
    return g

def plot(data,filename, xlabel):
    """ Plot Distribution """
    plt.plot(range(len(data)),data,'bo')
    plt.yscale('log')
    plt.xscale('log')
    plt.ylabel('Freq')
    plt.xlabel(xlabel)
    plt.savefig(filename + '_distribution.png')
    plt.clf()

    """ Plot CDF """
    s = float(data.sum())
    cdf = data.cumsum(0)/s
    plt.plot(range(len(cdf)),cdf,'bo')
    plt.xscale('log')
    plt.ylim([0,1])
    plt.ylabel('CDF')
    plt.xlabel(xlabel)
    plt.savefig(filename + '_cdf.png')
    plt.clf()

    """ Plot CCDF """
    ccdf = 1-cdf
    plt.plot(range(len(ccdf)),ccdf,'bo')
    plt.xscale('log')
    plt.yscale('log')
    plt.ylim([0,1])
    plt.ylabel('CCDF')
    plt.xlabel(xlabel)
    plt.savefig(filename + '_ccdf.png')
    plt.clf()

def gen_listings(keys, floats):
    listings = {}
    with open(os.path.join(AIRBNB_DATA_DIR, "listings_simple.csv"), 'r') as f:
        r = csv.DictReader(f)
        for row in r:
            info = {}
            for k in keys:
                if k in floats:
                    info[k] = float(row[k])
                else:
                    info[k] = row[k]
            listings[row["id"]] = info
    return listings

def read_partitions():
    to_return = {}
    with open("partition.txt", 'r') as f:
        for l in f:
            if l:
                node = map(int, l.strip().split(" "))
                to_return[node[0]] = node[1]
    return to_return

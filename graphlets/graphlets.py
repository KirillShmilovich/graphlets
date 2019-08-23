"""
graphlets.py
Python package for computing graphlets

Handles the primary functions
"""
from .utils import *

import numpy as np
import networkx as nx
from joblib import Parallel, delayed
import subprocess

__all__ = ["Graphlets"]

class Graphlets():

    def __init__(self, X, dims=None, metric="euclidean"):
        "X is (time_steps, num_structures, p_dims)"
        self.X = X
        self.metric = metric
        self.depth = 5
        self.dims = dims
    
    def make_graphs(self, r_cut, n_jobs=-1):
        if n_jobs==1:
            return [compute_graph(x, r_cut, dims=self.dims, metric=self.metric) for x in self.X]
        else:
            return Parallel(n_jobs=n_jobs)(delayed(compute_graph)(x, r_cut, dims=self.dims, metric=self.metric) for x in self.X)

    def decompose(self, G, t):
        in_file = f".edgelist_{t}.dat"
        out_file = f".edgelist_{t}.out"

        f = open(in_file,"wb")
        f.write(f"{nx.number_of_nodes(G)} {nx.number_of_edges(G)}\n".encode())
        nx.write_edgelist(G, f, data=False)
        f.close()

        command = [ORCA_PATH, "node", str(self.depth), in_file, out_file]
        subprocess.call(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        decomposition = np.loadtxt(out_file)*weights
        command = ["rm", out_file, in_file]
        subprocess.call(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return decomposition
    
    def compute(self, r_cut, reduce=True, n_jobs=-1):
        self.G = self.make_graphs(r_cut=r_cut, n_jobs=n_jobs)
        if n_jobs==1:
            G_total = np.asarray([self.decompose(G,t) for t,G in enumerate(self.G)])
        else:
            G_total = np.asarray(Parallel(n_jobs=n_jobs)(delayed(self.decompose)(G,t) for t,G in enumerate(self.G)))

        if reduce is True:
            G_sum = G_total.sum(axis=1)
            return G_sum / G_sum.sum(axis=1,keepdims=True)
        else:
            return G_total
    
    def scan_r_cut(self, r_min, r_max, num=25, n_jobs=-1):
        r_scan = np.empty(shape=num)
        if n_jobs==1:
            for i,r in enumerate(np.linspace(r_min,r_max,num=num)):
                self.G = self.make_graphs(r_cut=r, n_jobs=n_jobs)
                r_scan[i] = np.asarray([nx.number_of_edges(G) for G in self.G]).mean()
        else: 
            for i,r in enumerate(np.linspace(r_min,r_max,num=num)):
                self.G = self.make_graphs(r_cut=r, n_jobs=n_jobs)
                r_scan[i] = np.asarray(Parallel(n_jobs=n_jobs)(delayed(nx.number_of_edges)(G) for G in self.G)).mean()
        return r_scan


    

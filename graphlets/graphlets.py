"""
graphlets.py
Python package for computing graphlets

Handles the primary functions
"""
from .utils import *

import numpy as np
from joblib import Parallel, delayed
import subprocess


class Graphlets():

    def __init__(self, X, dims=None, metric="euclidean", depth=5):
        "X is (time_steps, num_structures, p_dims)"
        self.X = X
        self.metric = metric
        self.depth = depth
        self.dims = dims
    
    def decompose(self,G,t):
        in_file = f".edgelist_{t}.dat"
        out_file = f".edgelist_{t}.out"

        f = open(in_file,"wb")
        f.write(f"{nx.number_of_nodes(G)} {nx.number_of_edges(G)}\n".encode())
        nx.write_edgelist(G,f,data=False)
        f.close()

        command = [ORCA_PATH,"node",str(self.depth),in_file,out_file]
        subprocess.call(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        decomposition = np.loadtxt(out_file)*weights
        command = ["rm",out_file,in_file]
        subprocess.call(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return decomposition
    
    def compute(self,r_cut, reduce=True, n_jobs=-1):
        G_all = np.asarray(Parallel(n_jobs=n_jobs)(delayed(self.decompose)(compute_graph(x, r_cut, dims=self.dims, metric=self.metric),t) for t,x in enumerate(self.X)))
        if reduce is True:
            return G_all
        else:
            return G_all

    

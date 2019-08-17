"""
util.py

Some utility functions
"""
import os
import numpy as np
from sklearn.neighbors import BallTree, radius_neighbors_graph
import networkx as nx

__all__ = ["ORCA_PATH", "pbc", "orbits", "weights", "compute_graph"]

ORCA_PATH = os.path.abspath(os.path.abspath(__file__) + "../../../orca/orca.exe")


def pbc(x0, x1, dims):
    delta = np.abs(x0 - x1)
    delta = np.where(delta > 0.5 * dims, delta - dims, delta)
    return np.sqrt((delta**2).sum(axis=-1))


orbits = np.array([
    1, 2, 2, 2, 3, 4, 3, 3, 4, 3, 4, 4, 4, 4, 3, 4, 6, 5, 4, 5, 6, 6, 4, 4, 4, 5, 7, 4, 6, 6, 7, 4, 6, 6, 6, 5, 6, 7,
    7, 5, 7, 6, 7, 6, 5, 5, 6, 8, 7, 6, 6, 8, 6, 9, 5, 6, 4, 6, 6, 7, 8, 6, 6, 8, 7, 6, 7, 7, 8, 5, 6, 6, 4
],
                  dtype=np.float)
weights = 1. - np.log(orbits) / np.log(73.)


def compute_graph(X, r_cut, **kwargs):
    if kwargs["dims"] is not None:
        BT = BallTree(X, metric=kwargs["metric"], dims=kwargs["dims"])
    else:
        BT = BallTree(X, metric=kwargs["metric"])
    rng_con = radius_neighbors_graph(BT, r_cut, n_jobs=1, mode='connectivity')
    A = np.matrix(rng_con.toarray())
    G = nx.from_numpy_matrix(A)
    return G

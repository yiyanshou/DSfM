# -*- coding: utf-8 -*-
"""
Created on Wed Nov 11 21:26:05 2020

@author: yiyan
"""

import numpy as np
import numpy.linalg as lin
from random import sample

#the top n ranked nodes will be printed
n = 6

#0-read existing adjacency matrix from file, 1-generate new
#adjacency matrix and save to file
generate = 0

path = "ex6.npy"

#size of adjacency matrix (only used if generate = 1)
N = 100

#default range of numbers of incoming edges (only used if generate = 1)
default_in = (20, 25)

#specifies a range of numbers of incoming edges for specific vertices (only
#used if generate = 1)
override_in = {0 : (40, 40), 1 : (30, 30)}

#adds positive noise to each entry to ensure connectivity. Should be between
#0 and 1
noise = 0.15

#randomly generates an adjacency matrix based on parameters above
if generate == 1:
    adj = np.zeros((N, N))
    for j in range(N):
        if j in override_in:
            in_min = override_in[j][0]
            in_max = override_in[j][1]
        else:
            in_min = default_in[0]
            in_max = default_in[1]
        num_in = sample(range(in_min, in_max + 1), 1)[0]
        ind_in = sample([i for i in range(N) if not i == j], num_in)
        for i in ind_in:
            adj[i, j] = 1
    np.save(path, adj)
else:
    adj = np.load(path)

#adjacency matrix with positive noise added
noise_array = np.full(adj.shape, 1 / adj.shape[0])
noisy_adj = (1 - noise) * adj + noise * noise_array

#noised adjacency matrix reweighted according to numbers of outgoing edges
#(row-stochastic)
stoch_adj = noisy_adj.copy()
for i in range(adj.shape[0]):
    stoch_adj[i, 0:] /= np.sum(noisy_adj[i, 0:])

#transpose of the reweighted, noised adjacency matrix. The unique 1-eigenvector
#is the vector of rankings given by the PageRank algorithm.
P = stoch_adj.transpose()
eigvals, eigvecs = lin.eig(P)
rank = eigvecs[0:, np.abs(eigvals).argmax()]

#vector of rankings normalized to have supremum norm 1
rank /= rank[np.abs(rank).argmax()]

#the top n highest ranked nodes and their rankings
inds_sorted = rank.argsort()[-n:]
ranks_sorted = np.array([rank[i] for i in inds_sorted[-n:]], dtype = 'float32')
print(inds_sorted)
print(ranks_sorted.round(2))
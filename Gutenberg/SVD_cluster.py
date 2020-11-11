# -*- coding: utf-8 -*-
"""
Created on Mon Nov  9 19:37:28 2020

@author: yiyan
"""

import numpy as np
import numpy.linalg as lin
import matplotlib.pyplot as plt
import mpl_toolkits.mplot3d

plt.ion()

#path for term-by-page matrix as comma separated array
mat_txt = open("term_by_doc_mat.txt")

#0-read SVD from file, 1-recalculate SVD and save to file
calc = 0

#list of term-by-document matrices with W[0] = raw matrix, 
#W[1] = column normalized, W[2] = boolean
W = [None] * 3
W[0] = np.array([line[:len(line) - 2].split(',') for line in mat_txt], 
                   dtype = np.float)
W[1] = np.empty(W[0].shape)
for j in range(W[0].shape[1]):
    col_norm = lin.norm(W[0][0:, j])
    if col_norm == 0:
        W[1][0:, j] = W[0][0:, j]
    else:
        W[1][0:, j] = W[0][0:, j] / col_norm
        
W[2] = np.empty(W[0].shape)
for i in range(W[0].shape[0]):
    for j in range(W[0].shape[1]):
        if W[0][i, j] == 0:
            W[2][i, j] = 0
        else:
            W[2][i, j] = 1

#projects onto the first 1, 2, and 3 singular vectors
for i in range(3):
    if calc == 0:
        U = np.load("U%d_mat.npy" % i)
        s = np.load("s%d_vals.npy" % i)
        V = np.load("V%d_mat.npy" % i)
    else:
        U, s, V = lin.svd(W[i])
        np.save("U%d_mat.npy" % i, U)
        np.save("s%d_vals.npy" % i, s)
        np.save("V%d_mat.npy" % i, V)
        
    #projects onto first 2 singular directions
    U_red = U[0:, 0:2]
    V_red = V[0:2, 0:]
    doc_proj = U_red.transpose().dot(W[i])
    term_proj = W[i].dot(V_red.transpose())
    
    fig = plt.figure()
    fig.suptitle("Weighting scheme: %d" % i)
    
    plt.subplot(121)
    plt.title("Documents")
    plt.plot(doc_proj[0, 0:], doc_proj[1, 0:], "bo")
    
    plt.subplot(122)
    plt.title("Terms")
    plt.plot(term_proj[0:, 0], term_proj[0:, 1], "ro")
    
    #projects onto first 3 singular directions
    U_red = U[0:, 0:3]
    V_red = V[0:3, 0:]
    doc_proj = U_red.transpose().dot(W[i])
    term_proj = W[i].dot(V_red.transpose())
    
    fig = plt.figure()
    fig.suptitle("Weighting scheme: %d" % i)
    
    plt.subplot(121, projection = '3d')
    plt.title("Documents")
    plt.plot(doc_proj[0, 0:], doc_proj[1, 0:], doc_proj[2, 0:], "bo")
    
    plt.subplot(122, projection = '3d')
    plt.title("Terms")
    plt.plot(term_proj[0:, 0], term_proj[0:, 1], term_proj[0:, 2], "ro")
    
plt.show(block = True)
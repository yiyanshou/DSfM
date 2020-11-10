# -*- coding: utf-8 -*-
"""
Created on Mon Nov  9 19:37:28 2020

@author: yiyan
"""

import numpy as np
import numpy.linalg as lin
from nltk import PorterStemmer

#path for term-by-page matrix as comma separated array
mat_txt = open("term_by_doc_mat.txt")

#list of strings to query from the database
query = ['good', 'evil', 'legend', 'myth', 'god', 'demon', 'spirit', 'ritual',
         'sacred', 'sacrement', 'divine', 'holy', 'sin', 'deity']

#minimum relative error in rank reduced matrix measured in Frobenius norm
err = 0.1

#threshold for when a document is considered a good match
thresh = 0.0

#number of recommendations
n = 3

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

#reduces the ranks of the W[i] matrices using SVD. The rank will be reduced to
#to the point where the relative error measured in Frobenius norm is at least
#err.
W_red = [None] * 3

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
    s_red = s.copy()
    k = -1
    while (((lin.norm(s) ** 2) - (lin.norm(s_red) ** 2)) 
                / (lin.norm(s) ** 2)) < err ** 2:
        s_red[k] *= 0
        k -= 1
    S = np.zeros((U.shape[1], V.shape[0]))
    for j in range(s_red.shape[0]):
        S[j, j] = s_red[j]
    W_red[i] = U.dot(S.dot(V))
    
#turns query into a binary vector based on supplied dictionary of terms
porter = PorterStemmer()
terms = {}   
with open("terms.txt") as f:
    for line in f:
        pair = line.split(',')
        terms[pair[0]] = int(pair[1])

q_vec = np.zeros((1, W[0].shape[0]))      
for word in query:
    s = porter.stem(word.lower())
    if s in terms:
        q_vec[0, terms[s]] = 1

#vectorized recommendation based on query
rec_vec = [np.zeros(q_vec.shape)] * 3
q_vec_norm = lin.norm(q_vec)
for i in range(3):
    for j in range(W[0].shape[1]):
        d = np.dot(q_vec, W_red[i][0:, j])
        rec_vec[i][0, j] = d / (q_vec_norm * lin.norm(W_red[i][0:, j]))

#retrieves a list of recommendations based on thresh and supplied dictionary of
#documents. List is in ascending order of relevance.
docs = {}
with open("docs.txt") as f:
    for line in f:
        pair = line.split(',')
        docs[int(pair[1])] = pair[0]

recs = [None] * 3
for i in range(3):
    recs[i] = []
    threshed_inds = []
    for j in range(rec_vec[i].shape[1]):
        if rec_vec[i][0, j] >= thresh:
            threshed_inds.append(j)
    threshed = np.array([rec_vec[i][0, j] for j in threshed_inds])
    m = min(len(threshed), n)
    highest_inds = [threshed_inds[j] for j in threshed.argpartition(-m)[-m:]]
    highest = np.array([rec_vec[i][0,j] for j in highest_inds])
    ascending_inds = [highest_inds[j] for j in highest.argsort()]
    ascending = np.array([rec_vec[i][0,j] for j in ascending_inds])
    for j in ascending_inds:
        recs[i].append((docs[j], rec_vec[i][0,j]))
 
print(recs)  
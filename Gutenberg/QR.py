# -*- coding: utf-8 -*-
"""
Created on Sun Nov  8 01:10:53 2020

@author: yiyan
"""
import numpy as np
import numpy.linalg as lin
import math
from nltk import PorterStemmer

#path for term-by-page matrix as comma separated array
mat_txt = open("term_by_doc_mat.txt")

#list of strings to query from the database
query = ['twighlight', 'gods', 'legend', 'myth', 'story', 'tale', 'mystic',
         'magic', 'good', 'evil', 'epic', 'quest', 'journey']

#proportion of rank to retain (assumes term_by_doc matrix is full rank)
rp = 0.20

#threshold for when a document is considered a good match
thresh = 0.0

#number of recommendations
n = 5

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

#reduces the ranks of the W[i] matrices using QR decomposition
W_red = [None] * 3
for i in range(3):       
    Q, R = lin.qr(W[i])
    D = np.array([abs(R[j, j]) for j in range(min(R.shape[0],
                    R.shape[1]))])
    r_red = math.floor((1 - rp) * W[i].shape[1])
    for j in np.argpartition(D, r_red)[:r_red]:
        R[j, 0:] *= 0
    W_red[i] = np.dot(Q, R)

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
#documents
docs = {}
with open("docs.txt") as f:
    for line in f:
        pair = line.split(',')
        docs[int(pair[1])] = pair[0]

recs = [None] * 3
for i in range(3):
    recs[i] = []
    inds = []
    for j in range(rec_vec[i].shape[1]):
        if rec_vec[i][0, j] >= thresh:
            inds.append(j)
    threshed = np.array([rec_vec[i][0, j] for j in inds])
    m = min(len(threshed), n)
    highest = np.argpartition(threshed, -m)[-m:]
    highest_inds = [inds[j] for j in highest]
    sorted_inds = np.argsort(np.array([rec_vec[i][0, j] for j in highest_inds]))
    for j in sorted_inds:
        recs[i].append(docs[j])

print (np.max(rec_vec[0]))
print (np.max(rec_vec[1])) 
print (np.max(rec_vec[2])) 
print(recs)  
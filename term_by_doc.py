# -*- coding: utf-8 -*-
"""
Created on Sat Nov  7 21:19:54 2020

@author: yiyan
"""

import numpy as np
import os

n = 2000    # n is the number of words to extract from each document
files_dir = "files\\"     #relative path to directory containg documents

docs = os.listdir(files_dir)
terms = []
doc_coords = {}
term_coords = {}
term_by_doc = np.zeros((1, len(docs)), dtype = np.int16)

for i in range(len(docs)):
    doc_coords[docs[i]] = i

for filename in docs:
    words = []
    file = open(files_dir + filename)
    s = ""
    while len(words) < n:
        next_char = file.read(1).lower()
        if next_char == "\'" or (s == "" and not next_char.isalpha()):
            continue
        if next_char == "-":
            pos = file.tell()
            check_next = file.read(1)
            if not check_next == "-":
                continue
            else:
                file.seek(pos)
        if not next_char.isalpha():
            if len(s.strip()) > 0:
                words.append(s)
            s = ""
        else:
            s += next_char
        if next_char == "":
            break
    
    for word in words:
        if word not in terms:
            terms.append(word)
            term_coords[word] = len(terms) - 1
            term_by_doc.resize((len(terms), len(docs)))
        term_by_doc[term_coords[word], doc_coords[filename]] += 1
    file.close()

with open("docs.txt", "w") as f:
    for doc in doc_coords:
        f.write(doc + ',' + str(doc_coords[doc]) + '\n')
with open("terms.txt", "w") as f:
    for term in term_coords:
        f.write(term + ',' + str(term_coords[term]) + '\n')
with open("term_by_doc_mat.txt", "w") as f:
    d = term_by_doc.shape
    for i in range(d[0]):
        for j in range(d[1]):
            f.write(str(term_by_doc[i,j]) + ",")
        f.write('\n')
print("dimensions of matrix: " + str(term_by_doc.shape))
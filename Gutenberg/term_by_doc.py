# -*- coding: utf-8 -*-
"""
Created on Sat Nov  7 21:19:54 2020

@author: yiyan
"""

import numpy as np
import os
from nltk import PorterStemmer

n = 2000    # n is the number of words to extract from each document
files_dir = "files\\"     #relative path to directory containg documents

docs = os.listdir(files_dir)
terms = []
doc_coords = {}
term_coords = {}
term_by_doc = np.zeros((1, len(docs)), dtype = np.int16)

#creates a dictionary of document : coordinate pairs
for i in range(len(docs)):
    doc_coords[docs[i]] = i

#finds the first n words in each document and forms the term-by-document matrix
for filename in docs:
    words = []
    file = open(files_dir + filename)
    
    #skips past the boilerplate at the beginning of each document
    line = " "
    while not (len(line) >= 2 and line[len(line) - 2:] == '**'):
        line = file.readline().strip()

    #parses document into words using whitespace as delimiters. Removes
    #punctuation except for apostrophes and hyphens.
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
   
    #updates the dictionary of terms and the term-by-document matrix as each
    #new document is parsed. Performs stemming of terms.
    for word in words:
        #stemming using Porter Stemmer from nltk
        porter = PorterStemmer()
        word = porter.stem(word)
        
        #if a new term was found, updates the dictionary of terms
        if word not in terms:
            terms.append(word)
            term_coords[word] = len(terms) - 1
            term_by_doc.resize((len(terms), len(docs)))
            
        #updates term-by-document matrix
        term_by_doc[term_coords[word], doc_coords[filename]] += 1
    file.close()

#creates text file encoding a dictionary of document : coordinate pairs as 
#a list of comma separated pairs
with open("docs.txt", "w") as f:
    for doc in doc_coords:
        f.write(doc + ',' + str(doc_coords[doc]) + '\n')
        
#creates text file encoding a dictionary of term : coordinate pairs as 
#a list of comma separated pairs
with open("terms.txt", "w") as f:
    for term in term_coords:
        f.write(term + ',' + str(term_coords[term]) + '\n')
        
#creates a text file encoding the term-by-document matrix as a list of comma
#separated rows
with open("term_by_doc_mat.txt", "w") as f:
    d = term_by_doc.shape
    for i in range(d[0]):
        for j in range(d[1]):
            f.write(str(term_by_doc[i,j]) + ",")
        f.write('\n')
        
print("dimensions of matrix: " + str(term_by_doc.shape))
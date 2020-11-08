# -*- coding: utf-8 -*-
"""
Created on Sat Nov  7 15:52:11 2020

@author: yiyan
"""

# Writes a list of ebook numbers for English language books 
# on Project Gutenberg.
index = open("gutindex.txt", "r")
ebooks = open("ebooks.txt", 'w')
count = 0
while True:
    try:
        s = index.readline()
    except:
        continue
    if s ==  "":
        break
    s = s.strip()
    if s == "" or s.isnumeric():
        continue
    if s[-1].isnumeric():
        t = ""
        try:
            while True:
                n = index.readline().strip()
                if n == "":
                    break
                t += n
        except:
            continue
        if t.upper().find("[LANG") == -1:
            i = -1
            while s[i].isnumeric():
                i -= 1
            ebooks.write(s[i + 1 : ] + '\n')
            count += 1

ebooks.write("---Count---\n " + str(count))           
index.close()
ebooks.close()
print(count)
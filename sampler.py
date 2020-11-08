# -*- coding: utf-8 -*-
"""
Created on Sat Nov  7 18:06:16 2020

@author: yiyan
"""

import subprocess
from random import sample
from time import sleep

n = 300    # number of books to sample

ebooks = open("ebooks.txt")
nums = []
count = 0
files_dir = "C:\\Users\\yiyan\\OneDrive\\Documents\\Python\\Gutenberg_robot\\files"
for line in ebooks:
    if line[0] == '-':
        count = int(ebooks.readline())
        break
    nums.append(line.strip())
rand_sample = sample(nums, n)

URL_base = "http://aleph.gutenberg.org/"
for s in rand_sample:
    URL = URL_base
    for k in s[0 : len(s) - 1]:
        URL += k + '/'
    URL += s + '/' + s + ".zip"
    sleep(2)
    subprocess.run(["wget", "-P", files_dir, URL])
    subprocess.run(["tar", "-xf", "files\\" + s + ".zip", "-C", "files"])
    subprocess.run(["del", "files\\" + s + ".zip"], shell = True)
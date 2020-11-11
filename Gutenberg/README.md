# Gutenberg
Colletion of scripts for downloading books from Project Gutenberg and creating and analyzing term-by-document matrices.

# Downloading ebooks
index_eng.py scans the Project Gutenberg index for books in Enlgish. It then creates a text file with the corresponding ebook numbers.

sampler.py takes a file of ebook numbers and downloads a random sample of the corresponding books in .txt format through the Project Gutenberg API.

# Linear algebraic techniques
term_by_doc.py takes a folder of text files and produces a term-by-document matrix from the first n words in each file.

QR.py uses rank reduction via QR decomposition to recommend books based on a list of keywords.

SVD.py uses rank reduction via SVD to recommend books based on a list of keywords.

SVD_cluster.py projects terms and documents onto the first two and three singular directions and displays the corresponding scatter plots.

# Gutenberg
colletion of scripts for downloading books from Project Gutenberg and creating term-by-document matrices for further analysis

index_eng.py scans the Project Gutenberg index for books in Enlgish. It then creates a text file with the corresponding ebook numbers.

sampler.py takes a file of ebook numbers and downloads a random sample of the corresponding books in .txt format through the Project Gutenberg API.

term_by_doc.py takes a folder of text files and produces a term-by-document matrix from the first n words in each file.

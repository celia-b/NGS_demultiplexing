#!/usr/bin/env python3
import gzip, sys, subprocess
from joblib import Parallel, delayed

'''
This program takes:
    1. An NGS file
    2. Its index file 
    (previously generated with fastqindexing.py)
    3. A list of barcodes that correspond to the individuals sequenced 
    (previously generated with barcodes.py)

It starts a number of parallel processes that look for each of the different barcodes
in the index file and subsequently print the corresponding sequences onto a file named
after the barcode.
'''

## Functions
def openfiler(filename):
    '''
    This function opens compressed/uncompressed files for reading.
    '''
    try:
        if filename.endswith('.gz'):
            fh = gzip.open(filename, mode='rb')
        else:
            fh = open(filename, 'rb')
    except:
        print("Can't open file:", filename)
    return fh

def openfilew(filename):
    '''
    This function opens compressed/uncompressed files for writing.
    '''
    try:
        if filename.endswith('.gz'):
            fh = gzip.open(filename, mode='wb')
        else:
            fh = open(filename, 'wb')
    except:
        print("Can't open file:", filename)
    return fh

def demultiplex(infilename, indexfilename, dir, barcode):
    '''
    This function writes all entries that have the same barcode
    in a file that is now exclusive to the individual they belong to.
    When run for all barcodes in an NGS file, it performs demultiplexing.
    '''
    infile = openfiler(infilename)
    indexfile = openfiler(indexfilename)
    outfile = openfilew(dir + barcode + '.fastq')

    # Find barcode in indexfile:
    for line in indexfile:
        if line[-9:-1] == barcode.encode():
            indices = line.split()
            infile.seek(int(indices[0].decode('utf-8')))
            entry = infile.read(int(indices[7].decode('utf-8')) - int(indices[0].decode('utf-8')))
            outfile.write(entry + b'\n')

    infile.close()
    indexfile.close()
    outfile.close()


## Main program
if __name__ == '__main__':
    # File names and directories
    ngsfilename = '/home/projects/pr_course/ngs1.fastq.gz' 
    indexfilename = '/home/projects/pr_course/people/celbur/week13/fastqindex.lst.gz'
    dir = '/home/projects/pr_course/people/celbur/week13/'

    # Get barcodes from previously generated file
    barcodesfile = open("/home/projects/pr_course/people/celbur/week13/correctbarcodes.lst", "r")
    barcodes = list()
    for line in barcodesfile:
        barcodes.append(line.rstrip())
    barcodesfile.close()
    
    # Demultiplex in parallel
    results = Parallel(n_jobs = 4)(delayed(demultiplex)(ngsfilename, indexfilename, dir, barcode) for barcode in barcodes)

    '''
    # Or demultiplex sequentially
    for barcode in barcodes:
        demultiplex(ngsfilename, indexfilename, dir, barcode)
    '''
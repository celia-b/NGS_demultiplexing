#!/usr/bin/env python3
import gzip, sys, subprocess

'''
This program indexes an NGS fastq file. 
It creates a file where each line contains 8 indices 
(header start, header end, sequence start, sequence end, 
comment start, comment end, quality string start, quality string end) 
and the barcode of the sequence --> 9 fields per line/entry
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
            fh = gzip.open(filename, mode='w')
        else:
            fh = open(filename, 'w')
    except:
        print("Can't open file:", filename)
    return fh

def fastqindex(filename, indexfilename):
    '''
    This function generates an idex file for NGS reads in fastq format.
    The read barcode is included at the end of the line for easier further processing.

    The index file has the following fields separated by spaces: 
    Header start, header end, sequence start, sequence end, 
    comment start, comment end, quality string start, quality string end, barcode.
    '''
    myfilehandle = openfiler(filename)
    indexedfastq = openfilew(indexfilename)

    chunksize = 1024*1024
    filepos = 0

    print('Indexing fastq')

    entry = list()
    entry.append('0') # We assume the file starts with the first header

    line = 0

    # Read file in chunks
    while True:
        content = myfilehandle.read(chunksize)
        if len(content) == 0:
            break

        # Every linebreak means a new line of the 4 fastq lines
        chunkpos = 0
        while chunkpos != -1:
            chunkpos = content.find(b'\n', chunkpos)
            if chunkpos != -1:
                line += 1

                # By including the barcode along with the indices
                # the demultiplexing will be faster
                if line == 1:
                    barcode = content[chunkpos-8:chunkpos]

                # End of line
                entry.append(str(chunkpos + filepos)) 
                
                # When we have the indices for an entire fastq entry,
                # write them onto file
                if line == 4:
                    line = 0
                    print(' '.join(entry) + ' ' + barcode.decode('utf-8'), file = indexedfastq)
                    entry = list()
                
                # Beginning of next line
                entry.append(str(chunkpos + filepos + 1)) 

                chunkpos += 1

        filepos += len(content)
    
    # Close files
    myfilehandle.close()
    indexedfastq.close()


## Main program
if __name__ == '__main__':
    ngsfilename = "/home/projects/pr_course/ngs1.fastq.gz"
    indexfilename = "/home/projects/pr_course/people/celbur/week13/fastqindex.lst"

    # Index file
    print('Starting...')
    fastqindex(ngsfilename, indexfilename)
    print('File indexing done')

    # Compress the file
    print('Compressing...')
    subprocess.run(['gzip', '-f', indexfilename])
    print('Compressing done')

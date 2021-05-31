# Demultiplexing of sequencing data files
In this project we create a tool to handle sequencing data files (in fastq format) that contain reads from a number of different organisms, samples or patients. This is very common in e.g. microbiome or metagenomic sequencing data. Each sample recieves a unique barcode, which is included in the header of the read.

However, the task becomes more challenging when we account for the fact that any current sequencing technology creates sequencing errors. This means that not only the reads themselves but also the barcodes can be sequenced incorrecly and some of the reads in the file belong to samples we can not identify. In this program we dentify which barcodes are real and which are due to sequencing errors and demultiplex accordingly.

The tool is divided into 3 programs:
 1. A fastq file indexer: creates an index of the input file and records the read's barcode for easier access.
 2. A barcode retriever: out of all the barcodes present in the file, it finds which correspond to a sample and which are sequencing errors.
 3. A demultiplexer: with the information from the other two programs, it splits the multiplexed file into multiple single-sample files.

Multiplexing is a way to make sequencing efforts more affordable and to increase the run's throughputs. Below is a diagram of multiplexing sequencing as provided by https://thesequencingcenter.com/cost-savings-with-multiplex-samples/

![multiplexing](https://user-images.githubusercontent.com/55362769/120242871-48dfa080-c266-11eb-80c8-71ab3a31630f.png)

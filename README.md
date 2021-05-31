# Demultiplexing of sequencing data files
In this project we create a tool to handle sequencing data files (in fastq format) that contain reads from a number of different organisms, samples or patients. This is very common in e.g. microbiome or metagenomic sequencing data. Each sample recieves a unique barcode, which is included in the header of the read.

However, the task becomes more challenging when we account for the fact that any current sequencing technology creates sequencing errors. This means that not only the reads themselves but also the barcodes can be sequenced incorrecly and some of the reads in the file belong to samples we can not identify. In this program we dentify which barcodes are real and which are due to sequencing errors and demultiplex accordingly.

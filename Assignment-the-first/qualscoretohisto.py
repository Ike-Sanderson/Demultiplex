#!/usr/bin/env python

import bioinfo
import argparse
import matplotlib.pyplot as plt
import gzip


parser = argparse.ArgumentParser(description="opens file and returns mean quality scores")
parser.add_argument("-f", "--fn", type=str, help="filename.fastq.gz", required=True)
parser.add_argument("-l", type=int, help="how many bases in the sequence", required=True)
parser.add_argument("-o", type=str, help="outfile.png name", required=True)
args = parser.parse_args()

# Global variables
file = args.fn
linelength = args.l
outfile = args.o

def populate_list(file: str) -> tuple:
    """loops, base by base, through every line of quality scores in a fastq file. 
    makes list of sums at each bp site"""
    linecount = 0   
    q_list=bioinfo.init_list([],linelength)
    with gzip.open(file, 'rt') as fh: #open FASTQ.gz file
        for line in fh:
            line = line.strip()
            #print(line)
            if linecount%4 == 3: # read every 4th line starting at L2
                for index, qual in enumerate(line): #enumerate makes the index as it reads char by char over line
                    qual = bioinfo.convert_phred(qual)
                    q_list[index] += qual #taking old index and adding it to the int value coming in (qual)
                    #print(index, qual)
            linecount += 1    
    return q_list, linecount

def calculate_mean(q_list,linecount) -> list:
    for i in range(len(q_list)):
        q_list[i] = q_list[i]/(linecount/4) 
    #print(q_list)
    return q_list   

def plot_histogram(mean):
    plt.bar(range(len(mean)), mean)
    plt.xlabel('base position', fontsize = 12)
    plt.ylabel('mean quality score', fontsize = 12)
    plt.title('mean quality score per base position in sequence', fontsize = 10)
    #plt.show()
    plt.savefig(outfile)

if __name__ == "__main__": 
    q_list,linecount=populate_list(file)
    mean=calculate_mean(q_list,linecount)
    #print(f'{len(mean)=} {mean=}')
    plot_histogram(mean)


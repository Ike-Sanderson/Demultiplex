#!/usr/bin/env python

import argparse

parser = argparse.ArgumentParser(description="A program to open 4 FASTQ files, output demultiplexed data")
parser.add_argument("-f1", "--fn1", type=str, help="filename1.fastq.gz", required=True)
parser.add_argument("-f2", "--fn2", type=str, help="filename2.fastq.gz", required=True)
parser.add_argument("-f3", "--fn3", type=str, help="filename3.fastq.gz", required=True)
parser.add_argument("-f4", "--fn4", type=str, help="filename4.fastq.gz", required=True)
#parser.add_argument("-o", type=str, help="outfile.png name", required=True)
args = parser.parse_args()

# Global variables
R1 = args.fn1
R2 = args.fn2
R3 = args.fn3
R4 = args.fn4
#outfile = args.o
filenamedict={}
complementarydict={"A":"T","T":"A","C":"G","G":"C","N":"N"}
unknowncount = 0 #this might be the wrong way to keep track of how many: it's really generic
revcompindex2=""
index1=[]
index2=[]
revcomp=[]

#functions
def readin_record(fh):
    header=fh.readline().strip()
    sequence=fh.readline().strip()
    plus=fh.readline().strip()
    qualscoreline=fh.readline().strip()
    return header,sequence,plus,qualscoreline

def reverse_complement(index2):
    revcomp=""
    index2=index2[::-1]
    for base in index2:
        revcomp+=(complementarydict[base])
    #print(f'{revcomp=}')
    return revcomp

def convert_phred(letter: str) -> int:
    """Converts a single character into a phred 33 score"""
    return ord(letter) - 33

def qual_score(phred_score: str) -> float:
    """calculate the average quality score of the whole phred string"""
    qual_score=0
    i=0
    for value in (phred_score):
        score=convert_phred(value)
        qual_score=score+qual_score
        #print(f"{i}: {value} - {score} - {qual_score}")
        i+=1
    return qual_score/i

#probably need a function to write files

#open known index file and put into a dictionary
#indexset=set(line.strip() for line in open(/projects/bgmp/shared/2017_sequencing/indexes.txt))
indexset=set()          
f=open('indexes.txt','r')   #open file with indexes
f.readline()                #when I want to read and drop a first line- note the f. first 
for indexesin in f:         
    indexset.add(indexesin.strip().split('\t')[4])
f.close

#populate dictionary using indexset with index as key and file name as value
#will use dictionary to write files as a, which means they can be added to
for index in indexset:      
    filenamedict[index]=[open(f'{index}_R1.fq','a'),open(f'{index}_R4.fq','a')]
filenamedict["unknown"]=[open(f'unknown_R1.fq','a'),open(f'unknown_R4.fq','a')] #add unknown to dictionary
filenamedict["indexhopped"]=[open(f'indexhopped_R1.fq','a'),open(f'indexhopped_R4.fq','a')] #add indexhopped to dictionary

#begin main loop
with open (R1, "r") as fh1, open(R2, "r") as fh2, open(R3, "r") as fh3, open(R4, "r") as fh4:
    while True:                     
        readlistR1=(readin_record(fh1))
        if readlistR1[0] == "":     #exit the loop when the lines end, i.e. no more text and header is empty
            break
        readlistR2=(readin_record(fh2))
        readlistR3=(readin_record(fh3))
        readlistR4=(readin_record(fh4))
        index2=readlistR3[1]
        index1=readlistR2[1]
        revcomp=reverse_complement(index2)
        print(f'{index1=},{revcomp=}')
        #check if N in index
        print(f'{readlistR2[1]=},{readlistR3[1]=}')
        Npresent2=readlistR2[1].find('N')
        Npresent3=readlistR3[1].find('N')

        if Npresent2 != -1:
            #insert write to unknown file
            filenamedict["unknown"][0].write
        elif Npresent3 != -1:
            #insert write to unknown file
            filenamedict["unknown"][1].write
        
        #check quality scores of indices (strict Q control)
            #if low, insert write to unknown file
        #print(readlistR2[3],readlistR3[3])
        index1qualavg=qual_score(readlistR2[3])
        index2qualavg=qual_score(readlistR3[3])
        #print(index1qualavg,index2qualavg)
        if index1qualavg < 32:
           filenamedict["unknown"][0].write
        elif index2qualavg < 32:
           filenamedict["unknown"][1].write

        #check if index exists in dictionary (i.e. else it's not part of experiment)
            #if not in dict, insert write to unknown file
        if index1 not in indexset:
            filenamedict["unknown"][0].write
        elif revcomp not in indexset:
            filenamedict["unknown"][1].write
           
        #everything else is either a proper match or index hopped
              #insert write to specific matched file

        #check to see if index R2 != revcomp (i.e. index hopping)
            #insert write to index hopped
        if index1 == revcomp:
            filenamedict[index1][0].write
            filenamedict[revcomp][1].write
        else: 
            filenamedict["indexhopped"][0].write
            filenamedict["indexhopped"][1].write
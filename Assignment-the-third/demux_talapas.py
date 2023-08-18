#!/usr/bin/env python
#ver 0.6.6

#need to close files(????)
#need to figure out how to generate report about % reads from each sample
#ISSUE: counts are off because double counting (matched written to both) Is this wrong(????)

import argparse
from itertools import permutations
import gzip

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
unknowncount = 0
hoppedcount = 0
matchedcount = 0
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

#open known index file and put into a dictionary

indexset=set()          
#f=open('indexes.txt','r')   #open file with indexes not on talapas
f=open('/projects/bgmp/shared/2017_sequencing/indexes.txt','r') #open file with indexes
f.readline()                #when I want to read and drop a first line- note the f. first 
for indexesin in f:         
    indexset.add(indexesin.strip().split('\t')[4])
f.close

#populate dictionary using indexset with index as key and file name as value
#will use dictionary to write files as a, which means they can be added to
for index in indexset:      
    filenamedict[index]=[open(f'{index}_R1.fq','w'),open(f'{index}_R2.fq','w')]
filenamedict["unknown"]=[open(f'unknown_R1.fq','w'),open(f'unknown_R2.fq','w')] #add unknown to dictionary
filenamedict["indexhopped"]=[open(f'indexhopped_R1.fq','w'),open(f'indexhopped_R2.fq','w')] #add indexhopped to dictionary

#dictionary with each different combination of indexes as keys and number of matches as values
#use this dict [HOW???] to generate report about which index pairs matched&how often
r = 2
combodict = {}
for combo in permutations(indexset,2):
    combodict[combo] = 0

#dictionary with each matched combination of indexes as keys and number of matches as values
#use this dict [HOW???] to generate report about which index pairs matched&how often
matcheddict = {}
for index in indexset:
    matcheddict[index,index] = 0

#begin main loop
with gzip.open (R1, "rt") as fh1, gzip.open(R2, "rt") as fh2, gzip.open(R3, "rt") as fh3, gzip.open(R4, "rt") as fh4:
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
        #print(f'{index1=},{revcomp=}')
        #check if N in index
        Npresent2=readlistR2[1].find('N') #also could have used if N in
        Npresent3=readlistR3[1].find('N')

        #if an N exists in index then write to unknown file
        if Npresent2 != -1 or Npresent3 != -1:
            filenamedict["unknown"][0].write(f'{readlistR1[0]} {index1} {revcomp}\n{readlistR1[1]}\n{readlistR1[2]}\n{readlistR1[3]}\n')
            unknowncount += 1 #if count still off, look here: is this count necessary?
            filenamedict["unknown"][1].write(f'{readlistR4[0]} {revcomp} {index1}\n{readlistR4[1]}\n{readlistR4[2]}\n{readlistR4[3]}\n')
            
        #check if index exists in dictionary (i.e. else it's not part of experiment)
            #if not in dict, insert write to unknown file
        elif index1 not in indexset or revcomp not in indexset:
            unknowncount += 1
            filenamedict["unknown"][1].write(f'{readlistR4[0]} {index1} {revcomp}\n{readlistR4[1]}\n{readlistR4[2]}\n{readlistR4[3]}\n')
            filenamedict["unknown"][0].write(f'{readlistR1[0]} {index1} {revcomp}\n{readlistR1[1]}\n{readlistR1[2]}\n{readlistR1[3]}\n')

           
        
        #check quality scores of indices (strict Q control)
        else:
            written=False
            for value in (readlistR2[3]):
                score=convert_phred(value)
                if score < 2:
                    filenamedict["unknown"][0].write(f'{readlistR1[0]} {index1} {revcomp}\n{readlistR1[1]}\n{readlistR1[2]}\n{readlistR1[3]}\n')
                    filenamedict["unknown"][1].write(f'{readlistR4[0]} {revcomp} {index1}\n{readlistR4[1]}\n{readlistR4[2]}\n{readlistR4[3]}\n')
                    unknowncount += 1
                    written=True
                    
            if written==False:
                for value in (readlistR3[3]):
                    score=convert_phred(value)
                    if score < 2:
                        filenamedict["unknown"][0].write(f'{readlistR1[0]} {index1} {revcomp}\n{readlistR1[1]}\n{readlistR1[2]}\n{readlistR1[3]}\n')
                        filenamedict["unknown"][1].write(f'{readlistR4[0]} {revcomp} {index1}\n{readlistR4[1]}\n{readlistR4[2]}\n{readlistR4[3]}\n')
                        unknowncount += 1
                        written=True

            #everything else is either a proper match or index hopped
            #check to see if index R2 != revcomp (i.e. index hopping)
            if written==False:
                if index1 == revcomp:
                    filenamedict[index1][0].write(f'{readlistR1[0]} {index1} {revcomp}\n{readlistR1[1]}\n{readlistR1[2]}\n{readlistR1[3]}\n')
                    matcheddict[(index1,revcomp)] += 1
                    matchedcount += 1
                    filenamedict[revcomp][1].write(f'{readlistR4[0]} {revcomp} {index1}\n{readlistR4[1]}\n{readlistR4[2]}\n{readlistR4[3]}\n')
                    matcheddict[(revcomp,index1)] += 1
                else: 
                    filenamedict["indexhopped"][0].write(f'{readlistR1[0]} {index1} {revcomp}\n{readlistR1[1]}\n{readlistR1[2]}\n{readlistR1[3]}\n')
                    filenamedict["indexhopped"][1].write(f'{readlistR4[0]} {revcomp} {index1}\n{readlistR4[1]}\n{readlistR4[2]}\n{readlistR4[3]}\n')
                    combodict[(index1,revcomp)] += 1
                    hoppedcount += 1

for schtuff in filenamedict:
    filenamedict[schtuff][0].close()
    filenamedict[schtuff][1].close()

totalcount = (hoppedcount + matchedcount + unknowncount)
pcthopped = (hoppedcount / totalcount) * 100
pctmatched = (matchedcount / totalcount) * 100
pctunknown = (unknowncount / totalcount) * 100
print(f'{hoppedcount=}')
print(f'{matchedcount=}')
print(f'{unknowncount=}')
print(f'{totalcount=}')
print(f'{pctunknown=} percent')
print(f'{pcthopped=} percent')
print(f'{pctmatched=} percent')

with open("final_report.tsv", 'w') as fin:
    fin.write(f'Index pair\tNumReads\tPercent of total\n')
    for pair,x in combodict.items():
        readpercent = (x / totalcount) * 100
        fin.write(f'{pair}\t{x}\t{readpercent}\n')
    for matches,y in matcheddict.items():
        readpercent = (y / totalcount) * 100
        fin.write(f'{matches}\t{y}\t{readpercent}\n')

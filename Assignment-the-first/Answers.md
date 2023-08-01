# Assignment the First

## Part 1
1. Be sure to upload your Python script. Provide a link to it here:

| File name | label | Read length | Phred encoding |
|---|---|---|---|
| 1294_S1_L008_R1_001.fastq.gz | R1 | 101 | 33 |
| 1294_S1_L008_R2_001.fastq.gz | R2 |   8 | 33 |
| 1294_S1_L008_R3_001.fastq.gz | R3 |   8 | 33 |
| 1294_S1_L008_R4_001.fastq.gz | R4 | 101 | 33 |

2. Per-base NT distribution
    1. Use markdown to insert your 4 histograms here.
    2. **YOUR ANSWER HERE**
    3. **YOUR ANSWER HERE**
    
## Part 2
1. Define the problem
   The problem is that the files were the product of a multiplexed output because the lanes can take so many different experimental results and output the data for each of those experiments. The data need to be separated into different reads by index. 
2. Describe output
   The output will consist of two files for each index (one for the forward read and one for the reverse read) plus two files of unknown or low quality reads, plus two files for index hopped reads. Should be a total of 52 files in this case as we have 24 indices unless for some reason there are no high quality properly mapped reads corresponding to one or more of the indices.
3. Upload your [4 input FASTQ files](../TEST-input_FASTQ) and your [>=6 expected output FASTQ files](../TEST-output_FASTQ).
4. Pseudocode
5. High level functions. For each function, be sure to include:
    1. Description/doc string
    2. Function headers (name and parameters)
    3. Test examples for individual functions
    4. Return statement

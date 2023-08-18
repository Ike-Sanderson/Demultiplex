Overall counts after demultiplex of 2017 sequencing reads:
```
hoppedcount=707740
matchedcount=331755033
unknowncount=30783962
totalcount=363246735
pctunknown=8.474669978795541 percent
pcthopped=0.19483726398807136 percent
pctmatched=91.33049275721639 percent
```
Of the matched reads, 
```
'TACCGGAT', 'TACCGGAT' paired most frequently with just over 42%
'TCTTCGAC', 'TCTTCGAC' followed with 23.18%
'CTCTGGAT', 'CTCTGGAT' with 19.26%
```
greatest hits mismatched pairs:
```
('TGTTCCGT', 'TATGGCAC')	85536	0.023547630786000043 (fox treatment)
('TATGGCAC', 'TGTTCCGT')	88571	0.024383151028184738 (fox treatment)
('TACCGGAT', 'CTCTGGAT')	20269	0.005579953801924744 **
('TACCGGAT', 'TCTTCGAC')	13576	0.0037374045495550015 **
('TCTTCGAC', 'TACCGGAT')	10986	0.0030243905702276993 **
```
The three pairs of index hopped reads marked "**" above include at least one index that was most highly represented 
in the matched reads. Given the higher concentration of those indexes, the greater hopped index count is logical.

I find the first two hopped indexes more confusing. They are the same two indexes, each mismatched about 0.024%. But why 
those two indexes? Perhaps the following information from the index file is relevant:
```
sample	group	treatment	index	sequence
17	3E	fox	B7	TATGGCAC
19	3F	fox	A3	TGTTCCGT
```
Those two indexes are both from the same treatment. The groups working on the sequencing may have worked together. Perhaps 
the work had more error than usual. Maybe the insert length was too long and the reads bridge amplified while attached to 
adjacent wells on the flow cell.


Note on my project submission:
When I read through the "final_report" file on Friday night 8/11 I discovered that there wasn't any data written from the 
index hopped dictionary. It took a couple of days for me to get back to work and another day of problem-solving to track down 
my errors (there were several). I didn't submit the work until a week past due.

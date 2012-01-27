#!/usr/bin/env python

from sys import argv, stdout, stderr

# Usage: combineXplorModels.py refine_##_name.pdb.stats > bundle.pdb

# Afterwards, if you want to use the PDB procheck
# ( http://deposit.rcsb.org/cgi-bin/validate/adit-session-driver )
# you should use cyana to add a chain ID and translate HN->H, HB1->HB3, etc:

#cyana> translate xplor
#    Using XPLOR/CNS nomenclature.
#cyana> read pdb xplormodels
#cyana> translate off
#    Using default nomenclature.
#cyana> write pdb newcyanabundle
#    PDB coordinate file "newcyanabundle.pdb" written.

statsfile = argv[1]

#files = argv[1:]
#files = ['refine_2_h2.pdb','refine_5_h2.pdb']

############### Read stats to make file list #################
openfile = open(statsfile)
lines = openfile.readlines()
openfile.close()
l = 0
while 'Filename' not in lines[l]:
    l+=1
l+=1
first=l
while len(lines[l])>1:
    l+=1
last=l
files = [line.split()[0] for line in lines[first:last]]
stderr.write('Combining files:\n')
for f in files:
    stderr.write('%s\n'%f)

############## Combine files in list ####################


model=1
for file in files:
    print "MODEL %8d" % model
    lines = open(file).readlines()
    for line in lines:
        if 'OT1' not in line and 'END' not in line:
            stdout.write(line)
        elif 'OT1' in line: # Replace OT1 with O & make a TER line
            TERid = int(line.split()[1])+1
            newlines = line[0:14]+'  '+line[16:]+'TER    %d'%TERid+'  	 '+line[17:26]+'\n'
            stdout.write(newlines)
    print "ENDMDL"
    model += 1
    pass


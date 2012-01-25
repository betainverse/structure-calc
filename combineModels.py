#!/usr/bin/env python

from sys import argv, stdout

# Usage: combineModels.py > bundle.pdb
# or comment out files = [], uncomment files = argv[1:], and
# combineModels.py refine*.pdb > bundle.pdb

# Copy list of best structures from refine_##_h2.pdb.stats
# Then use ^x-r k in emacs to remove the other columns, use find-replace to add commas and quotes, and adjust tabs manually

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


#files = argv[1:]
files = ['refine_62_h2.pdb',
    'refine_61_h2.pdb',
    'refine_88_h2.pdb',
    'refine_31_h2.pdb',
    'refine_60_h2.pdb',
    'refine_17_h2.pdb',
    'refine_75_h2.pdb',
    'refine_15_h2.pdb',
    'refine_82_h2.pdb',
    'refine_2_h2.pdb',
    'refine_30_h2.pdb',
    'refine_89_h2.pdb',
    'refine_20_h2.pdb',
    'refine_94_h2.pdb',
    'refine_63_h2.pdb',
    'refine_74_h2.pdb',
    'refine_41_h2.pdb',
    'refine_83_h2.pdb',
    'refine_7_h2.pdb',
    'refine_45_h2.pdb']

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


#!/usr/bin/env python

from sys import argv, stdout

#files = argv[1:]
# Copy list of best structures from refine_##_h2.pdb.stats
# Then use ^x-r k to remove the other columns, use find-replace to add commas and quotes, and adjust tabs manually
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
        elif 'OT1' in line:
            TERid = int(line.split()[1])+1
            newline = line[0:14]+'  '+line[16:]+'TER    %d'%TERid+'  	 '+line[17:26]+'\n'
            stdout.write(newline)
    #stdout.write(open(file).read())
    print "ENDMDL"
    model += 1
    pass

# Is it necessary to add TER fields and chain IDs?

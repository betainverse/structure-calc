#!/nmr/programs/python/bin/python2.5
"""
purgeIntegratedPeakfile.py has several purposes:
1. Removal of negative volume peaks.
2. Removal of peaks with unassigned spins.
3. Addition of assignment information to the end of the line.

purgeIntegratedPeakfile.py is expected to be used on peaklist with the
order Hdirect N/C Hnoe. This order is not necessary, but gives nicer results.

purgeIntegratedPeakfile.py takes advantage of the fact that cyana does not
use any data in the xeasy-formatted peak list after the 3 columns that
reference spin numbers. This script uses the spin numbers and the prot file
to find the assignment for each peak. The script then stores that assignment
information in new columns to the right of the columns that cyana uses.
"""
import sys

# Here I list strips from which I prefer not to count NOEs. In most cases,
# there is too much overlap to trust any picked NOEs from these strips.
# Alternatively, I may not trust the assignment, particularly for the
# heteronucleus. In some cases, it may simply be that there is no possibility
# for interresidue NOEs, and I am simply trying to reduce the peak count
# to prevent cyana noeassign from crashing. 

badresidues = ['1236','1237','1238','1296','1347','1379','1405']

potentiallyRemove = ['1351']
potentiallyAddBackLater = [('HG','1301'),('HB','1322'),
                           ('HG13','1332'),('HA','1346'),('HG','1346'),
                           ('HA','1349'),('HB2','1349'),('HB3','1349'),
                           ('HA','1358'),('HB','1358'),
                           ('HG2','1379'),('HG3','1379'),
                           ('HB2','1377'),('HB3','1377'),'1347']

badstrips = [('',''),
             ('HB2','1295'),('HB3','1295'),('HG2','1295'),('HG3','1295'),
             ('HD2','1295'),('HD3','1295'),
             ('HB2','1298'),('HB3','1298'),('HG2','1298'),('HG3','1298'),
             ('HB2','1300'),
             ('HG','1301'),
             ('HA','1302'),
             ('HB2','1305'),('HB3','1305'),('HG','1305'),
             ('HB2','1311'),('HG','1311'),
             ('HA','1315'),('HB2','1315'),('HB3','1315'),
             ('HB2','1318'),('HB3','1318'),
             ('HA','1322'),('HB','1322'),
             ('HG','1324'),
             ('HA','1325'),('HB','1325'),
             ('HG12','1332'),('HG13','1332'),
             ('HG13','1334'),
             ('HG2','1335'),('HG3','1335'),
             ('HB2','1338'),('HB3','1338'),
             ('HG','1339'),
             ('HG','1341'),
             ('HA','1346'),('HG','1346'),
             ('HB','1345'),
             ('HA','1349'),('HB2','1349'),('HB3','1349'),('HG','1349'),
             ('HA','1351'),
             ('HG','1355'),
             ('HB3','1356'),
             ('HA','1358'),('HB','1358'),
             ('HB2','1359'),('HB3','1359'),('HG','1359'),
             ('HB','1361'),
             ('HG12','1363'),('HG13','1363'),
             ('HB','1367'),('HG','1367'),
             ('HB2','1368'),('HB3','1368'),('HG2','1368'),('HG3','1368'),
             ('HG2','1369'),('HG3','1369'),
             ('HG','1370'),
             ('HB','1376'),('HG','1376'),
             ('HB2','1377'),('HB3','1377'), ('HG','1377'),
             ('HA','1378'),('HB2','1378'),('HB3','1378'), ('HG','1378'),
             ('HG12','1380'),('HG13','1380'),
             ('HA','1381'),('HB2','1381'),('HB3','1381'), ('HG','1381'),
             ('HA','1383'),('HG','1383'),
             ('HB2','1384'),('HB3','1384'),('HG','1384'),
             ('HG','1391'),('HD','1391'),('HE','1391'),
             ('HA','1410'),
             ('HB2','1421'),('HB3','1421'),
             ('HD2','1422'),('HD3','1422'),('HE2','1422'),('HE3','1422'),
             ('HB2','1424'),('HB3','1424')]


             ## ('HA','1236'),('HB','1236'),('HA','1237'),('HB','1237'),
             ## ('HB2','1238'),('HB3','1238'),('HG','1238'),('HD1','1238'),
             ## ('HD2','1238')
             
def main():
    if len(sys.argv) not in [3,4]:
        print '=============================================================================='
        print 'purgeIntegratedPeakfile.py reads in peaks file and a prot file in xeasy format'
        print 'and adds assignment information from the prot file to the end of each line in'
        print 'the peaks file.'
        print ''
        print 'This script filters out peaks with unassigned spins or negative volumes.'
        print 'This script generates two output files:'
        print 'purge_infile.peaks contains assigned peaks with positive volume.'
        print 'errors_infile.peaks contains unassigned peaks and peaks with negative volume.'
        print ''
        print 'Usage: purgeIntegratedPeakfile.py infile.peaks infile.prot [C]'
        print ''
        print 'An optional third argument can be used to indicate C, rather than N.'
        print 'Number of arguments given: %d'%(len(sys.argv)-1)
        print '=============================================================================='
        return

    heteronuc = 'C'

    if len(sys.argv) == 4:
        if sys.argv[3] == 'N':
            heteronuc = 'N'

    peakfile = sys.argv[1]
    protfile = sys.argv[2]
    errorfile = 'errors_%s'%peakfile
    goodfile = 'purge_%s'%peakfile

    print 'Reading peaks from %s.'%peakfile
    print 'Reading assignments from %s'%protfile
    print 'The heteronucleus is %s'%heteronuc
    print 'Output file is %s'%goodfile
    print 'Unassigned and negative peaks will go to %s'%errorfile

    openprot = open(protfile,'r')
    protlines = openprot.readlines()
    openprot.close()

    # spinDict is a dictionary keyed by spin number, returning a tuple
    # consisting of residue number, spin name, and chemical shift.
    spinDict = {}
    for line in protlines:
        if line[0]!='#':
            columns = line.split()
            if len(columns) >= 5:
                spinNum = columns[0]
                shift = columns[1]
                spinName = columns[3]
                resNum = columns[4]
                spinDict[spinNum] = (resNum,spinName,shift)
    
    keys = spinDict.keys()

    openpeaks = open(peakfile,'r')
    peaklines = openpeaks.readlines()
    openpeaks.close()

    errorlines = []
    errorlines.append('# Number of dimensions 3')
    errorlines.append('#INAME 1 H')
    errorlines.append('#INAME 2 %s'%heteronuc)
    errorlines.append('#INAME 3 H')

    goodlines = []
    goodlines.append('# Number of dimensions 3')
    goodlines.append('#INAME 1 H')
    goodlines.append('#INAME 2 %s'%heteronuc)
    goodlines.append('#INAME 3 H')
    goodlines.append('#CYANAFORMAT H%sh'%heteronuc)



    
    for line in peaklines:
        if line[0]!='#':
            assigned = True
            positive = True
            error = ''
            columns = line.split()
            spins = columns[10:13]
            integral = columns[6]
            assignment = ''
            unassigned = ''
            if float(integral) <= 20:
                #errorlines.append('#negative')
                positive = False
            for spin in spins:
                if spin not in keys:
                    assigned = False
                    unassigned = ' '.join([unassigned,'%s'%spin])
            if assigned:
                res = [spinDict[spin][0] for spin in spins]
                atoms = [spinDict[spin][1] for spin in spins]
                # Find and exclude all amide peaks in C noesy, since these have unreliable volume.
                # And they have corresponding peaks in the N noesy that should be reliable.
                #if heteronuc == 'C' and 'H' in atoms:
                    #errorlines.append('#amide')
                    #positive = False 
                if res[1] == res[0]:
                    assignment = '%s-%s %s  %s %s'%(atoms[0].rjust(4),atoms[1].ljust(4),res[0].rjust(4),atoms[2].rjust(4),res[2].rjust(4))
                    strip = (atoms[0],res[0])
                    if res[0] in badresidues or strip in badstrips:
                        positive = False
                    # Find and exclude diagonal peaks.
                    if res[2] == res[0] and atoms[2] == atoms[0]:
                        #errorlines.append('#diagonal')
                        positive = False
                else:
                    assignment = '\t%s %s\t%s %s\t%s %s'%(atoms[0],res[0],atoms[1],res[1],atoms[2],res[2])
            else:
                for spin in spins:
                    if spin in keys:
                        spinassign = '%s %s'%(spinDict[spin][1],spinDict[spin][0])
                        assignment = '\t'.join([assignment,spinassign])
            if assigned and heteronuc == 'C' and 'H' in atoms:
                positive = False
            elif assigned and positive:
                goodlines.append(' '.join([line[0:62],'a',line[63:-1],assignment]))
            elif assigned:
                errorlines.append(' '.join([line[0:-1],assignment]))
                errorlines.append(' '.join(['#',assignment]))
            else:
                errorlines.append(' '.join([line[0:-1],assignment]))
                errorlines.append('#unassigned: %s'%unassigned)
    goodlines.append('')

    finalerrors = '\n'.join(errorlines)
    openerrorfile = open(errorfile,'w')
    openerrorfile.write(finalerrors)
    openerrorfile.close()
    
    finaloutput = '\n'.join(goodlines)
    outputfile = open(goodfile,'w')
    outputfile.write(finaloutput)
    outputfile.close()

    
main()
    
    

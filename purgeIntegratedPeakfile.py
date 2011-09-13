#!/nmr/programs/python/bin/python2.5
"""
purgeIntegratedPeakfile.py has several purposes:
1. Removal of negative volume peaks.
2. Removal of peaks with unassigned spins.
3. Addition of assignment information to the end of the line.

purgeIntegratedPeakfile.py is intended to be used after peakint.
Since peakint requires the columns to be in the order Hnoe Hdirect N/C,
purgeIntegratedPeakfile.py assumes this order. This order is not necessary,
but gives nicer results.

purgeIntegratedPeakfile.py takes advantage of the fact that cyana does not
use any data in the xeasy-formatted peak list after the 3 columns that
reference spin numbers. This script uses the spin numbers and the prot file
to find the assignment for each peak. The script then stores that assignment
information in new columns to the right of the columns that cyana uses.
"""
import sys

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

    heteronuc = 'N'

    if len(sys.argv) == 4:
        if sys.argv[3] == 'C':
            heteronuc = 'C'

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
    goodlines = []
    goodlines.append('# Number of dimensions 3')
    goodlines.append('#INAME 1 H')
    goodlines.append('#INAME 2 H')
    goodlines.append('#INAME 3 %s'%heteronuc)
    goodlines.append('#CYANAFORMAT hH%s'%heteronuc)
    
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
            if float(integral) <= 500:
                errorlines.append('#negative')
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
                if heteronuc == 'C' and 'H' in atoms:
                    errorlines.append('#amide')
                    positive = False 
                if res[1] == res[2]:
                    assignment = '%s-%s %s  %s %s'%(atoms[1].rjust(4),atoms[2].ljust(4),res[1].rjust(4),atoms[0].rjust(4),res[0].rjust(4))
                    # Find and exclude intraresidue peaks.
                    if res[1] == res[0]:
                        errorlines.append('#intraresidue')
                        positive = False
                else:
                    assignment = '\t%s %s\t%s %s\t%s %s'%(atoms[0],res[0],atoms[1],res[1],atoms[2],res[2])
            else:
                for spin in spins:
                    if spin in keys:
                        spinassign = '%s %s'%(spinDict[spin][1],spinDict[spin][0])
                        assignment = '\t'.join([assignment,spinassign])
            if assigned and positive:
                goodlines.append(' '.join([line[0:-1],assignment]))
            elif assigned:
                errorlines.append(' '.join([line[0:-1],assignment]))
            else:
                errorlines.append('#unassigned: %s'%unassigned)
                errorlines.append(' '.join([line[0:-1],assignment]))

    finalerrors = '\n'.join(errorlines)
    openerrorfile = open(errorfile,'w')
    openerrorfile.write(finalerrors)
    openerrorfile.close()
    
    finaloutput = '\n'.join(goodlines)
    outputfile = open(goodfile,'w')
    outputfile.write(finaloutput)
    outputfile.close()

    
main()
    
    

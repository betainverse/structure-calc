#!/nmr/programs/python/bin/python2.5
"""
TITLE: classifyPeaks.py adds several columns to the end of a peak line in an xeasy peaks file.

USAGE: classifyPeaks.py input.peaks input.prot

results in file classify_input.peaks

Region1 Region2 ResidueNumberOffset ContactType
"""
import sys

def Region(resnum):
    if resnum in range(1219,1243):
        region = "Nterm"
        pair = 0
    elif resnum in range(1243,1258):
        region = "Helix1"
        pair = 1
    elif resnum in range(1258,1260):
        region = "Turn1"
        pair = 1
    elif resnum in range(1260,1271):
        region = "Helix2"
        pair = 1
    elif resnum in range(1271,1276):
        region = "Turn2"
        pair = 1
    elif resnum in range(1276,1289):
        region = "Helix3"
        pair = 2
    elif resnum in range(1289,1292):
        region = "Turn3"
        pair = 2
    elif resnum in range(1292,1308):
        region = "Helix4"
        pair = 2
    elif resnum in range(1308,1313):
        region = "Turn4"
        pair = 2
    elif resnum in range(1313,1334):
        region = "Helix5"
        pair = 3
    elif resnum in range(1334,1337):
        region = "Turn5"
        pair = 3
    elif resnum in range(1337,1350):
        region = "Helix6"
        pair = 3
    elif resnum in range(1350,1356):
        region = "Turn6"
        pair = 3
    elif resnum in range(1356,1371):
        region = "Helix7"
        pair = 4
    elif resnum in range(1371,1372):
        region = "Turn7"
        pair = 4
    elif resnum in range(1372,1388):
        region = "Helix8"
        pair = 4
    elif resnum in range(1388,1391):
        region = "Turn8"
        pair = 4
    elif resnum in range(1391,1407):
        region = "Helix9"
        pair = 5
    elif resnum in range(1407,1414):
        region = "Turn9"
        pair = 5
    elif resnum in range(1414,1427):
        region = "Helix10"
        pair = 5
    elif resnum in range(1427,1438):
        region = "Cterm"
        pair = 5
    else:
        region = "Error"
        pair = 10
    return (region,pair)

def SS(atom1,atom2,offset):
    # atom1 must have the smaller residue number
    if 'A' in atom1 and atom2 == 'H':
        if offset in range(1,5):
            tag = 'daN%d SS'%offset
        else: tag = 'daNx'
    elif atom1 == atom2 == 'H':
        if offset in range(1,3):
            tag = 'dNN%d SS'%offset
        else: tag = 'dNNx'
    elif 'B' in atom1 and atom2 == 'H':
        if offset == 1:
            tag = 'dbN1 SS'
        else: tag = 'dbNx'
    elif 'A' in atom1 and 'B' in atom2:
        if offset == 3:
            tag = 'dab3 SS'
        else: tag = 'dabx'
    else: tag = ''
    return tag

def isMethyl(atom,aa):
    if 'HB' in atom and aa == 'ALA':
        return True
    elif 'HG' in atom and aa == 'VAL':
        return True
    elif 'HD' in atom and aa == 'ILE':
        return True
    elif 'HD' in atom and aa == 'LEU':
        return True
    else:
        return False

def isAromat(atom,aa):
    if 'HD' in atom and aa in ['TYR','PHE','HIS']:
        return True
    elif 'HE' in atom and aa in ['TYR','PHE','HIS']:
        return True
    else:
        return False

def main():
    if len(sys.argv) not in [4,5]:
        print '=============================================================================='
        print 'Usage: classifyPeaks.py infile.peaks infile.prot infile.seq [C]'
        print ''
        print 'results in file classify_input.peaks'
        print ''
        print 'Number of arguments given: %d'%(len(sys.argv)-1)
        print '=============================================================================='
        return

    heteronuc = 'N'

    if len(sys.argv) == 5:
        if sys.argv[4] == 'C':
            heteronuc = 'C'

    peakfile = sys.argv[1]
    protfile = sys.argv[2]
    seqfile = sys.argv[3]
    goodfile = 'classify_%s'%peakfile

    print 'Reading peaks from %s.'%peakfile
    print 'Reading assignments from %s'%protfile
    print 'The heteronucleus is %s'%heteronuc
    print 'Output file is %s'%goodfile

    openseq = open(seqfile,'r')
    seqlines = openseq.readlines()
    openseq.close()

    seqDict = {}
    for line in seqlines:
        columns = line.split()
        aa = columns[0]
        resnum = columns[1]
        seqDict[resnum] = aa

    openprot = open(protfile,'r')
    protlines = openprot.readlines()
    openprot.close()

    # spinDict is a dictionary keyed by spin number, returning a tuple
    # consisting of residue number, spin name, and chemical shift.
    spinDict = {}
    for line in protlines:
        columns = line.split()
        if len(columns) >=5:
            spinNum = columns[0]
            shift = columns[1]
            spinName = columns[3]
            resNum = columns[4]
            spinDict[spinNum] = (resNum,spinName,shift)
    
    keys = spinDict.keys()

    openpeaks = open(peakfile,'r')
    peaklines = openpeaks.readlines()
    openpeaks.close()

    goodlines = []
    goodlines.append('# Number of dimensions 3')
    goodlines.append('#INAME 1 H')
    goodlines.append('#INAME 2 H')
    goodlines.append('#INAME 3 %s'%heteronuc)
    goodlines.append('#CYANAFORMAT hH%s'%heteronuc)
    
    for line in peaklines:
        if line[0]!='#':
            assigned = True
            commented = False
            columns = line.split()
            spins = columns[10:13]
            for spin in spins:
                if spin not in keys:
                    assigned = False
                    commented = True
            if assigned:
                res = [spinDict[spin][0] for spin in spins]
                atoms = [spinDict[spin][1] for spin in spins]
                num0 = int(res[0])
                num1 = int(res[1])
                aa0 = seqDict[res[0]]
                aa1 = seqDict[res[1]]
                (region0,pair0) = Region(num0)
                (region1,pair1) = Region(num1)
                offset = abs(num0-num1)
                if num0 < num1:
                    secStr = SS(atoms[0],atoms[1],offset)
                else:
                    secStr = SS(atoms[1],atoms[0],offset)
                if heteronuc == 'N':
                    if isMethyl(atoms[0],aa0):
                        secStr += ' Methyl'
                    if isAromat(atoms[0],aa0):
                        secStr += ' Aromat'
                if heteronuc == 'C':
                    if isMethyl(atoms[0],aa0) and isMethyl(atoms[1],aa1):
                        secStr += ' Methyl-Methyl'
                    if isMethyl(atoms[0],aa0) and isAromat(atoms[1],aa1):
                        secStr += ' Methyl-Aromat'
                line = ' '.join([line[0:-1],aa0,aa1,region0.rjust(7),region1.rjust(7),'%d'%offset,secStr])
                goodlines.append(line)
            
                    

    
    finaloutput = '\n'.join(goodlines)
    outputfile = open(goodfile,'w')
    outputfile.write(finaloutput)
    outputfile.close()

    
main()
    
    

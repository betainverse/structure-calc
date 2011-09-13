#!/nmr/programs/python/bin/python2.5
import sys

def main():
    if len(sys.argv) not in [2]:
        print '=============================================================================='
        print 'zxy_peaks.py reads in peaks file in xeasy format and swaps the first two'
        print 'dimensions. If the original order is HN N Hnoe, it returns a peak file with'
        print 'order Hnoe HN N, as required by peakint.'
        print ''
        print 'Usage: zxy_peaks.py infile.peaks > outfile.peaks'
        print 'Number of arguments given: %d'%(len(sys.argv)-1)
        print '=============================================================================='
        return

    infile = sys.argv[1]
    openfile = open(infile,'r')

    lines = openfile.readlines()

    print lines[0][0:-1]

    for line in lines[1:4]:
        pass
    
    for line in lines[4:]:
        if line[0]!='#':
            columns = line.split()
            peaknum = columns[0].rjust(4)
            Hshift = columns[1].rjust(7)
            NOEshift = columns[3].rjust(7)
            Nshift = columns[2].rjust(7)
            integrals = line[29:67]
            Hid = columns[10].rjust(4)
            NOEid = columns[12].rjust(4)
            Nid = columns[11].rjust(4)
            end = columns[13]
            print peaknum,NOEshift,Hshift,Nshift,integrals,NOEid,Hid,Nid,end
#        else:
#            print line[0:-1]

main()    

awk '   BEGIN { 
		ONE   = "AcCDEFGHIKLMNPQRSTVWY";
		THREE = "ALA.cys.CYS.ASP.GLU.PHE.GLY.HIS.ILE.LYS.LEU.MET.ASN.PRO.GLN.ARG.SER.THR.VAL.TRP.TYR";
	}
	
        (($NF=="Good")&&($2!="P")){
		dphi=$5; if(dphi<5) dphi=5; if(dphi>35) dphi=35; 
		dpsi=$6; if(dpsi<5) dpsi=5; if(dpsi>35) dpsi=35; 
		pos = index( ONE,toupper($2) );
		printf("%4d  %4s  PHI  %8.1f%8.1f\n",$1,substr(THREE,pos*4-3,3),$3-2*dphi,$3+2*dphi); 
		printf("%4d  %4s  PSI  %8.1f%8.1f\n",$1,substr(THREE,pos*4-3,3),$4-2*dpsi,$4+2*dpsi);
	}' $1

# (C) Shen and Bax 2007-2009, Lab of Chemical Physics, NIDDK, NIH
#
# talos2dyana.com: converts talos/talos+ output to dyana/cyana angle restraints
#         syntax: talos2dyana.com pred.tab > talos.aco
#
# Modified by Katie Edmonds Sept 2011 to use narrower error estimates and remove proline predictions,
# which are rejected by cyana
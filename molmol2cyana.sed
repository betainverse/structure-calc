#!/bin/sed -f
#Arginine
s/ARG+/ARG /g
s/2HB  ARG/3HB  ARG/g
s/1HB  ARG/2HB  ARG/g
s/2HG  ARG/3HG  ARG/g
s/1HG  ARG/2HG  ARG/g
s/2HD  ARG/3HD  ARG/g
s/1HD  ARG/2HD  ARG/g
#Glutamine
s/2HB  GLU/3HB  GLU/g
s/1HB  GLU/2HB  GLU/g
s/2HG  GLU/3HG  GLU/g
s/1HG  GLU/2HG  GLU/g
/HE  GLU/d
#Methionine
s/2HB  MET/3HB  MET/g
s/1HB  MET/2HB  MET/g
s/2HG  MET/3HG  MET/g
s/1HG  MET/2HG  MET/g
#Lysine
s/LYS+/LYS /g
s/2HB  LYS/3HB  LYS/g
s/1HB  LYS/2HB  LYS/g
s/2HG  LYS/3HG  LYS/g
s/1HG  LYS/2HG  LYS/g
s/2HD  LYS/3HD  LYS/g
s/1HD  LYS/2HD  LYS/g
s/2HE  LYS/3HE  LYS/g
s/1HE  LYS/2HE  LYS/g
#Serine
s/2HB  SER/3HB  SER/g
s/1HB  SER/2HB  SER/g
#Leucine
s/2HB  LEU/3HB  LEU/g
s/1HB  LEU/2HB  LEU/g
#Phenylalanine
s/2HB  PHE/3HB  PHE/g
s/1HB  PHE/2HB  PHE/g
#Isoleucine
s/1HG2 ILE/HG21 ILE/g
s/2HG2 ILE/HG22 ILE/g
s/3HG2 ILE/HG23 ILE/g
s/1HG1 ILE/HG12 ILE/g
s/2HG1 ILE/HG13 ILE/g
s/1HD1 ILE/HD11 ILE/g
s/2HD1 ILE/HD12 ILE/g
s/3HD1 ILE/HD13 ILE/g
#Asparagine
s/2HB  ASN/3HB  ASN/g
s/1HB  ASN/2HB  ASN/g
/3HD2 ASN/d
#Aspartate
s/2HB  ASP/3HB  ASP/g
s/1HB  ASP/2HB  ASP/g
/HD  ASP/d
#Cysteine
s/2HB  CYS/3HB  CYS/g
s/1HB  CYS/2HB  CYS/g
#Glycine
s/2HA  GLY/3HA  GLY/g
s/1HA  GLY/2HA  GLY/g
#Glutamine
s/2HB  GLN/3HB  GLN/g
s/1HB  GLN/2HB  GLN/g
s/2HG  GLN/3HG  GLN/g
s/1HG  GLN/2HG  GLN/g
#Proline
s/2HB  PRO/3HB  PRO/g
s/1HB  PRO/2HB  PRO/g
s/2HG  PRO/3HG  PRO/g
s/1HG  PRO/2HG  PRO/g
s/2HD  PRO/3HD  PRO/g
s/1HD  PRO/2HD  PRO/g
#Histidine
s/HIS+/HIS /g
s/2HB  HIS/3HB  HIS/g
s/1HB  HIS/2HB  HIS/g
/HE  HIS/d
#Tyrosine
s/2HB  TYR/3HB  TYR/g
s/1HB  TYR/2HB  TYR/g
#Tryptophan
s/2HB  TRP/3HB  TRP/g
s/1HB  TRP/2HB  TRP/g
s/ HD  TRP/HD1  TRP/g
s/ HH  TRP/HH2  TRP/g
#ALA,THR,VAL shouldn't need changes
/OXT/d
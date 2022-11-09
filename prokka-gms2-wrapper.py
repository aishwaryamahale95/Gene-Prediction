#!/usr/bin/env python3

import argparse
import os
from os import walk

#Define command line arguments
parser = argparse.ArgumentParser()
parser.add_argument('-i', '--input', metavar = "<Input Contigs>",
    help = "Path to directory containing input contigs in FASTA format", required = True)
parser.add_argument('-gms2', '--GeneMarkS2', action = 'store_true',
    help = "Use to predict genes with GeneMarkS-2")
parser.add_argument('-pr', '--prokka', action = 'store_true', 
    help = "Use to predict genes with Prokka")
parser.add_argument('-c', '--combine', action = 'store_true',
    help = "Use to predict genes with Prokka and GeneMarkS-2 and combine results")
parser.add_argument('-o', '--output', metavar = "<Output file name>",
    help = "Name of the output file")
args = parser.parse_args()

#Setup tempdir within working directory
os.system('mkdir gene-predictions')

################################################################
# The path to the gms2.pl script should be updated here:
gms2_path = ('/home/groupb/bin/tools/gms2test/gms2.pl')
# Note: the key for gms2 must be copied to your home directory:
# cp gm_key_64 ~/.gmhmmp2_key
################################################################

#Get list of files
files = []
for (dirpath, dirnames, filenames) in walk(args.input):
    files.extend(filenames)
    break
files.sort()

#Run GeneMarkS2
def run_gms2(handle):
    command = ('perl' + ' ' + gms2_path + ' ' +  '--seq' + ' ' + args.input + '/' + handle + ' ' + '--genome-type bacteria' + ' ' + '--fnn' + ' ' + handle + '.gms2.fnn' + ' ' + '--faa' + ' ' + handle + '.gms2.faa' + ' ' + '--output' + ' ' + handle + '.gms2.gff' + ' ' + '--format gff3')
    print(f"Executing: {command}")
    os.system(command)
    os.system('mv' + ' ' + handle + '.*' + ' ' + 'gene-predictions/genemarks2_output')
if args.GeneMarkS2 == True:
    os.system('mkdir gene-predictions/genemarks2_output')
    for file in files:
        run_gms2(file)

#Run Prokka
def run_prokka(handle):
    command = ('prokka' + ' ' + '--kingdom Bacteria' + ' ' + '--rfam' + ' ' + '--quiet' + ' ' + '--prefix' + ' ' + handle + '.prokka' + ' ' + '--outdir' + ' ' + 'gene-predictions/prokka_output' + ' ' + '--force' + ' ' + args.input + '/' + handle)
    print(f"Executing: {command}")
    os.system(command)
if args.prokka == True:
    setup = ('prokka --setupdb --quiet')
    print(f"Setting up databases: {setup}")
    os.system(setup)
    for file in files:
        run_prokka(file)

#Run prokka and gms2 and merge output
def combine():
    os.system('mkdir gene-predictions/prokka_gms2_merged_out')
    
    #run GMS2
    print('Running GeneMarkS-2')
    os.system('mkdir gene-predictions/genemarks2_output')
    for file in files:
        run_gms2(file)
    
    #Run Prokka
    print('Running Prokka')
    setup = ('prokka --setupdb --quiet')
    print(f"Setting up databases: {setup}")
    os.system(setup)
    for file in files:
        run_prokka(file)    

def merge(handle):
       merge = 'gffcompare ' + 'gene-predictions/genemarks2_output/' + handle + '.gms2.gff' + ' ' + 'gene-predictions/prokka_output/' + handle + '.prokka.gff' + ' ' + '-p' + ' ' + handle
       print(f"Executing: {merge}")
       os.system(merge)
       os.system('rm gffcmp.loci gffcmp.stats gffcmp.tracking')
       os.system('mv gffcmp.combined.gtf' + ' ' + 'gene-predictions/prokka_gms2_merged_out/' + handle + '.combined.gtf')
       make_gff = 'gffread -E' + ' ' + 'gene-predictions/prokka_gms2_merged_out/' + handle + '.combined.gtf' + ' ' + '-o- > ' + handle + '.combined.gff'
       print(f"Executing: {make_gff}")
       os.system(make_gff)
       os.system('mv *.combined.gff gene-predictions/prokka_gms2_merged_out')
       write_fnn = 'bedtools getfasta -fi ' + args.input + '/' + handle + ' ' + '-bed ' + 'gene-predictions/prokka_gms2_merged_out/' + handle + '.combined.gff' + ' -fo ' + handle + '.fnn'
       os.system(write_fnn)
       #Remove duplicate sequences
       fix = "awk '!seen[$0]++'" + ' ' + handle + '.fnn > gene-predictions/prokka_gms2_merged_out/' + handle + '.fnn'
       os.system(fix)
       os.system('rm *.fnn')
       os.system('rm gene-predictions/prokka_gms2_merged_out/*.fai.*')

if args.combine == True:
    combine()
    for file in files:
        merge(file)

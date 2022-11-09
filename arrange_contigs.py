#!/usr/bin/env python3

import os
from os import walk
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-i', '--input', metavar = "<Assmebly Output Directory>",
    help = "Path to directory containing sub-directories that contain contigs", required = True)
args = parser.parse_args()

os.system('mkdir' + ' ' + args.input + '/contigs_named')
#Get list of directories
directories = []
for (dirpath, dirnames, filenames) in walk(args.input):
    #files.extend(filenames)
    directories.extend(dirnames)
    break

#rename files into new directory
for directory in directories:
    rename = 'cp' + ' ' + args.input + '/' + directory + '/contigs.fasta' + ' ' + args.input + '/' + 'contigs_named/' + directory + '.contigs.fasta'
    os.system(rename)



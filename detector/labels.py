#!/usr/bin/python3

from argparse import ArgumentParser
import re
import os

arg_parser = ArgumentParser()
arg_parser.add_argument('-f', '--files', type=str, required=False, help='set input file names')
arg_parser.add_argument('-d', '--directory', type=str, required=True, help='set input directory')
args = arg_parser.parse_args()

if args.files is None and args.directory is None:
    exit("At least one of input argument '--files' or '--directory' must be set")

files = None
if args.files is not None:
    files = args.files.split(',')
directory = args.directory

def add_labels(in_f, out_f):
    h = None
    f = None
    with open(in_f, 'r') as fh:
        h = fh.readline().split(',')
        f = fh.readline().split(',')
    h[-1] = h[-1][:-1]
    f[-1] = f[-1][:-1]
    with open(out_f, 'w') as fh:
        h.append('is_anomaly')
        if (f[6] == '1'): # comm_changed
            f.append('1')
        elif (f[1] != '0' and f[10] == '1'): # mmap_rwx_page
            f.append('1')
        elif (f[5] != '0' and (f[8] == '1' or f[9] == '1')): # openat_proc_or_passwd
            f.append('1')
        elif f[3] != '0' and f[7] == '1': # execve_with_sh_arg
            f.append('1')
        else:
            f.append('0')    # not anomaly    
        fh.write(','.join(h) + '\n' + ','.join(f) + '\n')

all_files = ([] if files is None else files) + \
    ([] if directory is None or not os.path.isdir(directory) else
     [os.path.join(directory, f) for f in os.listdir(directory) if f.endswith('.features') and os.path.isfile(os.path.join(directory, f))])
for f in all_files:
    print('Processed file:', f)
    add_labels(f, re.sub(r'\.features$', '.features_with_labels', f))

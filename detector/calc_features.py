#!/usr/bin/python3

from argparse import ArgumentParser
import re
import json as js
import os
from collections import OrderedDict

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

SYSCALL_LIST = ['write', 'mmap', 'getpid', 'execve', 'clock_nanosleep', 'openat']

def calc_features(in_f, out_f):
    l = None
    with open(in_f, 'r') as fh:
        l = js.load(fh)
    with open(out_f, 'w') as fh:
        for i in range(len(l)):
            features = OrderedDict()
            is_comm_changed = 0
            is_sh_in_args = 0
            is_passwd_in_open_args = 0
            is_proc_in_open_args = 0
            is_rwx_in_mmap_args = 0
            for s in SYSCALL_LIST:
                c = 0
                for d in l:
                    if d['syscall_name'] == s:
                        c += 1
                features[s] = c
            for s in ['is_comm_changed', 'is_sh_in_args', 'is_passwd_in_openat_args', 'is_proc_in_openat_args', 'is_rwx_in_mmap_args']:
                features[s] = 0
            for d in l:
                if features['is_comm_changed'] == 0 and d['proc_name'] == 'sh':
                    features['is_comm_changed'] = 1
                if features['is_sh_in_args'] == 0 and 'syscall_args' in d.keys() and re.compile('.*\/+bin\/+sh.*').match(d['syscall_args']):
                    features['is_sh_in_args'] = 1
                if features['is_passwd_in_openat_args'] == 0 and 'syscall_args' in d.keys() and re.compile('.*\/+etc\/+passwd.*').match(d['syscall_args']):
                    features['is_passwd_in_openat_args'] = 1
                if features['is_proc_in_openat_args'] == 0 and 'syscall_args' in d.keys() and re.compile('.*\/+proc.*').match(d['syscall_args']):
                    features['is_proc_in_openat_args'] = 1
                if features['is_rwx_in_mmap_args'] == 0 and 'syscall_args' in d.keys() and re.compile('.*prot: 0x7.*').match(d['syscall_args']):
                    features['is_rwx_in_mmap_args'] = 1
            if i == 0:
                fh.write(','.join(features.keys()) + '\n')
        fh.write(','.join(list(map(lambda x: str(x), features.values()))) + '\n')
all_files = ([] if files is None else files) + \
    ([] if directory is None or not os.path.isdir(directory) else
     [os.path.join(directory, f) for f in os.listdir(directory) if f.endswith('.out') and os.path.isfile(os.path.join(directory, f))])
for f in all_files:
    print('Processed file:', f)
    calc_features(f, re.sub(r'\.out$', '.features', f))

#!/usr/bin/python3

from argparse import ArgumentParser
import re
import subprocess as sp
import json as js
import signal
import time as tm
import os

arg_parser = ArgumentParser()
arg_parser.add_argument('-t', '--time_window_size', type=float, required=False, help='set time window size')
arg_parser.add_argument('-o', '--out_directory', type=str, required=False, help='set output directory')
args = arg_parser.parse_args()

time_window_size = 5 # default value (in seconds)
if args.time_window_size is not None:
    time_window_size = args.time_window_size

out_directory = 'out_dir' # default value
if args.out_directory is not None:
    out_directory = args.out_directory

is_break = False
def signal_handler(sig, frame):
    is_break = True

signal.signal(signal.SIGINT, signal_handler)

def save_to_file(s, f):
    if not os.path.isdir(out_directory):
        os.makedirs(out_directory)
    with open(os.path.join(out_directory, f), 'w') as fh:
        fh.write(s)  

# run bpftrace
cmd = "bpftrace simple_loop_tracer.bt"
proc = sp.Popen(re.split('\s+', cmd), stdout=sp.PIPE)
# process bpftrace output line by line
psc = []
st = None
i = 0
while not is_break:
    ct = tm.time()
    if st is None:
        st = ct
    elif ct - st > time_window_size:
        if len(psc) > 0:
            save_to_file(js.dumps(psc, indent=2), "output_{}_{}.out".format(st, ct))
            psc = []
        st = ct
    
    line = proc.stdout.readline()
    if not line:
        break
    patt = re.search('(^[a-z_]+) -> ([a-z_]+)[(](.*)[)]; return value: (.*)', str(line))
    nano = re.search('(^[a-z_]+) -> ([a-z_]+)[(](.*)[)]$', str(line))
    if patt:
        comm = patt.group(1)
        syscall = patt.group(2)
        args = patt.group(3)
        ret_val = patt.group(4)
        syscall_info = {'proc_name': comm,'syscall_name': syscall, 'syscall_args': args, 'syscall_ret_val': ret_val}
    elif nano:
        comm = nano.group(1)
        syscall = nano.group(2)
        syscall_info = {'proc_name': comm, 'syscall_name': syscall}
    else:
    	continue
    psc += [syscall_info]
    print(js.dumps(psc, indent=2))

#!/usr/bin/python3

from argparse import ArgumentParser
import re

arg_parser = ArgumentParser()
arg_parser.add_argument('-p', '--pid', type=int, required=True, help='set process id')
args = arg_parser.parse_args()

pid = str(args.pid)

curr_pid = '/pid == {}/'.format(pid)
with open('simple_loop_tracer.bt', 'r') as f:
    data = f.read()
data = re.sub('/pid == ([\d]+)/', curr_pid, data)
with open('simple_loop_tracer.bt', 'w') as f:
    f.write(data)

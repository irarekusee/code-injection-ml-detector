#!/usr/bin/python

from argparse import ArgumentParser
from code_injection import call_execve

arg_parser = ArgumentParser()
arg_parser.add_argument('-p', '--pid', type=int, required=True,
                        help='set process id')
arg_parser.add_argument('-a', '--addr', type=int, required=False,
                        help='set address')

args = arg_parser.parse_args()
pid = args.pid
addr = args.addr
call_execve(pid, addr)

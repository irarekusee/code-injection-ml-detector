This repository contains the following scripts:

- simple_loop_tracer.bt to intercept system calls made by the process of the running program simple_loop.c

- replace_pid.py to replace PID values in simple_loop_tracer.bt

For the correct functioning of the script, you must run: 
"python3 replace_pid.py -p $(pgrep simple_loop)"
or
"python3 replace_pid.py -p $(pgrep simple_loop_dl)"

- process_output.py to run simple_loop_tracer.bt and process its output messages line by line in json format

For the correct functioning of the script, you must:
1. install bpftrace
2. run "python3 replace_pid.py -p $(pgrep simple_loop)" to set correct values of PID in the script
3. run "python3 process_output.py -t 5 -o out_dir" (requires superuser rights),
where the -t parameter denotes the time window during which json records about the attributes of system calls are collected,
the -o parameter denotes the name of the directory in which json files will be saved

- calc_features.py to calculate features. Input files of the form "output_%.%_%.%.out" are converted to files of the form "output_%.%_%.%.features"

- labels.py to mark vectors of feature attributes

- clf_records.py to classify feature vectors of system calls

To run calc_features.py or labels.py or clf_records.py you must run one of the following commands:
1. "python3 <name>.py -d out_dir", where the -o parameter specifies the name of the directory with processed files
2. "python3 <name>.py -f files", where the -f parameter specifies the names of the processed files, separated by a comma

Note: file metrics.txt contains the output of the clf_records.py script
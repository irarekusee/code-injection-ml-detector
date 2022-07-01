#include <stdio.h>
#include <dlfcn.h>
#include <unistd.h>
#define DL_LIB "/lib/x86_64-linux-gnu/libdl-2.31.so"

int main(int argc, char *argv[]) {
	void *l = dlopen(DL_LIB, RTLD_LAZY);
	printf("RTLD_LAZY: %d\n", RTLD_LAZY);
	if (l != NULL) {
		void *s = dlsym(l, "dlopen");
		if (s != NULL)
			printf("dlopen address: %llx\n", (unsigned long long)s);
		else
			printf("could not find dlopen\n");
		dlclose(l);
	}
	else
		printf("could notopen library '%s'\n", DL_LIB);

	sleep(10);
	return 0;
}

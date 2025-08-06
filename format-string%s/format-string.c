#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main() {
    FILE *fd;
    char *flag = malloc(64);
    if (!flag) {
        perror("malloc failed");
        return 1;
    }

    fd = fopen("flag.txt", "rt");
    if (fd == NULL) {
        perror("Error opening file");
        free(flag);
        return 1;
    }

    fgets(flag, 64, fd);
    fclose(fd);

    char *buf = flag;

    char fmstr[16];
    puts("Welcome Human!");
    puts("If you is a hacker, I have gift for u.");
    fgets(fmstr, sizeof(fmstr), stdin);
    printf(fmstr, buf);

    free(flag);
    return 0;
}

#include <stdio.h>

int main() {
    FILE *fd;
    char fmstr[16];
    char buf[24];
    fd = fopen("flag.txt", "rt");
    if (fd == NULL) {
        perror("Error opening file");
        return 1;
    }
    fgets(buf, sizeof(buf), fd);
    fclose(fd);

    puts("Welcome Human!");
    puts("If you is a hacker, I have gift for u.");
    fgets(fmstr, 32, stdin);
    printf(fmstr);
    return 0;
}

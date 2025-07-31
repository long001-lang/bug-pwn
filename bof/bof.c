#include<stdio.h>
#include <stdlib.h>

char *gets(char *);
void win() {
    system("/bin/sh");
}

int main(){
    char buf[128];
    puts("welcome to bof ez !!!");
    puts("Can you get shell");
    gets(buf);
    return 0;
}

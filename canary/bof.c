#include<stdio.h>
#include <stdlib.h>
#include <unistd.h>


char *gets(char *);
void win() {
    system("/bin/sh");
}

void vul(){
    char secret[64];
    puts("Gift for u:");
    gets(secret);
}
int main(){
    char buf[64];
    puts("welcome to bof ez !!!");
    puts("Can you get shell");
    read(0,buf,73);
    puts("Oh... I see!");
    puts(buf);
    vul();
    return 0;
}

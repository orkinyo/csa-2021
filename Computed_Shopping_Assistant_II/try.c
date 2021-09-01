#include <stdio.h>
#include <string.h>
#include <stdlib.h>

int main() {
    char buffer[20];
    fgets(buffer, 20, stdin);
    for(int i = 0 ; i < 21 ; i ++) {
        printf("%02x ",buffer[i]);
    }
}
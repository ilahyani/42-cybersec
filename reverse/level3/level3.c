#include <stdio.h>
#include <string.h>
#include <stdlib.h>

void ___syscall_malloc() {
    puts("Nope.");
    exit(1);
}

void ____syscall_malloc() {
    puts("Good job.");
    exit(1);
}

int main() {
    
    char user_key[24];

    printf("Please enter key: ");
    if (scanf("%23s", user_key) != 1) {
        ___syscall_malloc();
    }

    if (user_key[0] != '4' || user_key[1] != '2') {
        ___syscall_malloc();
    }
    
    char result[9];
    result[0] = '*';
    int user_key_index = 2;
    int res_index = 1;

    while (1) {

        if (res_index == 8) {
            result[8] = '\0';
            break;
        }

        char chunk[4];
        strncpy(chunk, &user_key[user_key_index], 3);
        chunk[3] = '\0';

        result[res_index] = (char) atoi(&chunk[0]);

        user_key_index += 3;
        res_index += 1;
    }

    switch(strcmp(result, "********")) { 
        case 0:
            ____syscall_malloc();
        case 1:
            ___syscall_malloc();
        case 2:
            ___syscall_malloc();
        case 3:
            ___syscall_malloc();
        case 4:
            ___syscall_malloc();
        case 5:
            ___syscall_malloc();
        case 0x73:
            ___syscall_malloc();
        case 0xfffffffe:
            ___syscall_malloc();
        case 0xffffffff:
            ___syscall_malloc();
    }
    ___syscall_malloc(); 
}

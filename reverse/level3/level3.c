#include <stdio.h>
#include <string.h>
#include <stdlib.h>

int main() {
    
    char user_key[24];

    printf("Please enter key: ");
    if (scanf("%23s", user_key) != 1) {
        return printf("Nope.\n");
    }

    if (user_key[0] != '4' || user_key[1] != '2') {
        return printf("Nope.\n");
    }
    
    char result[9];
    
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

    if (strcmp(result, "********") == 0) {
        return printf("Good job.\n");
    }

    return printf("Nope.\n"); 
}

//24
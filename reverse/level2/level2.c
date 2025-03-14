#include <stdio.h>
#include <string.h>
#include <stdlib.h>

void no() {
    puts("Nope.");
    exit(1);
}

void ok() {
    puts("Good job.");
    exit(1);
}

int main() {
    
    char user_key[24];

    printf("Please enter key: ");
    if (scanf("%23s", user_key) != 1) {
        no();
    }

    if (user_key[0] != '0' || user_key[1] != '0') {
        no();
    }
    
    char result[9];
    result[0] = 'd';

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

    if (strcmp(result, "delabere") == 0) {
        ok();
    }

    no(); 
}

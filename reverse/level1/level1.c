#include <stdio.h>
#include <string.h>

int main() {
    char key[] = "__stack_check";
    char user_key[14];

    printf("Please enter key: ");
    scanf("%13s", user_key);

    if (strcmp(key, user_key) == 0) {
        return printf("Good job.\n");
    }

    return printf("Nope.\n");
}

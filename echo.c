#include <stdio.h>

int main(int argc, char **argv){

    if(argc == 2){
        if(*argv[1] == '1'){
            printf("You can pass arguments to echo program by --args option\n");
            printf("Return non-zero to print stdout to shell but not excuting diff\n");
            return 1;
        }
        else if(*argv[1] == '2'){
            fprintf(stderr, "stderr will also be written into output file. You should return non-zero to move output file to log file\n");
            return 2;
        }
    }
    int c;
    while((c = getchar()) != EOF){
        putchar(c);
    }
    return 0;
}

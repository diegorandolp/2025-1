#include <stdio.h>
#include <stdlib.h>
#include <signal.h>
#include <assert.h>
#include <unistd.h>
#include <fcntl.h>

#define FILENAME "temp.txt"

int fd;

static void myHandler (int signum) {
    printf("Deleting file %s\n", FILENAME);
    int rm = remove(FILENAME);
    if (rm == 0){
      printf("File %s deleted\n", FILENAME);
    } else {
      printf("File %s could not be deleted\n", FILENAME);
    }
    exit(0);
}

int main(){
    fd = open(FILENAME, O_CREAT);

    unsigned long int i = 0;

    int iRet;
    struct sigaction sAction;
    sAction.sa_flags = 0;
    sAction.sa_handler = myHandler;

    sigemptyset(&sAction.sa_mask);
    iRet = sigaction(SIGINT, &sAction, NULL);

    assert(iRet == 0);

    printf("Working with file %s\n", FILENAME);

    while(1){
      sleep(1);
    }

    return 0;
}

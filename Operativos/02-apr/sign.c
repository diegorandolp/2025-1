#include <stdio.h>
#include <stdlib.h>
#include <signal.h>
#include <assert.h>
#include <unistd.h>

static void myHandler (int signum) {
    printf("In myHandler with argument %d\n", signum);
}

int main(){
    unsigned long int i = 0;

    int iRet;
    struct sigaction sAction;
    sAction.sa_flags = 0;
    sAction.sa_handler = myHandler;

    sigemptyset(&sAction.sa_mask);
    for (int i = 0; i <= 64; i++) {
        if (i == 32 || i == 33) {
            continue;
        }
        iRet = sigaction(i, &sAction, NULL);
    }
    assert(iRet == 0);

    while(1){
      sleep(1);
    }
    return 0;

}
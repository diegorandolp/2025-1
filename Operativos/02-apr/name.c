#include <stdio.h>
#include <stdlib.h>
#include <signal.h>
#include <assert.h>
#include <unistd.h>
#include <fcntl.h>


static void myHandler (int signum) {
    printf("Diego");
    exit(0);
}

int main(){


    int iRet;
    struct sigaction sAction;
    sAction.sa_flags = 0;
    sAction.sa_handler = myHandler;

    sigemptyset(&sAction.sa_mask);
    iRet = sigaction(SIGALRM, &sAction, NULL);

    assert(iRet == 0);
    int alrm = alarm(6);

    while(1){
      sleep(1);
    }

    return 0;
}

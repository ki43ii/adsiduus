#include <stdio.h>
#include <stdlib.h>
#include <time.h>

int main(){
    srand(time(NULL));

    float message = 0.0f;

    while (1) {
        system("clear");
        printf("\033[%d%d;%d%dm", rand() % 10, rand() % 10, rand() % 10, rand() % 10);
        if (message < 20)
            printf("You are who hath repaved a path long forgotten by your damned books!\n");
        else if (message > 20)
            printf("Worthless barbaric creatures like you are clearly worthy enough to fight me, but just not worthy enought to win\n");
        if (message == 40)
            break;
        message++;
        sleep(0);

    }

    return 0;
}

void sleep(int suggestedTime){
        time_t priorTime = time(NULL);
        while(1){
                time_t currentTime = time(NULL);
                if(currentTime - priorTime == suggestedTime){
                        break;
                }
        }
}

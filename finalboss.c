#include <stdio.h>
#include <stdlib.h>
#include <time.h>

extern void sleep(int suggestedTime);

int main(){
    srand(time(NULL));
    
    puts("epilepsy warning!");
    sleep(3);

    float message = 0.0f;
    time_t priorTime = time(NULL);
    
    while (1) {
        system("clear");
	time_t currentTime = time(NULL);
	int wastedTime = currentTime - priorTime;
	for(int i = 0; i <= 1000; i++)
        	printf("\033[%d%d;%d%dm", rand() % 10, rand() % 10, rand() % 10, rand() % 10);
        if (wastedTime < 7)
            printf("You are who hath repaved a path long forgotten by your damned books!\n");
        else if (wastedTime > 6)
            printf("You have made it clear that a pariah like you is worthy enough to fight me. However, you are just not worthy enough to win.\n");
        if (wastedTime == 15)
            break;
        message++;

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
	//sleep is an OS-dependent function, i js made a universal one lmao

}

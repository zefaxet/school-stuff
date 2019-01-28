#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>
#include <string.h>

// #define nPhilosophers 20
pthread_mutex_t mutex = PTHREAD_MUTEX_INITIALIZER;

void* eat(void* nHunger);
int count = 0;

int main( int argc, char** argv)
{
	
	if (argc == 3)
	{
		
		int nPhilosophers = strtol(argv[2], (char**) NULL, 10);
		int nHunger = strtol(argv[1], (char**) NULL, 10);
		
		printf("Number of philosophers: %d\n", nPhilosophers);
		if (nPhilosophers < 2)
		{
			//TODO fix?
			puts("Bad number of philosophers:\n\tThere must be at least 2.");
			goto leave;
		}
		printf("Each philosopher will eat %d times.\n", nHunger);
		
		pthread_t tThreads[nPhilosophers];
		
		int i, j;
		for(i=0; i < nPhilosophers; i++)
		{
			
			printf("Create thread %d\n", i);
			pthread_create( &tThreads[i], NULL, &eat, (void*) &nHunger);
			
		}
		
		for(j=0; j < nPhilosophers; j++)
		{
			
			int err = pthread_join( tThreads[j], NULL);
			if (err)
			{
				
				printf("pthread_join %d failed.\n\t%s\n", j, strerror(err));
				goto leave;
				
			}
			else
			{
				
				printf("Join thread success: %d.\n", j);
				
			}
			
		}
		
	}
	
	leave:
	exit(0);
	
}

void* eat(void* nHunger)
{	
	// printf("\tHunger %d\n", *(int*) nHunger);
	pthread_mutex_lock( &mutex );
	count++;
	printf("\tCount %d\n", count);
	pthread_mutex_unlock( &mutex );
}
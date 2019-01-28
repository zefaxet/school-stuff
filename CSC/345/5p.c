#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>

#define n 2
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
		printf("Each philosopher will eat %d times.\n", nHunger);
		
		pthread_t tThreads[n];
		
		int i = 0;
		for(int i=0; i < n; i++)
		{
			
			printf("Create thread %d\n", i);
			pthread_create( &tThreads[i], NULL, &eat, (void*) &nHunger);
			
		}
		
		for(int i=0; i < n; i++)
		{
			
			printf("Join thread %d\n", i);
			pthread_join( tThreads[1], NULL);
			
		}
		
		printf("AND IN THE END... %d\n", count);
		
	}
	else
	{
		
		printf("Bad number of arguments: %d.\n", argc);
		puts("Use:
		
	}
	
	exit(0);
	
}

void* eat(void* nHunger)
{	
	printf("test %d\n", *(int*) nHunger);
	pthread_mutex_lock( &mutex );
	count++;
	printf("count %d\n", count);
	pthread_mutex_unlock( &mutex );
	return (void*) NULL;
}
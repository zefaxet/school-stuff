#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>
#include <string.h>
#include <unistd.h>

#define DEBUG 0
pthread_mutex_t chopsticks[32];
pthread_mutex_t init_mutex = PTHREAD_MUTEX_INITIALIZER;
void* start(void* philosopher);
int nHunger;
int nPhilosophers;

int main( int argc, char** argv)
{
	
	if (argc == 3)
	{
		
		nPhilosophers = strtol(argv[2], (char**) NULL, 10);
		nHunger = strtol(argv[1], (char**) NULL, 10);
		
		printf("Number of philosophers: %d\n", nPhilosophers);
		if (nPhilosophers < 2)
		{
			//TODO fix?
			puts("Bad number of philosophers:\n\tThere must be at least 2.");
			goto leave;
		}
		printf("Each philosopher will eat %d times.\n", nHunger);
		
		pthread_mutex_t mutexes[nPhilosophers];
		for (int i = 0; i < nPhilosophers; i++)
		{
			if (DEBUG)
			{
				printf("Make mutex %d.\n", i);
			}
			// pthread_mutex_init(&mutexes[i], NULL);
			pthread_mutex_init( &chopsticks[i], NULL);
			
		}
		
		// chopsticks = mutexes;
		
		pthread_t tThreads[nPhilosophers];
		
		int i, j;
		for(i=0; i < nPhilosophers; i++)
		{
			int * philosopher = &i;
			if (DEBUG)
			{
				printf("Create thread %d\n", i);
			}
			pthread_mutex_lock( &init_mutex );
			pthread_create( &tThreads[i], NULL, &start, (void*) philosopher);
			
		}
		
		for(j=0; j < nPhilosophers; j++)
		{
			
			int err = pthread_join( tThreads[j], NULL);
			if (err)
			{
				
				printf("pthread_join %d failed.\n\t%s\n", j, strerror(err));
				goto leave;
				
			}
			else if (DEBUG)
			{
				
				printf("Join thread success: %d.\n", j);
				
			}
			
		}
		
	}
	
	leave:
	exit(0);
	
}

void * start(void * i)
{	
	int philosopher = * (int *) i;
	int hunger = nHunger;
	int left_mutex_index = philosopher;
	int right_mutex_index = (philosopher + 1) % nPhilosophers;
	printf("Philosopher %d has joined the table.\n", philosopher);
	pthread_mutex_unlock( &init_mutex );
	while(hunger > 0)
	{
		printf("Philosopher %d is thinking.\n", philosopher);
		/* 
		Sleeping the thread for 1 millisecond 'disturbs' the order and allows another thread to pick up a chopstick mutex.
		Without this sleep the distribution of the mutexes does not vary much and the same thread can tend to hog them.
		*/
		usleep(1000);
		// pthread_mutex_lock( (chopsticks + sizeof(pthread_mutex_t) * philosopher) );
		// pthread_mutex_lock( (chopsticks + sizeof(pthread_mutex_t) * (philosopher + 1)) );
		pthread_mutex_lock( &chopsticks[left_mutex_index] );
		pthread_mutex_lock( &chopsticks[right_mutex_index] );
		if (DEBUG)
		{
			printf("Locked mutexes %d and %d.\n", left_mutex_index, right_mutex_index);
		}
		printf("Philosopher %d has eaten. Hunger is now %d.\n", philosopher, --hunger);
		// pthread_mutex_unlock( (chopsticks + sizeof(pthread_mutex_t) * philosopher) );
		// pthread_mutex_unlock( (chopsticks + sizeof(pthread_mutex_t) * philosopher) );
		pthread_mutex_unlock( &chopsticks[left_mutex_index] );
		pthread_mutex_unlock( &chopsticks[right_mutex_index] );
		if (DEBUG)
		{
			printf("Unlocked mutexes %d and %d.\n", left_mutex_index, right_mutex_index);
		}
	}
}
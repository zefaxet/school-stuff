/*
Made by Edward Auttonberry
Dining Philosophers solution using POSIX pthreads
For CSC 345 Operating Systems
*/

#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>
#include <string.h>
#include <unistd.h>

#define DEBUG 0
#define MAX_PHILOSOPHERS 2048

/* This program supports up to 2048 philosophers and any number of eatings */
pthread_mutex_t chopsticks[MAX_PHILOSOPHERS];
pthread_mutex_t init_mutex = PTHREAD_MUTEX_INITIALIZER;
void* start(void* philosopher);
int nHunger;
int nPhilosophers;

int main( int argc, char** argv)
{
	
	// Need to run binary as well as define number of eating sessions and philosophers: 3 args
	if (argc == 3)
	{
		
		// Arg parsing
		nPhilosophers = strtol(argv[2], (char**) NULL, 10);
		nHunger = strtol(argv[1], (char**) NULL, 10);
		
		// The solution requires that the number of philosophers sitting is greater than one
		// So that more than one chopstick exists (2 are required)
		printf("Number of philosophers: %d\n", nPhilosophers);
		if (nPhilosophers < 2)
		{
			puts("Bad number of philosophers:\n\tThere must be at least 2.");
			goto leave;
		}
		printf("Each philosopher will eat %d times.\n", nHunger);
		
		// Create mutexes
		pthread_mutex_t mutexes[nPhilosophers];
		for (int i = 0; i < nPhilosophers; i++)
		{
			if (DEBUG)
			{
				printf("Make mutex %d.\n", i);
			}
			pthread_mutex_init( &chopsticks[i], NULL);
			
		}
		
		
		pthread_t tThreads[nPhilosophers];
		
		// Start threafs
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
		
		// Join threads
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

// Thread method
void * start(void * i)
{	

	// Dereference the method argument for further use
	int philosopher = * (int *) i;
	int hunger = nHunger;
	// Assign mutex indices
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
		pthread_mutex_lock( &chopsticks[left_mutex_index] );
		pthread_mutex_lock( &chopsticks[right_mutex_index] );
		if (DEBUG)
		{
			printf("Locked mutexes %d and %d.\n", left_mutex_index, right_mutex_index);
		}
		printf("Philosopher %d has eaten. Hunger is now %d.\n", philosopher, --hunger);
		pthread_mutex_unlock( &chopsticks[left_mutex_index] );
		pthread_mutex_unlock( &chopsticks[right_mutex_index] );
		if (DEBUG)
		{
			printf("Unlocked mutexes %d and %d.\n", left_mutex_index, right_mutex_index);
		}
		
	}
	
	printf("===== Philosopher %d has finished eating. =====\n", philosopher);
	
}
#include <string.h>
#include <stdio.h>
#include <stdlib.h>

int main()
{
	
	char * tok = "abc | de | f";
	char * next  = strdup(tok);
	char * test = malloc(sizeof(next));
	test = strsep(&next, ",");
	// puts(tok);
	puts(test);
	puts(next);
	
}

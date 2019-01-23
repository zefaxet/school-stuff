#include <regex.h>
#include <stdio.h>

regex_t regt;
int succ;

int main()
{
	
	succ = regcomp(&regt, "^ *exit", 0);
	if (succ)
	{
		printf("fail");
		exit(1);
	}
	succ = regexec(&regt, "   exit", 0, NULL, 0);
	if (!succ)
	{

		printf("Match\n");

	}
	else if (succ == REG_NOMATCH)
	{
		printf("No Match\n");
	}

}

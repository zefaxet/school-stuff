#include <string.h>
#include <stdio.h>

int main()
{
	char * sett = "sett       ";
	char set[3] = "set";
	printf("%d\n", sizeof(set));
	printf("%d\n", strlen(sett));
	printf("%d\n", strncmp(set, sett, sizeof(set)));
	printf("%d\n", strcmp(set, sett));

	int l = strlen(sett);
	while(isspace(sett[l - 1]))
	{
		set[--l] - 0;
		puts("test");
	}
	memmove(sett, sett, l + 1);
	char * af = malloc(sizeof(char) * l);
	strncpy(af, sett, l);
	puts("");
	puts(af);
	printf("%d\n", strlen(af));
	puts("");
	char in[4];
	char exit[5] = "exit\0";
	fgets(in, 5, stdin);
	printf("%s,%s\n", in, exit);
	printf("%d\n", strcmp(in, exit));
	puts(NULL);
}

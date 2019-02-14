#include <ctype.h>
#include <errno.h>
#include <fcntl.h>
#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <sys/stat.h>
#include <sys/wait.h>
#include <unistd.h>
#include <strmap.h>

const char EXIT[5] = "exit";
const char PWD[3] = "pwd";
const char CD[3] = "cd";
const char SET[4] = "set";
const char LIST[5] = "list";
const char * DELIM = " |\n\r\t";

int stdin_fd, stdout_fd, infd, outfd;

char cwd[1024]; //directory to print at beginning of each line

char in[1024]; //user input
char * token;
char * args[32];

pid_t child, c;
int cstatus;

StrMap * symbol_table;

//error handling with strerr(errno)
extern int errno;

void trim_trailing_whitespace(char * str)
{

	int len = strlen(str);
	while(isspace(str[len - 1])) len--;
	char * stripped = malloc(sizeof(char) * len);
	stripped = strncpy(stripped, str, len);
	str = stripped;	

}

void lambda(char * key, char * value, void * obj)
{
	printf("%s: %s\n", key, value);
}

void parse(char * args, int stdin_fd)
{
	
}

int main()
{

	printf("Tech Shell - CSC 345 Version\nBy Edward Auttonberry\nWinter 2018\n");

	symbol_table = sm_new(1024);

	stdin_fd = dup(0);
	stdout_fd = dup(1);
	
	while(1)
	{

		dup2(stdin_fd,0);
		dup2(stdout_fd,1); //reset stdio
		infd = 0;
		outfd = 1;
		
		//clear args
		memset(args, 0, sizeof(args));

		getcwd(cwd, sizeof(cwd));
		printf("%s$ ",cwd);
	
		fgets(in, sizeof(in), stdin);
		
		char * outref;
		char * inref;
		char * fileref;

		//REDIRECTION
		if((outref = strstr(in, ">")))
		{
			
			fileref = strtok(outref + 1, DELIM);
			outfd = open(fileref, O_TRUNC | O_WRONLY | O_CREAT); 
			if (dup2(outfd, 1) < 0)
			{
				perror("Failed to duplicate stdout.");
				continue;
			}

			*outref = (char) NULL;

		}
		if((inref = strstr(in, "<")))
		{

			fileref = strtok(inref + 1, DELIM);
			infd = open(fileref, O_RDONLY);
			if (errno == ENOENT)
			{
				perror(strerror(errno));
				continue;
			}
			if (dup2(infd, 0) < 0)
			{
				perror("Failed to duplicate stdin.");
				continue;
			}

			*inref = (char) NULL;

		}
		//REDIRECTION~		

		token = strtok(in, DELIM);
		trim_trailing_whitespace(token);
		
		if (token != NULL)
		{
			if(!strcmp(token, EXIT))
			{
				
				token = strtok(NULL, DELIM);
				if (token == NULL)
				{
					printf("Exiting with status code 0.\n");
					exit(0);
				}
				else if (isdigit(*token))
				{
					int code = *token - '0';
					printf("Exiting with status code %d\n",code);
					exit(code);
				}
				else
				{
					printf("Invalid exit code '%s'. Exiting with -1.\n", token);
					exit(-1);
				}
			}
			else if(!strcmp(token, PWD))
			{
				printf("%s\n",cwd);
				continue;
			}
			else if(!strcmp(token, CD))
			{
				token = strtok(NULL, DELIM);
				chdir(token);
				continue;
			}
			else if(!strcmp(token, SET))
			{
				token = strtok(NULL, DELIM);
				if (token)
				{
					char * identifier = token;
					token = strtok(NULL, "\n");
					if (token)
					{
						char * value = token;
						sm_put(symbol_table, identifier, value);
						goto set_success;
					}
					else
					{
						goto set_error;
					}
				}
				else
				{
					goto set_error;
				}
				
				set_error:
				puts("Invalid usage: set <name> <value>");
				set_success:
				continue;
			}
			else if(!strcmp(token, LIST))
			{
				
				sm_enum(symbol_table, (sm_enum_func) lambda, NULL); 
			}
			else
			{

				int i = 0;

				do
				{
					
					args[i++] = token;	

				}
				while( (token = strtok( NULL, DELIM )) != NULL);
				
				if ((child = fork()) == 0)
				{
					
					if(execvp(args[0],args) == -1)
					{
						printf("You tryna run this '%s' trash, fam? Aight bet.\n",args[0]);
						exit(-1);
					}
					

				}
				else
				{
					
					if (child == (pid_t)(-1))
					{
						puts("Fork failed.");
					}
					else
					{
						c == wait(&cstatus);
					}
				}

			}

		}

		if (outfd != 1)
		{
			fflush(stdout);
			close(outfd);
		}
		if (infd != 0)
		{
			fflush(stdin);
			close(infd);
		}

	}
}

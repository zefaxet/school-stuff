#include <ctype.h>
#include <errno.h>
#include <fcntl.h>
#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <sys/stat.h>
#include <sys/wait.h>
#include <unistd.h>

const char EXIT[4] = "exit";
const char PWD[3] = "pwd";
const char CD[2] = "cd";
const char * DELIM = " \n\r\t";

int stdin_fd, stdout_fd, infd, outfd;

char cwd[1024]; //directory to print at beginning of each line

char in[1024]; //user input
char * token;
char * args[32];

pid_t child, c;
int cstatus;

extern int errno;

//error handling with strerr(errno)

int main()
{

	printf("Tech Shell - CSC 222 Version\nBy Edward Auttonberry\nFall 2018\n");

	stdin_fd = dup(0);
	stdout_fd = dup(1);
	
	while(1)
	{

		dup2(stdin_fd,0);
		dup2(stdout_fd,1); //reset stdio
		infd = 0;
		outfd = 1;

		memset(args, 0, sizeof(args));

		getcwd(cwd, sizeof(cwd));
		printf("%s$ ",cwd);
	
		fgets(in, sizeof(in), stdin);
		
		char * outref;
		char * inref;
		char * fileref;

		//REDIRECTION
		if((outref = strstr(in,">")))
		{
			
			fileref = strtok(outref + 1, DELIM);
			outfd = open(fileref, O_TRUNC | O_WRONLY | O_CREAT); 
			if (dup2(outfd, 1) < 0)
			{
				perror("Failed to duplicate stdout.");
				continue;
			}

			*outref = (char *) NULL;

		}
		if((inref = strstr(in,"<")))
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

			*inref = (char *) NULL;

		}
		//		

		token = strtok(in, DELIM);
		
		if (token != NULL)
		{
			if(!strncmp(token, EXIT, sizeof(EXIT)))
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
			else if(!strncmp(token, PWD, sizeof(PWD)))
			{
				printf("%s\n",cwd);
				continue;
			}
			else if(!strncmp(token, CD, sizeof(CD)))
			{
				token = strtok(NULL, DELIM);
				chdir(token);
				continue;
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

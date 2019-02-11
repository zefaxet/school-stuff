#include <stdio.h>
#include <string.h>
#include <ctype.h>
#include <stdlib.h>
#include <stdbool.h>

#define BUFFER_SIZE 1024
#define TOKEN_SIZE 32

typedef struct symbol
{
    char* identifierName;
    int offset;
    struct symbol* next;
} symbol;

void insert(symbol** headRef,char* identifier)
{
    symbol* newnode = malloc(sizeof(symbol));
    static symbol* prevnode;
    newnode->identifierName = (char*) malloc((strlen(identifier)+1)*sizeof(char));

    if(*headRef==NULL) 
    {
        newnode->offset=0;
        prevnode = newnode;
    }

    strcpy(newnode->identifierName,identifier);

	(newnode->offset) = (prevnode->offset) + sizeof(char);

    prevnode = newnode;
    newnode->next = (*headRef);
    (*headRef) = newnode;
}

void display(symbol* node)
{
    while(node!=NULL)
    {
        printf("%s %d \n",node->identifierName,node->offset);
        node = node->next;
    }
}

bool isIdentifier(const char* token)
{
    if(isalpha(token[0]) || token[0]=='_')
    {
        for(int i=1; token[i] != NULL; i++)
        {
            if(!isalnum(token[i]))
                return false;
        }
        return true;
    }
    return false;
}

bool isDatatype(const char* token)
{
    const char *datatype[]={"char","double","float","int"};
    for(size_t i=0;i<(sizeof(datatype)/sizeof(char*));i++)
    {
        if(strcmp(token,datatype[i])==0)
            return true;
    }
    return false;
}

void isDeclaration(char* statement,symbol** head)
{
    char *delimiters = " ,;\t";
    char *token = strtok(statement,delimiters);
    if(!isDatatype(token))
        return;
    char *datatype = token;
    while((token=strtok(NULL,delimiters)))
        if(isIdentifier(token))
            insert(head,token);    
}

FILE* openFile(int param1,char* param2[])
{
    if(param1<2) 
    {
        fprintf(stderr,"No file specified to read. \n");
        exit( EXIT_FAILURE );
    }

    if(param1>2)
    {
        fprintf(stderr,"Too many arguments for read to perform. \n");
        exit( EXIT_FAILURE );
    }

    FILE *fp = fopen(param2[1],"r");

    if(fp==NULL)
    {
        fprintf(stderr,"File access denied on read. \n");
        exit( EXIT_FAILURE );
    }
    return fp;
}


int main(int argc, char *argv[])
{   
    FILE *fp = openFile(argc,argv);

    char string[BUFFER_SIZE];
    symbol* head = NULL;

    while(fgets(string,sizeof string, fp))
        isDeclaration(string,&head);

    display(head);
    return 0;
}
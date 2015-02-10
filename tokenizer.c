//
//  tokenizer.c
//  
//
//  Created by Max Bucci on 9/22/14.
//
//  Takes an input C file from user input and generates a list of tokens
//  and lexemes for that file. This list is output to the terminal as well 
//  as to a .txt file "tokens.txt" in the current directory. 
//
//

#include "tokenizer.h"

#include <stdlib.h>
#include <stdio.h>
#include <ctype.h>
#include <math.h>
#include <string.h>


#define NUM_TOK 1000

//Returns 1 if a terminal symbol ( ;, {, }, [, ], (, ) ), 0 otherwise
int checkTerminal(char *c) {
    
    if (!strcmp(c,"(") || !strcmp(c,"{") || !strcmp(c,"[") || !strcmp(c,")") || !strcmp(c,"}") || !strcmp(c,"]") || !strcmp(c,";"))
    {
        return 1;
    }
    return 0;
}



//Returns 1 if string contains only digits ( {digit}* ), 0 otherwise.
int checkDigit(char *s) {
    
    for (int i = 0; i < strlen(s); i++) {
        if (!isdigit(s[i]))
            return 0;
    }
    return 1;
}


//Returns 1 if string is a float ({digit}*.{digit}*), 0 otherwise.
int checkFloat(char *s) {
    
    if (strstr(s, ".") && (s[0] != '.') && (s[strlen(s)-1] != '.')) {
        for (int i = 0; i < strlen(s); i++) {
            if (!isdigit(s[i]) && !(s[i] == '.'))
                return 0;
        }
        return 1;
    }
    return 0;
}

//Returns 1 if string is a charLiteral '{char}', 0 otherwise.
int checkChar(char *s) {
    
    //printf("string is %s\n", s);
    if ((s[0] ==  '\'') && (s[strlen(s)-1] == '\'')) {
        if( (s[1] == '\\') && (isalpha(s[2])) && (strlen(s) == 4) ) {
            return 1;
        } else if (strlen(s) == 3) {
            return 1;
        } else {
            return 0;
        }
    }
    return 0;
}


//Returns 1 if string is an id ( [char]* {char | digit}* ), 0 otherwise.
int checkId(char *s) {
    
    for (int i = 0; i < strlen(s); i++) {
        if (!isdigit(s[i]) && !isalpha(s[i]))
            return 0;
    }
    return 1;
}


//Prints out the tokens and their respective lexemes.
void reportTokensAndLexemes(char **tokens, char **lexemes, int count) {
    

    printf("%-15s %s\n", "Tokens", "Lexemes");
    printf("__________________________\n");
    for (int i = 0; i < count; i++) {
        printf("%-15s %s\n", tokens[i], lexemes[i]);
    }
}


void outputTokensAndLexemes(char **tokens, char **lexemes, char *filename, int count) {

    FILE *f = fopen(filename, "w");
    if (f == NULL) {
        printf("Error opening file\n");
        exit(1);
    }

    for (int i = 0; i < count; i++) {
        fprintf(f, "%-15s %s\n", tokens[i], lexemes[i]);
    }

    fclose(f);

    printf("tokens output to %s\n", filename);

}


//Does the brunt of the work. Reads the input file and pareses it into 
//tokens and lexemes. 
int main(int argc, char** argv) {
    
    //Holds the file name
    char *fileName, *outFile;

    //Used to identify tokens as a comment. 1 if currently a commnent, 0 if not. 
    int isComment = 0;
    
    //Initialize tokens and lexems data structures, and a counter for them.
    int count = 0;
    char **tokens, **lexemes;
    tokens = lexemes = NULL;
    tokens = (char**)malloc(NUM_TOK * sizeof(char*));
    lexemes = (char**)malloc(NUM_TOK * sizeof(char*));
    for (int i = 0; i < NUM_TOK; i++) {
        tokens[i] = (char*)malloc(10 * sizeof(char));
        lexemes[i] = (char*)malloc(10 * sizeof(char));
    }
    
    //read number of points from user
    if (argc!=3) {
        printf("usage: tokenizer <CLite File Name> <output File Name\n");
        exit(1);
    }
    
    //Prepare to read in file
    fileName = argv[1];
    printf("You entered file: %s\n", fileName);
    
    outFile = argv[2];
    
    char mode1[] = "r";
    char *file1 = NULL;
    char *buff = NULL;
    char ch;
    file1 = (char*)malloc(100 * sizeof(char));
    buff = (char*)malloc(100 * sizeof(char));
    
    getcwd(file1);
    strcat(file1, "/");
    strcat(file1, fileName);
    FILE *file_ptr1;
    if ( (file_ptr1 = fopen(file1, mode1)) == NULL) {
        printf("Error opening file\n");
        exit(1);
    }
    
    //Increments through the file using whitespaces as the delimiter, ending when it hits the end of the file. 
    //Also scans the trailing character into ch, used to look for end of line characters. 
    while (fscanf(file_ptr1, "%s%c", buff, &ch)==2) {

        //printf("%s ", buff);
        char *temp = (char*)malloc(10 * sizeof(char));

        //Strip off the first character from the buffer string. 
        do {
            char *firstChar = (char*)malloc(10 * sizeof(char));
            strncpy(firstChar, buff, 1);
            buff++;
            
            //printf("first char is %s\n", firstChar);
            //First check if the char is a terminal symbol (;,(,),{,},[,]). 
            if (checkTerminal(firstChar)) {
                tokens[count] = firstChar;
                lexemes[count] = firstChar;
                count++;
            } else if (!isalpha(firstChar[0]) && !isdigit(firstChar[0]) && !(firstChar[0] == '.')) {
                strcat(temp, firstChar);
                //printf("temp is %s\n", temp);
                
                if ((strlen(buff) == 0) || (strlen(temp) > 1) || isalpha(buff[0]) || isdigit(buff[0])) {
                    if (isComment) {
                        strcpy(tokens[count], "comment");
                        strcpy(lexemes[count], temp);
                        temp[0] = '\0';
                        count++;
                    } else if (!strcmp(temp, "=")) {
                        strcpy(tokens[count], "assignOp");
                        strcpy(lexemes[count], temp);
                        temp[0] = '\0';
                        count++;
                    } else if (!strcmp(temp, "//")) {
                        strcpy(tokens[count], "comment");
                        strcpy(lexemes[count], temp);
                        temp[0] = '\0';
                        count++;
                        isComment = 1;
                    } else if (!strcmp(temp, "||")) {
                        strcpy(tokens[count], temp);
                        strcpy(lexemes[count], temp);
                        temp[0] = '\0';
                        count++;
                    } else if (!strcmp(temp, "&&")) {
                        strcpy(tokens[count], temp);
                        strcpy(lexemes[count], temp);
                        temp[0] = '\0';
                        count++;
                    } else if (checkChar(temp)) {
                        strcpy(tokens[count], "charLiteral");
                        strcpy(lexemes[count], temp);
                        temp[0] = '\0';
                        count++;
                    } else if (!strcmp(temp, "==") || !strcmp(temp, "!=")) {
                        strcpy(tokens[count], "equOp");
                        strcpy(lexemes[count], temp);
                        temp[0] = '\0';
                        count++;
                    } else if (!strcmp(temp, "+") || !strcmp(temp, "-")) {
                        strcpy(tokens[count], "addOp");
                        strcpy(lexemes[count], temp);
                        temp[0] = '\0';
                        count++;
                    } else if (!strcmp(temp, "*") || !strcmp(temp, "/") || !strcmp(temp, "%")) {
                        strcpy(tokens[count], "multOp");
                        strcpy(lexemes[count], temp);
                        temp[0] = '\0';
                        count++;
                    } else if (!strcmp(temp, "<") || !strcmp(temp, ">") || !strcmp(temp, "<=") || !strcmp(temp, ">=")) {
                        strcpy(tokens[count], "relOp");
                        strcpy(lexemes[count], temp);
                        temp[0] = '\0';
                        count++;
                    } else {
                        strcpy(tokens[count], "ImproperToken");
                        strcpy(lexemes[count], temp);
                        temp[0] = '\0';
                        count++;
                    }
                }
                
            } else {
                strcat(temp, firstChar);
                //printf("temp is %s\n", temp);
                
                if ((!isalpha(buff[0]) && !isdigit(buff[0])) && !(buff[0] == '\'') && !(buff[0] == '.')) {
                    
                    if (isComment) {
                        strcpy(tokens[count], "comment");
                        strcpy(lexemes[count], temp);
                        temp[0] = '\0';
                        count++;
                    } else if (checkFloat(temp)) {
                        strcpy(tokens[count], "floatLiteral");
                        strcpy(lexemes[count], temp);
                        temp[0] = '\0';
                        count++;
                    } else if (checkDigit(temp)) {
                        strcpy(tokens[count], "intLiteral");
                        strcpy(lexemes[count], temp);
                        temp[0] = '\0';
                        count++;
                    } else if (!strcmp(temp, "main") || !strcmp(temp, "if") || !strcmp(temp, "else") || !strcmp(temp, "while") || !strcmp(temp, "return") || !strcmp(temp, "print") ) {
                        strcpy(tokens[count], temp);
                        strcpy(lexemes[count], temp);
                        temp[0] = '\0';
                        count++;
                    } else if (!strcmp(temp, "int") || !strcmp(temp, "float") || !strcmp(temp, "char") || !strcmp(temp, "bool")) {
                        strcpy(tokens[count], "type");
                        strcpy(lexemes[count], temp);
                        temp[0] = '\0';
                        count++;
                    } else if (!strcmp(temp, "true") || !strcmp(temp, "false")) {
                        strcpy(tokens[count], "boolLiteral");
                        strcpy(lexemes[count], temp);
                        temp[0] = '\0';
                        count++;
                    } else if (checkId(temp)){
                        strcpy(tokens[count], "id");
                        strcpy(lexemes[count], temp);
                        temp[0] = '\0';
                        count++;
                    } else {
                        strcpy(tokens[count], "ImproperToken");
                        strcpy(lexemes[count], temp);
                        temp[0] = '\0';
                        count++;
                    }
                }
            }
        } while (strlen(buff) > 0);

        if (ch == '\n') 
            isComment = 0;
    }
    reportTokensAndLexemes(tokens, lexemes, count);
    outputTokensAndLexemes(tokens, lexemes, outFile, count);
}




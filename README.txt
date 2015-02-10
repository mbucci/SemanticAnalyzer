Semantic Analyzer README
author: Max Bucci
date created: 9/22/14
last modified: 10/29/14

How to Run:

	from the Analyzer directory:
		Start Python idle process. 
		run the main() function from idle and give input values when prompted. 

Input:
			
	The user is given the option to compile and run the tokenizer program with a cLite file 
	provided by them. Tokens are written into a file, the name of which is also given by the user.

	The user must provide a file name which contains the tokens they wish to analyze. 

	The user must then choose if they want the file to be analyzed as an assignment
	or as a program

Output:

	If the file was semantically and syntactically correct, the value of print statements
	in the file (if any) will be output. 
	
	If either semantically or syntactically incorrect, an error message will be output
	indicating the specifics of the error. 
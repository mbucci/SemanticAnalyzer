#
#Python Syntactic Analyzer
#Created 10/1/14
#Author Max Bucci
#
# Recursive-Descent (RD) Syntactic analyzer and parser for Clite syntax. Checks for syntactic correctness of
# a complete Clite syntax including declarations, and if/else, while, print, and return statements. 
# Literals include: int, float, bool and char. 
# Operations include: ||, &&, ==, !=, <, <=, >, >=, *, /, %, +, - 
#
# #Input: text file of tokens and lexemes to be tested.
# #Output: Statement of whether the tokens were syntactically correct or not 
#

import sys
import os

def main():
	global tokenStream, lexemeStream

	tokenStream = []
	lexemeStream = []
	iNextToken = 0

	#Gives the user the option to Compile and run the tokenizer program with a cLite file 
	#they provide. Tokens are written into a file, the name of which is also provided by user.
	print "Would you like to tokenize a cLite file first? (y/n):",
	answer = raw_input().lower()
	if (answer == "y"):
		print "Enter cLite file:",
		cFile = raw_input()
		print "Enter output filename:",
		outFile = raw_input()
		termCmd = "./tokenizer " + cFile + " " + outFile
		os.system("make")
		os.system(termCmd)
	elif (answer != "n"):
		print "Incorrect response"
		sys.exit()
	
	#Get tokens file from user input
	print "Enter filename with tokens:",
	file = raw_input()
	f = open(file, "r")

	#Reads tokens and lexemes into respective arrays. 
	for line in f:
		#Split lines by white space. Tokens are first element, Lexemes are last. 
		#Add to respective arrays.
		if (line.split(' ')[0] != "comment"):  #Ignore comments
			tokenStream.append(line.split(' ')[0])   
			lexemeStream.append((line.split(' ')[-1]).rstrip())   #Strip of end-of-line characters. 
	f.close()
	
	#print "Tokens:", "\n\n", tokenStream, "\n"
	#print "Lexemes:", "\n\n", lexemeStream, "\n"

	#Beginning of recursive descent, start with start symbol 
	#Option to analyze a program on an assignment 
	print "Would you like to analyze <", file, "> as a program or an assignment? (p/a):",
	answer = raw_input().lower()
	if (answer == "a"):
		iNextToken = assignment(iNextToken)    #Assignment Part 1
	elif (answer == "p"):
		iNextToken = program(iNextToken)       #Assignment Part 2
	else:
		print "Incorrect response"
		sys.exit()

	#Check if we didn't make it all the way through 
	if (iNextToken < len(tokenStream)):    
		error(iNextToken)
	#All Good!
	else:
		print "===Valid Expression==="


def checkTokens(iNextToken, *tokens):
	#For a given next token and list of tokens, checks if the tokenStream contains the tokens in the 
	#order passed to the function call. Note: order of tokens is critical. 

	for token in tokens:
		if (iNextToken < len(tokenStream) and tokenStream[iNextToken] == token):
			iNextToken += 1
		else:
			error(iNextToken)

	return iNextToken


def program(iNextToken):
	#First check in RD, checks basic program syntax. type main () { Declarations Statements }

	iNextToken = checkTokens(iNextToken, "type", "main", "(", ")", "{")
	iNextToken = declarations(iNextToken)
	iNextToken = statements(iNextToken)
	iNextToken = checkTokens(iNextToken, "}")

	return iNextToken


def declarations(iNextToken):
	#Second check in RD, looks for declarations 

	while (iNextToken < len(tokenStream) and tokenStream[iNextToken] == "type"):
		iNextToken = declaration(iNextToken)

	return iNextToken

def declaration(iNextToken):
	#Declarations have form: type id {, id} ;

	iNextToken = checkTokens(iNextToken, "type", "id")

	while (iNextToken < len(tokenStream) and tokenStream[iNextToken] == ","):
		iNextToken += 1
		iNextToken = checkTokens(iNextToken, "id")

	iNextToken = checkTokens(iNextToken, ";")

	return iNextToken


def statements(iNextToken):
	#Third check in RD, looks for statements 

	while (iNextToken < len(tokenStream) and (tokenStream[iNextToken] == "if" or tokenStream[iNextToken] == "print" \
			or tokenStream[iNextToken] == "while" or tokenStream[iNextToken] == "return" or tokenStream[iNextToken] == "id")):
		iNextToken = statement(iNextToken)
	return iNextToken


def statement(iNextToken):
	#Statements have form: Assignment | IfStmt | PrintStmt | WhileStmt | ReturnStmt

	if (tokenStream[iNextToken] == "if"):
		iNextToken = ifStmt(iNextToken)
	elif (tokenStream[iNextToken] == "print"):
		iNextToken = printStmt(iNextToken)
	elif (tokenStream[iNextToken] == "while"):
		iNextToken = whileStmt(iNextToken)
	elif (tokenStream[iNextToken] == "return"):
		iNextToken = returnStmt(iNextToken)
	elif (tokenStream[iNextToken] == "id"):
		iNextToken = assignment(iNextToken)
	else:
		error(iNextToken)

	return iNextToken


def printStmt(iNextToken):
	#PrintStmt has form: print Expression ;

	iNextToken = checkTokens(iNextToken, "print")
	iNextToken = expression(iNextToken)
	iNextToken = checkTokens(iNextToken, ";")
	
	return iNextToken


def ifStmt(iNextToken):
	#IfStmt has form: if ( Expression ) { Statement }  [ else { Statement } ]

	iNextToken = checkTokens(iNextToken, "if", "(")
	iNextToken = expression(iNextToken)
	iNextToken = checkTokens(iNextToken, ")", "{")
	iNextToken = statements(iNextToken)
	iNextToken = checkTokens(iNextToken, "}")

	#Option for else statement. Not an issue if it's not there 
	if (tokenStream[iNextToken] == "else"):
		iNextToken += 1
		iNextToken = checkTokens(iNextToken, "{")
		iNextToken = statement(iNextToken)
		iNextToken = checkTokens(iNextToken, "{")

	return iNextToken


def whileStmt(iNextToken):
	#WhileStmt has form: while ( Expression ) { Statement }

	iNextToken = checkTokens(iNextToken, "while", "(")
	iNextToken = expression(iNextToken)
	iNextToken = checkTokens(iNextToken, ")", "{")
	iNextToken = statement(iNextToken)
	iNextToken = checkTokens(iNextToken, "}")

	return iNextToken


def returnStmt(iNextToken):
	#ReturnStmt has form: return Expression ;

	iNextToken = checkTokens(iNextToken, "return")
	if (iNextToken < len(tokenStream) and tokenStream[iNextToken] == ";"):
		iNextToken += 1
		return iNextToken
	else:
		iNextToken = expression(iNextToken)
		iNextToken = checkTokens(iNextToken, ";")

	return iNextToken


def assignment(iNextToken):
	#Assignment has form: id assignOp Expression ;

	iNextToken = checkTokens(iNextToken, "id", "assignOp")
	iNextToken = expression(iNextToken)
	iNextToken = checkTokens(iNextToken, ";")

	return iNextToken


def expression(iNextToken):
	#Expression has form: Conjunction { || Conjunction }

	iNextToken = conjunction(iNextToken)

	#Iteration for multiple Conjunctions 
	while iNextToken < len(tokenStream) and (tokenStream[iNextToken] == "||"):
		iNextToken += 1 
		iNextToken = conjunction(iNextToken)

	return iNextToken 


def conjunction(iNextToken):
	#Conjuction has form: Equality { && Equality }

	iNextToken = equality(iNextToken)

	#Iteration for multiple Equality's
	while iNextToken < len(tokenStream) and (tokenStream[iNextToken] == "&&"):
		iNextToken += 1 
		iNextToken = equality(iNextToken)

	return iNextToken


def equality(iNextToken):
	#Equality has form: Relation [ equOp Relation ]

	iNextToken = relation(iNextToken)

	#Option for additional Relation		
	if iNextToken < len(tokenStream) and (tokenStream[iNextToken] == "equOp"):
		iNextToken += 1 
		iNextToken = relation(iNextToken)

	return iNextToken


def relation(iNextToken):
	#Relation has form: Addition [ relOp Addition ]

	iNextToken = addition(iNextToken)

	#Option for additional Addition
	while iNextToken < len(tokenStream) and (tokenStream[iNextToken] == "relOp"):
		iNextToken += 1 
		iNextToken = addition(iNextToken)

	return iNextToken


def addition(iNextToken):
	#Addition has form: Term { addOp Term }

	iNextToken = term(iNextToken)

	#Iteration for multiple Terms
	while iNextToken < len(tokenStream) and (tokenStream[iNextToken] == "addOp"):
		iNextToken += 1 
		iNextToken = term(iNextToken)

	return iNextToken


def term(iNextToken):
	#Term has form: Factor { multOp Factor }

	iNextToken = factor(iNextToken)

	#Iteration for multiple Factors 
	while iNextToken < len(tokenStream) and (tokenStream[iNextToken] == "multOp"):
		iNextToken += 1 
		iNextToken = factor(iNextToken)

	return iNextToken


def factor(iNextToken):
	#Factor has form: id | intLiteral | boolLiteral | floatLiteral | ( Expression ) | charLiteral 

	parenPresent = False

	if (tokenStream[iNextToken] == "("):     #Check for leading parenthese, if so then look for expression 
		parenPresent = True					 #Make sure to note that there was a leading parenthese
		iNextToken += 1
		iNextToken = expression(iNextToken)

	if (tokenStream[iNextToken] == "intLiteral" or tokenStream[iNextToken] == "boolLiteral" or \
			tokenStream[iNextToken] == "floatLiteral" or tokenStream[iNextToken] == "id" or \
			tokenStream[iNextToken] == "charLiteral"):
		iNextToken += 1
	elif (parenPresent and tokenStream[iNextToken] == ")"):   #If there was a leading paren. look for trailing paren. 
		iNextToken += 1
		parenPresent = False
	else:
		error(iNextToken)     #If none of the above, then error. 

	return iNextToken


def error(iNextToken):
	#Prints an error if something went wrong along the way. 

	if (iNextToken < len(tokenStream)):     #Made it through RD, but not completely
		print "===Error: Invalid expression at <", tokenStream[iNextToken], ",", lexemeStream[iNextToken], ">==="
	else:                                   #Didn't make it through RD 
		print "===Error: Missing terms==="

	sys.exit()


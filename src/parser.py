import sys, os
#from subprocess import Popen, PIPE

from ply import yacc,lex

from tokens import *
from rules import *
from semantic import *
from interpreter import *
#from codegen.builder import *

def get_input(file=False):
	if file:
		f = open(file,"r")
		data = f.read()
		f.close()
	else:
		data = ""
		while True:
			try:
				data += raw_input() + "\n"
			except:
				break
	return data

def main(options={},filename=False):
	logger = yacc.NullLogger()
	yacc.yacc(debug = logger, errorlog= logger )
	
	data = get_input(filename)
	ast =  yacc.parse(data,lexer = lex.lex(nowarn=1))	
	
	if options.graph:
		from codegen.graph import graph
		graph(ast, filename)

	print(ast)
	return ast
 
if __name__ == '__main__':
	main()
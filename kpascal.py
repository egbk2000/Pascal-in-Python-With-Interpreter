#!/usr/bin/env python

from optparse import OptionParser

from src.parser import main

from src.semantic import *
from src.interpreter import interpreter
import operator

parser = OptionParser()
parser.add_option("-o", "--out", dest="filename", default=False,
                  help="write output to <filename>", metavar="<filename>")
parser.add_option("-e", "--emit",
                  action="store_true", dest="verbose", default=False,
                  help="prints the bytecode to the screen")

parser.add_option("-g", "--graph",
                  action="store_true", dest="graph", default=False,
                  help="shows the AST graph")


parser.add_option("-i", "--instant",
                  action="store_true", dest="run", default=False,
                  help="runs the result instead of saving")

(options, args) = parser.parse_args()


if not options.filename:
	if len(args) > 0:
		options.filename = args[0].replace(".p",".out")
	else:
		options.filename = "a.out"
		
if len(args) > 0:
	f = args[0]
else:
	f = False

toplevel_env = [["+", operator.add], 
                 ["-", operator.sub],
                 ["*", operator.mul],
                 ["/", operator.div],
                 ["=", lambda a,b: 1 if a == b else 0]]

ast = main(options,"tests/addition.p")
#checked = check(ast)
results = interpreter(ast)
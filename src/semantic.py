
types = ['integer','real','char','string','boolean','void']

class Any(object):
	def __eq__(self,o):
		return True
	def __ne__(self,o):
		return False

class Context(object):
	def __init__(self,name=None):
		self.variables = {}
		self.var_count = {}
		self.name = name
	
	def has_var(self,name):
		return name in self.variables
	
	def get_var(self,name): #make a version that returns type and value
		return self.variables[name][0]
		#return self.values[name]

	def get_value(self,name): 
		return self.variables[name][1]
	
	def set_var(self,name,typ,val):
		self.variables[name] = typ, val #have a variable be bound to both a type and a value
		self.var_count[name] = 0
		#self.values[name]
	def assign_var(self,name,typ,varvalue):
		self.variables[name] = typ,varvalue

contexts = []
functions = {
	'write':('void',[
			("a",Any())
		]),
	'writeln':('void',[
			("a",Any())
		]),
	'writeint':('void',[
			("a",'integer')
		]),
	'writereal':('void',[
			("a",'real')
		]),
	'writelnint':('void',[
			("a",'integer')
		]),
	'writelnreal':('void',[
			("a",'real')
		])
}

def pop():
	count = contexts[-1].var_count
	for v in count:
		if count[v] == 0:
			print "Warning: variable %s was declared, but not used." % v
	contexts.pop()

def check_if_function(var):
	if var.lower() in functions and not is_function_name(var.lower()):
		raise Exception, "A function called %s already exists" % var
		
def is_function_name(var):
	for i in contexts[::-1]:
		if i.name == var:
			return True
	return False
		
def has_var(varn):
	var = varn.lower()
	check_if_function(var)
	for c in contexts[::-1]:
		if c.has_var(var):
			return True
	return False

def get_var(varn):
	var = varn.lower()
	for c in contexts[::-1]:
		if c.has_var(var):
			c.var_count[var] += 1
			return c.get_var(var)
	raise Exception, "Variable %s is referenced before assignment" % var

def get_value(varn):
	var = varn.lower()
	for c in contexts[::-1]:
		if c.has_var(var):
			c.var_count[var] += 1
			return c.get_value(var)
	raise Exception, "Variable %s is referenced before assignment" % var
	
def set_var(varn,typ,val):
	var = varn.lower()
	check_if_function(var)
	now = contexts[-1]
	now.set_var(var,typ.lower(),val)
	print("contexts - set new varible")
	for i in contexts:
		print(i.variables)
		
def flatten(n):
	if not is_node(n): return [n]
	if not n.type.endswith("_list"):
		return [n]
	else:
		l = []
		for i in n.args:
			l.extend(flatten(i))
		return l

def is_node(n):
	return hasattr(n,"type")

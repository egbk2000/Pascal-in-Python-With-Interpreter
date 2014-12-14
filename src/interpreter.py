from src.semantic import *

def get_params(node):
    if node.type == "parameter":
        return [interpreter(node.args[0])]
    else:
        l = []
        for i in node.args:
            l.extend(get_params(i))
        return l

def interpreter(node):
    #if it is not a node
    if not is_node(node):
        #check to see if it is a list of nodes and cycle through them
        if hasattr(node,"__iter__") and type(node) != type(""):
            for i in node:
                interpreter(i)
        else:
            return node

    elif node.type in ['identifier']:
        return node.args[0]
        
    elif node.type in ['var_list','statement_list','function_list']:
        return interpreter(node.args)
        
    elif node.type in ["program","block"]:
        contexts.append(Context())
        map(interpreter, node.args)
        pop()
    
    elif node.type == "var":
        var_name = node.args[0].args[0]
        var_type = node.args[1].args[0]
        #set the variable, default value is 0
        set_var(var_name, var_type, 0)
    
    elif node.type in ['function','procedure']:
        head = node.args[0]
        name = head.args[0].args[0].lower()
        check_if_function(name)
        
        if len(head.args) == 1:
            args = []
        else:
            args = flatten(head.args[1])
            args = map(lambda x: (x.args[0].args[0],x.args[1].args[0]), args)
        
        if node.type == 'procedure':
            rettype = 'void'
        else:
            rettype = head.args[-1].args[0].lower()

        functions[name] = (rettype,args)
        contexts.append(Context(name))
        
        interpreter(node.args[1])
        pop()

    elif node.type in ["function_call","function_call_inline"]:
        fname = node.args[0].args[0].lower()
        if fname not in functions:
            raise Exception, "Function %s is not defined" % fname
        if len(node.args) > 1:
            args = get_params(node.args[1])
        else:
            args = []
        rettype,vargs = functions[fname]
        
        if len(args) != len(vargs):
            raise Exception, "Function %s is expecting %d parameters and got %d" % (fname, len(vargs), len(args))
        else:
            for i in range(len(vargs)):
                if vargs[i][1] != args[i]:
                    raise Exception, "Parameter #%d passed to function %s should be of type %s and not %s" % (i+1,fname,vargs[i][1],args[i])
        
        #if the function called was writeln, print the arguments
        if fname == "writeln":
            args = get_params(node.args[1])
            for element in args:
                print(element)

        return rettype
    
    elif node.type == "assign":
        varn = interpreter(node.args[0]).lower()
        if is_function_name(varn):
            vartype = functions[varn][0]
        else:
            if not has_var(varn):
                raise Exception, "Variable %s not declared" % varn
            vartype = get_var(varn)
        newval = interpreter(node.args[1])
        #assign the new value to the variable
        if vartype == 'integer':
            set_var(varn, vartype, int(newval))
        else:
            set_var(varn, vartype, newval)
    
    elif node.type == 'and_or':
        op = node.args[0].args[0]
        for i in range(1,2):
            a = interpreter(node.args[i])
            if a != "boolean":
                raise Exception, "%s requires a boolean. Got %s instead." % (op,a)
    
    elif node.type == "op":
        op = node.args[0].args[0]
        vt1 = interpreter(node.args[1])
        vt2 = interpreter(node.args[2])

        #if the arguments are ints convert from strings to ints
        if node.args[1].args[0].type == "integer":
            vt1 = int(vt1)

        if node.args[2].args[0].type == "integer":
            vt2 = int(vt2)

        if op == '+':
            result = vt1 + vt2
            return result
        elif op == '-':
            result = vt1 - vt2
            return result
        elif op == '/' or op == 'div':
            result = vt1 / vt2
            return result
        elif op == '*':
            result = vt1 * vt2
            return result
        elif op == 'mod':
            result = vt1 % vt2
            return result
        elif op == '=':
            if vt1 == vt2:
                return True
            else:
                return False
        elif op == '<=':
            if vt1 <= vt2:
                return True
            else:
                return False
        elif op == '>=':
            if vt1 >= vt2:
                return True
            else:
                return False
        elif op == '>':
            if vt1 > vt2:
                return True
            else:
                return False
        elif op == '<':
            if vt1 < vt2:
                return True
            else:
                return False
        elif op == '<>':
            if vt1 != vt2:
                return True
            else:
                return False
    
    elif node.type in ['if']:
        test = interpreter(node.args[0])
        if test == True:
            # check body
            interpreter(node.args[1])
        elif len(node.args) > 2:
            #check else
            interpreter(node.args[2])
    
    elif node.type in ['while','repeat']:
        if node.type == 'repeat':
            c = 1
            switch = False
        else:
            c = 0
            switch = True

        test = interpreter(node.args[c])
        while test == switch:
            interpreter(node.args[1-c])
            test = interpreter(node.args[c])
    
    elif node.type == 'for':
        #contexts.append(Context())
        v = node.args[0].args[0].args[0].lower()
        #assign initial value to v
        interpreter(node.args[0])
        #retrieve initial value
        initialValue = contexts[1].variables[v][1]
        #retrieve ending value
        endValue = int(interpreter(node.args[2].args[0].args[0]))
        
        st = node.args[0].args[1].args[0].type.lower()
        if st != 'integer':
            raise Exception, 'For requires a integer as a starting value'
        
        fv = node.args[2].args[0].type.lower()
        if fv != 'integer':
            raise Exception, 'For requires a integer as a final value'
        
        while initialValue != endValue:
            interpreter(node.args[3])
            initialValue = initialValue + 1
   
    elif node.type == 'not':
        result = interpreter(node.args[0])
        result = (int(result) + 1) * -1 
        return result
    
    elif node.type == "element":
        if node.args[0].type == 'identifier':
            #returns value of the identifier
            return get_value(node.args[0].args[0])
            #return get_var(node.args[0].args[0]) #returns the type of the identifier
        elif node.args[0].type == 'function_call_inline':
            return interpreter(node.args[0])
        else:
            if node.args[0].type in types:
                return node.args[0].args[0]
            else:
                return interpreter(node.args[0])

    else:
        print "semantic missing:", node.type
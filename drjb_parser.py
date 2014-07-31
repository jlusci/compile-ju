import sys
import copy
import PLYex
from PLYex import tokenlist as tokens
import ply.lex as lex

# tokens = []

mathop_list = ['<','>','==','<=','>=','!=']

global_ENV = {}

class Env(dict):
    def __init__(self, parms=(), args=(), outer=None):
        self.update(zip(parms, args))
        self.outer = outer
    def find(self, var):
        "Find the innermost Env where var appears."
        return self if var in self else self.outer.find(var)

class NodeTemplate(object):
    pass

class ProgramNode(NodeTemplate):
    def __init__(self, functions):
        self.functions = functions

    def emit(self):
        for function in self.functions:
            function.emit()

    def eval(self, env):
        for fn in self.functions:
            # fn.eval(env)
            if fn.name == "main":
                fn.eval(env)

class FunctionNode(NodeTemplate):
    def __init__(self, name, params, body):
        self.name = name
        self.params = params
        self.body = body

    def emit(self):
        print "def", self.name+"():"
        self.body.emit()

    def eval(self, env):
        self.params.eval(env)        
        self.body.eval(env)

class ParamsNode(NodeTemplate):
    def __init__(self, params):
        self.params = params

    def emit(self):
        pass

    def eval(self, env):
        for param in self.params:
            # print "parameter in function definition:", param.name
            # print "*****", param.eval(env)
            param.eval(env)

class BlockNode(NodeTemplate):
    def __init__(self, lines):
        self.lines = lines

    def emit(self):
        for line in self.lines:
            line.emit()

    def eval(self, env):
        for line in self.lines:
            line.eval(env)

class CallNode(NodeTemplate):
    def __init__(self, fn, args):
        self.fn = fn
        self.args = args

    def eval(self, env):
        paramlist = []
        arglist = []
        fn_call = global_ENV[self.fn.name]
        params = fn_call.params
        # print params.params
        for param in params.params:
            paramlist.append(param.name)
        for arg in self.args:
            arglist.append(arg.name)
        new_env = Env(paramlist, arglist, env)        
        fn_call.eval(new_env)
        # copy.deepcopy(global_ENV)

class IndexNode(NodeTemplate):
    def __init__(self, var, val):
        self.var = var
        self.val = val

    def eval(self, env):
        look_up = env[self.var.name]
        target = look_up[self.val.list_of_objects[0].eval(env)]
        return target

class AssignNode(NodeTemplate):
    def __init__(self, first, second):
        self.first = first
        self.second = second
        
    def emit(self):
        print "    ",self.first.name, "=", self.second

    def eval(self, env):
        env[self.first.name] = self.second.eval(env)

class OpNode(NodeTemplate):
    def __init__(self, op, first, second):
        self.op = op
        self.first = first
        self.second = second

    def emit(self):
        print "    ",self.first, self.op, self.second

    def eval(self, env):
        if self.op == "+":
            return self.first.eval(env) + self.second.eval(env)
        if self.op == "-":
            return self.first.eval(env) - self.second.eval(env)
        if self.op == "*":
            return self.first.eval(env) * self.second.eval(env)
        if self.op == "/":
            return self.first.eval(env) / self.second.eval(env)
        if self.op == "%":
            return self.first.eval(env) % self.second.eval(env)
        if self.op == "<":
            if self.first.eval(env) < self.second.eval(env):
                return True
            else:
                return False
        if self.op == ">":
            if self.first.eval(env) > self.second.eval(env):
                return True
            else:
                return False
        if self.op == ">=":
            if self.first.eval(env) >= self.second.eval(env):
                return True
            else:
                return False
        if self.op == "<=":
            if self.first.eval(env) <= self.second.eval(env):
                return True
            else:
                return False
        if self.op == "==":
            if self.first.eval(env) == self.second.eval(env):
                return True
            else:
                return False
        if self.op == "!=":
            if self.first.eval(env) != self.second.eval(env):
                return True
            else:
                return False

class IfNode(NodeTemplate):
    def __init__(self, first, second, third):
        self.first = first
        self.second = second
        self.third = third

    def emit(self):
        print "     if", self.first.first, self.first.op, self.first.second,":"
        print "        ", 
        # for item in self.second:
        #     print item.first, "=", item.second.first,item.second.op,item.second.second

    def eval(self, env):
        result = self.first.eval(env)
        if result:
            return self.second.eval(env)
        else:
            if self.third:                      #if there is no else statement
                return self.third.eval(env)
            else:
                return None

class ForNode(NodeTemplate):
    def __init__(self, first, second, third, block):
        self.first = first
        self.second = second
        self.third = third
        self.block = block

    def emit(self):
        pass

    def eval(self, env):
        self.first.eval(env)
        while self.second.eval(env):
            self.block.eval(env)
            self.third.eval(env)

class WhileNode(NodeTemplate):
    def __init__(self, cond, block):
        self.cond = cond
        self.block = block

    def emit(self):
        pass

    def eval(self,env):
        while self.cond.eval(env):
            self.block.eval(env)

class PrintNode(NodeTemplate):
    def __init__(self, lines):
        self.lines = lines

    def emit(self, env):
        for line in self.lines:
            print "print", line.eval(env)

    def eval(self, env):
        if len(self.lines) == 1:
            print self.lines[0].eval(env)
        else:
            for item in range(len(self.lines)-1):
                print self.lines[item].eval(env),
            print self.lines[-1].eval(env)          #beth fixed this

class StringNode(NodeTemplate):
    def __init__(self, val):
        self.val = val 

    def eval(self, env):
        return self.val

class IntNode(NodeTemplate):
    def __init__(self, name):
        self.name = name

    def eval(self, env):
        return self.name

class FloatNode(NodeTemplate):
    def __init__(self, val):
        self.val = val

    def eval(self, env):
        return self.val

class IDNode(NodeTemplate):
    def __init__(self, name):
        self.name = name

    def eval(self, env):
        return env.get(self.name)

class ListNode(NodeTemplate):
    def __init__(self, list_of_objects):
        self.list_of_objects = list_of_objects 

    def eval(self, env):
        contents = []
        for item in self.list_of_objects:
            contents.append(item.eval(env))
        return contents

class DictNode(NodeTemplate):
    def __init__(self, vals):
        self.vals = vals

    def eval(self, env):
        dictcontents = {}
        for key in self.vals.keys():
            dictcontents[key.eval(env)] = self.vals.get(key).eval(env)
        return dictcontents

def expect(thing_to_expect):
    token = tokens.pop(0)
    if token.value != thing_to_expect:
        raise Exception("Wrong token! Expected: ", thing_to_expect, "and got: ", 
            token.value, "on line:", token.lineno, ", position:", token.lexpos)
    return token

def parse_program():
    functions = []
    while tokens:
        if tokens[0].value == 'function':
            tokens.pop(0)
            fn = parse_function()
            functions.append(fn)
    pgm = ProgramNode(functions)
    return pgm
            
def parse_function():
    name = parse_id().name
    # print "OUR FUNCTION IS CALLED:", name
    params = parse_params()
    body = parse_block()

    fn_obj = FunctionNode(name,params,body)
    global_ENV[name] = fn_obj
    return fn_obj

def parse_id():
    name = tokens.pop(0)
    id_ = IDNode(name.value)
    return id_

def parse_params():
    paramslist = []
    expect("(")
    while tokens[0].value != ")":
        if tokens[0].value == ",":
            tokens.pop(0)
        paramslist.append(parse_id())
    expect(")")
    expect("{")
    params_obj = ParamsNode(paramslist)
    return params_obj

def parse_block():
    lines = []
    while tokens[0].value != "}":
        lines.append(parse_statement())
    expect("}")
    block_obj = BlockNode(lines)
    return block_obj 

def parse_statement():
    if tokens[0].value == "var":
        return parse_variable_def()
    elif tokens[0].value == "while":
        return parse_while()
    elif tokens[0].value == "for":
        return parse_for()
    elif tokens[0].value == "if":
        return parse_if()
    elif tokens[0].value == "print":
        return parse_print()
    elif tokens[0].type == "ID" and tokens[1].value == "=":#tokens[1].value != "(" and tokens[1].value != "[":
        x = parse_var_assign()
        expect(";")
        return x
    elif tokens[0].type == "NUMBER" or tokens[0].type == "FLOAT":# and tokens[1].value == "[":
        # print global_ENV.find(tokens[0].value)[tokens[0].value]
        x = parse_expression()
        expect(";")
        return x
    elif tokens[0].type == "ID":
        x = parse_expression()
        expect(";")
        return x        
    # else:
    #     token = tokens[0].value
    #     # token = token[:-2]
    #     if token in global_ENV.keys():
    #         x = parse_expression()
    #         expect(";")
    #         return x
    #     else:
    #         x = parse_expression()
    #         expect(";")
    #         return x
    else:
        raise Exception("WTF ", tokens[0].value, "IS NOT A KEYWORD. Error on line:",
            tokens[0].lineno)

def parse_args():
    argslist = []
    tokens.pop(0)
    while tokens[0].value != ")":
        if tokens[0].value == ",":
            tokens.pop(0)
        arg = parse_expression()
        argslist.append(arg)
    expect(")")
    return argslist

def parse_variable_def():
    expect("var")
    var_name = parse_id()
    expect("=")
    val = parse_expression()    
    expect(";")
    assign_obj = AssignNode(var_name,val)
    return assign_obj

# EXPR : FACTOR { ('+' | '-') EXPR } ;
# FACTOR : INT | '(' EXPR ')' ;

# EXPR : TERM { ('<' | '>' | '<=' | '>=' | '!=' | '=!') EXPR } ;
# TERM : MULT { ('+' | '-') TERM } ;
# MULT : FACTOR { ('*' | '/' | '%') MULT };
# FACTOR : INT | ID | '(' EXPR ')' ;

# EXPR : TERM { ('<' | '>' | '<=' | '>=' | '!=' | '=!') EXPR } ;
# TERM : MULT { ('+' | '-') TERM } ;
# MULT : FUNC { ('*' | '/' | '%') MULT };
# CALL : FACTOR { ('*' | '/' | '%') CALL };
# FACTOR : INT | ID | '(' EXPR ')' ;

def parse_expression():
    if tokens[0].value == "[":
        return parse_list()
    elif tokens[0].value == "{":
        return parse_dict()
    elif tokens[0].type == "STRING":
        token = tokens.pop(0)
        return StringNode(token.value)

    x = parse_term()
    if tokens[0].value in mathop_list:
        operator = tokens.pop(0)
        operator = operator.value
        y = parse_expression()
        
        op_obj = OpNode(operator,x,y)

        return op_obj

    return x

def parse_term():
    x = parse_mult()
    if tokens[0].value == '+' or tokens[0].value == '-':
        operator = tokens.pop(0)
        operator = operator.value
        y = parse_term()
        
        op_obj = OpNode(operator,x,y)

        return op_obj

    return x

def parse_mult():
    x = parse_call()
    # x = parse_factor()
    if tokens[0].value == '*' or tokens[0].value == '/' or tokens[0].value == '%':
        operator = tokens.pop(0)
        operator = operator.value
        y = parse_mult()
        
        op_obj = OpNode(operator,x,y)

        return op_obj

    return x

def parse_call():
    x = parse_factor()
    if tokens[0].value == '(':
        val = parse_args()
        fn_call_obj = CallNode(x, val)
        return fn_call_obj
    elif tokens[0].value == '[':
        val = parse_list()
        call_obj = IndexNode(x, val)
        return call_obj
    return x

def parse_factor():
    token = tokens[0]
    #token = atom(token)
    if token.type == "NUMBER": 
        tokens.pop(0)
        return IntNode(token.value)
    elif token.type == "FLOAT":
        tokens.pop(0)
        return FloatNode(token.value)
    elif token.type == "ID" and tokens[1].value == "(":
        fn_token = token.value
        tokens.pop(0)
        fn_obj = global_ENV[fn_token]
        return fn_obj
    elif token.type == "ID": # and tokens[1].value == "[":
        tokens.pop(0)
        return IDNode(token.value)
    expect("(")  
    expr = parse_expression()
    expect(")")
    return expr 

def parse_for():
    expect("for")
    expect("(")
    n1 = parse_variable_def()         #declare variable inside loop
    n2 = parse_expression()
    expect(";")
    n3 = parse_var_assign()
    expect(")")
    expect("{")
    block = parse_block()

    for_obj = ForNode(n1, n2, n3, block)
    # for_obj.emit()
    return for_obj

def parse_while():
    expect("while")
    expect("(")
    n1 = parse_expression()
    expect(")")
    expect("{")
    block = parse_block()

    while_obj = WhileNode(n1, block)
    # while_obj.emit()
    return while_obj

def parse_if():
    expect("if")
    expect("(")
    n1 = parse_expression()
    expect(")")
    expect("{")
    conseq = parse_block()
    alt = None
    if tokens[0].value == "else":
        expect("else")
        expect("{")
        alt = parse_block()

    if_obj = IfNode(n1, conseq, alt)
    return if_obj

def parse_print():
    printcontents = []
    expect("print")
    while tokens[0].value != ";":
        if tokens[0].value == ",":
            tokens.pop(0)
        val = parse_expression()
        printcontents.append(val)
    expect(";")
    print_obj = PrintNode(printcontents)
    return print_obj

def parse_var_assign():
    var_name = parse_id()
    expect("=")
    val = parse_expression()
    assign_obj = AssignNode(var_name, val)
    return assign_obj  

def parse_list():
    list_of_objects = []
    expect("[")
    while tokens[0].value != "]":
        if tokens[0].value == ",":
            tokens.pop(0)
        val = parse_expression()
        list_of_objects.append(val)
    expect("]")
    return ListNode(list_of_objects)

def parse_dict():
    dictcontents = {}
    expect("{")
    while tokens[0].value != "}":
        if tokens[0].value == ",": 
            tokens.pop(0)
        key = parse_expression()
        expect(":")
        value = parse_expression()
        dictcontents[key] = value
    expect("}")
    return DictNode(dictcontents)

# def parse_str():
#     # contents = []
#     # while tokens[0].value != ";":
#     #     token = tokens.pop(0)
#     #     token = token.value
#     #     contents.append(token)
 
#     # return " ".join(contents)
#     str_obj = StringNode()

# def atom(var):
#     try: return int(var)
#     except: return str(var)

def emit_all():
    for fn in global_ENV.keys():
        fn_obj = global_ENV[fn]
        fn_obj.emit()
        # fn_obj.body[1].second[0].eval()
        # for stmt in fn_obj.body:
        #     # print stmt.istype, stmt.first, stmt.second
        #     # stmt.emit_assign_expr()
        #     stmt.emit()
        #     stmt.eval()


def main():
    global tokens
    # f = open(sys.argv[1])
    # lines = f.read()
    # f.close()
    
    # print lines
    # tokens = lines.replace(';',' ; ').split()

    # for item in range(len(tokenlist)):
        # # appends ONLY list of values
        # tokens.append(tokenlist[item].value)

    print "HERE ARE MY TOKENS:", tokens         #check tokens list

    program = parse_program() 
    program.eval({})
    # program.eval(global_ENV)
    print global_ENV.keys()

if __name__ == "__main__":
    main()

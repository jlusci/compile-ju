import sys
import PLYex
from PLYex import tokenlist as tokens
import ply.lex as lex

# tokens = []

mathop_list = ['<','>','==','<=','>=','!=']

ENV = {}

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
    def __init__(self, name, args, body):
        self.name = name
        self.args = args
        self.body = body

    def emit(self):
        print "def", self.name+"():"
        self.body.emit()

    def eval(self, env):
        self.body.eval(env)

class BlockNode(NodeTemplate):
    def __init__(self, lines):
        self.lines = lines

    def emit(self):
        for line in self.lines:
            line.emit()

    def eval(self, env):
        for line in self.lines:
            line.eval(env)

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
    # def emit_ifnode(self):
        print "     if", self.first.first, self.first.op, self.first.second,":"
        print "        ", 
        # for item in self.second:
        #     print item.first, "=", item.second.first,item.second.op,item.second.second

    def eval(self, env):
        result = self.first.eval(env)
        if result:
            return self.second.eval(env)
        else:
            return self.third.eval(env)

class ForNode(NodeTemplate):
    def __init__(self, first, second, third, block):
        self.first = first
        self.second = second
        self.third = third
        self.block = block

    def emit(self):
        pass
        # print self.first.first.name, self.first.second.val
        # print self.second.first.name, self.second.op, self.second.second.val
        # print self.third.first, self.third.second.first.name, self.third.second.op, \
        # self.third.second.second.val
        # for line in self.block.lines:
        #     print "*****", line.first.name  #ID node has .name attribute

    def eval(self, env):
        self.first.eval(env)
        while self.second.eval(env):
            self.block.eval(env)
            self.third.eval(env)

class WhileNode(NodeTemplate):
    def __init__(self,cond,block):
        self.cond = cond
        self.block = block

    def emit(self):
        pass

    def eval(self,env):
        while self.cond.eval(env):
            self.block.eval(env)

class PrintNode(NodeTemplate):
    def __init__(self,first):
        self.first = first

    def emit(self):
        print "print", self.first

    def eval(self, env):
        print self.first.eval(env)

class StringNode(NodeTemplate):
    def __init__(self,val):
        self.val = val 

    def eval(self, env):
        return self.val

class IntNode(NodeTemplate):
    def __init__(self, val):
        self.val = val

    def eval(self, env):
        return self.val

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
    def __init__(self, val):
        self.val = val 

    def eval(self, env):
        return self.val

class DictNode(NodeTemplate):
    def __init__(self, val):
        self.val = val 

    def eval(self, env):
        return self.val

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
    print "OUR FUNCTION IS CALLED:", name
    args = parse_args()
    body = parse_block()

    # while tokens[0].value != "}":
    #     body.append(parse_statement())   #fn body is a list of dictionaries
    # expect("}")

    fn_obj = FunctionNode(name,args,body)

    # fn =  {"type": "function",
    #         "name": name,
    #         "args": args,
    #         "body": body}

    ENV[name] = fn_obj
    return fn_obj

def parse_id():
    name = tokens.pop(0)
    id_ = IDNode(name.value)
    return id_

def parse_args():
    expect("(")
        # maybe put something in here?
    expect(")")
    expect("{")
    return []

def parse_block():
    lines = []
    while tokens[0].value != "}":
        lines.append(parse_statement())
    expect("}")
    block = BlockNode(lines)
    return block 

def parse_statement():
    if tokens[0].value == "var":
        return parse_variable_def()
    elif tokens[0].value == "for":
        return parse_for()
    elif tokens[0].value == "if":
        return parse_if()
    elif tokens[0].value == "print":
        return parse_print()
    elif tokens[0].type == "ID" and tokens[1].value != "(":
        x = parse_var_assign()
        expect(";")
        return x
    else:
        token = tokens[0].value
        # token = token[:-2]
        if token in ENV.keys():
            token = tokens.pop(0)
            fn_token = token.value
            fn_obj = ENV[fn_token]
            expect("(")
            expect(")")
            expect(";")
            return fn_obj
            # print "THIS FUNCTION CALLS THE FUNCTION:", fn_token
            # return {"name": fn_token,
            #         "type": "function call"}
        raise Exception("WTF ", tokens[0].value, "IS NOT A KEYWORD. Error on line:",
            tokens[0].lineno)

def parse_variable_def():
    expect("var")
    var_name = parse_id()
    expect("=")
    # if tokens[0].value == "[":
    #     val = parse_list()
    # elif tokens[0].value == "{":
    #     val = parse_dict()    
    # else:
    val = parse_expression()    
    expect(";")
    assign_obj = AssignNode(var_name,val)
    # assign_obj.emit_expr()
    return assign_obj
    # return {"type": "assign_expr",
    #             "first": {"type": "id_expr",
    #                     "val": var_name},
    #             "second": {"type": "eval_expr",
    #                     "val": val}}

# EXPR : FACTOR { ('+' | '-') EXPR } ;
# FACTOR : INT | '(' EXPR ')' ;

# EXPR : TERM { ('<' | '>' | '<=' | '>=' | '!=' | '=!') EXPR } ;
# TERM : MULT { ('+' | '-') TERM } ;
# MULT : FACTOR { ('*' | '/' | '%') MULT };
# FACTOR : INT | ID | '(' EXPR ')' ;

def parse_expression():
    if tokens[0].type == "LAMBDA":
        pass
    elif tokens[0].value == "[":
        val = parse_list()
        return ListNode(val)
    elif tokens[0].value == "{":
        val = parse_dict()
        return DictNode(val)
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

        # return {"type": "op_expr",
        #         "val": operator,
        #         "first": {"type": "int_const_expr",
        #                 "val": x},
        #         "second": {"type": "int_const_expr",
        #                 "val": y}}
    return x

def parse_term():
    x = parse_mult()
    if tokens[0].value == '+' or tokens[0].value == '-':
        operator = tokens.pop(0)
        operator = operator.value
        y = parse_term()
        
        op_obj = OpNode(operator,x,y)

        return op_obj

        # return {"type": "op_expr",
        #         "val": operator,
        #         "first": {"type": "int_const_expr",
        #                 "val": x},
        #         "second": {"type": "int_const_expr",
        #                 "val": y}}
    return x

def parse_mult():
    x = parse_factor()
    if tokens[0].value == '*' or tokens[0].value == '/' or tokens[0].value == '%':
        operator = tokens.pop(0)
        operator = operator.value
        y = parse_mult()
        
        op_obj = OpNode(operator,x,y)

        return op_obj

        # return {"type": "op_expr",
        #         "val": operator,
        #         "first": {"type": "int_const_expr",
        #                 "val": x},
        #         "second": {"type": "int_const_expr",
        #                 "val": y}}
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
    elif token.type == "ID":
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

    for_obj = ForNode(n1,n2,n3,block)
    for_obj.emit()
    return for_obj
    # return {"type": "for",
    #         "first": n1,
    #         "second": n2,
    #         "third": n3,
    #         "block": block}

def parse_while():
    expect("while")
    expect("(")
    n1 = parse_expression()
    expect(")")
    expect("{")
    block = parse_block()

    while_obj = WhileNode(n1,block)
    while_obj.emit()
    return while_obj

def parse_if():
    # conseq = []
    # alt = []
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

    if_obj = IfNode(n1,conseq,alt)
    # print if_obj.first.first.first, if_obj.first.first.op, if_obj.first.first.second,\
    # if_obj.first.op, if_obj.first.second
    # print if_obj.second[0].first
    # print "***** HERE IS MY ELSE STATEMENT:",if_obj.third[0].first
    # print type(if_obj.third[0])
    # print if_obj.eval()
    return if_obj
    # return {"type": "if",
    #         "first": n1,
    #         "second": conseq,
    #         "third": alt}

def parse_print():
    expect("print")
    val = parse_expression()
    print_obj = PrintNode(val)
    expect(";")
    return print_obj

def parse_var_assign():
    var_name = parse_id()
    # var_name = tokens.pop(0)
    # var_name = var_name.value
    expect("=")
    val = parse_expression()
    # expect(";")
    assign_obj = AssignNode(var_name,val)
    return assign_obj
    # return {"type": "assign_expr",
    #             "first": {"type": "id_expr",
    #                     "val": var_name},
    #             "second": {"type": "eval_expr",
    #                     "val": val}}     

def parse_list():
    contents = []
    expect("[")
    while tokens[0].value != "]":
        if tokens[0].value == ',':
            tokens.pop(0)
        contents.append(tokens[0].value)  #don't need atom()
        tokens.pop(0)
    expect("]")
    return contents

def parse_dict():
    dictcontents = {}
    expect("{")
    while tokens[0].value != "}":
        if tokens[0].value == ",":
            tokens.pop(0)
        dictcontents[tokens[0].value] = tokens[2].value    #don't need atom()
        # tokens = tokens[3:]
        tokens.pop(0)
        tokens.pop(0)
        tokens.pop(0)
    expect("}")
    return dictcontents

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
    for fn in ENV.keys():
        fn_obj = ENV[fn]
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
    print ENV.keys()

if __name__ == "__main__":
    main()

import sys
import PLYex
from PLYex import tokenlist as tokens
import ply.lex as lex

# tokens = []

mathop_list = ['<','>','==','<=','>=','!=']

ENV = {}

class NodeTemplate(object):
    pass

class FunctionNode(NodeTemplate):
    def __init__(self,name,args,body):
        self.name = name
        self.args = args
        self.body = body

    def emit_function(self):
        print "def", self.name,"():"

class AssignNode(NodeTemplate):
    def __init__(self,first,second):
        self.first = first
        self.second = second
        
    def emit_expr(self):
    # def emit_assign_expr(self):
        print self.first, "=", self.second

class OpNode(NodeTemplate):
    def __init__(self,op,first,second):
        self.op = op
        self.first = first
        self.second = second

    def emit_expr(self):
        print self.first, self.op, self.second

class IfNode(NodeTemplate):
    def __init__(self,first,second,third):
        self.first = first
        self.second = second
        self.third = third

    def emit_expr(self):
    # def emit_ifnode(self):
        print "if", self.first.first, self.first.op, self.first.second, ":"
        print "     ", 
        for item in self.second:
            print item.first, "=", item.second.first,

class ForNode(NodeTemplate):
    def __init__(self,first,second,third,block):
        self.first = first
        self.second = second
        self.third = third
        self.block = block

def expect(thing_to_expect):
    token = tokens.pop(0)
    if token.value != thing_to_expect:
        raise Exception("Wrong token! Expected: ", thing_to_expect, "and got: ", 
            token.value, "on line:", token.lineno, ", position:", token.lexpos)
    return token

def parse_tokens():
    while tokens:
        if tokens[0].value == 'function':
            tokens.pop(0)
            parse_function()

def parse_function():
    name = parse_id().value
    print "OUR FUNCTION IS CALLED:", name
    args = parse_args()
    body = []

    while tokens[0].value != "}":
        body.append(parse_statement())   #fn body is a list of dictionaries
    expect("}")

    fn_obj = FunctionNode(name,args,body)

    # fn =  {"type": "function",
    #         "name": name,
    #         "args": args,
    #         "body": body}

    ENV[name] = fn_obj
    # ENV[name] = fn
    # fn_obj.emit_function()

def parse_id():
    return tokens.pop(0)

def parse_args():
    expect("(")
        # maybe put something in here?
    expect(")")
    expect("{")
    return []

def parse_statement():
    if tokens[0].value == "var":
        return parse_variable_def()
    elif tokens[0].value == "for":
        return parse_for()
    elif tokens[0].value == "if":
        return parse_if()
    elif tokens[0].type == "ID" and tokens[1].value != "(":
        x = parse_var_assign()
        expect(";")
        return x
    else:
        token = tokens[0].value
        # token = token[:-2]
        if token in ENV.keys():
            token = tokens.pop(0)
            token = token.value
            expect("(")
            expect(")")
            expect(";")
            print "THIS FUNCTION CALLS THE FUNCTION:", token
            return {"name": token,
                    "type": "function call"}
        raise Exception("WTF ", tokens[0].value, "IS NOT A KEYWORD. Error on line:",
            tokens[0].lineno)

def parse_variable_def():
    expect("var")
    # token = tokens.pop(0)
    token = parse_id()
    var_name = token.value
    expect("=")
    if tokens[0].value == "[":
        val = parse_list()
    elif tokens[0].value == "{":
        val = parse_dict()    
    elif tokens[0].type == "STRING":
        val = parse_str()
    else:
        val = parse_math_expression()    
    expect(";")
    assign_obj = AssignNode(var_name,val)
    assign_obj.emit_expr()
    return assign_obj
    # return {"type": "assign_expr",
    #             "first": {"type": "id_expr",
    #                     "val": var_name},
    #             "second": {"type": "eval_expr",
    #                     "val": val}}

# EXPR : FACTOR { ('+' | '-') EXPR } ;
# FACTOR : INT | '(' EXPR ')' ;

def parse_math_expression():
    x = parse_term()
    # if tokens[0].value in mathop_table:
    if tokens[0].value in mathop_list:
        operator = tokens.pop(0)
        operator = operator.value
        y = parse_math_expression()
        
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
    if tokens[0].value == '*' or tokens[0].value == '/':
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
    if token.type == "NUMBER" or token.type == "ID":
        tokens.pop(0)
        return token.value
    expect("(")  
    expr = parse_math_expression()
    expect(")")
    return expr 

def parse_for():
    block = []
    expect("for")
    expect("(")
    n1 = parse_variable_def()         #declare variable inside loop
    n2 = parse_math_expression()
    expect(";")
    n3 = parse_var_assign()
    expect(")")
    expect("{")
    while tokens[0].value != "}":
        block.append(parse_statement())   
    expect("}")

    for_obj = ForNode(n1,n2,n3,block)
    return for_obj
    # return {"type": "for",
    #         "first": n1,
    #         "second": n2,
    #         "third": n3,
    #         "block": block}

def parse_if():
    conseq = []
    alt = []
    expect("if")
    expect("(")

    n1 = parse_math_expression()
    expect(")")
    expect("{")
    while tokens[0].value != "}":
        conseq.append(parse_statement())   
    expect("}")
    if tokens[0].value == "else":
        expect("else")
        expect("{")
        while tokens[0].value != "}":
            alt.append(parse_statement())  
        expect("}")

    if_obj = IfNode(n1,conseq,alt)
    # print if_obj.first.first, if_obj.first.op, if_obj.first.second
    return if_obj
    # return {"type": "if",
    #         "first": n1,
    #         "second": conseq,
    #         "third": alt}

def parse_var_assign():
    var_name = tokens.pop(0)
    var_name = var_name.value
    expect("=")
    val = parse_math_expression()
    # expect(";")
    assign_obj = AssignNode(var_name,val)
    # assign_obj.emit_assign_expr()
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
        contents.append(atom(tokens[0].value))
        tokens.pop(0)
    expect("]")
    return contents

def parse_dict():
    dictcontents = {}
    expect("{")
    while tokens[0].value != "}":
        if tokens[0].value == ",":
            tokens.pop(0)
        dictcontents[atom(tokens[0].value)] = atom(tokens[2].value)
        # tokens = tokens[3:]
        tokens.pop(0)
        tokens.pop(0)
        tokens.pop(0)
    expect("}")
    return dictcontents

def parse_str():
    contents = []
    while tokens[0].value != ";":
        token = tokens.pop(0)
        token = token.value
        contents.append(token)
 
    return " ".join(contents)

def atom(var):
    try: return int(var)
    except: return str(var)

def emit_all():
    for fn in ENV.keys():
        fn_obj = ENV[fn]
        fn_obj.emit_function()
        for stmt in fn_obj.body:
            # print stmt.istype, stmt.first, stmt.second
            # stmt.emit_assign_expr()
            stmt.emit_expr()


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

    print "HERE ARE MY TOKENS:", tokens

    parse_tokens()               
    print ENV
    emit_all()

if __name__ == "__main__":
    main()

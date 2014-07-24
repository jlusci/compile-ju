import sys
import PLYex
from PLYex import tokenlist as tokens
import ply.lex as lex

# tokens = []

mathop_table = ['+','-','/','*','%','<','>','=','<=','>=','!=']

ENV = {}

class NodeTemplate(object):
    pass

class FunctionNode(NodeTemplate):
    def __init__(self,name,args,body):
        self.name = name
        self.args = args
        self.body = body

class AssignNode(NodeTemplate):
    def __init__(self,first,second):
        self.first = first
        self.second = second

class OpNode(NodeTemplate):
    def __init__(self,istype,first,second):
        self.istype = istype
        self.first = first
        self.second = second

class IfNode(NodeTemplate):
    def __init__(self,first,second,third):
        self.first = first
        self.second = second
        self.third = third

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
            token.value, "on line:", token.lineno)
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
        body.append(parse_statement())   #statments is a list of dictionaries
    expect("}")

    fn_obj = FunctionNode(name,args,body)
    fn =  {"type": "function",
            "name": name,
            "args": args,
            "body": body}

    # ENV[name] = fn_obj
    ENV[name] = fn

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
    elif tokens[0].type == "NUMBER":
        return parse_math_expression()
    #need another elif to look for variable definitions inside function
    #elif tokens[0].type == "ID":
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
    return {"type": "assign_expr",
                "first": {"type": "id_expr",
                        "val": var_name},
                "second": {"type": "eval_expr",
                        "val": val}}

# EXPR : FACTOR { ('+' | '-') EXPR } ;
# FACTOR : INT | '(' EXPR ')' ;

def parse_math_expression():
    x = parse_factor()
    if tokens[0].value in mathop_table:
    # if tokens[0].value == '+' or tokens[0].value == '-':
        operator = tokens.pop(0)
        operator = operator.value
        y = parse_math_expression()
        
        op_obj = OpNode(operator,x,y)
        # return op_obj

        return {"type": "op_expr",
                "val": operator,
                "first": {"type": "int_const_expr",
                        "val": x},
                "second": {"type": "int_const_expr",
                        "val": y}}
    return x

def parse_factor():
    token = tokens[0].value
    token = atom(token)
    if type(token) == int:
        tokens.pop(0)
        return token
    expect("(")  
    expr = parse_math_expression()
    expect(")")
    return expr 

def parse_for():
    # block = []
    expect("for")
    expect("(")
    n1 = parse_expression()
    n2 = parse_expression()
    n3 = parse_expression()
    block = parse_statement()
    expect(";")
    expect("}")
    return {"type": "for",
            "first": n1,
            "second": n2,
            "third": n3,
            "block": block}

def parse_if():
    conseq = []
    alt = []
    expect("if")
    expect("(")

    n1 = parse_expression()
    expect("{")
    conseq = parse_statement()
    expect(";")
    expect("}")
    if tokens[0].value == "else":
        expect("else")
        expect("{")
        alt = parse_statement()
        expect(";")
        expect("}")

    if_obj = IfNode(n1,conseq,alt)

    # return if_obj
    return {"type": "if",
            "first": n1,
            "second": conseq,
            "third": alt}

def parse_expression():
    contents = [] 

    if tokens[0].value == 'var':                #var definition inside statement
        first = parse_variable_def()
        return first
        # tokens.pop(0)
        # while tokens[0].value != ";":
        #     var_init.append(atom(tokens[0].value))
        #     tokens.pop(0)
        # expect(";")
        # return {"type": "assign_expr",
        #         "first": {"type": "id_expr",
        #                 "val": var_init[0]},
        #         "second": {"type": "int_const_expr",
        #                 "val": var_init[2]}}
    else:
        while tokens[0].value != ";" and tokens[0].value != ")":
                contents.append(atom(tokens[0].value))
                tokens.pop(0)
        # expect(";")
        tokens.pop(0)
        if len(contents) == 3:                  #simple comparison, ex x < 5
            return {"type": "op_expr",
                    "val": contents[1],
                    "first": {"type": "id_expr",
                            "val": contents[0]},
                    "second": {"type": "int_const_expr",
                            "val": contents[2]}}
        elif len(contents) == 5:                #doing some operation, ex x = x + 1
            # tokens.pop(0)
            expect("{")
            # tokens.pop(0)
            rightn = {"type": "op_expr",
                    "val": contents[3],
                    "first": {"type": "id_expr",
                            "val": contents[2]},
                    "second": {"type": "int_const_expr",
                            "val": contents[4]}}
            return {"type": "assign_expr",
                    "val": contents[1],
                    "first": {"type": "id_expr",
                            "val": contents[0]},
                    "second": rightn}      

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

if __name__ == "__main__":
    main()

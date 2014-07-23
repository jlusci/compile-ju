import sys
import PLYex
from PLYex import tokenlist as tokens
import ply.lex as lex

# tokens = []

symbol_table = ['+','-','/','*','%']

ENV = {}

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

    fn =  {"type": "function",
            "name": name,
            "args": args,
            "body": body}

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
    contents = []
    dictcontents = {}
    expect("var")
    # token = tokens.pop(0)
    token = parse_id()
    var_name = token.value
    expect("=")

    if tokens[0].value == "[":
        expect("[")
        while tokens[0].value != "]":
            if tokens[0].value == ',':
                tokens.pop(0)
            contents.append(atom(tokens[0].value))
            tokens.pop(0)
        expect("]")
        val = contents
        expect(";")
        return {"type": "assign_expr",
                "first": {"type": "id_expr",
                        "val": var_name},
                "second": {"type": "list_expr",
                        "val": val}}
    elif tokens[0].value == "{":
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
        val = dictcontents
        expect(";")
        return {"type": "assign_expr",
                "first": {"type": "id_expr",
                        "val": var_name},
                "second": {"type": "dict_expr",
                        "val": val}}
    
    elif type(atom(tokens[0].value)) == str and tokens[0].value != "(":
        val = parse_str()
        expect(";")
        return {"type": "assign_expr",
                    "first": {"type": "id_expr",
                            "val": var_name},
                    "second": {"type": "str_const_expr",
                            "val": val}}
    else:
        val = parse_math_expression()
        expect(";")
        return {"type": "assign_expr",
                    "first": {"type": "id_expr",
                            "val": var_name},
                    "second": {"type": "eval_expr",
                            "val": val}}

# EXPR : FACTOR { ('+' | '-') EXPR } ;
# FACTOR : INT | '(' EXPR ')' ;

def parse_math_expression():
    x = parse_factor()
    if tokens[0].value in symbol_table:
    # if tokens[0].value == '+' or tokens[0].value == '-':
        operator = tokens.pop(0)
        operator = operator.value
        y = parse_math_expression()
        
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
    block = []
    expect("for")
    expect("(")

    n1 = parse_expression()
    n2 = parse_expression()
    n3 = parse_expression()

    while tokens[0].value != ";":
        block.append(atom(tokens[0].value))
        tokens.pop(0)
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

    while tokens[0].value != ";":
        conseq.append(atom(tokens[0].value))
        tokens.pop(0)
    expect(";")
    expect("}")
    if tokens[0].value == "else":
        expect("else")
        expect("{")
        while tokens[0].value != ";":
            alt.append(atom(tokens[0].value))
            tokens.pop(0)
        expect(";")
        expect("}")
    
    return {"type": "if",
            "first": n1,
            "second": conseq,
            "third": alt}

def parse_str():
    contents = []
    while tokens[0].value != ";":
        token = tokens.pop(0)
        token = token.value
        contents.append(token)
 
    return " ".join(contents)

def parse_expression():
    var_init = []
    contents = [] 

    if tokens[0].value == 'var':                      #var definition inside statement
        tokens.pop(0)
        while tokens[0].value != ";":
            var_init.append(atom(tokens[0].value))
            tokens.pop(0)
        expect(";")
        return {"type": "assign_expr",
                "first": {"type": "id_expr",
                        "val": var_init[0]},
                "second": {"type": "int_const_expr",
                        "val": var_init[2]}}
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
            return {"type": "op_expr",
                    "val": contents[1],
                    "first": {"type": "id_expr",
                            "val": contents[0]},
                    "second": rightn}      

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

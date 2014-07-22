import sys
import PLYex
from PLYex import tokenlist as tokens
import ply.lex as lex

# tokens = []

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
        # token = tokens.pop(0)
        # token = token.value
        # return token

def parse_variable_def():
    contents = []
    dictcontents = {}
    expect("var")
    token = tokens.pop(0)
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
                "left": {"type": "id_expr",
                        "name": var_name},
                "right": {"type": "list_expr",
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
                "left": {"type": "id_expr",
                        "name": var_name},
                "right": {"type": "dict_expr",
                        "val": val}}
    else:
        val = parse_var()
        val = atom(val)
        expect(";")

    # print "VARIABLE %s is %s"%(var_name, val)

        if type(val) == int:
            return {"type": "assign_expr",
                    "left": {"type": "id_expr",
                            "name": var_name},
                    "right": {"type": "int_const_expr",
                            "val": val}}
        elif type(val) == str:
            return {"type": "assign_expr",
                    "left": {"type": "id_expr",
                            "name": var_name},
                    "right": {"type": "str_const_expr",
                            "val": val}}

# EXPR : FACTOR { ('+' | '-') EXPR } ;
# FACTOR : INT | '(' EXPR ')' ;

def parse_for():
    block = []
    expect("for")
    expect("(")
    # n1 = {}
    # n2 = {}
    # n3 = {}
    # # n4 = {}
    # expect("for")
    # expect("(")
    # while tokens[0].value != ";":
    #     if tokens[0].value == 'var':
    #         tokens.pop(0)
    #     var_init.append(atom(tokens[0].value))
    #     tokens.pop(0)
    # expect(";")
    # n1 = {"type": "assign_expr",
    #     "left": {"type": "id_expr",
    #     "name": var_init[0]},
    #     "right": {"type": "int_const_expr",
    #     "val": var_init[2]}}

    n1 = parse_expression(tokens)
    n2 = parse_expression(tokens)
    n3 = parse_expression(tokens)

    # while tokens[0].value != ";":
    #     cond.append(atom(tokens[0].value))
    #     tokens.pop(0)
    # expect(";")
    # n2 = {"type": cond[1],
    #     "left": {"type": "id_expr",
    #     "name": cond[0]},
    #     "right": {"type": "int_const_expr",
    #     "val": cond[2]}}
    # while tokens[0].value != ")":
    #     incr.append(atom(tokens[0].value))
    #     tokens.pop(0)
    # expect(")")
    # n3 = {"type": "incr",
    #         "name": incr}
    # expect("{")
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
    n1 = parse_expression(tokens)
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

def parse_var():
    contents = []
    while tokens[0].value != ";":
        if type(tokens[0].value) == int:
            token = tokens.pop(0)
            token = token.value
            return token
        else:
            token = tokens.pop(0)
            token = token.value
            contents.append(token)
    return " ".join(contents)

def parse_expression(tokens):
    var_init = []
    contents = [] 
    # print tokens       
    if tokens[0].value == 'var':                      #var definition inside statement
        tokens.pop(0)
        while tokens[0].value != ";":
            var_init.append(atom(tokens[0].value))
            tokens.pop(0)
        expect(";")
        return {"type": "assign_expr",
                "left": {"type": "id_expr",
                        "name": var_init[0]},
                "right": {"type": "int_const_expr",
                        "val": var_init[2]}}
    else:
        while tokens[0].value != ";" and tokens[0].value != ")":
                contents.append(atom(tokens[0].value))
                tokens.pop(0)
        # expect(";")
        tokens.pop(0)
        if len(contents) == 3:                  #simple comparison, ex x < 5
            return {"type": contents[1],
                    "left": {"type": "id_expr",
                            "name": contents[0]},
                    "right": {"type": "int_const_expr",
                            "val": contents[2]}}
        elif len(contents) == 5:                #doing some operation, ex x = x + 1
            # tokens.pop(0)
            expect("{")
            # tokens.pop(0)
            rightn = {"type": contents[3],
                    "left": {"type": "id_expr",
                            "name": contents[2]},
                    "right": {"type": "int_const_expr",
                            "name": contents[4]}}
            return {"type": contents[1],
                    "left": {"type": "id_expr",
                            "name": contents[0]},
                    "right": rightn}      

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

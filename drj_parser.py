import sys

tokens = []

ENV = {}

def expect(thing_to_expect):
    token = tokens.pop(0)
    if token != thing_to_expect:
        raise Exception("Wrong token! Expected: ", thing_to_expect, "and got: ", token)
    return token

def parse_tokens():
    while tokens:
        if tokens[0] == 'function':
            tokens.pop(0)
            parse_function()

def parse_function():
    name = parse_id()
    print "OUR FUNCTION IS CALLED:", name
    args = parse_args()
    body = []

    while tokens[0] != "}":
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
    if tokens[0] == "var":
        return parse_variable_def()
    elif tokens[0] == "for":
        return parse_for()
    elif tokens[0] == "if":
        return parse_if()
    else:
        token = tokens[0]
        token = token[:-2]
        if token in ENV.keys():
            token = tokens.pop(0)
            expect(";")
            print "THIS FUNCTION CALLS THE FUNCTION:", token
            return {"name": token,
                    "type": "function call"}
        raise Exception("WTF ", tokens[0], "IS NOT A KEYWORD")
        token = tokens.pop(0)
        return token

def parse_variable_def():
    contents = []
    dictcontents = {}
    expect("var")
    var_name = tokens.pop(0)
    expect("=")
    if tokens[0] == "[":
        expect("[")
        while tokens[0] != "]":
            if tokens[0] == ',':
                tokens.pop(0)
            contents.append(atom(tokens[0]))
            tokens.pop(0)
        expect("]")
        val = contents
        expect(";")
        return {"type": "assign_expr",
                "left": {"type": "id_expr",
                        "name": var_name},
                "right": {"type": "list_expr",
                        "val": val}}
    elif tokens[0] == "{":
        expect("{")
        while tokens[0] != "}":
            if tokens[0] == ",":
                tokens.pop(0)
            dictcontents[atom(tokens[0])] = atom(tokens[2])
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
    # while tokens[0] != ";":
    #     if tokens[0] == 'var':
    #         tokens.pop(0)
    #     var_init.append(atom(tokens[0]))
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

    # while tokens[0] != ";":
    #     cond.append(atom(tokens[0]))
    #     tokens.pop(0)
    # expect(";")
    # n2 = {"type": cond[1],
    #     "left": {"type": "id_expr",
    #     "name": cond[0]},
    #     "right": {"type": "int_const_expr",
    #     "val": cond[2]}}
    # while tokens[0] != ")":
    #     incr.append(atom(tokens[0]))
    #     tokens.pop(0)
    # expect(")")
    # n3 = {"type": "incr",
    #         "name": incr}
    # expect("{")
    while tokens[0] != ";":
        block.append(atom(tokens[0]))
        tokens.pop(0)
    expect(";")
    expect("}")
    test = {"type": "for",
            "first": n1,
            "second": n2,
            "third": n3,
            "block": block}

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
    while tokens[0] != ";":
        conseq.append(atom(tokens[0]))
        tokens.pop(0)
    expect(";")
    expect("}")
    if tokens[0] == "else":
        expect("else")
        expect("{")
        while tokens[0] != ";":
            alt.append(atom(tokens[0]))
            tokens.pop(0)
        expect(";")
        expect("}")
    
    return {"type": "if",
            "first": n1,
            "second": conseq,
            "third": alt}

def parse_var():
    contents = []
    while tokens[0] != ";":
        contents.append(tokens.pop(0))
 
    return " ".join(contents)

def parse_expression(tokens):
    var_init = []
    contents = [] 
    print tokens       
    if tokens[0] == 'var':                      #var definition inside statement
        tokens.pop(0)
        while tokens[0] != ";":
            var_init.append(atom(tokens[0]))
            tokens.pop(0)
        expect(";")
        return {"type": "assign_expr",
            "left": {"type": "id_expr",
            "name": var_init[0]},
            "right": {"type": "int_const_expr",
            "val": var_init[2]}}
    else:
        while tokens[0] != ";" and tokens[0] != ")":
                contents.append(atom(tokens[0]))
                tokens.pop(0)
        # expect(";")
        tokens.pop(0)
        if len(contents) == 3:                  #simple comparison
            return {"type": contents[1],
                    "left": {"type": "id_expr",
                    "name": contents[0]},
                    "right": {"type": "int_const_expr",
                    "val": contents[2]}}
        elif len(contents) == 5:                #doing some operation
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
    f = open(sys.argv[1])
    lines = f.read()
    f.close()
    
    print lines
    tokens = lines.replace(';',' ; ').split()
    print tokens

    parse_tokens()               
    print ENV
    
if __name__ == "__main__":
    main()

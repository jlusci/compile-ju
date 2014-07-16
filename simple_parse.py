tokens = []

ENV = {}
ENV['functions'] = []

def expect(thing_to_expect):
    token = tokens.pop(0)
    if token != thing_to_expect:
        raise Exception("Your program is bad and you should feel bad")
    return token

def parse_function():
    expect("function")
    name = parse_fn_name()
    print "OUR FUNCTION IS CALLED:", name
    statements = []

    expect("{")

    while tokens[0] != "}":
        statements.append(parse_statement())   #statments is a list of dictionaries
    expect("}")


    fn =  {"name": name,
            "stmts": statements}

    fn_list = ENV.get('functions')             #add new function statements to ENV
    fn_list.append(fn)

    if tokens:
        parse_function()                       #call parse_function() again if more tokens

    return fn

def parse_fn_name():
    contents = []
    while tokens[0] != "{":
        contents.append(tokens[0])
        tokens.pop(0)
    return " ".join(contents)

def parse_statement():
    stmtlist = ENV.get('functions')
    # index = 0
    if tokens[0] == "var":
        return parse_variable_def()
    # elif tokens[0] == "for":
    #     return parse_for()
    elif tokens[0] == "if":
        return parse_if()
    else:
        for index in range(len(stmtlist)):
            if stmtlist[index].get('name') == tokens[0]:
                token = tokens.pop(0)
                expect(';')
                print "THIS FUNCTION CALLS THE FUNCTION:", token
                return {"name": token,
                        "type": "function call"}
            # else:
            #     # if index == len(stmtlist):
            #     token = tokens.pop(0)
            #     return token
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
            contents.append(tokens[0])
            tokens.pop(0)
        expect("]")
        val = contents
    elif tokens[0] == "{":
        expect("{")
        while tokens[0] != "}":
            if tokens[0] == ",":
                tokens.pop(0)
            dictcontents[tokens[0]] = tokens[2]
            # tokens = tokens[3:]
            tokens.pop(0)
            tokens.pop(0)
            tokens.pop(0)
        expect("}")
        val = dictcontents
    else:
        val = parse_string()
    
    expect(";")
    print "VARIABLE %s is %s"%(var_name, val)
    return {"name": var_name,
            "val": val,
            "type": "assign"}

# def parse_for():
#     contents = []
#     expect("for")
#     expect("(")
#     while tokens[0] != ")":
#         contents.append(tokens[0])
#         tokens.pop(0)
#     tokens.pop(0)
#     contents = " ".join(contents)
#     contents = contents.split(';')
#     var_def = contents[0]
#     condition = contents[1]
#     incr = contents[2]
#     x = (var_def, condition, incr)
#     print x
#     return x

def parse_if():
    test = []
    conseq = []
    alt = []
    dictcontents = {}
    expect("if")
    expect("(")
    while tokens[0] != ")":
        test.append(tokens[0])
        tokens.pop(0)
    expect(")")
    expect("{")
    while tokens[0] != ";":
        conseq.append(tokens[0])
        tokens.pop(0)
    expect(";")
    expect("}")
    if tokens[0] == "else":
        expect("else")
        expect("{")
        while tokens[0] != ";":
            alt.append(tokens[0])
            tokens.pop(0)
        expect(";")
        expect("}")
    
    return {"type": "if",
            "test": test,
            "conseq": conseq,
            "alt": alt}



def parse_string():
    name_words = []
    
    while tokens[0] != ";":
        name_words.append(tokens.pop(0))
 
    return " ".join(name_words)

def main():
    f = open("onefun.txt")
    lines = f.read()
    f.close()
    print lines
    global tokens
    tokens = lines.replace(';',' ; ').split()
    print tokens

    parse_function()               
    # run_all(???)
    global ENV
    print ENV
    
if __name__ == "__main__":
    main()

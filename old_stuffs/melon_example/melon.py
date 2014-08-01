# Program
    # function main
        # 2 statements
        # var assignment
        # print var


tokens = []

ENV = {}

def expect(thing_to_expect):
    token = tokens.pop(0)
    if token != thing_to_expect:
        raise Exception("Your program is bad and you should feel bad")
    # print tokens    
    return token


def parse_program():
    # see the word 'program'
    # see a name afterwards

    # one or more functions
    # the keyword end

    expect("program")
    # Expect more things
    name = parse_string()
    print "PROGRAM NAME IS", name

    # Expect program is filled with functions
    functions = []

    while tokens[0] != "margorp":
        functions.append(parse_function())

    expect("margorp")

    program = {"name": name,
               "functions": functions #program is a dictionary with all program definitions and values
}
    print "*************", program
    return program

def parse_function():
    expect("function")
    name = parse_string()
    print "OUR FUNCTION IS CALLED", name
    statements = []

    while tokens[0] != "noitcnuf":
        statements.append(parse_statement())  #statments is a list of dictionaries
    expect("noitcnuf")

    fn =  {"name": name,
            "stmts": statements}

    print "$$$$$$$$$$$$$$$$$$", fn
    return fn

def parse_statement():
    if tokens[0] == "var":
        return parse_variable()
    elif tokens[0] == "print":
        return parse_print()

    else:
        raise Exception("WTF THAT IS NOT A KEYWORD")

def parse_variable():
    expect("var")
    var_name = tokens.pop(0)
    expect("is")
    val = parse_string()
    expect("rav")
    # print "VARIABLE %s is %s"%(var_name, val)
    return {"name": var_name,
            "val": val,
            "type": "assign"}

def parse_string():
    expect("string")

    name_words = []
    
    while tokens[0] != "gnirts":
        name_words.append(tokens.pop(0))
    expect("gnirts")

    return " ".join(name_words)


def parse_print():
    expect("print")
    contents = {"type": "print"}

    if tokens[0] == "var":
        expect("var")
        var_name = tokens.pop(0)
        expect("rav")
        contents["var"] = var_name

    elif tokens[0] == "string":
        s = parse_string()
        contents["str"] = s

    expect("tnirp")

    # print "################", contents
    return contents

def run_melon_program(pgm):
    print "EXECUTING", pgm['name']  #pgm['name'] returns string name of program
    fns = pgm["functions"]          #pgm['functions'] returns list of functions
    # print "$$$$$$$$$$$", fns
    for fn in fns:                  #fn is one element in list fns, fn is dictionary
        run_fn(fn)

def run_fn(fn):
    print "RUNNING FUNCTION", fn['name']

    stmts = fn['stmts']             
    # print "@@@@@@@@@", stmts
    for stmt in stmts:#fn['stmts']:     #stmt is a dictionary of stmts associated with fn
        # print "This is stmt:", stmt
        run_statement(stmt)

def run_statement(stmt):
    #print "RUNNING STATEMENT", stmt
    if stmt['type'] == "print":
        run_print(stmt)
    elif stmt['type'] == "assign":
        run_var(stmt)

def run_var(stmt):
    #print "VARIABLE ASSIGNMENT", stmt
    var_name = stmt['name']
    val = stmt['val']
    ENV[var_name] = val
    print ENV

def run_print(stmt):
    #print "PRINTING", stmt
    raw_string = stmt.get("str")
    if raw_string:
        print raw_string

    elif stmt.get("var"):
        name = stmt.get("var")
        variable_val = ENV[name]
        print variable_val

def main():
    f = open("basic.melonmelon")
    # f = open("hello_world.melon")
    lines = f.read()
    f.close()
    print lines
    global tokens
    tokens = lines.split()
    print tokens

    pgm = parse_program()
    run_melon_program(pgm)
    
if __name__ == "__main__":
    main()

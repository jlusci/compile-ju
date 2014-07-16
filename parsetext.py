import sys

script, filename = sys.argv

CLASS = 1


def parse_tokens(tokens):
	if tokens[0] == 'class':
		expect('class')
		tokens.pop(0)
		next(tokens)

def expect(expected_thing):
	if tokens[0] != expected_thing:
		print "You didn't get the expected token, try again, fool"
	elif tokens[0] == expected_thing:
		print "Nice work! You got the expected token: %s" %(expected_thing)

def next(tokens):
	print tokens

# def break_line(line):
#     space = line.find(" ")
#     if space == -1:
#         command = line.strip().lower()
#         rest = ""
#     else:
#         command = line[:space].strip().lower()
#         rest = line[space:].strip()
#     return command, rest

def main():
	global tokens 
	tokens = []
	f = open(filename)
	words = f.read()
	tokens = words.split()
	print tokens
	parse_tokens(tokens)


	# 	if command == "class":
	# 		parse_class(rest) 
	# 	elif command == "var":
	# 		parse_var(rest)
	# 	elif command == "def":
	# 		parse_def(line, file_lines)
	# 	elif command == "end":
	# 		if rest == "function":
	# 			print "End of function definition"
	# 		if rest == "class":
	# 			print "End of class definition"
	# 			break
	# 	else:
	# 		print "Command not found"


if __name__ == "__main__":
    main()
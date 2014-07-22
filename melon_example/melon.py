# Program
	#function main
		#2 statements
		#var assignment
		#print var

tokens = []

def expect(thing_to_expect):
	token = tokens.pop(0)
	if token != thing_to_expect:
		raise Exception("bad")

	return token 

def parse_program():
	# see the word 'program'
	# see a name afterwards

	# one or more functions
	# the keyword 'end'

	expect("program")

	# expect more things
	name = parse_name()

	expect("margorp")

	expect("end")

def main():
	f.open("basic.melon")
	lines = f.read()
	global tokens
	tokens = lines.split()

	parse_program()
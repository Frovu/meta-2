import string
import sys
indent = 0
out_buf = ""
in_buf = ""
flag = 1
def push(x): global out_buf; out_buf += x
def escape(x):
	return x.replace(chr(39), chr(39)*3) if chr(39) in x and chr(10) in x else x
def out(): global out_buf; print(chr(9)*indent + out_buf); out_buf=""
def check_err():
	if not flag: raise Exception("ERROR"); sys.exit(1)
def skip():
	if len(input.peek(1)[:1]):
		while input.peek(1)[:1] in bytes([9,10,32]): input.seek(1, 1)
def read(t):
	global in_buf, flag;
	skip(); n = input.peek(1)[:1].decode()
	if not len(n) or not((t=="id" and n in string.printable[10:62])
		or (t=="str" and ord(n) == 39)
		or (t=="num" and n in string.printable[:10])):
		flag = 0; return
	in_buf = n; input.seek(1, 1); flag = 1
	while n := input.peek(1)[:1].decode():
		if not ((t=="id" and n in string.printable[:62])
			or (t=="str" and ord(n) != 39)
			or (t=="num" and n in string.printable[:10])): break
		in_buf += n; input.seek(1, 1)
	if t=="str": in_buf = escape(in_buf + n); input.seek(1, 1)
def test(x):
	skip(); global flag
	if input.peek(len(x))[:len(x)] == x.encode():
		input.seek(len(x), 1); flag = 1
	else: flag = 0

def e_ARG():
	global flag, indent
	while True:
		test('*')
		if flag:
			pass
			push('push(in_buf)')
			out()
		if flag: break
		read("str")
		if flag:
			pass
			push('push(')
			push(in_buf)
			push(')')
			out()
		break

def e_OUTPUT():
	global flag, indent
	while True:
		test('.out')
		if flag:
			pass
			test('(')
			check_err()
			flag = 1
			while flag:
				e_ARG()
			flag = 1
			check_err()
			test(')')
			check_err()
			push('out()')
			out()
		if flag: break
		test('{')
		if flag:
			pass
			push('indent+=1')
			out()
		if flag: break
		test('}')
		if flag:
			pass
			push('indent-=1')
			out()
		break

def e_EX3():
	global flag, indent
	while True:
		read("id")
		if flag:
			pass
			push('e_')
			push(in_buf)
			push('()')
			out()
		if flag: break
		read("str")
		if flag:
			pass
			push('test( ')
			push(in_buf)
			push(' )')
			out()
		if flag: break
		test('.ID')
		if flag:
			pass
			push('read("id")')
			out()
		if flag: break
		test('.NUMBER')
		if flag:
			pass
			push('read("num")')
			out()
		if flag: break
		test('.STRING')
		if flag:
			pass
			push('read("str")')
			out()
		if flag: break
		test('(')
		if flag:
			pass
			e_EX1()
			check_err()
			test(')')
			check_err()
		if flag: break
		test('.EMPTY')
		if flag:
			pass
			push('flag = 1')
			out()
		if flag: break
		test('$')
		if flag:
			pass
			push('flag = 1')
			out()
			push('while flag:')
			out()
			indent+=1
			e_EX3()
			check_err()
			indent-=1
			push('flag = 1')
			out()
		break

def e_EX2():
	global flag, indent
	while True:
		while True:
			e_EX3()
			if flag:
				pass
				push('if flag:')
				out()
			if flag: break
			e_OUTPUT()
			if flag:
				pass
				push('if True:')
				out()
			break
		if flag:
			pass
			indent+=1
			push('pass')
			out()
			flag = 1
			while flag:
				while True:
					e_EX3()
					if flag:
						pass
						push('check_err()')
						out()
					if flag: break
					e_OUTPUT()
					if flag:
						pass
					break
			flag = 1
			check_err()
			indent-=1
		break

def e_EX1():
	global flag, indent
	while True:
		push('while True:')
		out()
		if True:
			pass
			indent+=1
			e_EX2()
			check_err()
			flag = 1
			while flag:
				while True:
					test('/')
					if flag:
						pass
						push('if flag: break')
						out()
						e_EX2()
						check_err()
					break
			flag = 1
			check_err()
			push('break')
			out()
			indent-=1
		break

def e_STATEMENT():
	global flag, indent
	while True:
		read("id")
		if flag:
			pass
			push('def e_')
			push(in_buf)
			push('():')
			out()
			test('=')
			check_err()
			indent+=1
			push('global flag, indent')
			out()
			e_EX1()
			check_err()
			indent-=1
			test(';')
			check_err()
			push('')
			out()
		break

def e_PROGRAM():
	global flag, indent
	while True:
		push('''import string
import sys
indent = 0
out_buf = ""
in_buf = ""
flag = 1
def push(x): global out_buf; out_buf += x
def escape(x):
	return x.replace(chr(39), chr(39)*3) if chr(39) in x and chr(10) in x else x
def out(): global out_buf; print(chr(9)*indent + out_buf); out_buf=""
def check_err():
	if not flag: raise Exception("ERROR"); sys.exit(1)
def skip():
	if len(input.peek(1)[:1]):
		while input.peek(1)[:1] in bytes([9,10,32]): input.seek(1, 1)
def read(t):
	global in_buf, flag;
	skip(); n = input.peek(1)[:1].decode()
	if not len(n) or not((t=="id" and n in string.printable[10:62])
		or (t=="str" and ord(n) == 39)
		or (t=="num" and n in string.printable[:10])):
		flag = 0; return
	in_buf = n; input.seek(1, 1); flag = 1
	while n := input.peek(1)[:1].decode():
		if not ((t=="id" and n in string.printable[:62])
			or (t=="str" and ord(n) != 39)
			or (t=="num" and n in string.printable[:10])): break
		in_buf += n; input.seek(1, 1)
	if t=="str": in_buf = escape(in_buf + n); input.seek(1, 1)
def test(x):
	skip(); global flag
	if input.peek(len(x))[:len(x)] == x.encode():
		input.seek(len(x), 1); flag = 1
	else: flag = 0

''')
		out()
		if True:
			pass
			flag = 1
			while flag:
				e_STATEMENT()
			flag = 1
			check_err()
			test('.SYNTAX')
			check_err()
			read("id")
			check_err()
			push('''
if len(sys.argv) < 2:
	print(f"Usage: {sys.argv[0]} <program_file>")
else:
	input = open(sys.argv[1], "rb")
	e_''')
			push(in_buf)
			push('()')
			out()
		break


if len(sys.argv) < 2:
	print(f"Usage: {sys.argv[0]} <program_file>")
else:
	input = open(sys.argv[1], "rb")
	e_PROGRAM()

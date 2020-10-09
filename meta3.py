import string
import sys
indent = 0
out_buf = ""
in_buf = ""
flag = 0
def push(x): out_buf += x
def out(): print("\t"*indent + out_buf); out_buf=""
def check_err():
	if flag: print("ERROR"); sys.exit(1)
def skip():
	while input.peek(1)[:1] in b" \t\n": input.seek(1, 1)
def read(t):
	skip(); n = input.peek(1)[:1].decode()
	if not((t=="id" and n in string.printable[10:62]+".")
		or (t=="str" and ord(n) == 39)
		or (t=="num" and n in string.printable[:10])):
		flag = 0; return
	global in_buf; in_buf = n; input.seek(1, 1); flag = 1
	while n := input.peek(1)[:1].decode():
		if not ((t=="id" and n in string.printable[:62])
			or (t=="str" and ord(n) != 39)
			or (t=="num" and n in string.printable[:10])): break
		in_buf += n; input.seek(1, 1);
def test(x):
	skip(); global flag
	if input.peek(len(x))[:len(x)] == x.encode():
		input.seek(len(x), 1); flag = 1
	else: flag = 0

if len(sys.argv) < 2:
	print(f"Usage: {sys.argv[0]} <program_file>")
else:
	input = open(sys.argv[1], "rb")
	e_PROGRAM()


def e_OUTA():
	while True:
		get_literal('*')
		if flag:
			pass
			push('push(in_buf)')
			out()
		if flag: break
		get_str()
		if flag:
			pass
			push('push(')
			push(in_buf)
			push(')')
			out()
		break
def e_OUTPUT():
	while True:
		get_literal('.out')
		if flag:
			pass
			get_literal('(')
			check_err()
			flag = 1
			while flag:
				e_OUTA()
			check_err()
			get_literal(')')
			check_err()
			push('out()')
			out()
		if flag: break
		get_literal('{')
		if flag:
			pass
			push('indent+=1')
			out()
		if flag: break
		get_literal('}')
		if flag:
			pass
			push('indent-=1')
			out()
		if flag: break
		get_literal('\n')
		if flag:
			pass
			push('out()')
			out()
		break
def e_EX3():
	while True:
		get_tok()
		if flag:
			pass
			push('e_')
			push(in_buf)
			push('()')
			out()
		if flag: break
		get_str()
		if flag:
			pass
			push('test( ')
			push(in_buf)
			push(' )')
			out()
		if flag: break
		get_literal('.ID')
		if flag:
			pass
			push('read("id")')
			out()
		if flag: break
		get_literal('.NUMBER')
		if flag:
			pass
			push('read("num")')
			out()
		if flag: break
		get_literal('.STRING')
		if flag:
			pass
			push('read("str")')
			out()
		if flag: break
		get_literal('(')
		if flag:
			pass
			e_EX1()
			check_err()
			get_literal(')')
			check_err()
		if flag: break
		get_literal('.EMPTY')
		if flag:
			pass
			push('flag = 1')
			out()
		if flag: break
		get_literal('$')
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
		break
def e_EX2():
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
			check_err()
			indent-=1
		break
def e_EX1():
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
					get_literal('/')
					if flag:
						pass
						push('if flag: break')
						out()
						e_EX2()
						check_err()
					break
			check_err()
			push('break')
			out()
			indent-=1
		break
def e_STATEMENT():
	while True:
		get_tok()
		if flag:
			pass
			push('def e_')
			push(in_buf)
			push('():')
			out()
			push('global flag, indent')
			out()
			get_literal('=')
			check_err()
			indent+=1
			e_EX1()
			check_err()
			indent-=1
			get_literal(';')
			check_err()
			push('')
			out()
		break
def e_PROGRAM():
	while True:
		get_literal('.SYNTAX')
		if flag:
			pass
			get_tok()
			check_err()
			push('''import string
import sys
indent = 0
out_buf = ""
in_buf = ""
flag = 0
def push(x): out_buf += x
def out(): print("\t"*indent + out_buf); out_buf=""
def check_err(): if flag: print("ERROR"); sys.exit(1)
def skip():
		while input.peek(1)[:1] in b" \t\n": input.seek(1, 1)
def read(t):
		skip(); n = input.peek(1)[:1].decode()
		if not((t=="id" and n in string.printable[10:62]+".")
				or (t=="str" and ord(n) == 39)
				or (t=="num" and n in string.printable[:10])):
				flag = 0; return
		global in_buf; in_buf = n; input.seek(1, 1); flag = 1
		while n := input.peek(1)[:1].decode():
				if not ((t=="id" and n in string.printable[:62])
						or (t=="str" and ord(n) != 39)
						or (t=="num" and n in string.printable[:10])): break
				in_buf += n; input.seek(1, 1);
def test(x):
		skip(); global flag
		if input.peek(len(x))[:len(x)] == x.encode():
				input.seek(len(x), 1); flag = 1
		else: flag = 0

if len(sys.argv) < 1:
	print(f"Usage: {sys.argv[0]} <program_file>")
else:
	input = open(sys.argv[1], "rb")
	''')
			push(in_buf)
			push('''()

''')
			out()
			flag = 1
			while flag:
				e_STATEMENT()
			check_err()
			get_literal('.END')
			check_err()
		break

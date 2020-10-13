import string
import sys
indent = 0
in_buf = ""
flag = 1
fn_gen = (f"fn_{i}()" for i in range(9999))
def genfn(): global fn; fn = next(fn_gen); return fn;
def escape(x):
	return x.replace(chr(39), chr(39)*3) if chr(39) in x and chr(10) in x else x
def out(x): print((chr(9)*indent + x[1:]) if ord(x[0])==9 else x, end="");
def err(): raise Exception("ERROR"); sys.exit(1)
def check_err():
	if not flag: raise Exception(f"ERROR inp={in_buf}"); sys.exit(1)
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
		if not ((t=="id" and n in string.printable[:62]+"_")
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
			out(""+' + in_buf')
		if flag: break
		read("str")
		if flag:
			pass
			out(""+'+'+in_buf)
		if flag: break
		test('.fn')
		if flag:
			pass
			out(""+' + fn')
		if flag: break
		test('.genfn')
		if flag:
			pass
			out(""+' + genfn()')
		break

def e_OUTPUT():
	global flag, indent
	while True:
		test('.out(')
		if flag:
			pass
			out(""+'\tout(""')
			flag = 1
			while flag:
				e_ARG()
			flag = 1
			check_err()
			test(')')
			check_err()
			out(""+')\n')
		if flag: break
		test('{')
		if flag:
			pass
			out(""+'\tindent+=1\n')
		if flag: break
		test('}')
		if flag:
			pass
			out(""+'\tindent-=1\n')
		break

def e_EX3():
	global flag, indent
	while True:
		read("id")
		if flag:
			pass
			out(""+'\te_'+in_buf+'()\n')
		if flag: break
		read("str")
		if flag:
			pass
			out(""+'\ttest('+in_buf+')\n')
		if flag: break
		test('.ID')
		if flag:
			pass
			out(""+'\tread("id")\n')
		if flag: break
		test('.NUMBER')
		if flag:
			pass
			out(""+'\tread("num")\n')
		if flag: break
		test('.STRING')
		if flag:
			pass
			out(""+'\tread("str")\n')
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
			out(""+'\tflag = 1\n')
		if flag: break
		test('$')
		if flag:
			pass
			out(""+'\tflag = 1\n')
			out(""+'\twhile flag:\n')
			indent+=1
			e_EX3()
			check_err()
			indent-=1
			out(""+'\tflag = 1\n')
		break

def e_EX2():
	global flag, indent
	while True:
		while True:
			e_EX3()
			if flag:
				pass
				out(""+'\tif flag:\n')
			if flag: break
			e_OUTPUT()
			if flag:
				pass
				out(""+'\tif True:\n')
			break
		if flag:
			pass
			indent+=1
			out(""+'\tpass\n')
			flag = 1
			while flag:
				while True:
					e_EX3()
					if flag:
						pass
						out(""+'\tcheck_err()\n')
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
		out(""+'\twhile True:\n')
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
						out(""+'\tif flag: break\n')
						e_EX2()
						check_err()
					break
			flag = 1
			check_err()
			out(""+'\tbreak\n')
			indent-=1
		break

def e_STATEMENT():
	global flag, indent
	while True:
		read("id")
		if flag:
			pass
			out(""+'def e_'+in_buf+'():\n')
			test('=')
			check_err()
			indent+=1
			out(""+'\tglobal flag, indent\n')
			e_EX1()
			check_err()
			indent-=1
			test(';')
			check_err()
			out(""+'\n')
		break

def e_PROGRAM():
	global flag, indent
	while True:
		out(""+'''import string
import sys
indent = 0
in_buf = ""
flag = 1
fn_gen = (f"fn_{i}()" for i in range(9999))
def genfn(): global fn; fn = next(fn_gen); return fn;
def escape(x):
	return x.replace(chr(39), chr(39)*3) if chr(39) in x and chr(10) in x else x
def out(x): print((chr(9)*indent + x[1:]) if ord(x[0])==9 else x, end="");
def err(): raise Exception("ERROR"); sys.exit(1)
def check_err():
	if not flag: raise Exception(f"ERROR inp={in_buf}"); sys.exit(1)
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
		if not ((t=="id" and n in string.printable[:62]+"_")
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
			out(""+'''
if len(sys.argv) < 2:
	print(f"Usage: {sys.argv[0]} <program_file>")
else:
	input = open(sys.argv[1], "rb")
	e_'''+in_buf+'()')
		break


if len(sys.argv) < 2:
	print(f"Usage: {sys.argv[0]} <program_file>")
else:
	input = open(sys.argv[1], "rb")
	e_PROGRAM()

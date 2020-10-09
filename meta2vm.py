#!/usr/bin/python

from sly import Lexer
import re

class inputLexer(Lexer):
    tokens = { NAME, STRING, SEMICOLON, L1, L2, ASTERISK,
        OR, EQUAL, LPAREN, RPAREN, SEQ, CBR}
    SEMICOLON = r'\.\,|;'
    CBR = '{|}'
    L1 = r'\*1'
    L2 = r'\*2'
    ASTERISK = r'\*'
    NAME   = r'[\.a-zA-Z][a-zA-Z0-9]*'
    STRING = r'\'[^\']*\''
    SEQ    = r'\$'
    OR     = r'/'
    EQUAL  = r'='
    LPAREN = r'\('
    RPAREN = r'\)'
    ignore = ' \t\n'
class progLexer(Lexer):
    tokens = { CMD, STRING, LABEL, ARG }
    ignore = ' '
    CMD = r'\n?\t[A-Z0-9]+'
    LABEL = r'\n[A-Z0-9]+'
    ARG = r'[A-Z0-9]+'
    STRING = r'\'[^\']*\''

class METAII:
    def parse(self, text):
        self.labels = {}
        self.program = []
        counter = 0
        toks = [t for t in progLexer().tokenize(text[:-1])]
        for tok in toks:
            value = tok.value.strip()
            if tok.type == 'CMD':
                self.program.append([value, ''])
                counter += 1
            elif tok.type == 'LABEL':
                self.labels[value] = counter
            else:
                self.program[-1][1] = value.strip("'")

    def __init__(self, program, input, output_filename):
        self.parse(program)
        self.SW = False
        self.IP = 0
        self.print_label = False
        self.indent = 0
        self.lastLabel = 0
        self.stack = [['', '', len(self.program)]]
        self.input = [t.value for t in inputLexer().tokenize(input)]
        self.output = []
        self.output_text = ''
        self.token_buffer = ''
        self.run()
        with open(output_filename, 'w') as file:
            file.write(self.output_text)

    def run(self):
        cc = 0
        while self.IP < len(self.program):
            saved = self.IP
            self.execute(self.program[self.IP])
            if saved == self.IP: # bad solution
                self.IP += 1
            cc += 1
        print(f'ran {cc} commands')

    def execute(self, command):
        inp = self.input[0] if len(self.input) else ''
        order = command[0]
        arg = command[1]
        #print(f'{self.IP}:\t{order}\t({arg})\t<- {inp}')
        if order == 'TST':
            #if '.meta3' in sys.argv[2]:
            #    print(f'test: {inp} == {arg}')
            if inp == arg:
                self.SW = True
                self.input.pop(0)
            else:
                self.SW = False
        elif order == 'ID':
            self.get_token('ID')
        elif order == 'NUM':
            self.get_token('NUM')
        elif order == 'SR':
            self.get_token('SR')
        elif order == 'CLL':
            #print(f'calling {arg}')
            self.stack.append(['', '', self.IP+1])
            self.IP = self.labels[arg]
        elif order == 'R':
            stack_frame = self.stack.pop()
            self.IP = stack_frame[2]
        elif order == 'SET':
            self.SW = True
        elif order == 'B':
            self.IP = self.labels[arg]
        elif order == 'BT':
            if self.SW:
                #print(f'branching t')
                self.IP = self.labels[arg]
        elif order == 'BF':
            if not self.SW:
                #print(f'branching f')
                self.IP = self.labels[arg]
        elif order == 'BE':
            if not self.SW:
                print(f'PANIC!')
                self.program = []
        elif order == 'CL':
            self.output.append(str(arg))
        elif order == 'CI':
            self.output.append(str(self.token_buffer))
        elif order == 'GN1':
            self.gen_label(0)
        elif order == 'GN2':
            self.gen_label(1)
        elif order == 'LB':
            self.print_label = True
        elif order == 'OUT':
            p = "".join(self.output)
            self.output = []
            if self.print_label:
                self.print_label = False
                if '.meta3' in sys.argv[2]:
                    self.indent += 1 if '{' in p else -1
                else:
                    self.output_text += f'{p}\n'
            else:
                if '.meta3' in sys.argv[2]:
                    if "'" in p and "\n" in p:
                        p = p.replace("'", "'''")
                    self.output_text += "\t"*self.indent + p + '\n'
                else:
                    self.output_text += f'\t{p}\n'
        elif order == 'ADR':
            if arg in self.labels:
                self.IP = self.labels[arg]
        elif order == 'END':
            pass
            #print('end')

    def gen_label(self, id):
        frame = self.stack[-1]
        if not frame[id]:
            self.lastLabel += 1
            frame[id] = f'L{self.lastLabel}'
        self.output.append(frame[id])

    def get_token(self, type):
        inp = self.input[0]
        if(type == 'ID' and re.match(r'[a-zA-Z][a-zA-Z]*', inp)
        or type == 'NUM' and re.match(r'\d+', inp)
        or type == 'SR' and re.match(r'\'[^\']*\'', inp)):
            self.SW = 1
            self.token_buffer = self.input.pop(0)
            #if '.meta3' in sys.argv[2]:
            #    print(f'read tok: ({type})\t{inp}')
        else:
            self.SW = 0

import sys
if len(sys.argv) < 3:
    print(f'Usage: {sys.argv[0]} <program> <input> <output>')
else:
    with open(sys.argv[2]) as file:
        prog = file.read()
    with open(sys.argv[1]+'.m2asm') as file:
        meta = METAII(file.read(), prog, sys.argv[3])

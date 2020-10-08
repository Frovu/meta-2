#!/usr/bin/python

import re

class METAII:
    def parse(self, text):
        self.labels = {}
        self.program = []
        counter = 0
        for line in text.splitlines():
            if line[0] == '\t' or line[0] == ' ':
                cmd = line.strip().split()[0]
                arg = "".join(line.strip().split()[1:]).strip("'")
                self.program.append((cmd, arg))
                counter += 1
            else:
                self.labels[line.strip()] = counter
        #for l in self.program: print(l)
        #print(self.labels)

    def __init__(self, program, input, output_filename):
        self.parse(program)
        self.SW = False
        self.IP = 0
        self.print_label = False
        self.lastLabel = 0
        self.stack = [['', '', len(self.program)]]
        self.input = input.split()
        self.output = []
        self.output_text = ''
        self.token_buffer = ''
        self.run()
        with open(output_filename, 'w') as file:
            file.write(self.output_text)

    def run(self):
        while self.IP < len(self.program):
            saved = self.IP
            self.execute(self.program[self.IP])
            if saved == self.IP: # bad solution
                self.IP += 1

    def execute(self, command):
        print(f'{self.IP}: {command}')
        inp = self.input[0]
        order = command[0]
        arg = command[1]
        if order == 'TST':
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
            print(f'calling {arg}')
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
                print(f'branching')
                self.IP = self.labels[arg]
        elif order == 'BF':
            if not self.SW:
                print(f'branching')
                self.IP = self.labels[arg]
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
            p = " ".join(self.output)
            self.output = []
            if self.print_label:
                self.output_text += f'{p}\n'
                self.print_label = False
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
        or type == 'SR' and re.match(r'\'[^\']+\'', inp)):
            self.SW = 1
            self.token_buffer = self.input.pop(0)
        else:
            self.SW = 0


with open('meta2.meta2') as file:
    prog = file.read()
with open('meta2.m2asm') as file:
    meta = METAII(file.read(), prog, 'test.m2asm')

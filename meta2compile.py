#!/usr/bin/python

from sly import Lexer, Parser

class metaLexer(Lexer):
    tokens = {  NAME, STRING, SEQ,
        OR, EQUAL, LPAREN, RPAREN, SEMICOLON,
        LABEL, LSYN, LEND, OUT, L1, L2, ASTERISK,
        LSTR, LNUM, LEMP, LID}
    ignore = ' \t\n'
    SEMICOLON = r'\.\,'
    LSYN = r'\.SYNTAX'
    LEND = r'\.END'
    OUT  = r'\.OUT'
    LID  = r'\.ID'
    LABEL= r'\.LABEL'
    LSTR = r'\.STRING'
    LNUM = r'\.NUMBER'
    LEMP = r'\.EMPTY'
    L1 = r'\*1'
    L2 = r'\*2'
    ASTERISK = r'\*'
    NAME   = r'[\.a-zA-Z][a-zA-Z0-9]*'
    STRING = r'\'[^\']+\''
    SEQ    = r'\$'
    OR     = r'/'
    EQUAL  = r'='
    LPAREN = r'\('
    RPAREN = r'\)'

def label(s): # vm assembly label
    return f'{s}\n'
def inst(s): # vm assembly instruction
    return f'\t{s}\n'

class metaParser(Parser):
    tokens = metaLexer.tokens

    def labelsGen(count):
        while True:
            yield f'L{count}'
            count += 1

    labels = labelsGen(1)

    @_('LSYN NAME rule_list LEND')
    def program(self, p):
        print('-> program')
        return inst('ADR '+p.NAME) + p.rule_list + inst('END')

    @_('rule')
    def rule_list(self, p):
        return p.rule
    @_('rule rule_list')
    def rule_list(self, p):
        return p.rule + p.rule_list

    @_('NAME EQUAL ex1 SEMICOLON')
    def rule(self, p):
        print('-------> rule')
        return label(p.NAME) + p.ex1 + inst('R')

    @_('L1')
    def out1(self, p):
        return inst('GN1')
    @_('L2')
    def out1(self, p):
        return inst('GN2')
    @_('ASTERISK')
    def out1(self, p):
        return inst('CI')
    @_('STRING')
    def out1(self, p):
        return inst('CL '+p.STRING)

    @_('out1_list out1')
    def out1_list(self, p):
        return p.out1 + p.out1_list
    @_('out1')
    def out1_list(self, p):
        return p.out1

    @_('OUT LPAREN out1_list RPAREN')
    def output(self, p):
        print('-> output')
        return p.out1_list + inst('OUT')
    @_('LABEL LPAREN out1 RPAREN')
    def output(self, p):
        return inst('LB') + p.out1 + inst('OUT')


    @_('NAME')
    def ex3(self, p):
        return inst('CLL '+p[0])
    @_('LID')
    def ex3(self, p):
        return inst('ID')
    @_('STRING')
    def ex3(self, p):
        return inst('TST '+p[0])
    @_('LNUM')
    def ex3(self, p):
        return inst('NUM')
    @_('LSTR')
    def ex3(self, p):
        return inst('SR')
    @_('LPAREN ex1 RPAREN')
    def ex3(self, p):
        return p.ex1
    @_('LEMP')
    def ex3(self, p):
        return inst('SET')
    @_('SEQ ex3')
    def ex3(self, p):
        ll = next(self.labels)
        return label(ll) + p.ex3 + inst('BT '+ll) + inst('SET')

    @_('ex3')
    def ex2_h(self, p):
        return p.ex3 + inst('BE')
    @_('output')
    def ex2_h(self, p):
        print('--> ex2_h')
        return p.output
    @_('output ex2_h', 'ex3 ex2_h')
    def ex2_h(self, p):
        print('--> ex2_h nested')
        return p[0] + inst('BE') + p.ex2_h


    @_('ex3 ex2_h')
    def ex2(self, p):
        print('---> ex2')
        ll = next(self.labels)
        self.lastl = next(self.labels)
        return p.ex3 + inst('BF '+ll) +  p.ex2_h + label(ll)
    @_('ex3')
    def ex2(self, p):
        print('---> ex2')
        ll = next(self.labels)
        self.lastl = next(self.labels)
        return p.ex3 + inst('BF '+ll) + label(ll)
    @_('output ex2_h')
    def ex2(self, p):
        print('---> ex2')
        self.lastl = next(self.labels)
        return p.output + p.ex2_h
    @_('output')
    def ex2(self, p):
        print('---> ex2')
        self.lastl = next(self.labels)
        return p.output


    @_('ex1_h OR ex2')
    def ex1_h(self, p):
        print('----> ex1h 2')
        ll = self.lastl
        return p.ex1_h + inst('BT '+ll) + p.ex2
    @_('OR ex2')
    def ex1_h(self, p):
        print('----> ex1h 1')
        ll = self.lastl
        return inst('BT '+ll) + p.ex2

    @_('ex2 ex1_h')
    def ex1(self, p):
        print('-----> ex1 with /')
        ll = self.lastl
        return p.ex2 + p.ex1_h + label(ll)
    @_('ex2')
    def ex1(self, p):
        print('-----> ex1')
        ll = self.lastl
        return p.ex2 + label(ll)




text = '''.SYNTAX PROGRAM
EX3 = .ID .OUT('LD ' *) / '(' EX1 ')' .,
EX2 = EX3 $ ('*' EX3 .OUT('MLT')) .,
EX1 = EX2 $ ('+' EX2 .OUT('ADD')) .,
.END
'''

lexer = metaLexer()
for tok in lexer.tokenize(text):
    print(f'{tok.value}\t\t{tok.type}')
parser = metaParser()
res = parser.parse(lexer.tokenize(text))
print()
print()
print(res)

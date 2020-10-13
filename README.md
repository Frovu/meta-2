# META II
me studying compiler writing languages with META II

## Source
http://ibm-1401.info/Meta-II-schorre.pdf

## Meta 3 Racket

Meta II that is being compiled to Racket(Scheme) script.

### Meta 3 Racket files

| File          | Contents                                                      |
| -----------   | --------------------------------------------------------------|
| `meta.rkt`    | Helper module mainly with i/o procedures                      |
| `meta3l.m3l`  | First version written in its own language                     |
| `meta3r.m3r`  | Improved/optimized version written in its own language        |
| `meta3l.rkt`  | My first meta3 compiler written by hand                       |
| `o_meta3l.rkt`| First version compiled itself                                 |
| `o_meta3r.rkt`| Better version compiled itself                                |

## Meta 2

Meta II with virtual machine simulating one from the paper

### Meta 3 files

| File          | Contents                                                      |
| -----------   | --------------------------------------------------------------|
| `meta2vm.py`  | My own Meta II virtual machine                                |
| `meta2compile.py` | My own compiler for META II language (using sly lex/yacc) |
| `meta2.m2asm` | Python compiler output for `meta2.meta2`                      |
| `meta2.meta2` | Original "META II written in its own language"                |
| `test.m2asm`  | Output of META II (compiled by python) compiling itself in vm |

## Meta 3

My Meta 3 is compiler writing language thats being compiled to standalone python code keeping syntax very close to original META II syntax

transitioned from meta2 to meta3 with something like:
```
./meta2vm.py meta2 meta3.meta2 meta3.m2asm
./meta2vm.py meta3 meta3.meta3 meta3.py
python meta3.py meta3.meta3 > meta3m.py
```

### Meta 3 files

| File          | Contents                                                      |
| -----------   | --------------------------------------------------------------|
| `meta3.meta2` | Meta 3 compiler written in META II  language                  |
| `meta3.m2asm` | Meta 3 compiler compiled for meta2vm                          |
| `meta3.meta3` | Meta 3 written in its own language                            |
| `meta3.py`    | Meta 3 compiled with META II runnning `meta3.m2asm`           |
| `meta3m.py`   | Meta 3 compiled itself                                        |

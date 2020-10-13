#lang racket
(require "meta.rkt")

(define (e-output)
	(cond
		[(if (test "<") (begin
			(output "(output")
			(while-ok (lambda () (cond
				[(if (test "*") (begin
					(output " buffer") #t) #f)]
				[(if (read-str) (begin
					(output " " buffer) #t) #f)]
				[else #f])))
			(unless (test ">") (err))
			(output ")")) #f)]
		[else #f]))

(define (e-exp_atom)
	(cond
		[(if (read-id) (begin
			(output "(e-" buffer ")") #t) #f)]
		[(if (read-str) (begin
			(output "(test " buffer ")") #t) #f)]
		[(if (test ".ID") (begin
			(output "(read-id)") #t) #f)]
		[(if (test ".NUMBER") (begin
			(output "(read-num)") #t) #f)]
		[(if (test ".STRING") (begin
			(output "(read-str)") #t) #f)]
		[(if (test ".EMPTY") #t #f)]
		[(if (test "(") (begin
			(e-expression) (unless (test ")") (err)) #t) #f)]
		[(if (test "$") (begin
			(output "(while-ok (lambda () ")
			(e-exp_atom)
			(output "))") #t) #f)]
		[else #f]))

(define (e-exp_body)
	(output "\n\t\t\t")
	(while-ok (lambda () (cond
		[(if (e-output)  (output "\n\t\t\t") #f)]
		[(if (e-exp_atom)(output "\n\t\t\t") #f)]
		[else #f])))
	#t)

(define (e-exp_option)
	(cond
		[(if (e-output) (begin
			(output "(begin ")
			(e-exp_body)
			(output " #t)") #t) #f)]
		[else
			(output "(if ")
			(e-exp_atom)
			(output " (begin ")
			(e-exp_body)
			(output " #t) #f)") #t]))

(define (e-expression)
	(output "(cond\n\t\t[")
	(e-exp_option)
	(output "]")
	(while-ok (lambda () (cond
		[(if (test "/") (begin
			(output "\n\t\t[")
			(e-exp_option)
			(output "]")) #f)]
		[else #f])))
	(output "\n\t\t[else #f])") #t)

(define (e-statement)
	(if (read-id) (begin
	(output "\n(define (e-" buffer ")\n\t")
	(test "=")
	(e-expression)
	(test ";")
	(output ")\n") #t) #f))

(define (e-compiler)
	(output "#lang racket\n(require \"meta.rkt\")\n")
	(while-ok e-statement)
	(test ".SYNTAX")
	(read-id)
	(output "\n(unless (e-" buffer ") \"\\nfailed\")"))

(unless (e-compiler) "\nfailed")
(newline)

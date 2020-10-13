#lang racket
(require "meta.rkt")

(define (e-output)
	(cond
		[(if (test "<") (begin
			(output "(output")
			(while-ok (lambda () (cond
		[(if (test "*") (begin
			(output " buffer")
			#t) #f)]
		[(if (read-str) (begin
			(output " " buffer)
			#t) #f)]
		[else #f])))
			(unless (test ">") (err))
			(output ")")
			#t) #f)]
		[else #f]))

(define (e-exp_atom)
	(cond
		[(if (read-id) (begin
			(output "(e-" buffer ")")
			#t) #f)]
		[(if (read-str) (begin
			(output "(test " buffer ")")
			#t) #f)]
		[(if (test ".ID") (begin
			(output "(read-id)")
			#t) #f)]
		[(if (test ".NUMBER") (begin
			(output "(read-num)")
			#t) #f)]
		[(if (test ".STRING") (begin
			(output "(read-str)")
			#t) #f)]
		[(if (test "(") (begin
			(unless (e-expression) (err))
			(unless (test ")") (err))
			#t) #f)]
		[(if (test ".EMPTY") (begin
			(output "#t")
			#t) #f)]
		[(if (test "$") (begin
			(output "(while-ok (lambda () ")
			(unless (e-exp_atom) (err))
			(output "))")
			#t) #f)]
		[else #f]))

(define (e-exp_atom_crit)
	(cond
		[(if (read-id) (begin
			(output "(unless (e-" buffer ") (err))")
			#t) #f)]
		[(if (read-str) (begin
			(output "(unless (test " buffer ") (err))")
			#t) #f)]
		[(if (test ".ID") (begin
			(output "(unless (read-id) (err))")
			#t) #f)]
		[(if (test ".NUMBER") (begin
			(output "(unless (read-num) (err))")
			#t) #f)]
		[(if (test ".STRING") (begin
			(output "(unless (read-str) (err))")
			#t) #f)]
		[(if (test "(") (begin
			(output "(if ")
			(unless (e-expression) (err))
			(unless (test ")") (err))
			(output " #t (err))")
			#t) #f)]
		[(if (test ".EMPTY") (begin
			(output "#t")
			#t) #f)]
		[(if (test "$") (begin
			(output "(while-ok (lambda () ")
			(unless (e-exp_atom) (err))
			(output "))")
			#t) #f)]
		[else #f]))

(define (e-exp_body)
	(cond
		[(output "\n\t\t\t")(begin
			(while-ok (lambda () (cond
		[(if (e-output) (begin
			(output "\n\t\t\t")
			#t) #f)]
		[(if (e-exp_atom_crit) (begin
			(output "\n\t\t\t")
			#t) #f)]
		[else #f])))
			#t)]
		[else #f]))

(define (e-exp_option)
	(cond
		[(if (e-output) (begin
			(output "(begin")
			(unless (e-exp_body) (err))
			(output "#t)")
			#t) #f)]
		[(output "(if ")(begin
			(unless (e-exp_atom) (err))
			(output " (begin")
			(unless (e-exp_body) (err))
			(output "#t) #f)")
			#t)]
		[else #f]))

(define (e-expression)
	(cond
		[(output "(cond\n\t\t[")(begin
			(unless (e-exp_option) (err))
			(output "]")
			(while-ok (lambda () (cond
		[(if (test "/") (begin
			(output "\n\t\t[")
			(unless (e-exp_option) (err))
			(output "]")
			#t) #f)]
		[else #f])))
			(output "\n\t\t[else #f])")
			#t)]
		[else #f]))

(define (e-statement)
	(cond
		[(if (read-id) (begin
			(output "\n(define (e-" buffer ")\n\t")
			(unless (test "=") (err))
			(unless (e-expression) (err))
			(unless (test ";") (err))
			(output ")\n")
			#t) #f)]
		[else #f]))

(define (e-compiler)
	(cond
		[(output "#lang racket\n(require \"meta.rkt\")\n")(begin
			(while-ok (lambda () (e-statement)))
			(unless (test ".SYNTAX") (err))
			(unless (read-id) (err))
			(output "\n(unless (e-" buffer ") \"\\nfailed\")")
			#t)]
		[else #f]))

(unless (e-compiler) "\nfailed")
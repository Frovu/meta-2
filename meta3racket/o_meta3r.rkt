#lang racket
(require "meta.rkt")

(define (e-output)
	(cond
		[(if (test "<") (if (not (and
			(output "(output")(while-ok (lambda () (cond
		[(if (test "*") (if (not (and
			(output " buffer"))) (err) #t) #f)]
		[(if (read-str) (if (not (and
			(output " " buffer))) (err) #t) #f)]
		[else #f])))
			(test ">")
			(output ")"))) (err) #t) #f)]
		[else #f]))

(define (e-exp_atom)
	(cond
		[(if (read-id) (if (not (and
			(output "(e-" buffer ")"))) (err) #t) #f)]
		[(if (read-str) (if (not (and
			(output "(test " buffer ")"))) (err) #t) #f)]
		[(if (test ".ID") (if (not (and
			(output "(read-id)"))) (err) #t) #f)]
		[(if (test ".NUMBER") (if (not (and
			(output "(read-num)"))) (err) #t) #f)]
		[(if (test ".STRING") (if (not (and
			(output "(read-str)"))) (err) #t) #f)]
		[(if (test "(") (if (not (and
			(e-expression)
			(test ")")
			)) (err) #t) #f)]
		[(if (test ".EMPTY") (if (not (and
			(output "#t"))) (err) #t) #f)]
		[(if (test "$") (if (not (and
			(output "(while-ok (lambda () ")(e-exp_atom)
			(output "))"))) (err) #t) #f)]
		[else #f]))

(define (e-exp_body)
	(cond
		[(output " (if (not (and\n\t\t\t") (if (not (and
			(while-ok (lambda () (cond
		[(if (e-output) (if (not (and
			)) (err) #t) #f)]
		[(if (e-exp_atom) (if (not (and
			(output "\n\t\t\t"))) (err) #t) #f)]
		[else #f])))
			(output ")) (err) #t)"))) (err) #t)]
		[else #f]))

(define (e-exp_option)
	(cond
		[(if (e-output) (if (not (and
			(e-exp_body)
			)) (err) #t) #f)]
		[(output "(if ") (if (not (and
			(e-exp_atom)
			(e-exp_body)
			(output " #f)"))) (err) #t)]
		[else #f]))

(define (e-expression)
	(cond
		[(output "(cond\n\t\t[") (if (not (and
			(e-exp_option)
			(output "]")(while-ok (lambda () (cond
		[(if (test "/") (if (not (and
			(output "\n\t\t[")(e-exp_option)
			(output "]"))) (err) #t) #f)]
		[else #f])))
			(output "\n\t\t[else #f])"))) (err) #t)]
		[else #f]))

(define (e-statement)
	(cond
		[(if (read-id) (if (not (and
			(output "\n(define (e-" buffer ")\n\t")(test "=")
			(e-expression)
			(test ";")
			(output ")\n"))) (err) #t) #f)]
		[else #f]))

(define (e-compiler)
	(cond
		[(output "#lang racket\n(require \"meta.rkt\")\n") (if (not (and
			(while-ok (lambda () (e-statement)))
			(test ".SYNTAX")
			(read-id)
			(output "\n(unless (e-" buffer ") \"\\nfailed\")"))) (err) #t)]
		[else #f]))

(unless (e-compiler) "\nfailed")
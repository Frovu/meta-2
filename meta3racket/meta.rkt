#lang racket

(provide err)
(provide skip-whitespace)
(provide read-str)
(provide read-num)
(provide read-id)
(provide test)
(provide output)
(provide while-ok)
(provide buffer)

(cond [(< (vector-length (current-command-line-arguments)) 2)
	(display "please provide input and output files as arguements\n")
	(exit 1)])
(define in-f (vector-ref (current-command-line-arguments) 0))
(define out-f (vector-ref (current-command-line-arguments) 1))
(current-input-port (open-input-file in-f))
(current-output-port (open-output-file out-f #:exists 'replace))

(define buffer "") ; input token buffer
(define (err)
	(display "error occured")
	(exit 1))
(define (skip-whitespace)
	(let ([ch (peek-char )])
		(unless (eof-object? ch)
			(when (char-whitespace? ch)
				(read-char )
				(skip-whitespace)))))

(define (read-it check res)
	(let ([ch (peek-char)])
		(if (check ch) (begin (read-char)
			(read-it check (string-append res (string ch))))
			(begin (set! buffer res) res))))
(define (read-str)
	(skip-whitespace)
	(let ([ch (peek-char)])
		(if (eof-object? ch) #f
			(if (char=? ch #\')
				(begin (read-char)
					(let ([a (string-replace (string-append
						(read-it (lambda (c) (not (char=? c #\'))) (string ch))
						(string (read-char))) "'" "\"")])
						(set! buffer a) a))
				#f))))
(define (read-num)
	(skip-whitespace)
	(let ([ch (peek-char)])
		(if (eof-object? ch) #f
			(if (char-numeric? ch)
				(read-it (lambda (c) (char-numeric? c)) (string))
				#f))))
(define (read-id)
	(skip-whitespace)
	(let ([ch (peek-char)])
		(if (eof-object? ch) #f
			(if (char-alphabetic? ch)
				(read-it (lambda (c)
						(or (char=? c #\_) (char-alphabetic? c) (char-numeric? c)))
					(string))
				#f))))

(define (test str)
	(skip-whitespace)
	(let ([peek-s (peek-string (string-length str) 0)])
		(if (eof-object? peek-s) #f
			(if (string=? str peek-s)
				(read-string (string-length str))
				#f))))

(define (output . args)
	(printf (string-join args "")))

(define (while-rec check i)
	(cond [(> i 10) #f]
		[(check) (while-rec check (add1 i))]
		[else #t]))
(define (while-ok check)
  (while-rec check 0))

#lang racket
(require racket/trace)
(current-input-port (open-input-file "test"))

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
			res)))

(define (read-str)
	(skip-whitespace)
	(let ([ch (peek-char)])
		(if (eof-object? ch) #f
			(if (char=? ch #\')
				(begin (read-char)
					(string-append
						(read-it (lambda (c) (not (char=? c #\'))) (string ch))
						(string (read-char))))
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

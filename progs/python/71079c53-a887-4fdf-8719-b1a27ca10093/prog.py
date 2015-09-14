#!/usr/bin/python
def number(n):
	result = []
	a = 0
	b = 1
	result.append(a)
	result.append(b)
	for i in range(n-1):
		c = a + b
		a = b
		b = c
		result.append(c)
	print result
number(1024)
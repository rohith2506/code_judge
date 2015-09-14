#!/usr/bin/python
''' This is Bubble sort preogram '''

def bubble(j):
	for p in range(0,len(j)):
		for i in range(0,p):
			if j[i] > j[i + 1]:
				number = j[i]
				j[i] = j[i+1]
				j[i + 1] = number


j = [5,2,3,4,5,6,7]
bubble(j)
print j
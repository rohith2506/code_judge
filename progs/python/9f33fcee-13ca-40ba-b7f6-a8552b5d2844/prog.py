#!/usr/bin/python
def all_perms(elements):
    if len(elements) <=1:
        yield elements
    else:
        for perm in all_perms(elements[1:]):
            for i in range(len(elements)):
                yield perm[:i] + elements[0:1] + perm[i:]

elements = [1,2,3,4]
results = all_perms(elements)
for result in results:
	print sum(result),
print('hello world')
# % operator - multiples of 3 or 5
# go to 100 - for loop
# print the numbers - print
# validate - output single constraint (proper at 3, 5, etc.)
# - output no constraints (proper at any num)
# - partial output (proper sequences)
# - format - type of output

def fizzbuzzgen(i):
    output = ''
    if(i % 3 == 0): output += 'fizz'
    if(i % 5 == 0): output += 'buzz'
    if output == '': return i
    return output

def fizzbuzz(n):
    for i in range(1,101): print(fizzbuzzgen(i))

"""This is a Python program that generates a Fibonacci sequence"""

def fib(n):
    """Calculate the n-th Fibonacci number"""
    if n == 0 or n == 1:
        return   n
    else:
        return fib(n-1) + fib(n-2)
def print_fib_sequence():
    """Print the first 10 Fibonacci numbers"""
    for i in range(1, 11):
        print('i: ' + str(i) + ' fib: ' + str(fib(i - 1)))

print('Fibonacci from 1 to 10: ')
print_fib_sequence()

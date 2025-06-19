from traceback import print_tb

from pyexpat.errors import messages

greeting = "hello"

def greet(name):
    global message
    message = f"{greeting}, {name}!"
    print(message)

greet("Dalmat")

print(message)
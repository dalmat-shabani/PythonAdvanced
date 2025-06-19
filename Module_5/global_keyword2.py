greeting= "Hello"
name = "Dalmat"

def greet():
    global greeting
    greeting = "Goodbye"
    name = "Dalmati"
    message = f"{greeting}, {name}"
    print(message)

greet()
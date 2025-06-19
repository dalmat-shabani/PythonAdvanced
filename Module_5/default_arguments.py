def greet_person(name, greeting="Hello"):
    message = f"{greeting}, {name}"
    return message

default_greeting = greet_person("Dalmat")

custom_greeting = greet_person("Dalmat", "Hi")

print(default_greeting)
print(custom_greeting)
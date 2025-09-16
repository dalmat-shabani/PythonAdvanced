def add (x, y):
    return x + y

def concantenate(x, y):
    return str(x) + str(y)

def operate (operation, x, y):
    return operation (x, y)

result_concantenate = operate(concantenate, "Hello", "world")
results_sum = operate(add, 3, 5)

print("Result of the sum: ", results_sum)
print("Result of the concetenate: ", result_concantenate)
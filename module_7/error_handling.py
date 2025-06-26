try:
    result = 10/0


except ZeroDivisionError:
    print("You cant divide by zero")



fruits = {"apple":5, "banana":7, "orange": 3}


try:
    print(fruits["cherry"])
except KeyError:
    print("The key dosent exist in the dictionary")



text = "This is not a number"

try:
    text_to_int = int(text)
except Exception as e:
    print("An error occoured while parsing the data: " ,e)



try:
    result = 10/2
except ZeroDivisionError:
    print("You cant divide by zero")
else:
    print("DIvision successful. Result: " result)


try:
    result = 10/0
except ZeroDivisionError:
    print("You cant divide by zero")
finally:
    print("Finally block executed")




def divide_numbers(a,b):
    try:
        result = a/b
        print("Result of division:" result)
    except ZeroDivisionError
        print("You cant divide by zero")
    except TypeError
        print("Invalid type for division")
    except Exception as e:
        print(f"Unexcpected error:{e}")

divide_numbers(10,2)
divide_numbers(10,0)
divide_numbers(10,'2')
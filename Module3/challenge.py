loyalty_set = {"James", "arthur", "Steph"}

loyal = "Steph"

print(loyal in loyalty_set)

my_list = ["bananas", "apples", "oranges"]

my_touple = (1,2,3)


print(my_list)
print(my_touple)
print(loyalty_set)



student_gpa = 4.0
student_test = 95

if student_gpa >= 3.6 and student_test > 65 :
    print("Full scolarship!!")
elif student_gpa >=3.5 and  50 <= student_test <= 65:
    print("Parital scholarship")
elif student_gpa >=3.5 and student_test < 50 :
    print("Not eligible for a scholarship")
else:
    print("Not eligible for a scholarship")
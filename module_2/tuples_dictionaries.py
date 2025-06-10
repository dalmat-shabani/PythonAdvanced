grade = {
    ("John", "Math"): 5,
    ("Alice", "Biology"): 4,
    ("Bob", "Chemistry"): 3,
    ("Eve", "Music"): 5,
    ("Johna", "English"): 2
}

john_math = grade[("John", "Math")]
print("John's grade in math is ",john_math)

grade[("Bob", "Math")] = 3
print(grade)


keys = list(grade.keys())


student, subject = keys[0]
print(student,"'s grade in ",subject, "is", john_math)


class Student:
    def __init__(self, name , age):
        self.__name = name
        self.__age = age


    @property
    def name(self ):
        return self.__name

    @name.setter
    def name(self, name):
        self.__name = name

    @property
    def age(self):
        return self.__age

    @age.setter
    def age(self, age):
        self.__age = age



student2 = Student("Alice", 17)

print("Name: ", student2.name)
print("Age: ", student2.age)

student2.name = "Bob"
student2.age = 18
print("Updated Name: ", student2.name)
print("Updated Age: ", student2.age)
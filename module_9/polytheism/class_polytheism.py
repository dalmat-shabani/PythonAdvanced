class Dog:
    def __innit__(self, name):
        self.name = name

    def sound(self):
        print(f"{self.name} makes the sound: Woof!")


class Cat:
    def __innit__(self, name):
        self.name = name

    def sound(self):
        print(f"{self.name} makes the sound: Meow!")


class Bird:
    def __innit__(self, name):
        self.name = name

    def sound(self):
        print(f"{self.name} makes the sound: Chrio!")


dog = Dog("Buddy")
cat = Cat("Whiskers")
bird = Bird("Tweetie")

for animal in (dog,cat , bird):
    animal.sound()
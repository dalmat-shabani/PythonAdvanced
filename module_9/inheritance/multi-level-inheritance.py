class Vehicle:
    def __init__(self, make, model, year):
        self.make = make
        self.model = model
        self.year = year

    def display_info(self):
        print(f"Make: {self.make}, Model: {self.model}, Year: {self.year}")

class Car(Vehicle):
    def __init__(self, make, model, year, body_style):
        super().__init__(make, model, year)
        self.body_style = body_style

class ElectricCar(Car):
    def __init__(self, make, model, year, body_style, battery_capacity):
        super().__init__(make,model,year,body_style)
        self.battery_capacity = battery_capacity


    def charge(self):
        print("Charging the electric car")




tesla = ElectricCar("Tesla", "Cybertruck", 2010 , "triangular" , 94.3)
tesla.display_info()
print("Body style: ", tesla.body_style)
print("Battery Capacity: ", tesla.battery_capacity)
tesla.charge()
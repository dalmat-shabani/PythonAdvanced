# bmi_app.py
from typing import List, Optional


class Person:
    """
    Base class representing a person. Encapsulates weight and height using properties.
    Subclasses should override calculate_bmi() if needed.
    """

    def __init__(self, name: str, age: int, weight_kg: float, height_m: float):
        self.name = name
        self.age = int(age)
        self._weight_kg = None
        self._height_m = None
        self.weight_kg = weight_kg
        self.height_m = height_m

    # weight property with simple validation
    @property
    def weight_kg(self) -> float:
        return self._weight_kg

    @weight_kg.setter
    def weight_kg(self, value: float):
        if value <= 0:
            raise ValueError("Weight must be a positive number (kg).")
        self._weight_kg = float(value)

    # height property with simple validation
    @property
    def height_m(self) -> float:
        return self._height_m

    @height_m.setter
    def height_m(self, value: float):
        if value <= 0:
            raise ValueError("Height must be a positive number (m).")
        self._height_m = float(value)

    def calculate_bmi(self) -> float:
        """Default adult formula: weight / (height^2). Subclasses may override."""
        bmi = self.weight_kg / (self.height_m ** 2)
        return bmi

    def get_bmi_category(self, bmi: Optional[float] = None) -> str:
        """Return BMI category based on the BMI value provided (or calculated)."""
        if bmi is None:
            bmi = self.calculate_bmi()

        if bmi < 18.5:
            return "Underweight"
        elif 18.5 <= bmi < 25.0:
            return "Healthy Weight"
        elif 25.0 <= bmi < 30.0:
            return "Overweight"
        else:
            return "Obesity"

    def print_info(self):
        """Print person's basic info and BMI results."""
        bmi_value = self.calculate_bmi()
        category = self.get_bmi_category(bmi_value)
        print(f"Name: {self.name}")
        print(f"Age: {self.age}")
        print(f"Weight (kg): {self.weight_kg:.2f}")
        print(f"Height (m): {self.height_m:.2f}")
        print(f"BMI: {bmi_value:.2f}")
        print(f"Category: {category}")


class Adult(Person):
    """Adult uses the standard BMI formula (no change)."""
    pass  # Inherits everything from Person unchanged


class Child(Person):
    """Child uses a modified BMI formula: BMI * 1.3 according to spec."""
    def calculate_bmi(self) -> float:
        base_bmi = super().calculate_bmi()
        adjusted_bmi = base_bmi * 1.3
        return adjusted_bmi


class BMIApp:
    """
    Application class to collect people, compute and print BMI results.
    Methods:
    - add_person(person)
    - collect_user_data()
    - print_results()
    - run()
    """
    def __init__(self):
        self.people: List[Person] = []

    def add_person(self, person: Person):
        self.people.append(person)

    def collect_user_data(self):
        """
        Collects one (or more) user entries from the console.
        Keeps asking whether user wants to add another person.
        """
        print("=== BMI App - enter person data ===")
        while True:
            try:
                name = input("Name: ").strip()
                age_str = input("Age (years): ").strip()
                weight_str = input("Weight (kg): ").strip()
                height_str = input("Height (meters, e.g. 1.75): ").strip()

                # Basic parsing and validation
                age = int(age_str)
                weight = float(weight_str)
                height = float(height_str)

                # Decide whether Adult or Child
                # Common convention: child if age < 18 (you can change threshold as you like)
                if age < 18:
                    person = Child(name=name, age=age, weight_kg=weight, height_m=height)
                else:
                    person = Adult(name=name, age=age, weight_kg=weight, height_m=height)

                self.add_person(person)
                print(f"Added: {name} ({'Child' if age < 18 else 'Adult'})\n")
            except ValueError as e:
                print(f"Invalid input: {e}. Please try again.\n")
                continue

            again = input("Add another person? (y/n): ").strip().lower()
            if again not in ("y", "yes"):
                break

    def print_results(self):
        """Show BMI results for all added people."""
        if not self.people:
            print("No people to show. Add people first.")
            return

        print("\n=== BMI RESULTS ===")
        for i, person in enumerate(self.people, start=1):
            print(f"\nPerson #{i}")
            person.print_info()

    def run(self):
        """High-level runner for the CLI app."""
        self.collect_user_data()
        self.print_results()
        print("\nThank you for using BMI App.")


if __name__ == "__main__":
    app = BMIApp()
    app.run()

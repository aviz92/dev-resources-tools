# property_cachedproperty.py

# 📌 Principle:
# The Property and CachedProperty patterns are used to define methods that act like attributes (i.e., they can be accessed without parentheses).
# @property: The full_name method is defined as a property. It can be accessed as if it were an attribute (emp.full_name), but it actually calls a method behind the scenes.
# @cached_property: The annual_salary method is defined as a cached property. It’s computed once and then cached for future access, avoiding redundant calculations.
# These patterns help keep the code clean and allow for the logic to be abstracted away, treating computed values as if they were simple attributes.

from functools import cached_property


class Employee:
    def __init__(self, first_name, last_name, hourly_rate):
        self.first_name = first_name
        self.last_name = last_name
        self.hourly_rate = hourly_rate

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    @cached_property
    def annual_salary(self):
        print("Calculating annual salary...")
        return self.hourly_rate * 40 * 52  # Assuming 40 hours/week, 52 weeks/year


def main():
    emp = Employee("John", "Doe", 25)

    # Using the property
    print("Full Name:", emp.full_name)

    # Using the cached_property
    print("Annual Salary:", emp.annual_salary)
    print("Annual Salary again:", emp.annual_salary)  # This won't recalculate


if __name__ == "__main__":
    main()

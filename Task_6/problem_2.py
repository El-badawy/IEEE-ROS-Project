class Calculator:
    def add(self, a, b):
        return a + b

    def subtract(self, a, b):
        return a - b

    def multiply(self, a, b):
        return a * b


calc = Calculator()

print(calc.add(5, 3))
print(calc.subtract(5, 3))
print(calc.multiply(5, 3))
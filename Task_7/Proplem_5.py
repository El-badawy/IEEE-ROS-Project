import math

class Shape:
    def area(self):
        pass

class Circle(Shape):
    def __init__(self, radius):
        self.radius = radius

    def area(self):
        return math.pi * self.radius ** 2

class Square(Shape):
    def __init__(self, side):
        self.side = side

    def area(self):
        return self.side ** 2

def print_area(shape_object):
    print(f"Area = {shape_object.area():.2f}")

radius = float(input("Enter circle radius: "))
side = float(input("Enter square side: "))

circle = Circle(radius)
square = Square(side)

print_area(circle)
print_area(square)
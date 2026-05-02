class Rectangle:
    def __init__(self, width=5, height=3):
        self.width = width
        self.height = height

    def get_area(self):
        return self.width * self.height


rect = Rectangle()
print(rect.get_area())
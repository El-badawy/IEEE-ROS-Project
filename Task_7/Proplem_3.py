class Passenger:
    def __init__(self, name, age):
        self.name = name
        self.age = age

class Flight:
    def __init__(self, flight_number):
        self.flight_number = flight_number
        self.passengers = []

    def add_passenger(self, passenger_obj):
        self.passengers.append(passenger_obj)

    def show_passengers(self):
        print(f"\nFlight {self.flight_number} Passengers:")
        for p in self.passengers:
            print(f"  - {p.name}, Age: {p.age}")

flight = Flight("EG-101")

num = int(input("How many passengers? "))
for i in range(num):
    name = input(f"Enter passenger {i+1} name: ")
    age = int(input(f"Enter passenger {i+1} age: "))
    passenger = Passenger(name, age)
    flight.add_passenger(passenger)

flight.show_passengers()
print(f"\nTotal passengers: {len(flight.passengers)}")
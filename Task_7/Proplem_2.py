class Classroom:
    def __init__(self):
        self.students = []

    def add_student(self, name):
        self.students.append(name)

    def count_students(self):
        return len(self.students)
    
classroom = Classroom()

num = int(input("How many students? "))

for i in range(num):
    name = input(f"Enter student {i+1} name: ")
    classroom.add_student(name)

print(f"\nTotal students: {classroom.count_students()}")
print("Students:", classroom.students)


print(classroom.count_students())  
print(classroom.students)              


        
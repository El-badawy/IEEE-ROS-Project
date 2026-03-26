numbers = []

while True:
    num = float(input("Enter number : "))
    
    if num == -1:
        break
    
    numbers.append(num)

if numbers: 
    print("Largest:", max(numbers))
    print("Smallest:", min(numbers))
else:
    print("No numbers entered")
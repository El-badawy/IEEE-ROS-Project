import random

def pick_winner(names):
    if not names:
        return "Error: The list is empty!"
    winner = random.choice(names)
    return f" Congratulations, {winner}! You are the winner!"

players = ["Ahmed", "Ali", "Sara"]
print(pick_winner(players))
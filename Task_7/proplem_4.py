class Player:
    def __init__(self, name, score):
        self.name = name
        self.score = score

class Team:
    def __init__(self):
        self.members = []

    def add_player(self, player_object):
        self.members.append(player_object)


p1 = Player("Ahmed", 5)
p2 = Player("Mahmoud", 8)
p3 = Player("Ali", 2)

team = Team()
team.add_player(p1)
team.add_player(p2)
team.add_player(p3)

for player in team.members:
    print(f"Name: {player.name}, Score: {player.score}")
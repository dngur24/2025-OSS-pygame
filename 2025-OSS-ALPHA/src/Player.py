import random
import Horse

class Player:
    def __init__(self, player_id, num_horses, board):
        self.player_id = player_id
        self.horses = [Horse.Horse(i + 1, board) for i in range(num_horses)]

    def roll_dice(self):
        return random.choice([-1, 1, 2, 3, 4, 5])

    def __repr__(self):
        return f"Player {self.player_id} with horses: {self.horses}"
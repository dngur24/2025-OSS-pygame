import Node
# import Horse
import Player

class Game:
    def __init__(self):
        self.board = Node.DoublyLinkedList()
        self.board.create_structure()
        
        while True:
            num_players = int(input("Enter the number of players (2-4): "))
            if 2 <= num_players <= 4:
                break
            print("Invalid number of players. Please enter a number between 2 and 4.")
        
        while True:
            num_horses_per_player = int(input("Enter the number of horses per player (1-4): "))
            if 1 <= num_horses_per_player <= 4:
                break
            print("Invalid number of horses. Please enter a number between 1 and 4.")

        self.players = [Player.Player(i + 1, num_horses_per_player, self.board) for i in range(num_players)]

    def play_round(self):
        for player in self.players:
            dice_result = player.roll_dice()
            print(f"Player {player.player_id} 님의 차례입니다.")
            print(f"주사위의 값: {dice_result}")

    def __repr__(self):
        return f"Game with players: {self.players}"

# 게임 객체 생성 및 초기화
game = Game()
print(game)

# 한 라운드 플레이 (각 Player가 주사위를 한 번씩 굴림)
game.play_round()
class Horse:
    def __init__(self, horse_id, board):
        self.horse_id = horse_id
        self.position = board.nodes[0]

    def __repr__(self):
        return f"Horse {self.horse_id} at Node {self.position.value}"
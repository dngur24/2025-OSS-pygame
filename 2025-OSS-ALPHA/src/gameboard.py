import pygame
import sys
import random

# Pygame 초기화
pygame.init()

# 화면 크기 설정
WIDTH, HEIGHT = 1000, 900
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Yutnori Game")

# 색상 정의
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
BEIGE = (245, 220, 183)

# 윷놀이판 위치
board_positions = [
    (150, 150), (250, 150), (350, 150), (450, 150), (550, 150), (650, 150),
    (150, 250), (250, 250), (550, 250), (650, 250),
    (150, 350), (350, 350), (450, 350), (650, 350),
    (150, 450), (400, 450), (650, 450),
    (150, 550), (350, 550), (450, 550), (650, 550),
    (150, 650), (250, 650), (550, 650), (650, 650),
    (150, 750), (250, 750), (350, 750), (450, 750), (550, 750), (650, 750)
]

# 말 클래스
class Piece:
    def __init__(self, color, team, piece_id):
        self.color = color
        self.team = team
        self.position = 0  # 말의 초기 위치 인덱스
        self.piece_id = piece_id  # 말 ID

    def draw(self):
        pos = board_positions[self.position]
        pygame.draw.circle(screen, self.color, pos, 10)

    def move(self, steps):
        # "백도"의 경우 뒤로 가기
        if steps == -1:
            self.position = max(0, self.position - 1)
        else:
            self.position = min(self.position + steps, len(board_positions) - 1)

# 윷 던지기 함수 (확률 적용)
def throw_yut():
    outcomes = ["도", "개", "걸", "윷", "모", "백도"]
    probabilities = [0.25, 0.375, 0.25, 0.0625, 0.0625, 0.05]  # 각 결과에 대한 확률
    result = random.choices(outcomes, probabilities)[0]

    # 결과 영어 변환
    english_result = {
        "도": "Do",
        "개": "Gae",
        "걸": "Geol",
        "윷": "Yut",
        "모": "Mo",
        "백도": "Back Do"
    }[result]

    steps = {
        "도": 1,
        "개": 2,
        "걸": 3,
        "윷": 4,
        "모": 5,
        "백도": -1
    }[result]

    print(f"Yut throw result: {english_result}")  # 콘솔에 결과 출력
    return english_result, steps

# 윷놀이판 그리기 함수
def draw_board():
    screen.fill(WHITE)
    pygame.draw.rect(screen, BEIGE, (70, 70, 650, 750))

    for pos in board_positions:
        pygame.draw.circle(screen, BLACK, pos, 20)

# 게임판 실행 함수
def gameboard():
    clock = pygame.time.Clock()

    # A팀, B팀 각각 4개의 말 생성
    team_a_pieces = [Piece(RED, "A", i) for i in range(4)]
    team_b_pieces = [Piece(BLUE, "B", i) for i in range(4)]
    
    current_piece_a = team_a_pieces[0]  # A팀 첫 번째 말
    current_piece_b = team_b_pieces[0]  # B팀 첫 번째 말
    yut_result_text = ""  # 윷 던지기 결과 텍스트 표시
    turn = "A"  # A팀과 B팀 번갈아가며 턴을 유지

    # 폰트 설정
    font = pygame.font.Font(None, 48)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:  # 스페이스바로 윷 던지기
                    result, steps = throw_yut()
                    yut_result_text = f"{turn} Team: '{result}'!"

                    # 턴에 따라 현재 팀의 말을 이동
                    if turn == "A":
                        current_piece_a.move(steps)
                        turn = "B"  # 다음 턴을 B팀으로 전환
                    else:
                        current_piece_b.move(steps)
                        turn = "A"  # 다음 턴을 A팀으로 전환

        draw_board()
        
        # 윷 던지기 결과 텍스트 표시
        result_surface = font.render(yut_result_text, True, BLACK)
        screen.blit(result_surface, (50, 50))

        # A팀과 B팀 말 그리기
        for piece in team_a_pieces + team_b_pieces:
            piece.draw()

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    gameboard()

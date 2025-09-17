import pygame
import random
import sys
from pygame.mixer import *
from Piece import *
from pygame.locals import *


# pretty UI
class P_UI:
    """docstring for P_UI"""
    # Tetris_Background
    black = (10, 10, 10)
    black_2 = (26, 26, 26)
    white = (255, 255, 255)
    grey = (35, 35, 35)
    grey_2 = (55, 55, 55)

    t_background = black_2
    backcolor = white
    # Piece_color
    cyan = (69, 206, 204)
    blue = (64, 111, 249)
    orange = (253, 189, 53)
    yellow = (246, 227, 90)
    green = (98, 190, 68)
    pink = (242, 64, 235)
    red = (225, 13, 27)

    # PIECES =                  {1: I,    2: J,    3: L,     4: O,      5: S,     6:T,     7:Z}
    COLORS = { 0: t_background, 1: cyan, 2: blue, 3: orange, 4: yellow, 5: green, 6: pink, 7:red, 8:grey_2}
    # width
    WIDTH = 500
    # height
    HEIGHT = 500
    # font_path , font = I LOVE U 
    path = "./materials/font/Iloveu.ttf"
    SPEED = 500
    SPEED_DOWN = 8

    delete_block_path = "./materials/sound/delete_block.mp3"
    drop_path = "./materials/sound/tok.wav"
    ssg_path = "./materials/sound/ssg.mp3"
    game_over_path = "./materials/sound/game_over.wav"
    delete3_path = "./materials/sound/dorrrru.wav"
    pause_path = "./materials/sound/didong.wav"
    hold_path = "./materials/sound/cutting.wav"
    cash_path = "./materials/sound/cash.wav"
    base_path = "./materials/sound/base.wav" 
    move_path = "./materials/sound/deb.wav"
    delete4_path = "./materials/sound/super_weapon.wav"
    delete_path = "./materials/sound/pop.flac"


class Mino:

    def __init__(self, piece_name=0): #블록을 생성하는
        if piece_name:
            self.piece_name = piece_name
        else:
            self.piece_name = random.randrange(1, 8)
        self.rotation = 0
        self.array2d = Piece.PIECES[self.piece_name][self.rotation]
        self.color = P_UI.COLORS[self.piece_name]

    def __iter__(self):
        for row in self.array2d:
            yield row

    def rotate(self, clockwise=True):  # 블록 회전기능
        self.rotation = (self.rotation + 1) % 4 if clockwise else \
                        (self.rotation - 1) % 4
        self.array2d = Piece.PIECES[self.piece_name][self.rotation]

class Board:
    # 추가한 코드 Start
    def calculate_highest(self):
        for y in range(self.t_height):
            if any(self.board[y]):
                return self.t_height - y
        return 0
    # 추가한 코드 End

    COLLIDE_EVENT = {'no_error': 0, 'right_wall': 1, 'left_wall': 2,
                     'bottom': 3, 'overlap': 4}

    def __init__(self, screen):
        #pygame.mixer.init()  # 사운드 믹서 초기화
        #delete_block_path = "./materials/sound/delete_block.mp3"  # 경로 지정
        #self.delete_sound = pygame.mixer.Sound(delete_block_path)  # 지정한 경로로 음원 로드

        # 기존 음원 경로 추가
        #self.newmain_sound = pygame.mixer.Sound("./materials/sound/newmain.mp3")  # 기본 음원
        #self.warning_sound = pygame.mixer.Sound("./materials/sound/warning.wav")  # 경고 음원

        self.screen = screen
        self.t_width = 10
        self.t_height = 25
        self.block_size = 20
        self.board = []
        self.next_1 = random.randrange(1, 8)
        self.mino_size_row_and_col = Piece.TETRIMINO_SIZE
        self.holding = False
        self.holding_block = None
        self.holding_count = False
        self.score = 0
        self.level = 0
        self.goal = 0
        self.toggle = False  # 배경 전환 토글 변수
        self.height_percentage = 0  # 높이 퍼센트 저장
        self.current_background = P_UI.backcolor  # 초기 배경색
        self.last_background_switch = 0  # 마지막 배경 전환 시간
        self.background_red = False  # 빨간색 여부

        for _ in range(self.t_height):
            self.board.append([0] * self.t_width)
        self.generate_piece()

    def update_background_state(self):
        # 60% 이상 높이에 도달하면 배경 전환 활성화
        height_percentage = (self.calculate_highest() / self.t_height) * 100
        self.height_percentage = height_percentage  # 저장

        # 배경과 음원 변경
        if height_percentage >= 60:
            # 경고 음원만 재생하도록 처리
            if not self.background_red:  # 이전 상태와 다를 때만 음원을 변경
                # self.warning_sound.stop()  # 기존 경고 음원 멈추기
                # self.warning_sound.play(-1)  # 경고 음원 반복 재생
                self.background_red = True
                self.current_background = (255, 0, 0)  # 배경을 빨간색으로 변경
        else:
            # 60% 이하로 떨어졌을 때 경고 음원 멈추기 및 배경을 하얀색으로 변경
            if self.background_red:  # 이전 상태와 다를 때만 음원을 변경
                # self.warning_sound.stop()  # 경고 음원 멈추기
                self.background_red = False
                self.current_background = (255, 255, 255)  # 배경을 하얀색으로 변경

        # 화면에 배경 색 적용
        self.screen.fill(self.current_background)  # 배경 색을 화면에 적용

    def generate_piece(self):
        
        #현재 블록 설정
        self.piece = Mino(self.next_1)  # next_1을 현재 블록으로 설정
        self.piece_num = self. next_1
        self.piece_x, self.piece_y = 3, 0
        self.holding_count = False

        # 높이 퍼센트 계산
        height_percentage = int((self.calculate_highest() / self.t_height) * 100)
        
        # 직사각형 블록 확률 결정
        if height_percentage >= 60:
            o_block_probability = 0.3  # 최고 높이 60% 이상 시 30% 확률
        else:
            o_block_probability = 0.1  # 최고 높이 60% 미만 시 10% 확률

        # 블록 생성
        if random.random() < o_block_probability:
            self.next_1 = 1  # 직사각형 블록 (O 블록)
        else:
            self.next_1 = random.choice([2, 3, 4, 5, 6, 7])
        
        

        #다음 블록을 미리 설정
        self.next_1 = random.choice([1, 2, 3, 4, 5, 6, 7])
    
    def tetris_location(self, x, y): 
        return self.block_size*(x+7), self.block_size*(y-2)

    def absorb_piece(self):
        for y, row in enumerate(self.piece):
            for x, block in enumerate(row):
                if block:
                    self.board[y+self.piece_y][x+self.piece_x] = block
        self.generate_piece()

    def _block_collide_with_board(self, x, y):
        if x < 0:
            return Board.COLLIDE_EVENT['left_wall']
        elif x >= self.t_width:
            return Board.COLLIDE_EVENT['right_wall']
        elif y >= self.t_height:
            return Board.COLLIDE_EVENT['bottom']
        elif self.board[y][x]:
            return Board.COLLIDE_EVENT['overlap']
        return Board.COLLIDE_EVENT['no_error']

    def collide_with_board(self, dx, dy):
        """Check if piece (offset dx, dy) collides with board"""
        for y, row in enumerate(self.piece):
            for x, block in enumerate(row):
                if block:
                    collide = self._block_collide_with_board(x=x+dx, y=y+dy)
                    if collide:
                        return collide
        return Board.COLLIDE_EVENT['no_error']

    def _can_move_piece(self, dx, dy):
        dx_ = self.piece_x + dx
        dy_ = self.piece_y + dy
        if self.collide_with_board(dx=dx_, dy=dy_):
            return False
        else : return True

    def _can_drop_piece(self):
        return self._can_move_piece(dx=0, dy=1)

    def _try_rotate_piece(self, clockwise=True):
        self.piece.rotate(clockwise)
        collide = self.collide_with_board(dx=self.piece_x, dy=self.piece_y)
        if not collide:
            pass
        elif collide == Board.COLLIDE_EVENT['left_wall']:
            if self._can_move_piece(dx=1, dy=0):
                self.move_piece(dx=1, dy=0)
            elif self._can_move_piece(dx=2, dy=0):
                self.move_piece(dx=2, dy=0)
            else:
                self.piece.rotate(not clockwise)
        elif collide == Board.COLLIDE_EVENT['right_wall']:
            if self._can_move_piece(dx=-1, dy=0):
                self.move_piece(dx=-1, dy=0)
            elif self._can_move_piece(dx=-2, dy=0):
                self.move_piece(dx=-2, dy=0)
            else:
                self.piece.rotate(not clockwise)
        else:
            self.piece.rotate(not clockwise)

    def move_piece(self, dx, dy):
        if self._can_move_piece(dx, dy):
            self.piece_x += dx
            self.piece_y += dy

    def drop_piece(self):
        if self._can_drop_piece():
            self.move_piece(dx=0, dy=1)
        else:
            self.absorb_piece()
            self.delete_lines()
    def rotate_piece(self, clockwise=True):
        self._try_rotate_piece(clockwise)

    def full_drop_piece(self):
        while self._can_drop_piece():
            self.drop_piece()
        self.score += self.level * 5
        self.drop_piece()


    def score_up(self, rline):
        if self.score > 500000 :
            self.score = 500000
        else :
            self.score += (10 + rline * rline * 20)
        if self.score >= self.goal : 
            self.level += 1
            P_UI.SPEED -= (P_UI.SPEED_DOWN * self.level)
            if P_UI.SPEED < 80: 
                P_UI.SPEED = 80
            self.set_timer(P_UI.SPEED)

        self.goal = 280 + self.level * self.level * self.level * 20

    def set_timer(self,timer):
        pygame.time.set_timer(Tetris.DROP_EVENT, timer)
    def _delete_line(self, y):
        for y in reversed(range(1, y+1)):
            self.board[y] = list(self.board[y-1])

    def delete_lines(self):
        remove = [y for y, row in enumerate(self.board) if all(row)]
        
        if remove:  # 블록이 삭제되었을 때만 소리 재생
            for y in remove:
                self._delete_line(y)
            #pygame.mixer.Sound(P_UI.delete_block_path).play()
            self.score_up(len(remove))

    

    def hold_block(self):
        if not self.holding_count :    # 한 턴에 한 번만 홀드 가능
            self.holding_count = True  # 홀드 상태 활성화

            if self.holding :          
                # 이미 홀드된 블록이 있을 경우
                self.piece, self.holding_block = self.holding_block, self.piece
            else :  
                # 홀드된 블록이 없는 경우
                self.holding_block = self.piece
                self.holding = True
                self.generate_piece()  # 새 블록 생성
            
            # 블록 위치 초기화
            self.piece_x, self.piece_y = 3, 0
        else :
            pass
    def game_over(self):
        result = sum(self.board[0]) > 0 or sum(self.board[1]) > 0
        return result
  

    # def lowest(self, array2d):
    #     x = self.piece_x
    #     y = self.piece_y
    #     for i in range(4):
    #         for j in range(4):
    #             if array2d[i][j] != 0:
    #                 if (y + i + 1) > 20:
    #                     return True
    #                 elif self.board[x + j][y + i + 1] != 0 and\
    #                      self.board[x + j][y + i + 1] != 8:
    #                     return True
    # def draw_ghost(self, array2d):

    #     tx, ty = self.piece_x, self.piece_y
    #     while not self.lowest(array2d):
    #         ty += 1

    #     for i in range(4):
    #         for j in range(4):
    #             if array2d[i][j] != 0:
    #                 self.board[tx + j][ty + i] = 8  

    def draw_blocks(self, array2d, dx=0, dy=0, board=0):
        # if not board :
        #    self. draw_ghost(array2d.array2d)
        for y, row in enumerate(array2d):
            y += dy
            if y >= 2 and y < self.t_height:
                for x, block in enumerate(row):
                    x += dx
                    x_pix, y_pix = self.tetris_location(x, y)
                    if block:
                        # match block and color
                        color = P_UI.COLORS [block]
                        # draw block
                        pygame.draw.rect(self.screen, color,
                                         (  x_pix, y_pix,
                                            self.block_size,
                                            self.block_size))
                    # Board
                    if board :
                        pygame.draw.rect(self.screen, P_UI.grey,
                        (  x_pix, y_pix,
                            self.block_size,
                            self.block_size), 1)


    def draw_static_block(self, next_name, dx, dy, size):
        next_block = Piece.PIECES[next_name][0]
        for x in range(self.mino_size_row_and_col):
            for y in range(self.mino_size_row_and_col):
                if next_block[x][y] != 0:
                    x_pix = dx + size * y
                    y_pix = dy + size * x
                    pygame.draw.rect(
                        self.screen,
                        P_UI.COLORS[next_block[x][y]],
                        Rect( x_pix, y_pix,size, size)
                          
                    )
                    pygame.draw.rect(self.screen, P_UI.backcolor,
                     ( x_pix, y_pix, size-2, size-2), 1)
                        
                       

     

    def draw_board(self):       
                    
        pygame.draw.circle(self.screen, P_UI.grey_2, (self.tetris_location(0, 0)[0], self.tetris_location(0, self.t_height)[1]), 6, 0)
        pygame.draw.circle(self.screen, P_UI.grey_2, (self.tetris_location(self.t_width, 0)[0], self.tetris_location(self.t_width, self.t_height)[1]), 6, 0)
        pygame.draw.rect(
            self.screen,P_UI.grey_2,
            Rect(self.tetris_location(0, 0)[0], self.tetris_location(0, 1)[1],
                 self.t_width * self.block_size, (self.t_height-1) * self.block_size), 13)
        pygame.draw.rect(
            self.screen,P_UI.t_background,
            Rect(self.tetris_location(0, 0)[0], self.tetris_location(0, 1)[1],
                 self.t_width * self.block_size, (self.t_height-1) * self.block_size))
        
        # 필요한 경우 나머지 블록 그리기
        pygame.draw.circle(self.screen, P_UI.grey_2, 
                       (self.tetris_location(0, 0)[0], self.tetris_location(0, self.t_height)[1]), 6, 0)
        
        #게임판 위에 고정된 블록들을 그리기
        self.draw_blocks(self.board) 

        # 외곽 경계선 그리기
        x_pix, y_pix = self.tetris_location(0, 0)
        x_end = x_pix + self.t_width * self.block_size
        y_end = y_pix + self.t_height * self.block_size
             
        pygame.draw.circle(self.screen, P_UI.grey_2, (x_pix, y_end), 6, 0)
        pygame.draw.circle(self.screen, P_UI.grey_2, (x_end, y_end), 6, 0)
        pygame.draw.rect(
                    self.screen, P_UI.grey_2,
                    Rect(x_pix, y_pix + self.block_size, 
                    self.t_width * self.block_size, (self.t_height-1) * self.block_size),13)        
        pygame.draw.rect(
                    self.screen, P_UI.t_background,
                    Rect(x_pix, y_pix + self.block_size, 
                    self.t_width * self.block_size, (self.t_height-1) * self.block_size))
        
       
        # 최고 높이 표시 추가
        font_high = pygame.font.Font(P_UI.path, 25)
        text_high = font_high.render("HEIGHT", 1, P_UI.black)
        num_high = pygame.font.Font(P_UI.path, 30).render(f"{int(self.height_percentage)}%", 1, P_UI.black)
        self.screen.blit(text_high, (392, 390))  # HEIGHT 텍스트 위치
        self.screen.blit(num_high, (410, 420))  # 퍼센트 출력 위치
        
        # 정보 텍스트 렌더링
        font0 = pygame.font.Font(P_UI.path, 25)
        font1 = pygame.font.Font(P_UI.path, 25)
        font0.set_underline(1)
        
        text_next = font0.render("NEXT", 1, P_UI.black)
        self.screen.blit(text_next, (400, 30))

        text_hold = font0.render("HOLD", 1, P_UI.black)
        text_level = font1.render("LEVEL", 1, P_UI.black)
        text_goal = font1.render("GOAL", 1, P_UI.black)
        text_next = font0.render("NEXT", 1, P_UI.black)
        text_score = font1.render("SCORE", 1, P_UI.black)
        num_level = pygame.font.Font(P_UI.path, 40).render(str(self.level), 1, P_UI.black)
        num_goal = pygame.font.Font(P_UI.path, 30).render(str(self.goal), 1, P_UI.black)
        num_score = pygame.font.Font(P_UI.path, 35).render(str(int(self.score)), 1, P_UI.black)

        self.screen.blit(text_hold, (39, 34))
        self.screen.blit(text_level, (40, 235))
        self.screen.blit(text_goal, (39, 360))
        self.screen.blit(text_next, (400, 30))
        self.screen.blit(text_score, (392, 300))
        self.screen.blit(num_level, (55, 280))
        self.screen.blit(num_goal, (50, 415))
        self.screen.blit(num_score, (410, 345))
        
        # 다음 블록 하나만 표시
        self.draw_static_block(self.next_1, 390, 85, self.block_size + 2)
        
        # 홀드 블록 표시
        if self.holding_block:       # 홀드된 블록이 있을 경우에만 표시
            self.draw_static_block(self.holding_block.piece_name, 30, 100, self.block_size + 2)

    def draw(self):
        self.draw_board()
        self.draw_blocks(self.piece, dx=self.piece_x, dy=self.piece_y)
        self.draw_blocks(self.board, board=1)
    
    
class Tetris:
    DROP_EVENT = USEREVENT + 1

    def __init__(self):
        self.screen = pygame.display.set_mode((P_UI.WIDTH, P_UI.HEIGHT))
        self.clock = pygame.time.Clock()
        self.board = Board(self.screen)
        self.is_fast_drop = False
        pygame.init()
        pygame.display.set_caption('Tetris_by_Lim')
        pygame.time.set_timer(Tetris.DROP_EVENT, P_UI.SPEED)
        #self.main_sound('back.wav')
        self.start()       

    #def main_sound (self, file):
        #pygame.mixer.music.load("./materials/sound/" + file)
        #pygame.mixer.music.play(loops=-1 , start=0.0)

    def start(self):
        self.screen.fill(P_UI.backcolor)
        hei, size = 240, 20
        self.board.draw_static_block(2, 60, hei, size)
        self.board.draw_static_block(5, 160, hei, size)
        self.board.draw_static_block(7, 250, hei, size)
        self.board.draw_static_block(3, 350, hei, size)
        self.board.draw_static_block(4, 80, hei+80, size)
        self.board.draw_static_block(1, 200, hei+80, size)
        self.board.draw_static_block(6, 330, hei+80, size)
        image = pygame.image.load('./materials/image/logo.jpg')
        self.screen.blit(image, (80, 50))
        image2 = pygame.image.load('./materials/image/start.jpg')
        self.screen.blit(image2, (140, 380))
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == KEYDOWN:
                    self.run()

            pygame.display.update()

    def handle_key(self, event_key): 
        if event_key == K_UP:
            self.board.rotate_piece()  # 블록 회전
        elif event_key == K_SPACE:
            self.board.full_drop_piece()  # 즉시 맨 아래로 이동
        elif event_key == K_ESCAPE:
            self.pause()  # 게임 일시 정지
        elif event_key == K_LSHIFT:
            self.board.hold_block()  # 블록 홀드

    def pause(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == KEYDOWN and event.key == K_ESCAPE:
                    running = False

    def run(self):
        screen = self.screen
        clock = self.clock
        #self.main_sound("newmain.mp3")
        pygame.time.set_timer(Tetris.DROP_EVENT, P_UI.SPEED)
        
        # 좌우 및 아래 키 상태 변수
        hold_left = hold_right = hold_down = False
        last_move_time = pygame.time.get_ticks()  # 마지막으로 이동한 시간
        move_interval = 150  # 좌우 이동 간격 (ms)
        drop_interval = 100  # 빠른 하강 간격 (ms) -> 충분히 빠르게 느껴지는 값으로 설정
        

        while True:
            if self.board.game_over():
                #pygame.mixer.Sound(P_UI.game_over_path).play()
                over = pygame.font.Font(P_UI.path, 80).render("Good Game !!", 1, (0, 255, 255))
                self.screen.blit(over, (70, 230))
                pygame.display.update()
                pygame.time.delay(2000)
                pygame.quit()
                sys.exit()

            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()

                elif event.type == KEYDOWN:
                    if event.key == K_LEFT:
                     # self.board.move_piece(dx=-1, dy=0)
                        hold_left = True
                    elif event.key == K_RIGHT:
                     # self.board.move_piece(dx=1, dy=0)
                        hold_right = True
                    elif event.key == K_DOWN:
                        hold_down = True
                    else:
                        self.handle_key(event.key)

                elif event.type == KEYUP:
                    if event.key == K_LEFT:
                        hold_left = False
                    elif event.key == K_RIGHT:
                        hold_right = False
                    elif event.key == K_DOWN:
                        hold_down = False
                elif event.type == Tetris.DROP_EVENT:
                    if not hold_down:
                        self.board.drop_piece()

            # 현재 시간 확인
            current_time = pygame.time.get_ticks()
            self.board.update_background_state() # 배경 상태 업데이트

            # 배경 전환 로직 (0.5초마다 전환)
            if self.board.background_red and current_time - self.board.last_background_switch > 500:  # 0.5초 간격
                self.board.last_background_switch = current_time
                self.board.toggle = not self.board.toggle
                self.board.current_background = (255, 0, 0) if self.board.toggle else P_UI.backcolor
                
            # 좌우 이동 처리
            if hold_left and current_time - last_move_time > move_interval:  # 100ms 간격으로 이동
                self.board.move_piece(dx=-1, dy=0)
                last_move_time = current_time
            if hold_right and current_time - last_move_time > move_interval:
                self.board.move_piece(dx=1, dy=0)
                last_move_time = current_time
            if hold_down and current_time - last_move_time > drop_interval:
                self.board.drop_piece()
                last_move_time = current_time

            # 화면 업데이트
            screen.fill(self.board.current_background)
            self.board.draw()
            pygame.display.update()
            clock.tick(60)
            



if __name__ == "__main__":
    Tetris()

#END


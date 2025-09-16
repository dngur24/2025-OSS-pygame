import pygame
import random
import os
from config import *
from background import *
# from sound import *
from ranking import *

RUNNING = [pygame.image.load(os.path.join("Assets/Dino", "DinoRun1.png")),
           pygame.image.load(os.path.join("Assets/Dino", "DinoRun2.png"))]

# sound_manager = SoundManager()

id_entered = False

def game_over_menu(player, menu_instance):
    global run, points, id_entered
    Ranking_sys = Ranking()  # 랭킹 관리 객체 생성
    font = pygame.font.Font('freesansbold.ttf', 30)

    # ID를 이미 입력한 경우, 루프를 건너뜀
    if id_entered:
        restart_button, ranking_button, home_button = draw_game_over_screen()
        return  # 이후 루프 실행 없이 바로 버튼 화면으로 이동

    if not pygame.display.get_init():
        pygame.display.init()
        menu_instance.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Dinosaur Game")

    theme_colors = menu_instance.current_color

    SCREEN.fill(theme_colors['background'])
    game_over_text = font.render("Game Over", True, theme_colors['text'])
    score_text = font.render(f"Your Score: {points}", True, theme_colors['text'])
    input_request = font.render("Enter your ID in English:", True, theme_colors['text'])
    # SCREEN.blit(input_request, (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2))

    #버튼 크기와 위치
    button_width = 200
    button_height = 50
    button_spacing = 20
    start_y = SCREEN_HEIGHT // 2 + 100

    #버튼 위치 설정
    restart_button = pygame.Rect(
        SCREEN_WIDTH // 2 - button_width // 2,
        start_y,
        button_width,
        button_height
        )
    ranking_button = pygame.Rect(
        SCREEN_WIDTH // 2 - button_width // 2, 
        start_y + button_height + button_spacing, 
        button_width, 
        button_height
        )
    home_button = pygame.Rect(
        SCREEN_WIDTH // 2 - button_width // 2, 
        start_y + 2 * (button_height + button_spacing), 
        button_width, 
        button_height
        )
    # 하이스코어 파일에서 데이터 로드
    Ranking_sys.load_high_scores_from_file()

    
    def draw_game_over_screen():
        # 화면 초기화 및 메시지 표시
        SCREEN.fill(theme_colors['background'])
        SCREEN.blit(game_over_text, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 200))
        SCREEN.blit(score_text, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 150))
        SCREEN.blit(RUNNING[0], (SCREEN_WIDTH // 2 - 17, SCREEN_HEIGHT // 2 - 110))
        
        # 버튼 그리기
        pygame.draw.rect(SCREEN, theme_colors['button'], restart_button)
        pygame.draw.rect(SCREEN, theme_colors['button'], ranking_button)
        pygame.draw.rect(SCREEN, theme_colors['button'], home_button)

        # 버튼 텍스트
        restart_text = font.render("Restart", True, theme_colors['text'])
        ranking_text = font.render("Ranking", True, theme_colors['text'])
        home_text = font.render("Home", True, theme_colors['text'])
        # 버튼 텍스트 위치 조정
        restart_text_rect = restart_text.get_rect(center=restart_button.center)
        ranking_text_rect = ranking_text.get_rect(center=ranking_button.center)
        home_text_rect = home_text.get_rect(center=home_button.center)
        # 버튼 텍스트 그리기
        SCREEN.blit(restart_text, restart_text_rect)
        SCREEN.blit(ranking_text, ranking_text_rect)
        SCREEN.blit(home_text, home_text_rect)

        pygame.display.update()
        return restart_button, ranking_button, home_button

    # 화면 초기 렌더링
    restart_button, ranking_button, home_button = draw_game_over_screen()

    # 입력 상자 설정
    user_id = ""  # 사용자 입력 저장
    input_box = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 50, 200, 50)

    pygame.display.update()  # 초기 화면 갱신

    # 사용자 입력 루프
    input_active = True
    while input_active:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:  # Enter 키로 입력 완료
                    input_active = False
                elif event.key == pygame.K_BACKSPACE:  # Backspace로 문자 삭제
                    user_id = user_id[:-1]
                else:
                    user_id += event.unicode  # 입력된 문자 추가

        # 화면 업데이트
        SCREEN.fill(theme_colors['background'])
        SCREEN.blit(game_over_text, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 200))
        SCREEN.blit(score_text, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 150))
        SCREEN.blit(input_request, (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2))
        SCREEN.blit(RUNNING[0], (SCREEN_WIDTH // 2 - 17, SCREEN_HEIGHT // 2 - 110))

        # 입력 상자 및 입력된 텍스트 표시
        pygame.draw.rect(SCREEN, theme_colors['button'], input_box)
        pygame.draw.rect(SCREEN, theme_colors['text'], input_box, 2)
        user_text_surface = font.render(user_id, True, theme_colors['text'])
        SCREEN.blit(user_text_surface, (input_box.x + 10, input_box.y + 10))

        pygame.display.update()

    # ID와 점수를 저장
    Ranking_sys.update_high_score(user_id, points)
    Ranking_sys.save_high_scores_to_file()

    restart_button, ranking_button, home_button = draw_game_over_screen()

    # 대기 상태
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                if restart_button.collidepoint(mouse_pos):
                    waiting = False  # 현재 게임 루프 종료
                    run = False
                    main(menu_instance)
                elif ranking_button.collidepoint(mouse_pos):
                    result = menu_instance.show_ranking(from_game_over=True)
                    if result == "game_over":  # ESC를 눌러 게임오버 화면으로 돌아옴
                        restart_button, ranking_button, home_button = draw_game_over_screen()  # 게임오버 화면 다시 그리기
                        continue
                elif home_button.collidepoint(mouse_pos):
                    waiting = False
                    run = False
                    pygame.display.init()  # 디스플레이 다시 초기화
                    if menu_instance.show_menu():   # 메뉴 화면으로 돌아가기
                        main(menu_instance)
                    return


pygame.init()  # Pygame 초기화
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))  # 화면 사이즈 설정
pygame.display.set_caption("Dinosaur Game")  # 게임 창 제목 설정

# 구름이랑 배경화면 이미지들
CLOUD = pygame.image.load(os.path.join("Assets/Other", "Cloud.png"))
BG = pygame.image.load(os.path.join("Assets/Other", "Track.png"))

xPos = 0
yPos = 0
black = 0, 0, 0
white = 255, 255, 255
GROUND_HEIGHT = SCREEN_HEIGHT - 100  # 공룡이 서 있을 땅 높이

# 메인
def main(menu_instance):
    from dinosaur import Dinosaur  # 'dinosaur' 파일에서 Dinosaur 클래스를 가져옵니다
    from obstacles import ObstacleManager
    from background import BackgroundManager
    import menu

    
    global game_speed, x_pos_bg, y_pos_bg, points
    # 게임 상태 설정
    run = True  # 게임 실행 상태
    clock = pygame.time.Clock()  # 게임 프레임 속도 관리
    game_speed = 20  # 게임 스피드
    x_pos_bg = 0  # 배경화면 x축 시작위치
    y_pos_bg = 380  # 배경화면 x축 시작위치
    points = 0  # 점수 초기화
    font = pygame.font.Font('freesansbold.ttf', 20)  # 점수 표시 및 폰트
    # sound_manager = SoundManager()
    # sound_manager.set_bgm_volume(menu_instance.bgm_volume)
    # sound_manager.set_sfx_volume(menu_instance.sfx_volume)
    # sound_manager.stop_bgm()
    # sound_manager.play_bgm() #게임 시작시 BGM 시작

    player = Dinosaur()  # 공룡 객체 생성
    obstacle_manager = ObstacleManager(SCREEN_WIDTH)  # 장애물 관리 객체 생성
    theme = 'white' if menu_instance.theme == 'day' else 'black'
    BG_manager = BackgroundManager(theme)

    from menu import start_game
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Dinosaur Game")

    # 테마 설정 적용
    theme = 'white' if menu_instance.theme == 'day' else 'black'
    BG_manager = BackgroundManager(theme)

    #폰트 색상 테마에 맞게
    font_color = (0,0,0) if theme == 'white' else (220, 220, 220)

    player = Dinosaur()
    obstacle_manager = ObstacleManager(SCREEN_WIDTH)

    # cloud = Cloud() 구름 객체 인데 아직 구름은 구현 안함

    if not pygame.display.get_init():
        pygame.init()
        pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Dinosaur Game")

    def score():  # 점수 관리 함수
        global points, game_speed
        points += 1
        if points % 100 == 0:
            game_speed += 1
        text = font.render("Points: " + str(points), True, (0, 0, 0))
        textRect = text.get_rect()
        textRect.center = (1000, 40)
        SCREEN.blit(text, textRect)

    def background():  # 배경 화면 함수
        global x_pos_bg, y_pos_bg
        image_width = BG.get_width()
        SCREEN.blit(BG, (x_pos_bg, y_pos_bg))
        SCREEN.blit(BG, (image_width + x_pos_bg, y_pos_bg))
        if x_pos_bg <= -image_width:
            SCREEN.blit(BG, (image_width + x_pos_bg, y_pos_bg))
            x_pos_bg = 0
        x_pos_bg -= game_speed

    # 게임 루프(게임 실행중일 때)
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # 창 닫기 이벤트 처리
                pygame.quit()
                exit()

        SCREEN.fill(menu_instance.current_color['background'])  # 화면 초기화
        userInput = pygame.key.get_pressed()  # 사용자 입력 감지
        
        BG_manager.background_update()
        
        # 공룡 업데이트 및 그리기
        player.draw(SCREEN)
        # player.update(userInput, sound_manager)

        # 장애물 업데이트 및 그리기
        obstacle_manager.update(game_speed)
        obstacle_manager.draw(SCREEN)

        # 공룡 충돌 로직
        obstacle_manager.update(game_speed)
        obstacle_manager.draw(SCREEN)
        for obstacle in obstacle_manager.obstacles:
            if player.dino_rect.colliderect(obstacle.rect):  # 공룡과 장애물 간 충돌 감지
                player.take_damage()  # 충돌 시 공룡의 take_damage() 메서드 호출

        if not player.dino_alive:
            game_over_menu(player, menu_instance)

        score()

        clock.tick(30)
        pygame.display.update()

        #sound
        userInput = pygame.key.get_pressed()
        # player.update(userInput, SoundManager)
        # sound_manager.set_bgm_volume(menu_instance.bgm_volume)
        # sound_manager.set_sfx_volume(menu_instance.sfx_volume)

        # 점수 증가 시 효과음 추가 (500점 얻을 시 실행)
        # if points % 500 == 0 and points > 0:
        #     sound_manager.play_point()


# 게임 시작
if __name__ == "__main__":
    pygame.init()

import pygame  # pygame 라이브러리 선언
import random
import os
import sys

pygame.init()  # pygame 초기화
#try:
    # pygame.mixer.init() # pygame mixer 초기화 (배경 음악)
    # pygame.mixer.music.set_volume(0.3)
#except pygame.error/as e:
    # print("재생 장치 관련 오류로 인해 BGM이 나오지 않습니다.")
    # print(f"{e}")

# 게임 화면 크기 및 색상 설정
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
size = [600, 800]
screen = pygame.display.set_mode(size)

def resource_path(relative_path):
    """ PyInstaller 실행 파일에서 리소스를 불러오기 위한 경로 반환 """
    try:
        base_path = sys._MEIPASS  # PyInstaller가 생성한 임시 폴더
    except AttributeError:
        base_path = os.path.abspath(".")  # 개발 환경 경로

    return os.path.join(base_path, relative_path)

# 배경 음악 및 효과음 파일 로드
# Intro = resource_path('bomb_game/sound/Intro.wav')
# bgm_1 = resource_path('bomb_game/sound/BGM1.wav')
# bgm_2 = resource_path('bomb_game/sound/BGM2.wav')
# bgm_3 = resource_path('bomb_game/sound/BGM3.wav')
# bgm_4 = resource_path('bomb_game/sound/BGM4.wav')
# star_effect = pygame.mixer.Sound(resource_path('bomb_game/sound/star.wav'))
# bomb_effect = pygame.mixer.Sound(resource_path('bomb_game/sound/bomb.wav'))
# heart_effect = pygame.mixer.Sound(resource_path('bomb_game/sound/heart.wav'))
# etc_effect = pygame.mixer.Sound(resource_path('bomb_game/sound/etc.wav'))/

#폰트 설정
gameover_font = pygame.font.Font(resource_path('bomb_game/font/Pixelify_Sans/static/PixelifySans-Medium.ttf'), 70)  # 게임오버 텍스트를 위한 폰트 설정
life_font = pygame.font.Font(resource_path('bomb_game/font/Pixelify_Sans/static/PixelifySans-Medium.ttf'), 50)  # 목숨 표시를 위한 폰트 설정
timer_font = pygame.font.Font(resource_path('bomb_game/font/Pixelify_Sans/static/PixelifySans-Medium.ttf'), 200) # 타이머에 사용할 폰트 설정
button_font = pygame.font.Font(resource_path('bomb_game/font/Pixelify_Sans/static/PixelifySans-Medium.ttf'), 30) # 버튼에 사용할 폰트 설정

#이미지 로드 및 크기 조정
bomb_image = pygame.image.load(resource_path('bomb_game/img/bomb.png')).convert_alpha() # 폭탄 이미지 로드
gameover_image = pygame.image.load(resource_path('bomb_game/img/gameover.png')).convert_alpha()#gameover 이미지 로드
background_img = pygame.image.load(resource_path('bomb_game/img/background.jpg'))#배경 이미지 로드
start_image = pygame.image.load(resource_path('bomb_game/img/start.png')).convert_alpha()#start 이미지 로드
quit_image = pygame.image.load(resource_path('bomb_game/img/Quit.png')).convert_alpha()#quit 이미지 로드
re_image = pygame.image.load(resource_path('bomb_game/img/Re.png')).convert_alpha()#re 이미지 로드
heart_image = pygame.transform.scale(pygame.image.load(resource_path('bomb_game/img/heart.png')).convert_alpha(), (70, 70))
fast_image = pygame.transform.scale(pygame.image.load(resource_path('bomb_game/img/fast.png')).convert_alpha(), (70, 91))
clock_image = pygame.transform.scale(pygame.image.load(resource_path('bomb_game/img/Clock.png')).convert_alpha(), (70, 84))
star_image = pygame.transform.scale(pygame.image.load(resource_path('bomb_game/img/star.png')).convert_alpha(), (70,70))
mainlogo_image = pygame.transform.scale(pygame.image.load(resource_path('bomb_game/img/mainlogo.png')).convert_alpha(), (530,334))
pause_image = pygame.transform.scale(pygame.image.load(resource_path('bomb_game/img/pause.png')).convert_alpha(), (45, 66))
play_image = pygame.transform.scale(pygame.image.load(resource_path('bomb_game/img/play.png')).convert_alpha(), (50, 66))
slow_image = pygame.transform.scale(pygame.image.load(resource_path('bomb_game/img/slow_bomb.png')).convert_alpha(),(100, 70))
damage_image = pygame.transform.scale(pygame.image.load(resource_path('bomb_game/img/damage_bomb.png')).convert_alpha(),(70, 99))

# 캐릭터 애니메이션 이미지 로드
person_idle_image = pygame.image.load(resource_path('bomb_game/img/person_idle.png')).convert_alpha()
person_left_images = [
    pygame.image.load(resource_path('bomb_game/img/person_left1.png')).convert_alpha(),
    pygame.image.load(resource_path('bomb_game/img/person_left2.png')).convert_alpha()
]
person_right_images = [
    pygame.image.load(resource_path('bomb_game/img/person_right1.png')).convert_alpha(),
    pygame.image.load(resource_path('bomb_game/img/person_right2.png')).convert_alpha()
]

# 캐릭터 이미지 크기 조정
person_idle_image = pygame.transform.scale(person_idle_image, (100, 100))
person_left_images = [pygame.transform.scale(img, (100, 100)) for img in person_left_images]
person_right_images = [pygame.transform.scale(img, (100, 100)) for img in person_right_images]

# 마스크 생성
person_idle_mask = pygame.mask.from_surface(person_idle_image) # 캐릭터 마스크 생성
person_left_masks = [pygame.mask.from_surface(img) for img in person_left_images]
person_right_masks = [pygame.mask.from_surface(img) for img in person_right_images]
bomb_mask = pygame.mask.from_surface(bomb_image) # 폭탄 마스크 생성
heart_mask = pygame.mask.from_surface(heart_image) # 생명 마스크 생성
fast_mask = pygame.mask.from_surface(fast_image) #번개 마스크 생성
clock_mask = pygame.mask.from_surface(clock_image) #시계 마스크 생성
star_mask = pygame.mask.from_surface(star_image)# 스타 마스크 생성
slow_mask = pygame.mask.from_surface(slow_image) #특성 폭탄 마스크 생성
damage_mask = pygame.mask.from_surface(damage_image)

# 애니메이션 관련 변수
animation_index = 0  # 현재 애니메이션 프레임 인덱스
animation_speed = 0.2  # 애니메이션 속도 (작을수록 빠름)
animation_timer = 0  # 프레임 전환을 위한 시간 누적
person_image = person_idle_image  # 초기 이미지는 가만히 있는 상태

def play_effect(effect):
    try:
        effect.play()
    except pygame.error as e:
        print("재생 장치 관련 오류로 인해 BGM이 나오지 않습니다.")
        print(f"{e}")

# 충돌 검사 함수
def check_collision(person_mask, obj_mask, offset):
    return person_mask.overlap(obj_mask, offset)

def reset(): # 게임 상태와 관련된 변수 초기화 함수
    global done, clock, start_ticks, game_over, lives, elapsed_time, paused
    done = False # 게임 루프를 제어하는 변수
    clock = pygame.time.Clock() # 프레임 속도 제어를 위한 시계 객체
    start_ticks = pygame.time.get_ticks() # 시작 시간 기록
    game_over = False # 게임 오버 상태를 나타내는 변수
    lives = 3 # 초기 목숨 개수 설정
    elapsed_time = 0 # 초기화 추가
    paused = False

def text_objects(text, font): # START버튼 
    textSurface = font.render(text, True, WHITE)
    return textSurface, textSurface.get_rect()

def button_with_image(image, x, y, w, h, action=None, centered=False,highlight_color=(255, 255, 255, 100)):
    if centered:
        x = (size[0] - w) // 2
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    button_rect = pygame.Rect(x, y, w, h)
    if button_rect.collidepoint(mouse):
        highlight_surface = pygame.Surface((w, h), pygame.SRCALPHA)  
        highlight_surface.fill(highlight_color)  
        screen.blit(highlight_surface, (x, y)) 
    screen.blit(image, button_rect) 

    if button_rect.collidepoint(mouse):
        if click[0] == 1 and action is not None:
            return True
    return False

def toggle_pause():
    global paused, countdown_active, countdown, countdown_timer
    current_time = pygame.time.get_ticks()
    if current_time - last_pause_time > pause_cooldown:
        if paused:
            countdown_active = True
            countdown = 3
            countdown_timer = pygame.time.get_ticks()
        else:
            paused = True
        return True
    return False

# def play_intro_sound():
    # try:
        # pygame.mixer.music.load(Intro)  # 음악 파일 로드
        # pygame.mixer.music.play()  # 음악 재생
    # except pygame.error as e:
    #     print("재생 장치 관련 오류로 인해 BGM이 나오지 않습니다.")
    #     print(f"{e}")
        
# def gameover_sound():
#     try:
#         pygame.mixer.music.stop()  # 기존 배경음악 정지
#         pygame.mixer.music.load(bgm_3)  # 게임 종료 음악 로드
#         pygame.mixer.music.play()  # 게임 종료 음악 재생
#         pygame.mixer.music.set_volume(1.5)
#         pygame.mixer.music.queue(bgm_4)  # bgm_3 종료 후 bgm_4 재생 대기열에 추가
#         pygame.mixer.music.set_volume(0.5)
#     except pygame.error as e:
#         print("재생 장치 관련 오류로 인해 게임 종료 음악이 나오지 않습니다.")
#         print(f"{e}")
        

# 게임 실행 함수 정의
def runGame(): 

    global done, game_over, lives, start_ticks, elapsed_time, animation_index, animation_timer
    global heart_spawned, last_heart_time, person_speed, fast_spawned, last_fast_time, star_spawned, last_star_time
    global clock_spawned, last_clock_time, slow_effect_active, slow_effect_end_time
    global invincible, invincible_start_time
    global paused, countdown, countdown_active,countdown_timer, last_pause_time, pause_cooldown
    countdown = 3  
    countdown_active = False  
    countdown_timer = 0  
    last_pause_time = 0 
    pause_cooldown = 500
    paused = False
    invincible = False
    invincible_start_time = 0

    # try:
    #     pygame.mixer.music.load(bgm_1)  # 첫 번째 음악을 로드
    #     pygame.mixer.music.queue(bgm_2) # 두 번째 음악을 대기열에 추가
    #     pygame.mixer.music.play()  # 첫 번째 음악 재생
    # except pygame.error as e:
    #     print("재생 장치 관련 오류로 인해 BGM이 나오지 않습니다.")
    #     print(f"{e}")
        
    reset()

    heart_spawned = False # 화면에 하트가 존재하는가
    last_heart_time = 0 # 마지막 하트 생성 시간 기록
    heart = pygame.Rect(heart_image.get_rect())

    fast_spawned = False # 화면에 번개가 존재하는가
    last_fast_time = 0 # 마지막 번개 생성 시간 기록
    fast = pygame.Rect(fast_image.get_rect()) 

    clock_spawned = False # 화면에 시계가 존재하는가
    last_clock_time = 0 # 마지막 시계 생성 시간 기록
    clock_rect = pygame.Rect(clock_image.get_rect())  # 시계 위치 및 크기 설정

    star_spawned = False # 화면에 스타가 존재하는가
    last_star_time = 0 # 마지막 스타 생성 시간 기록
    star = pygame.Rect(star_image.get_rect())

    slow_effect_active = False  # 폭탄 속도 감소 효과 활성화 여부
    slow_effect_end_time = 0  # 효과 종료 시간

    invincible = False
    invincible_start_time = 0

    bomb_image = pygame.image.load('bomb_game/img/bomb.png')  # 폭탄 이미지 파일을 불러옴
    bomb_image = pygame.transform.scale(bomb_image, (70, 120))  # 폭탄 이미지 크기를 70x120으로 조절
    bombs = []  # 폭탄 정보를 담을 리스트 초기화

    # 대각선 폭탄 관련 변수
    diagonal_bombs = []  # 대각선 폭탄 정보를 담을 리스트
    last_diagonal_bomb_time = 0  # 마지막 대각선 폭탄 생성 시간
    diagonal_bomb_interval = random.randint(3000, 5000)  # 3초~5초 사이 간격
    
    # 특성 폭탄 관련 변수
    special_bombs = []
    last_special_bomb_time = 0
    special_bomb_interval = random.randint(7000, 10000) # 7~10초 사이 간격    

    # 초기 폭탄 3개 생성
    for i in range(3):
        rect = pygame.Rect(bomb_image.get_rect())  # 폭탄 이미지 크기와 위치 설정
        rect.left = random.randint(0, size[0])  # 폭탄의 x 좌표를 무작위로 설정
        rect.top = -100  # 폭탄의 초기 y 좌표 설정
        dy = random.randint(3 + elapsed_time // 5000, 7 + elapsed_time // 5000)  # 폭탄 낙하 속도를 무작위로 설정
        bombs.append({'rect': rect, 'dy': dy})  # 폭탄 정보를 리스트에 추가

    # 캐릭터 이미지 불러오기 및 초기 위치 설정
    person_image = pygame.image.load('bomb_game/img/person_idle.png')
    person_image = pygame.transform.scale(person_image, (100, 100))
    person = pygame.Rect(person_image.get_rect())
    person.left = size[0] // 2 - person.width // 2  # 캐릭터를 화면 중앙에 배치
    person.top = size[1] - person.height  # 캐릭터를 화면 하단에 배치
    person_dx = 0  # 캐릭터의 초기 이동 속도 설정
    person_speed = 5 # 캐릭터 이동속도 변수
    moving = False

    game_over_time = None #게임 오버 시간을 저장하기 위한 변수

    while not done:
        clock.tick(30)  # 초당 30프레임 설정
        screen.blit(background_img,(0,0)) # 화면을 배경이미지로 채움

        if not game_over:
            PauseBtn = button_with_image(pause_image if not paused else play_image, 525, 25, 50, 50, action=True)
            if PauseBtn:
                if toggle_pause():
                    last_pause_time = pygame.time.get_ticks()

        if countdown_active:
            current_time = pygame.time.get_ticks()
            if current_time - countdown_timer >= 1000:  # 1초마다 카운트다운
                countdown -= 1
                countdown_timer = current_time
                
            if countdown <= 0:
                paused = False
                countdown_active = False
            
            # 카운트다운 숫자 표시
            countdown_font = pygame.font.SysFont(None, 200)
            countdown_text = countdown_font.render(str(max(countdown, 0)), True, BLACK)
            screen.blit(countdown_text, (size[0] // 2 - countdown_text.get_width() // 2, size[1] // 2 - countdown_text.get_height() // 2))       

        # 키 이벤트 처리
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if toggle_pause():
                        last_pause_time = pygame.time.get_ticks()
            if event.type == pygame.QUIT:
                done = True  # 게임 종료
                break
            elif event.type == pygame.KEYDOWN and not game_over:
                if event.key == pygame.K_LEFT:
                    person_dx = - person_speed  # 왼쪽 키를 누르면 왼쪽으로 이동
                    moving = True
                elif event.key == pygame.K_RIGHT:
                    person_dx = person_speed  # 오른쪽 키를 누르면 오른쪽으로 이동
                    moving = True
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    person_dx = 0  # 키를 떼면 이동 정지
                    moving = False
            
        if not paused:
            # 게임 오버가 아닐 때 게임 로직 실행
            if not game_over:
                # 경과 시간 계산 및 표시
                elapsed_time = pygame.time.get_ticks() - start_ticks
                timer = timer_font.render(f"{elapsed_time // 1000} : {elapsed_time % 100:02d}", True, WHITE).convert_alpha()
                timer.set_alpha(90) #투명도 설정 0~255
                screen.blit(timer, (size[0] // 2 - timer.get_width() // 2, size[1] // 2 - timer.get_height() // 2))

                # 폭탄 이동 및 화면을 벗어난 폭탄 제거 후 새 폭탄 추가
                for bomb in bombs:
                    bomb['rect'].top += bomb['dy']  # 폭탄의 y 좌표에 속도를 더하여 아래로 이동
                    if bomb['rect'].top > size[1]:  # 폭탄이 화면 하단을 벗어났을 경우
                        bombs.remove(bomb)
                        rect = pygame.Rect(bomb_image.get_rect())
                        rect.left = random.randint(0, size[0])  # 새 폭탄의 x 좌표를 무작위로 설정
                        rect.top = -100  # 새 폭탄의 y 좌표 초기화
                        dy = random.randint(3 + elapsed_time // 5000, 7 + elapsed_time // 5000)  # 폭탄 낙하 속도를 무작위로 설정
                        bombs.append({'rect': rect, 'dy': dy})  # 새 폭탄 추가

                # 대각선 폭탄 이동 및 그리기
                for bomb in diagonal_bombs[:]:
                    # 폭탄 위치 업데이트
                    bomb['rect'].left += bomb['dx']
                    bomb['rect'].top += bomb['dy']

                    # 오른쪽 벽에 닿으면 왼쪽으로 이동
                    if bomb['rect'].left > size[0]:
                        bomb['rect'].left = 0 - bomb['rect'].width  # 왼쪽으로 넘어감

                    # 왼쪽 벽에 닿으면 오른쪽으로 이동
                    elif bomb['rect'].left + bomb['rect'].width < 0:
                        bomb['rect'].left = size[0]  # 오른쪽으로 넘어감

                    # 폭탄이 화면 아래로 나가면 제거
                    if bomb['rect'].top > size[1]:
                        diagonal_bombs.remove(bomb)
                    else:
                        # 폭탄을 화면에 그리기
                        screen.blit(bomb_image, bomb['rect'])

                #10초마다 떨어지는 생명 추가
                if not heart_spawned and (elapsed_time - last_heart_time) >= 10000:  # 10초마다 하트 생성
                    last_heart_time = elapsed_time  # 마지막 생성 시간 업데이트
                    heart = pygame.Rect(heart_image.get_rect())
                    heart.left = random.randint(0, size[0])  # 하트의 x좌표를 무작위로 설정
                    heart.top = -150  # 하트의 초기 y좌표 설정
                    heart_dy = random.randint(3 + elapsed_time // 2000, 9 + elapsed_time // 2000)  # 낙하 속도 설정
                    heart_spawned = True

                if heart_spawned:
                    heart.top += heart_dy  # 하트를 아래로 이동
                    if heart.top > size[1]:  # 화면 아래로 나가면
                        heart_spawned = False  # 다시 생성 가능하도록 설정
                        heart.top = -150

                #20초마다 떨어지는 스타 추가
                if not star_spawned and (elapsed_time - last_star_time) >= 20000:  # 10초마다 하트 생성
                    last_star_time = elapsed_time  # 마지막 생성 시간 업데이트
                    star = pygame.Rect(heart_image.get_rect())
                    star.left = random.randint(0, size[0])  # 하트의 x좌표를 무작위로 설정
                    star.top = -150  # 하트의 초기 y좌표 설정
                    star_dy = random.randint(3 + elapsed_time // 2000, 9 + elapsed_time // 2000)  # 낙하 속도 설정
                    star_spawned = True

                if star_spawned:
                    star.top += star_dy  # 하트를 아래로 이동
                    if star.top > size[1]:  # 화면 아래로 나가면
                        star_spawned = False  # 다시 생성 가능하도록 설정
                        star.top = -150

                #13초마다 떨어지는 번개 추가
                if not fast_spawned and (elapsed_time - last_fast_time) >= 13000:  # 13초마다 번개 생성
                    last_fast_time = elapsed_time  # 마지막 생성 시간 업데이트
                    fast = pygame.Rect(fast_image.get_rect())
                    fast.left = random.randint(0, size[0])  # 번개의 x좌표를 무작위로 설정
                    fast.top = -150  # 번개의 초기 y좌표 설정
                    fast_dy = random.randint(3 + elapsed_time // 2000, 9 + elapsed_time // 2000)  # 낙하 속도 설정
                    fast_spawned = True

                if fast_spawned:
                    fast.top += fast_dy  # 번개를 아래로 이동
                    if fast.top > size[1]:  # 화면 아래로 나가면
                        fast_spawned = False  # 다시 생성 가능하도록 설정
                        fast.top = -150

                #15초마다 떨어지는 시계 추가    
                if not clock_spawned and (elapsed_time - last_clock_time) >= 15000:  # 15초마다 시계 생성
                    last_clock_time = elapsed_time  # 마지막 생성 시간 갱신
                    clock_rect = pygame.Rect(clock_image.get_rect())
                    clock_rect.left = random.randint(0, size[0] - clock_rect.width)  # x 좌표 무작위 설정
                    clock_rect.top = -150  # y 좌표 초기화
                    clock_dy = random.randint(3 + elapsed_time // 2000, 9 + elapsed_time // 2000)  # 낙하 속도 설정
                    clock_spawned = True

                if clock_spawned:
                    clock_rect.top += clock_dy
                    if clock_rect.top > size[1]:  # 화면 아래로 나가면 다시 생성 가능
                        clock_spawned = False

                # 대각선 폭탄 생성
                if elapsed_time - last_diagonal_bomb_time > diagonal_bomb_interval:
                    last_diagonal_bomb_time = elapsed_time  # 타이머 초기화
                    diagonal_bomb_interval = random.randint(3000, 5000)  # 새 간격 설정

                    # 대각선 폭탄 추가
                    rect = pygame.Rect(bomb_image.get_rect())
                    rect.left = random.randint(0, size[0] - rect.width)  # 화면의 랜덤 위치
                    rect.top = -100  # 화면 위에서 시작
                    dx = random.choice([-4, 4])  # 왼쪽(-) 또는 오른쪽(+) 방향
                    dy = random.randint(5, 10)
                    diagonal_bombs.append({'rect': rect, 'dx': dx, 'dy': dy})

                # 특성 폭탄 생성
                if elapsed_time - last_special_bomb_time > special_bomb_interval:
                    last_special_bomb_time = elapsed_time
                    special_bomb_interval = random.randint(7000, 10000)

                    bomb_type = random.choice(["slow", "damage"])
                    image = slow_image if bomb_type == "slow" else damage_image  # 크기 조정된 이미지 사용

                    rect = image.get_rect()  # 선택된 이미지 기준으로 Rect 생성
                    rect.left = random.randint(0, size[0] - rect.width)
                    rect.top = -100
                    dy = random.randint(4, 8)

                    special_bombs.append({'rect': rect, 'dy': dy, 'type': bomb_type, 'image': image})

                # 특성 폭탄 이동 및 그리기
                for bomb in special_bombs[:]:
                    bomb['rect'].top += bomb['dy']
                    if bomb['rect'].top > size[1]:
                        special_bombs.remove(bomb)
                    else:
                        screen.blit(bomb['image'], bomb['rect'])  # 크기 조정된 이미지를 화면에 그림

                # 특성 폭탄 충돌 처리
                for bomb in special_bombs[:]:
                    offset = (bomb['rect'].left - person.left + 10, bomb['rect'].top - person.top + 10)
                    if person_dx == 0:
                        collision = check_collision(person_idle_mask, bomb['type'] == "slow" and slow_mask or damage_mask, offset)
                    elif person_dx < 0:
                        collision = check_collision(person_left_masks[animation_index], bomb['type'] == "slow" and slow_mask or damage_mask, offset)
                    else:
                        collision = check_collision(person_right_masks[animation_index], bomb['type'] == "slow" and slow_mask or damage_mask, offset)

                    if collision and not invincible:
                        if bomb['type'] == "slow":
                            # play_effect(etc_effect)
                            special_bombs.remove(bomb)
                            person_speed = max(person_speed - 0.2, 0.2)
                        elif bomb['type'] == "damage":
                            # play_effect(bomb_effect)
                            special_bombs.remove(bomb)
                            lives -= 2
                            if lives <= 0:
                                # gameover_sound()
                                game_over = True
                                game_over_time = (pygame.time.get_ticks() - start_ticks) / 1000
                                bombs.clear()   # 게임 오버 시 모든 폭탄 제거
                                heart.top = -150 # 게임 오버 시 떨어지고 있는 생명 제거
                                heart_spawned = False
                                star.top = -150 # 게임 오버 시 떨어지고 있는 스타 제거
                                star_spawned = False
                                fast.top = -150 # 게임 오버 시 떨어지고 있는 번개 제거
                                fast_spawned = False
                                if bomb in diagonal_bombs:
                                    diagonal_bombs.remove(bomb)

                # 캐릭터 이동 처리
                person.left += person_dx  # 이동 속도를 현재 위치에 더함
                if person.left < -80:  # 화면 왼쪽을 넘어가지 않도록
                    person.left = size[0] - person.width + 70
                elif person.left > size[0] - person.width + 80:  # 화면 오른쪽을 넘어가지 않도록
                    person.left = - 70
                    
                if moving:
                    animation_timer += animation_speed
                    if animation_timer >= 1:
                        animation_timer = 0
                        animation_index = (animation_index + 1) % len(person_left_images)
                    if person_dx < 0:  # 왼쪽으로 이동 중
                        person_image = person_left_images[animation_index]
                    elif person_dx > 0:  # 오른쪽으로 이동 중
                        person_image = person_right_images[animation_index]
                else:
                    person_image = person_idle_image  # 이동하지 않을 때는 기본 이미지

                screen.blit(person_image, person)  # 캐릭터를 화면에 그림

                #생명 충돌 검사 및 생명 증가
                offset = (heart.left - person.left, heart.top - person.top)
                if person_dx == 0:
                    collision = check_collision(person_idle_mask, heart_mask, offset)
                elif person_dx < 0:
                    collision = check_collision(person_left_masks[animation_index], heart_mask, offset)
                else:
                    collision = check_collision(person_right_masks[animation_index], heart_mask, offset)
                
                if collision:
                    # play_effect(heart_effect)
                    lives += 1
                    heart_spawned = False
                    heart.top = -150

                #스타 충돌 검사 
                offset = (star.left - person.left, star.top - person.top)
                if person_dx == 0:
                    collision = check_collision(person_idle_mask, star_mask, offset)
                elif person_dx < 0:
                    collision = check_collision(person_left_masks[animation_index], star_mask, offset)
                else:
                    collision = check_collision(person_right_masks[animation_index], star_mask, offset)
                
                if collision:
                    # play_effect(star_effect)
                    invincible = True
                    invincible_start_time = pygame.time.get_ticks()
                    star_spawned = False
                    star.top = -150

                # 무적 상태 확인 및 해제
                current_time = pygame.time.get_ticks()
                if invincible and current_time - invincible_start_time > 5000:  
                    invincible = False

                #번개 충돌 검사 및 속도 증가
                offset = (fast.left - person.left, fast.top - person.top)
                if person_dx == 0:
                    collision = check_collision(person_idle_mask, fast_mask, offset)
                elif person_dx < 0:
                    collision = check_collision(person_left_masks[animation_index], fast_mask, offset)
                else:
                    collision = check_collision(person_right_masks[animation_index], fast_mask, offset)
                
                if collision:
                    # play_effect(etc_effect)
                    person_speed += 3
                    fast_spawned = False
                    fast.top = -150

                # 시계와 충돌 감지
                offset = (clock_rect.left - person.left, clock_rect.top - person.top)
                if person_dx == 0:
                    collision = check_collision(person_idle_mask, clock_mask, offset)
                elif person_dx < 0:
                    collision = check_collision(person_left_masks[animation_index], clock_mask, offset)
                else:
                    collision = check_collision(person_right_masks[animation_index], clock_mask, offset)

                if collision and clock_spawned: 
                    # play_effect(etc_effect)
                    slow_effect_active = True  # 폭탄 속도 감소 효과 활성화
                    slow_effect_end_time = pygame.time.get_ticks() + 4000  # 4초 동안 효과 지속
                    clock_spawned = False  # 시계 사라짐

                # 폭탄 속도 감소 효과 종료
                if slow_effect_active and pygame.time.get_ticks() > slow_effect_end_time:
                    slow_effect_active = False  # 효과 종료

                for bomb in bombs:
                    bomb_speed = bomb['dy'] // 4 if slow_effect_active else bomb['dy']  # 효과 적용 시 속도 감소
                    bomb['rect'].top += bomb_speed
                    if bomb['rect'].top > size[1]:  # 화면 아래로 나가면 새로운 폭탄 추가
                        bombs.remove(bomb)
                        rect = pygame.Rect(bomb_image.get_rect())
                        rect.left = random.randint(0, size[0] - rect.width)
                        rect.top = -100
                        dy = random.randint(3 + elapsed_time // 5000, 7 + elapsed_time // 5000)
                        bombs.append({'rect': rect, 'dy': dy})
                    
            # 대각선 폭탄 충돌 검사
            for bomb in diagonal_bombs[:]:
                offset = (bomb['rect'].left - person.left - 30, bomb['rect'].top - person.top - 30)
                if person_dx == 0:
                    collision = check_collision(person_idle_mask, bomb_mask, offset)
                elif person_dx < 0:
                    collision = check_collision(person_left_masks[animation_index], bomb_mask, offset)
                else:
                    collision = check_collision(person_right_masks[animation_index], bomb_mask, offset)

                if collision and not invincible:
                    # play_effect(bomb_effect)
                    diagonal_bombs.remove(bomb)
                    # 목숨 감소 로직
                    lives -= 1
                    if lives <= 0:
                        # gameover_sound()
                        game_over = True
                        game_over_time = (pygame.time.get_ticks() - start_ticks) / 1000
                        bombs.clear()   # 게임 오버 시 모든 폭탄 제거
                        heart.top = -150 # 게임 오버 시 떨어지고 있는 생명 제거
                        heart_spawned = False
                        star.top = -150 # 게임 오버 시 떨어지고 있는 스타 제거
                        star_spawned = False
                        fast.top = -150 # 게임 오버 시 떨어지고 있는 번개 제거
                        fast_spawned = False
                        if bomb in special_bombs:
                            special_bombs.remove(bomb)

            # 폭탄 충돌 검사 및 목숨 감소
            for bomb in bombs[:]:
                offset = (bomb['rect'].left - person.left - 30, bomb['rect'].top - person.top - 30)
                if person_dx == 0:
                    collision = check_collision(person_idle_mask, bomb_mask, offset)
                elif person_dx < 0:
                    collision = check_collision(person_left_masks[animation_index], bomb_mask, offset)
                else:
                    collision = check_collision(person_right_masks[animation_index], bomb_mask, offset)
                
                if collision and not invincible:
                    # play_effect(bomb_effect)
                    bombs.remove(bomb)
                    rect = pygame.Rect(bomb_image.get_rect())
                    rect.left = random.randint(0, size[0])
                    rect.top = -100
                    dy = random.randint(3 + elapsed_time // 5000, 7 + elapsed_time // 5000)
                    bombs.append({'rect': rect, 'dy': dy})
                    lives -= 1 
                    
                    if lives <= 0:
                        # gameover_sound()
                        game_over = True
                        game_over_time = (pygame.time.get_ticks() - start_ticks) / 1000
                        bombs.clear()   # 게임 오버 시 모든 폭탄 제거
                        heart.top = -150 # 게임 오버 시 떨어지고 있는 생명 제거
                        heart_spawned = False
                        star.top = -150 # 게임 오버 시 떨어지고 있는 스타 제거
                        star_spawned = False
                        fast.top = -150 # 게임 오버 시 떨어지고 있는 번개 제거
                        fast_spawned = False
                        if bomb in special_bombs:
                            special_bombs.remove(bomb)
                        if bomb in diagonal_bombs:
                            diagonal_bombs.remove(bomb)
                
                #생명그리기
                if heart_spawned == True:
                    screen.blit(heart_image, heart)

                #스타그리기
                if star_spawned == True:
                    screen.blit(star_image, star)

                #번개그리기
                if fast_spawned == True:
                    screen.blit(fast_image, fast)

                #시계그리기
                if clock_spawned:
                    screen.blit(clock_image, clock_rect)

                # 폭탄 그리기
                screen.blit(bomb_image, bomb['rect'])

                # 목숨 개수 표시
                lives_text = life_font.render(f"Lives: {lives}", True, WHITE)
                screen.blit(lives_text, (10, 10))

            # 게임 오버 시 메시지 출력
            if game_over:
                game_over_time_text = gameover_font.render(f"Time: {game_over_time:.2f} sec", True, WHITE)
                screen.blit(gameover_image, (size[0] // 2 - gameover_image.get_width() // 2, size[1] // 2 - gameover_image.get_height()))
                screen.blit(game_over_time_text, (size[0] // 2 - game_over_time_text.get_width() //2, size[1] // 2 + 10))
                endBtn=button_with_image(quit_image,0, 525, quit_image.get_width(), quit_image.get_height(), action=True, centered=True)
                if endBtn == True:
                    return pygame.quit()
                reBtn=button_with_image(re_image,  0, 650, re_image.get_width(), re_image.get_height(), action=True, centered=True)
                if reBtn == True:
                    return runGame()
                
                pygame.display.update()

        if paused and not countdown_active:
            pause_font = pygame.font.SysFont(None, 200)
            pause_text = pause_font.render("PAUSED", True, BLACK)
            screen.blit(pause_text, (size[0] // 2 - pause_text.get_width() // 2, size[1] // 2 - pause_text.get_height() // 2))        

        pygame.display.update()  # 화면 업데이트

def intro():
    # play_intro_sound()
    intro = True

    while intro:
        screen.blit(background_img,(0, 0))
        screen.blit(mainlogo_image, (size[0] // 2 - mainlogo_image.get_width() // 2, size[1] // 2 - mainlogo_image.get_height()))
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        strBtn=button_with_image(start_image, 0, 525, start_image.get_width(), start_image.get_height(), action=True, centered=True)
        if strBtn == True:
            return runGame()
        endBtn=button_with_image(quit_image, 0, 650, quit_image.get_width(), quit_image.get_height(), action=True, centered=True)
        if endBtn == True:
            return pygame.quit()
        pygame.display.update()        

intro()

pygame.quit()  # 게임 종료

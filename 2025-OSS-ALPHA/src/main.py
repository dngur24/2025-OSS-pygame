import pygame
import os
import random

# PyGame 초기화
pygame.init()

# 화면 설정
window_size_x = 800
window_size_y = 600
screen = pygame.display.set_mode((window_size_x, window_size_y))
pygame.display.set_caption("윷놀이")

# 색상 정의
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
LIGHT_BLUE = (153, 204, 255)
ORANGE = (255, 94, 0)
GREEN = (29, 219, 22)
RED = (255, 94, 0)
BLUE = (0, 84, 255)

# 버튼 설정
button_size_x = window_size_x // 20
button_size_y = button_size_x
button_interval = button_size_x * 1.25

yutQ = []

team_color = ["RED", "BLUE", "GREEN", "YELLOW"]

# 인트로 화면 생성
def Intro():
    # 2인용 버튼 생성
    player_num_2_button_rect = pygame.Rect(button_size_x * 1, button_size_y * 1, button_size_x * 5, button_size_y * 13)
    player_num_2_button_color = ORANGE

    # 3인용 버튼 생성
    player_num_3_button_rect = pygame.Rect(button_size_x * 7, button_size_y * 1, button_size_x * 5, button_size_y * 13)
    player_num_3_button_color = YELLOW

    # 4인용 버튼 생성
    player_num_4_button_rect = pygame.Rect(button_size_x * 13, button_size_y * 1, button_size_x * 5, button_size_y * 13)
    player_num_4_button_color = GREEN

    running = True
    player_num = 2
    while running:
        screen.fill(WHITE)

        player_num_font = pygame.font.SysFont('Malgun Gothic', 30)

        # 2인용 버튼 그리기
        pygame.draw.rect(screen, player_num_2_button_color, player_num_2_button_rect)
        player_num_2_text = player_num_font.render("2 people", True, BLACK)
        screen.blit(player_num_2_text, (player_num_2_button_rect.width//2, player_num_2_button_rect.height//2))

        # 3인용 버튼 그리기
        pygame.draw.rect(screen, player_num_3_button_color, player_num_3_button_rect)
        player_num_3_text = player_num_font.render("3 people", True, BLACK)
        screen.blit(player_num_3_text, (player_num_3_button_rect.width//2 + (button_size_x * 6), player_num_3_button_rect.height//2))

        # 4인용 버튼 그리기
        pygame.draw.rect(screen, player_num_4_button_color, player_num_4_button_rect)
        player_num_4_text = player_num_font.render("4 people", True, BLACK)
        screen.blit(player_num_4_text, (player_num_4_button_rect.width//2 + (button_size_x * 12), player_num_4_button_rect.height//2))

        # 이벤트 처리
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if player_num_2_button_rect.collidepoint(event.pos):
                    player_num = 2
                    running = False
                elif player_num_3_button_rect.collidepoint(event.pos):
                    player_num = 3
                    running = False
                elif player_num_4_button_rect.collidepoint(event.pos):
                    player_num = 4
                    running = False

        # 화면 업데이트
        pygame.display.flip()
    
    return player_num


# 윷 던지기 함수 정의
def throw_yoot(isCoupon):
    # 윷가락의 면 결정 (평평한 면 = True, 둥근 면 = False)
    if isCoupon:
        # sticks = [random.choices([True, False], weights=[60, 40])[0] for _ in range(2)]
        # sticks = [0, 4][random.choices([True, False], weights=[60, 40])[0]]
        sticks = [True, True] if random.random() < 0.6 else [False, False]

    else:
        sticks = [random.choices([True, False], weights=[60, 40])[0] for _ in range(4)]
    
    flat_count = sticks.count(True)
    
    if isCoupon:
        if flat_count == 2:
            flat_count = 4
        elif flat_count == 0:
            flat_count = 0

    if flat_count == 4:
        yutQ.append(4)
        return "Yut"  # 윷: 네 개 모두 평평한 면
    elif flat_count == 0:
        yutQ.append(5)
        return "Mo"   # 모: 네 개 모두 둥근 면
    elif flat_count == 3:
        yutQ.append(3)
        return "Geol"  # 걸: 세 개가 평평한 면
    elif flat_count == 2:
        yutQ.append(2)
        return "Gae"  # 개: 두 개가 평평한 면
    elif flat_count == 1:
        # 도: 한 개만 평평한 면일 때 1/4 확률로 백도
        if random.random() < 0.25:
            yutQ.append(-1)
            return "Baegdo"
        else:
            yutQ.append(1)
            return "Do"

def GameBoard(player_num):
    # 이미지 로드
    img_paths = [
        "./pygame-alpha-mine-sweeper/src/img/",
        "./src/img/",
        "./img/"
    ]
    for img_path in img_paths:
        try:
            circle_img = pygame.image.load(os.path.join(img_path, "circle.jpg"))
            bigcircle_img = pygame.image.load(os.path.join(img_path, "bigcircle.jpg"))
            startcircle_img = pygame.image.load(os.path.join(img_path, "startcircle.jpg"))
            line_img = pygame.image.load(os.path.join(img_path, "line.png"))

            bigorange_img = pygame.image.load(os.path.join(img_path, "bigorange.png"))
            orange_img = pygame.image.load(os.path.join(img_path, "orange.png"))

            bigblue_img = []
            bigblue_img.append(pygame.image.load(os.path.join(img_path, "bigblue1.jpg")))
            bigblue_img.append(pygame.image.load(os.path.join(img_path, "bigblue2.jpg")))
            bigblue_img.append(pygame.image.load(os.path.join(img_path, "bigblue3.jpg")))
            bigblue_img.append(pygame.image.load(os.path.join(img_path, "bigblue4.jpg")))

            blue_img = []
            blue_img.append(pygame.image.load(os.path.join(img_path, "blue1.jpg")))
            blue_img.append(pygame.image.load(os.path.join(img_path, "blue2.jpg")))
            blue_img.append(pygame.image.load(os.path.join(img_path, "blue3.jpg")))
            blue_img.append(pygame.image.load(os.path.join(img_path, "blue4.jpg")))


            biggreen_img = []
            biggreen_img.append(pygame.image.load(os.path.join(img_path, "biggreen1.jpg")))
            biggreen_img.append(pygame.image.load(os.path.join(img_path, "biggreen2.jpg")))
            biggreen_img.append(pygame.image.load(os.path.join(img_path, "biggreen3.jpg")))
            biggreen_img.append(pygame.image.load(os.path.join(img_path, "biggreen4.jpg")))

            green_img = []
            green_img.append(pygame.image.load(os.path.join(img_path, "green1.jpg")))
            green_img.append(pygame.image.load(os.path.join(img_path, "green2.jpg")))
            green_img.append(pygame.image.load(os.path.join(img_path, "green3.jpg")))
            green_img.append(pygame.image.load(os.path.join(img_path, "green4.jpg")))


            bigred_img = []
            bigred_img.append(pygame.image.load(os.path.join(img_path, "bigred1.jpg")))
            bigred_img.append(pygame.image.load(os.path.join(img_path, "bigred2.jpg")))
            bigred_img.append(pygame.image.load(os.path.join(img_path, "bigred3.jpg")))
            bigred_img.append(pygame.image.load(os.path.join(img_path, "bigred4.jpg")))

            red_img = []
            red_img.append(pygame.image.load(os.path.join(img_path, "red1.jpg")))
            red_img.append(pygame.image.load(os.path.join(img_path, "red2.jpg")))
            red_img.append(pygame.image.load(os.path.join(img_path, "red3.jpg")))
            red_img.append(pygame.image.load(os.path.join(img_path, "red4.jpg")))


            bigyellow_img = []
            bigyellow_img.append(pygame.image.load(os.path.join(img_path, "bigyellow1.jpg")))
            bigyellow_img.append(pygame.image.load(os.path.join(img_path, "bigyellow2.jpg")))
            bigyellow_img.append(pygame.image.load(os.path.join(img_path, "bigyellow3.jpg")))
            bigyellow_img.append(pygame.image.load(os.path.join(img_path, "bigyellow4.jpg")))

            yellow_img = []
            yellow_img.append(pygame.image.load(os.path.join(img_path, "yellow1.jpg")))
            yellow_img.append(pygame.image.load(os.path.join(img_path, "yellow2.jpg")))
            yellow_img.append(pygame.image.load(os.path.join(img_path, "yellow3.jpg")))
            yellow_img.append(pygame.image.load(os.path.join(img_path, "yellow4.jpg")))

            select_big_img = pygame.image.load(os.path.join(img_path, "bigorange.png"))
            select_img = pygame.image.load(os.path.join(img_path, "orange.png"))

            selected_idx = -1
            selected_i = -1

            select_new = False
            yut_new = False

            select_move_i = -1

            select_coupon = False
            prev_yut_ok = True
            break
        except FileNotFoundError:
            continue
    else:
        raise FileNotFoundError("Image files not found in any of the specified paths.")

    # 게임 변수 설정
    running = True

    # 패널 설정
    panel_pan = pygame.Surface((window_size_x, window_size_y))
    panel_pan.fill(WHITE)

    # 윷 판 버튼 생성
    pan_buttons = []
    xpos = button_size_x * 7
    ypos = button_size_y * 7
    ccc = (0,0)
    """
    10   9   8    7   6   5
    
    11  25            21  4
    
    12      26    22      3
    
               27

    13      23    28      2
    
    14  24           29   1
    
    15  16  17   18  19  20
    """
    board_pos = []

    # 윷 판 테두리 생성
    for i in range(1, 21):
        if i < 6:
            ypos -= button_interval
        elif i < 11:
            xpos -= button_interval
        elif i < 16:
            ypos += button_interval
        else:
            xpos += button_interval


        if i == 5 or i == 10 or i == 15:
            img = bigcircle_img
        elif i == 20:
            img = startcircle_img
        else:
            img = circle_img
        
        button_rect = img.get_rect(center=(xpos, ypos))
        pan_buttons.append((img, button_rect))

        board_pos.append((xpos, ypos))

    # 첫 번째 대각선 그리기
    xpos = button_size_x * 7 - 10
    ypos = button_size_y - 10
    for p in range(6):
        if p == 3:
            xpos -= button_size_x
            ypos += button_size_y
        else:
            if p == 0:
                xpos -= button_size_x
                ypos += button_size_y
            else:
                button_rect = circle_img.get_rect(center=(xpos, ypos))
                pan_buttons.append((circle_img, button_rect))
                
                board_pos.append((xpos, ypos))

                xpos -= button_size_x
                ypos += button_size_y


    # 두 번째 대각선 그리기
    xpos = button_size_x - 10
    ypos = button_size_y - 10
    for p in range(6):
        if p == 0:
            xpos += button_size_x
            ypos += button_size_y
        else:
            if p == 3:
                img = bigcircle_img
                # arrow_img = pygame.image.load(os.path.join(img_path, "rightup.jpg"))
                # arrow_rect = arrow_img.get_rect(center=(xpos - button_size_x, ypos))
                # pan_buttons.append((arrow_img, arrow_rect))
            else:
                img = circle_img
            
            if p == 3:
                ccc = (xpos, ypos)
            button_rect = img.get_rect(center=(xpos, ypos))
            pan_buttons.append((img, button_rect))
            
            board_pos.append((xpos, ypos))
            
            xpos += button_size_x
            ypos += button_size_y
    
    board_pos.append((xpos + (button_size_x + 3), ypos + (button_size_y + 3)))

    # 한번 더 버튼 생성
    coupon_button_rect = pygame.Rect(button_size_x * 6.8, button_size_y * 10, button_size_x * 2, button_size_y)
    coupon_button_color = BLACK

    # 한번 더 버튼 생성
    coupon_select_rect = pygame.Rect(button_size_x * 6.8, button_size_y * 10, button_size_x * 2, button_size_y)
    coupon_select_color = ORANGE

    # 윷 던지기 버튼 생성
    throw_button_rect = pygame.Rect(button_size_x * 9, button_size_y * 10, button_size_x * 3, button_size_y)
    throw_button_color = YELLOW

    # 윷 던지기 선택 효과 생성
    throw_new_rect = pygame.Rect(button_size_x * 9, button_size_y * 10, button_size_x * 3, button_size_y)
    throw_new_color = ORANGE

    # 새로운 말 버튼 생성
    new_piece_button_rect = pygame.Rect(button_size_x * 9, button_size_y * 11, button_size_x * 3, button_size_y)
    new_piece_button_color = LIGHT_BLUE

    # 새로운 말 선택 효과 생성
    select_new_button_rect = pygame.Rect(button_size_x * 9, button_size_y * 11, button_size_x * 3, button_size_y)
    select_new_button_color = ORANGE

    # 윷 판 클릭 버튼 생성
    pan_click_button_rect = pygame.Rect(button_size_x * 9, button_size_y * 9, button_size_x * 3, button_size_y)
    pan_click_button_color = LIGHT_BLUE
    
    now_player = 0
    yut = ""
    log_txt = ""

    num_horse = []
    horses = []
    points = []
    active = []

    coupon = []

    yut_ok = True

    now_horse_idx = 0

    prev_horse_pose = -1
    next_pos_list = []
    next_pos_btn = []
    now_yut_num = 0

    total_time = 60
    count_time = 0
    start_ticks = pygame.time.get_ticks()

    # 게임 루프
    while running:
        screen.fill(WHITE)
        
        # 윷 판 버튼 그리기
        for img, rect in pan_buttons:
            screen.blit(img, rect)

        # 윷 던지기 버튼 그리기
        pygame.draw.rect(screen, throw_button_color, throw_button_rect)
        throw_font = pygame.font.SysFont('Malgun Gothic', 14)
        throw_text = throw_font.render("Yut Throw", True, BLACK)
        screen.blit(throw_text, (throw_button_rect.x + 10, throw_button_rect.y + 10))

        if yut_new:
            # 윷 던지기 선택 그리기
            pygame.draw.rect(screen, throw_new_color, throw_new_rect, 3)
            new_piece_text = new_piece_font.render("", True, BLACK)
            screen.blit(new_piece_text, (throw_new_rect.x + 10, throw_new_rect.y + 10))
        
        # 새로운 말 버튼 그리기
        pygame.draw.rect(screen, new_piece_button_color, new_piece_button_rect)
        new_piece_font = pygame.font.SysFont('Malgun Gothic', 14)
        new_piece_text = new_piece_font.render("New Piece", True, BLACK)
        screen.blit(new_piece_text, (new_piece_button_rect.x + 10, new_piece_button_rect.y + 10))

        if select_new:
            # 새로운 말 선택 그리기
            pygame.draw.rect(screen, select_new_button_color, select_new_button_rect, 3)
            new_piece_text = new_piece_font.render("", True, BLACK)
            screen.blit(new_piece_text, (new_piece_button_rect.x + 10, new_piece_button_rect.y + 10))
        
        # 윷 판 클릭 버튼 그리기
        pygame.draw.rect(screen, pan_click_button_color, pan_click_button_rect)
        pan_click_font = pygame.font.SysFont('Malgun Gothic', 14)
        pan_click_text = pan_click_font.render("Choose the Piece", True, BLACK)
        screen.blit(pan_click_text, (pan_click_button_rect.x + 10, pan_click_button_rect.y + 10))

        # 현재 플레이어 버튼 생성
        now_player_rect = pygame.Rect(button_size_x, button_size_y * 10, button_size_x * 4, button_size_y)
        # pygame.draw.rect(screen, LIGHT_BLUE, now_player_rect)
        # now_player_font = pygame.font.SysFont('Malgun Gothic', 14)
        # now_player_text = now_player_font.render(team_color[now_player] + " 팀 차례", True, BLACK)
        # screen.blit(now_player_textㅊ, (now_player_rect.x + 10, now_player_rect.y + 10))
        # 플레이어 색상 지정
        if now_player == 0:
            button_color = RED  # 빨간색
        elif now_player == 1:
            button_color = BLUE  # 파란색
        elif now_player == 2:
            button_color = GREEN  # 노란색
        else:
            button_color = YELLOW  # 초록색
        pygame.draw.rect(screen, button_color, now_player_rect)
        now_player_font = pygame.font.SysFont('Malgun Gothic', 14)
        now_player_text = now_player_font.render(team_color[now_player] + " Team turn", True, BLACK)
        screen.blit(now_player_text, (now_player_rect.x + 10, now_player_rect.y + 10))

        # 윷 결과 라벨 생성
        yot_result_font = pygame.font.SysFont('Malgun Gothic', 14)
        yot_result_text = yot_result_font.render(yut, True, BLACK)
        yot_result_rect = pygame.Rect(button_size_x * 12 + 10, button_size_y * 10 + 10, 300, 70)
        screen.blit(yot_result_text, (yot_result_rect.x, yot_result_rect.y))

        # 게임 로그 메시지 생성
        yot_result_font = pygame.font.SysFont('Malgun Gothic', 14)
        yot_result_text = yot_result_font.render(log_txt, True, BLACK)
        yot_result_rect = pygame.Rect(400, 550, 400, 70)
        screen.blit(yot_result_text, (yot_result_rect.x, yot_result_rect.y))

        # 플레이어 정보 버튼과 라벨 생성
        player_info_buttons = []
        player_info_labels = []
        img_paths = ["red.jpg", "blue.jpg", "green.jpg", "yellow.jpg"]
        
        for i in range(player_num):
            num_horse.append(4)
            horses.append([0, 0, 0, 0])
            points.append(0)
            active.append(0)
            coupon.append(1)
            # 플레이어 아이콘 버튼 생성
            player_icon_img = pygame.image.load(os.path.join(img_path, img_paths[i]))
            player_icon_rect = player_icon_img.get_rect()
            player_icon_rect.topleft = (button_size_x * 9, i * button_size_y)
            player_info_buttons.append((player_icon_img, player_icon_rect))
            screen.blit(player_icon_img, player_icon_rect)

            # 플레이어 정보 라벨 생성
            player_info_font = pygame.font.SysFont('Malgun Gothic', 14)
            player_info_text = player_info_font.render(str(points[i]) + " / " + str(num_horse[i]) + " - 진출 : " + str(active[i]) + "   쿠폰 : " + str(coupon[i]), True, BLACK)
            player_info_rect = pygame.Rect(button_size_x * 10, i * button_size_y, 500, 50)
            player_info_labels.append((player_info_text, player_info_rect))
            screen.blit(player_info_text, player_info_rect)

        # 한번 더 버튼 그리기
        if coupon[now_player] > 0:
            pygame.draw.rect(screen, coupon_button_color, coupon_button_rect)
            coupon_font = pygame.font.SysFont('Malgun Gothic', 14)
            coupon_text = coupon_font.render("One more time", True, WHITE)
            screen.blit(coupon_text, (coupon_button_rect.x + 10, coupon_button_rect.y + 10))

            if select_coupon:
                pygame.draw.rect(screen, coupon_select_color, coupon_select_rect, 3)
                coupon_text = coupon_font.render("", True, WHITE)
                screen.blit(coupon_text, (coupon_button_rect.x + 10, coupon_button_rect.y + 10))

        # 이동 숫자 버튼 생성
        term_num = 0
        term_num2 = 0
        idx = 0
        # 이동 숫자 버튼들 리스트
        move_btn = []
        for i in yutQ:
            # 이동 버튼 생성
            move_btn.append(pygame.Rect(button_size_x * 12 + (term_num * 40), 480 + (term_num2 * 35), 30, 30))
            move_button_color = LIGHT_BLUE

            move_select_btn = pygame.Rect(button_size_x * 12 + (term_num * 40), 480 + (term_num2 * 35), 30, 30)
            move_select_color = ORANGE

            pygame.draw.rect(screen, move_button_color, move_btn[idx])
            move_font = pygame.font.SysFont('Malgun Gothic', 14)
            move_text = move_font.render(str(i), True, BLACK)
            screen.blit(move_text, (move_btn[idx].x + 10, move_btn[idx].y + 5))

            if select_move_i == idx:
                pygame.draw.rect(screen, move_select_color, move_select_btn, 3)
                move_text = move_font.render("", True, BLACK)
                screen.blit(move_text, (move_btn[idx].x + 10, move_btn[idx].y + 5))
            
            idx = idx + 1
            term_num = term_num + 1
            # 1줄에 8개 배치 후 아래칸에 이어서 배치
            if term_num == 8:
                term_num = 0
                term_num2 = term_num2 + 1

        # 먼저 나가있는 말 리스트
        my_btn_list = []
        # 나가있는 말 인덱스 번호 리스트
        tmp = []
        # 현재 나가있는 말 수
        now_horse = 0
        i = 0
        # 현재 플레이어의 말들을 하나씩 보고
        for h in horses[now_player]:
            # 현재 위치가 나가기전인 0보다 크거나 이미 도착한 30보다 작은 경우 나가있는 말이므로
            # 현재 나가있는 말 수 1증가 후 나가있는 말 인덱스 번호 리스트에 해당 인덱스 추가
            if h > 0 and h < 30:
                now_horse = now_horse + 1
                tmp.append(i)
            i = i + 1

        # 플레이어 별로 색깔에 맞게 말 이미지 생성
        if now_player == 0:
            for i in range(now_horse):
                img = red_img[tmp[i]]
                my_btn_list.append(img.get_rect(center=(520 + (50 * i), 380)))
                screen.blit(img, my_btn_list[i])
        elif now_player == 1:
            for i in range(now_horse):
                img = blue_img[tmp[i]]
                my_btn_list.append(img.get_rect(center=(520 + (50 * i), 380)))
                screen.blit(img, my_btn_list[i])
        elif now_player == 2:
            for i in range(now_horse):
                img = green_img[tmp[i]]
                my_btn_list.append(img.get_rect(center=(520 + (50 * i), 380)))
                screen.blit(img, my_btn_list[i])
        elif now_player == 3:
            for i in range(now_horse):
                img = yellow_img[tmp[i]]
                my_btn_list.append(img.get_rect(center=(520 + (50 * i), 380)))
                screen.blit(img, my_btn_list[i])
        
        if selected_i > -1:
            img = select_img
            selected_btn = img.get_rect(center=(520 + (50 * selected_i), 380))
            screen.blit(img, selected_btn)

        # 각 말들을 위치에 맞는 곳에 배치
        for i in range(len(horses)):
            for j in range(len(horses[i])):
                if i == 0:
                    if horses[i][j] > 0 and horses[i][j] < 30:
                        if horses[i][j] == 5 or horses[i][j] == 10 or horses[i][j] == 15 or horses[i][j] == 27:
                            img = bigred_img[j]
                            rect = img.get_rect(center=board_pos[horses[i][j]-1])
                            screen.blit(img, rect)

                            if i == now_player and selected_idx == j:
                                img = select_big_img
                                rect = img.get_rect(center=board_pos[horses[i][j]-1])
                                screen.blit(img, rect)
                        else:
                            img = red_img[j]
                            rect = img.get_rect(center=board_pos[horses[i][j]-1])
                            screen.blit(img, rect)

                            if i == now_player and selected_idx == j:
                                img = select_img
                                rect = img.get_rect(center=board_pos[horses[i][j]-1])
                                screen.blit(img, rect)
                elif i == 1:
                    if horses[i][j] > 0 and horses[i][j] < 30:
                        if horses[i][j] == 5 or horses[i][j] == 10 or horses[i][j] == 15 or horses[i][j] == 27:
                            img = bigblue_img[j]
                            rect = img.get_rect(center=board_pos[horses[i][j]-1])
                            screen.blit(img, rect)

                            if i == now_player and selected_idx == j:
                                img = select_big_img
                                rect = img.get_rect(center=board_pos[horses[i][j]-1])
                                screen.blit(img, rect)
                        else:
                            img = blue_img[j]
                            rect = img.get_rect(center=board_pos[horses[i][j]-1])
                            screen.blit(img, rect)

                            if i == now_player and selected_idx == j:
                                img = select_img
                                rect = img.get_rect(center=board_pos[horses[i][j]-1])
                                screen.blit(img, rect)
                elif i == 2:
                    if horses[i][j] > 0 and horses[i][j] < 30:
                        if horses[i][j] == 5 or horses[i][j] == 10 or horses[i][j] == 15 or horses[i][j] == 27:
                            img = biggreen_img[j]
                            rect = img.get_rect(center=board_pos[horses[i][j]-1])
                            screen.blit(img, rect)

                            if i == now_player and selected_idx == j:
                                img = select_big_img
                                rect = img.get_rect(center=board_pos[horses[i][j]-1])
                                screen.blit(img, rect)
                        else:
                            img = green_img[j]
                            rect = img.get_rect(center=board_pos[horses[i][j]-1])
                            screen.blit(img, rect)

                            if i == now_player and selected_idx == j:
                                img = select_img
                                rect = img.get_rect(center=board_pos[horses[i][j]-1])
                                screen.blit(img, rect)
                elif i == 3:
                    if horses[i][j] > 0 and horses[i][j] < 30:
                        if horses[i][j] == 5 or horses[i][j] == 10 or horses[i][j] == 15 or horses[i][j] == 27:
                            img = bigyellow_img[j]
                            rect = img.get_rect(center=board_pos[horses[i][j]-1])
                            screen.blit(img, rect)

                            if i == now_player and selected_idx == j:
                                img = select_big_img
                                rect = img.get_rect(center=board_pos[horses[i][j]-1])
                                screen.blit(img, rect)
                        else:
                            img = yellow_img[j]
                            rect = img.get_rect(center=board_pos[horses[i][j]-1])
                            screen.blit(img, rect)

                            if i == now_player and selected_idx == j:
                                img = select_img
                                rect = img.get_rect(center=board_pos[horses[i][j]-1])
                                screen.blit(img, rect)

        # 선택된 말들의 다음 위치 표시 버튼 리스트
        next_pos_btn = []
        # 각 위치에 맞는 이미지로 생성
        for np in next_pos_list:
            if np == 5 or np == 10 or np == 15 or np == 20 or np == 27:
                img = bigorange_img
            else:
                img = orange_img
            rect = img.get_rect(center=board_pos[np - 1])
            next_pos_btn.append(rect)
            screen.blit(img, rect)
        
        if yut_ok:
            log_txt = "Click [Throw Yut] to throw the Yut"
        # 이벤트 처리
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # 던지기 버튼 클릭
                if throw_button_rect.collidepoint(event.pos):
                    # 던지기 가능 상태일때만 작동
                    if yut_ok:
                        yut_new = True
                        selected_idx = -1
                        selected_i = -1
                        select_new = False
                        select_move_i = -1

                        start_ticks = pygame.time.get_ticks()

                        # 윷 던지기
                        yut = throw_yoot(select_coupon)
                        # 쿠폰 사용중이면 쿠폰 개수 감소
                        if select_coupon:
                            coupon[now_player] = coupon[now_player] - 1
                            yut_ok = prev_yut_ok
                        # 윷이나 모가 아니면 던지기 불가로 세팅
                        # 윷이나 모면 던지기 가능 상태 유지
                        elif yut not in ["윷", "모"]:
                            log_txt = (
                                "[" + yut + "]is out! Click the button to see where you can move. \n"
                                "- You can select the horse you want to move by using [Select Piece]. \n"
                                "- You can use [New Piece] to bring out new words. \n"
                                "- If you do not [Select a Piece], the horse that moved last will move."
                            )
                            yut_ok = False
                        else:
                            log_txt = "[" + yut + "]is out! You're lucky. You can roll the Yut one more time!"
                        # 쿠폰 사용종료 세팅
                        select_coupon = False
                    # 던지기 불가일 경우 말 이동해달라 출력
                    else:
                        log_txt = "Please move the piece"
                elif coupon_button_rect.collidepoint(event.pos):
                    selected_idx = -1
                    selected_i = -1
                    select_new = False
                    yut_new = False
                    select_move_i = -1

                    now_horse_idx = 0
                    # 다음 위치 관련 리스트를 비워 주황버튼들 제거
                    next_pos_list = []
                    next_pos_btn = []

                    prev_yut_ok = yut_ok

                    select_coupon = not select_coupon
                    if select_coupon:
                        yut_ok = True
                    else:
                        yut_ok = prev_yut_ok
                # 새 말 버튼 클릭
                elif new_piece_button_rect.collidepoint(event.pos):
                    # 윷 던지기 가능 상태일 경우 윷을 마저 던져달라고 출력
                    if yut_ok:
                        log_txt = "Please throw the Yut sticks"
                    # 윷 던지기 불가일 경우 새 말 지정
                    else:
                        selected_idx = -1
                        selected_i = -1
                        select_new = True
                        yut_new = False
                        select_move_i = -1
                        select_coupon = False

                        # chk를 우선 True로 초기화
                        chk = True
                        # 플레이어의 말을 모두 보면서
                        for h in range(len(horses[now_player])):
                            # 현재 위치가 0인 말을 새 말로 지정하고 chk를 False로 지정
                            if horses[now_player][h] == 0:
                                now_horse_idx = h
                                chk = False
                                break
                        
                        # chk가 반복을 끝나도 True인 경우 모든 말이 나가있는 경우로 오류 메시지 출력
                        if chk:
                            log_txt = "There is no new piece"
                else:
                    i = 0
                    for my_btn in my_btn_list:
                        # 나가 있는 말 버튼을 선택한 경우
                        if my_btn.collidepoint(event.pos):
                            # 아직 윷을 던질 수잇으면 던져달라고 하기
                            if yut_ok:
                                log_txt = "Please throw the Yut sticks again"
                            # 윷을 다 던진 상태면 현재 말 인덱스를 세팅해주기
                            else:
                                now_horse_idx = tmp[i]
                                selected_idx = tmp[i]
                                selected_i = i
                                select_new = False
                                yut_new = False
                                select_move_i = -1
                                select_coupon = False
                                break
                        i = i + 1

                    for npi in range(len(next_pos_btn)):
                        # 다음 이동위치 주황버튼을 선택한 경우
                        if next_pos_btn[npi].collidepoint(event.pos):
                            # 화면에 출력된 메시지들은 빈칸으로 생성
                            log_txt = ""
                            yut = ""
                            # 이동전 위치 백업
                            prev_horse_pos = horses[now_player][now_horse_idx]
                            # 이동할 말을 다음 위치로 변경
                            horses[now_player][now_horse_idx] = next_pos_list[npi]
                            selected_idx = -1
                            selected_i = -1
                            select_new = False
                            yut_new = False
                            select_move_i = -1
                            select_coupon = False

                            # 다음 위치 관련 리스트를 비워 주황버튼들 제거
                            next_pos_list = []
                            next_pos_btn = []
                            # 이동한 이동횟수는 리스트에서 제거
                            yutQ.remove(now_yut_num)

                            # 현재 플레이어의 4개의 말을 보면서
                            for hi in range(4):
                                # 현 위치가 0이 아니면서
                                if prev_horse_pos != 0:
                                    # 현재 말이 이전에 이동한 위치와 동일하다면
                                    # 말을 업은 상태로 해당 말도 똑같이 이동
                                    if horses[now_player][hi] == prev_horse_pos:
                                        horses[now_player][hi] = horses[now_player][now_horse_idx]
                                

                            # 플레이어들을 전체를 보고
                            for pi in range(player_num):
                                # 현재 플레이어와 같은 번호면 넘기고
                                if pi == now_player:
                                    continue
                                # 다른 번호면 해당 플레이어의 4개의 말을 모두 보고
                                for hi in range(4):
                                    # 현재 말이 이동후의 위치가 다른 플레이어의 말과 위치가 동일하고 30이 아니면 말을 먹은 상태
                                    # 30은 다 돌아서 점수를 낸 말을 의미
                                    # 먹힌 말은 0번으로 되돌리고 윷을 다시 던질 수 있게 yut_ok를 True로 지정
                                    if horses[pi][hi] == horses[now_player][now_horse_idx] and horses[now_player][now_horse_idx] != 30:
                                        horses[pi][hi] = 0
                                        yut_ok = True
                                        log_txt = "You've captured your opponent's piece! You can roll the Yut one more time! Yay!"

                            # 말이 이동할 남은 윷의 수가 0이고 현재 윷을 던지기 불가능 상태라면 모든 이동을 다한 상태
                            if len(yutQ) == 0 and not yut_ok:
                                # 윷 던지기를 True로 만들고
                                yut_ok = True
                                yut = ""

                                # 다음 플레이어로 변경
                                # 숫자가 현 플레이어 수보다 커지면 첫 플레이어인 0으로 생성
                                now_player = now_player + 1
                                if now_player >= player_num:
                                    now_player = 0
                                
                                count_time = 0
                                start_ticks = pygame.time.get_ticks()

                            break

                    i = 0
                    for move_btn_1 in move_btn:
                        # 이동 횟수 버튼 선택 시
                        if move_btn_1.collidepoint(event.pos):
                            selected_idx = -1
                            selected_i = -1
                            select_new = False
                            yut_new = False
                            select_move_i = i
                            select_coupon = False

                            # 현재 윷 이동 수를 저장
                            now_yut_num = yutQ[i]
                            # 이동가능한 다음 위치 리스트 새로 생성
                            next_pos_list = []
                            # 이동 전 위치 저장
                            prev_pos = horses[now_player][now_horse_idx]
                            # 이동 전 칸의 위치별로 이동 가능한 위치 리스트들 생성
                            if prev_pos == 5:
                                if yutQ[i] == -1:
                                    next_pos_list.append(4)
                                elif yutQ[i] == 3:
                                    next_pos_list.append(27)
                                    next_pos_list.append(8)
                                elif yutQ[i] < 3:
                                    next_pos_list.append(20 + yutQ[i])
                                    next_pos_list.append(5 + yutQ[i])
                                else:
                                    next_pos_list.append(19 + yutQ[i])
                                    next_pos_list.append(5 + yutQ[i])
                            elif prev_pos == 10:
                                if yutQ[i] == -1:
                                    next_pos_list.append(9)
                                elif yutQ[i] == 3:
                                    next_pos_list.append(27)
                                    next_pos_list.append(13)
                                elif yutQ[i] < 3:
                                    next_pos_list.append(24 + yutQ[i])
                                    next_pos_list.append(10 + yutQ[i])
                                else:
                                    next_pos_list.append(24 + yutQ[i])
                                    next_pos_list.append(10 + yutQ[i])
                            elif prev_pos == 15:
                                if yutQ[i] == -1:
                                    next_pos_list.append(14)
                                    next_pos_list.append(24)
                                else:
                                    next_pos_list.append(15 + yutQ[i])
                            elif prev_pos == 20:
                                if yutQ[i] == -1:
                                    next_pos_list.append(19)
                                else:
                                    next_pos_list.append(30)
                            elif prev_pos == 27:
                                if yutQ[i] == -1:
                                    next_pos_list.append(22)
                                    next_pos_list.append(26)
                                elif yutQ[i] == 3:
                                    next_pos_list.append(20)
                                    next_pos_list.append(15)
                                elif yutQ[i] < 3:
                                    next_pos_list.append(27 + yutQ[i])
                                    next_pos_list.append(22 + yutQ[i])
                                else:
                                    next_pos_list.append(30)
                                    next_pos_list.append(12 + yutQ[i])
                            elif prev_pos == 0:
                                if yutQ[i] == -1:
                                    next_pos_list.append(19)
                                else:
                                    next_pos_list.append(yutQ[i])
                            elif prev_pos == 21:
                                if yutQ[i] == -1:
                                    next_pos_list.append(5)
                                elif yutQ[i] == 1:
                                    next_pos_list.append(22)
                                elif yutQ[i] == 2:
                                    next_pos_list.append(27)
                                elif yutQ[i] < 5:
                                    next_pos_list.append(20 + yutQ[i])
                                else:
                                    next_pos_list.append(15)
                            elif prev_pos == 22:
                                if yutQ[i] == -1:
                                    next_pos_list.append(21)
                                elif yutQ[i] == 1:
                                    next_pos_list.append(27)
                                elif yutQ[i] < 4:
                                    next_pos_list.append(21 + yutQ[i])
                                else:
                                    next_pos_list.append(11 + yutQ[i])
                            elif prev_pos == 23:
                                if yutQ[i] == -1:
                                    next_pos_list.append(27)
                                elif yutQ[i] == 1:
                                    next_pos_list.append(24)
                                else:
                                    next_pos_list.append(13 + yutQ[i])
                            elif prev_pos == 24:
                                if yutQ[i] == -1:
                                    next_pos_list.append(23)
                                else:
                                    next_pos_list.append(14 + yutQ[i])
                            else:
                                if prev_pos + yutQ[i] >= 30:
                                    next_pos_list.append(30)
                                elif prev_pos < 20 and prev_pos + yutQ[i] > 20:
                                    next_pos_list.append(30)
                                else:
                                    next_pos_list.append(prev_pos + yutQ[i])

                        i = i + 1

        # 전체 플레이어들을 보면서        
        for pi in range(player_num):
            # 현재 말들이 30번에 있는게 몇개있지 세어서 현재 점수 생성
            total_point = 0
            for hi in range(4):
                if horses[pi][hi] == 30:
                    total_point = total_point + 1
            points[pi] = total_point

            # 현재 0 초과 30 미만에 있는게 몇개인지 세어서 진출 개수 생성
            total_point = 0
            for hi in range(4):
                if 0 < horses[pi][hi] < 30:
                    total_point = total_point + 1
            active[pi] = total_point

        count_time = (pygame.time.get_ticks() - start_ticks) // 1000
        # 타이머

        timer_font = pygame.font.SysFont('Malgun Gothic', 14)
        timer_text = timer_font.render(str(count_time) + " / " + str(total_time), True, BLACK)
        screen.blit(timer_text, (now_player_rect.x + 10, now_player_rect.y - 20))

        if count_time >= total_time:
            # 윷 던지기를 True로 만들고
            yut_ok = True
            yut = ""

            # 다음 위치 관련 리스트를 비워 주황버튼들 제거
            next_pos_list = []
            next_pos_btn = []
            yutQ.clear()

            selected_idx = -1
            selected_i = -1
            select_new = False
            yut_new = False
            select_move_i = -1
            select_coupon = False

            # 다음 플레이어로 변경
            # 숫자가 현 플레이어 수보다 커지면 첫 플레이어인 0으로 생성
            now_player = now_player + 1
            if now_player >= player_num:
                now_player = 0
                                
            count_time = 0
            start_ticks = pygame.time.get_ticks()

        # 화면 업데이트
        pygame.display.flip()

        if points[now_player] >= 4:
            log_txt = "Goal! " + team_color[now_player] + "Team has moved all the pieces!"
            return now_player


def ResultPage():
    result_rect = pygame.Rect(window_size_x // 2, window_size_y // 2, window_size_x // 4, window_size_y // 4)
    result_color = LIGHT_BLUE

    while True:
        pygame.draw.rect(screen, result_color, result_rect)
        result_font = pygame.font.SysFont('Malgun Gothic', 14)
        result_text = result_font.render(team_color[now_player] + " Team Victory", True, BLACK)
        screen.blit(result_text, (result_rect.x // 2, result_rect.y // 2))

        # 화면 업데이트
        pygame.display.flip()

player_num = Intro()
now_player = GameBoard(player_num)

# PyGame 종료
pygame.quit()
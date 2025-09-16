import time
import pygame
import os
from config import *
# from sound import *

RUNNING = [pygame.image.load(os.path.join("Assets/Dino", "DinoRun1.png")),
           pygame.image.load(os.path.join("Assets/Dino", "DinoRun2.png"))]
JUMPING = pygame.image.load(os.path.join("Assets/Dino", "DinoJump.png"))
DUCKING = [pygame.image.load(os.path.join("Assets/Dino", "DinoDuck1.png")),
           pygame.image.load(os.path.join("Assets/Dino", "DinoDuck2.png"))]

FULL_HEART = pygame.image.load(os.path.join("Assets/Hearts", "FullHeart.png"))
EMPTY_HEART = pygame.image.load(os.path.join("Assets/Hearts", "EmptyHeart.png"))

# sound_manager = SoundManager()  # SoundManager 객체 생성

class Dinosaur:
    X_POS = 80  # 가로 히트박스 크기
    Y_POS = 310  # 세로 히트박스 크기
    Y_POS_DUCK = 340  # 엎드리기 높이

    JUMP_VEL = 9.0  # 점프 높이
    DOUBLE_JUMP_VEL = 8.0  # 이단 점프 높이

    HP = 3  # 공룡 체력

    is_invincible = False  # 현재 무적 상태인지 확인
    invincible_start_time = 0  # 무적이 시작된 시간
    invincible_duration = 0.5  # 무적 지속 시간 (0.5초)

    blink_duration = 0.1  # 깜빡이는 시간 간격
    last_blink_time = 0  # 마지막 깜빡인 시간
    blink_visible = True  # 깜빡임 상태

    def __init__(self):
        self.duck_img = DUCKING  # 엎드린 이미지 할당
        self.run_img = RUNNING  # 달리는 이미지 할당
        self.jump_img = JUMPING  # 점프 이미지 할당

        self.dino_duck = False  # 공룡 엎드리기 상태
        self.dino_run = True  # 공룡 달리기 상태
        self.dino_jump = False  # 공룡 점프 상태
        self.double_jump_active = False  # 이단 점프 활성화 상태
        self.dino_alive = True  # 공룡 생존 상태

        self.step_index = 0
        self.jump_vel = self.JUMP_VEL  # 공룡 점프속도 설정
        self.image = self.run_img[0]  # 초기 이미지 설정
        self.dino_rect = self.image.get_rect()  # 히트박스 설정
        self.dino_rect.x = self.X_POS  # 히트박스 가로 크기 설정
        self.dino_rect.y = self.Y_POS  # 히트박스 세로 크기 설정
        self.dino_HP = self.HP  # 공룡 체력 설정

        self.dino_HP = self.HP  # 공룡 체력 설정
        self.hart_position = (10, 10)  # 하트 위치 (왼쪽 위)
        self.is_hurt = False  # 데미지 입었는지 여부

        # self.sound_manager = sound_manager
        self.is_sliding = False
        self.slide_start_time = 0  # 슬라이딩 시작 시간
        self.slide_sound_duration = 5.0  # 슬라이딩 효과음 길이

    def update(self, userInput, sound_manager):  # 공룡 상태 업데이트
        # 공룡 상태에 따라 동작 호출
        if self.dino_duck:
            self.duck()
        if self.dino_run:
            self.run()
        if self.dino_jump:
            self.jump()  # 점프 처리
        elif self.double_jump_active:  # 이단 점프 처리
            self.double_jump()

        if self.step_index >= 10:
            self.step_index = 0

        # 무적 시간이 끝났는지 확인
        if self.is_invincible and (time.time() - self.invincible_start_time > self.invincible_duration):
            self.is_invincible = False  # 무적 해제

        # 깜빡임 처리
        if self.is_hurt:  # 데미지를 입었을 때
            current_time = time.time()
            if current_time - self.last_blink_time >= self.blink_duration:
                self.blink_visible = not self.blink_visible  # 깜빡임 상태 토글
                self.last_blink_time = current_time  # 마지막 깜빡인 시간 업데이트

            # 피해를 받은 후 깜빡임이 끝나는 시간을 설정
            if current_time - self.invincible_start_time >= self.invincible_duration:
                self.is_hurt = False  # 깜빡임 종료
                self.blink_visible = True  # 깜빡임 종료 시 보이게 설정

        current_slide_time = time.time()  # 슬라이딩의 현재 시간 불러오기

        # 입력에 따라 상태 변경
        if userInput[pygame.K_UP]:
            if not self.dino_jump:  # 첫 번째 점프
                # self.sound_manager.play_jump()  # 점프 효과음
                self.dino_duck = False
                self.dino_run = False
                self.dino_jump = True
                self.jump_vel = self.JUMP_VEL  # 점프 속도 초기화
            #2단 점프 부분
                self.double_jump_active = True  # 이단 점프 가능 상태로 설정
            # elif self.double_jump_active:  # 점프 중일 때 다시 점프 (이단 점프)
               # self.sound_manager.play_jump()  # 점프 효과음
               # self.double_jump()

        elif not self.dino_jump and userInput[pygame.K_DOWN]:
            if not self.is_sliding:  # 슬라이딩 중 효과음 재생
                # self.sound_manager.play_slide()
                self.is_sliding = True
                self.slide_start_time = current_slide_time
            # 효과음이 끝났는지 확인
            elif current_slide_time - self.slide_start_time >= self.slide_sound_duration:
                # sound_manager.play_slide()
                self.slide_start_time = current_slide_time
            self.dino_duck = True
            self.dino_run = False
            self.dino_jump = False
            self.double_jump_active = False  # 엎드릴 때 이단 점프 해제
        elif not (self.dino_jump or userInput[pygame.K_DOWN]):
            if self.is_sliding:
                # sound_manager.stop_slide()  # 슬라이딩 안하면 효과음 재생 X
                self.is_sliding = False
            self.dino_duck = False
            self.dino_run = True
            self.dino_jump = False

        # 공룡이 화면을 넘어가지 않도록 제한
        if self.dino_rect.y < 0:
            self.dino_rect.y = 0  # 위로 나가지 않도록 제한

    def duck(self):  # 공룡 엎드리기 로직
        self.image = self.duck_img[self.step_index // 5]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS_DUCK
        self.step_index += 1

    def run(self):  # 공룡 달리기 로직
        self.image = self.run_img[self.step_index // 5]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS
        self.step_index += 1

    def jump(self):  # 공룡 점프 로직
        self.image = self.jump_img
        if self.dino_jump:
            self.dino_rect.y -= self.jump_vel * 3
            self.jump_vel -= 0.6  # 점프 속도 감소
        if self.jump_vel < -self.JUMP_VEL:  # 점프가 끝나면
            self.dino_jump = False
            self.jump_vel = self.JUMP_VEL  # 초기 점프 속도로 되돌리기
            self.dino_rect.y = self.Y_POS  # Y축 위치를 바닥으로 초기화 하는 코드 추가
            self.double_jump_active = True  # 이단 점프 가능 상태로 설정

    def double_jump(self):  # 이단 점프 로직
        self.image = self.jump_img
        self.dino_rect.y -= self.DOUBLE_JUMP_VEL * 3  # 이단 점프를 위한 속도
        self.double_jump_active = False  # 이단 점프 사용 후 해제
        # print("2단 접프")

    def draw(self, SCREEN):  # 공룡 그리기 로직
        if self.blink_visible:  # 깜빡이는 상태일 때만 공룡 그리기
            SCREEN.blit(self.image, (self.dino_rect.x, self.dino_rect.y))
            # pygame.draw.rect(SCREEN, (255, 0, 0), self.dino_rect, 2)   공룡 히트박스 표시

        # 하트 그리기
        for i in range(self.HP):
            heart_image = FULL_HEART if i < self.dino_HP else EMPTY_HEART
            SCREEN.blit(heart_image, (self.hart_position[0] + (i * 32), self.hart_position[1]))  # 하트 위치 조정

    def take_damage(self):  # 공룡 데미지 로직
        if not self.is_invincible:  # 무적이 아닐 때만 체력 감소
            self.dino_HP -= 1
            self.is_hurt = True  # 피해를 받았음을 표시
            if self.dino_HP > 0:
                # self.sound_manager.play_damage()
                self.invincibility()  # 무적 함수 호출
            else:
                # self.sound_manager.play_death()
                # self.sound_manager.stop_bgm()  # 죽으면 BGM 정지
                self.dino_alive = False

    # 무적 함수
    def invincibility(self):
        self.is_invincible = True
        self.invincible_start_time = time.time()
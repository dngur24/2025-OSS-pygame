import pygame
import os
import random
from config import *

CLOUD = pygame.image.load(os.path.join("Assets/Other/Cloud.png"))
ROAD = pygame.image.load(os.path.join("Assets/Other/Track.png"))
THEME_WHITE = (255,255,255) #밝은 테마 색상
THEME_BALCK = (20,20,50) #어두운 테마 색상

THEME_ocean=pygame.image.load(os.path.join("Assets/Other/ocean.jpg")) # 바다 테마
THEME_space=pygame.image.load(os.path.join("Assets/Other/space.jpg")) # 우주 테마
THEME_city=pygame.image.load(os.path.join("Assets/Other/city.jpg")) # 도시 테마

x_pos_bg = 0 # 배경화면 x축 시작위치
y_pos_bg = 380 # 배경화면 축 시작위치

class BackgroundManager:
    def __init__(self, theme_kind):
        # 테마 선택
        if theme_kind == 'white':
            self.theme = THEME_WHITE
        elif theme_kind == 'black':
            self.theme = THEME_BALCK
        
        self.Track = Track(ROAD, y_pos_bg)  # Background 객체 생성
        # self.Track = Track(THEME_city, y_pos_bg)  # Background 객체 생성
        self.Cloud = Cloud(CLOUD, SCREEN_WIDTH) #Cloud 객체 생성

    def background_setup(self):
        SCREEN.fill(self.theme)

    def background_update(self):
        self.Track.update()  # game_speed는 Background 클래스에서 직접 참조
        self.Track.draw(SCREEN)  # SCREEN은 config에서 직접 참조
        self.Cloud.update()
        self.Cloud.draw()    

class Track:
    def __init__(self, image, y_pos):
        self.image = image
        self.y_pos = y_pos
        self.x_pos = 0  # 초기 x 위치 설정
        self.image_width = self.image.get_width()

    def update(self):
        # 배경 이미지를 좌우로 스크롤
        global game_speed
        self.x_pos -= game_speed
        if self.x_pos <= -self.image_width:
            self.x_pos = 0  # 이미지가 화면을 벗어나면 위치를 초기화

    def draw(self,screen):
        # 첫 번째와 두 번째 이미지를 이어서 화면에 그림
        screen.blit(self.image, (self.x_pos, self.y_pos))
        screen.blit(self.image, (self.x_pos + self.image_width, self.y_pos))
        
class Cloud:
    def __init__(self, image, screen_width):
        self.x = screen_width + random.randint(3, 10)
        self.y = random.randint(50, 100)
        self.image = image
        self.width = self.image.get_width()

    def update(self):
        self.x -= game_speed
        if self.x < -self.width:
            self.x = SCREEN_WIDTH + random.randint(2500, 3000)
            self.y = random.randint(50, 100)

    def draw(self):
        SCREEN.blit(self.image, (self.x, self.y))







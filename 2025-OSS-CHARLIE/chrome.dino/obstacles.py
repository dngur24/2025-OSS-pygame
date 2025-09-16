import pygame
import random
import os

# 장애물 이미지 로드
SMALL_CACTUS = [pygame.image.load(os.path.join("Assets/Cactus", "SmallCactus1.png")),
                pygame.image.load(os.path.join("Assets/Cactus", "SmallCactus2.png")),
                pygame.image.load(os.path.join("Assets/Cactus", "SmallCactus3.png"))]
LARGE_CACTUS = [pygame.image.load(os.path.join("Assets/Cactus", "LargeCactus1.png")),
                pygame.image.load(os.path.join("Assets/Cactus", "LargeCactus2.png")),
                pygame.image.load(os.path.join("Assets/Cactus", "LargeCactus3.png"))]
BIRD = [pygame.image.load(os.path.join("Assets/Bird", "Bird1.png")),
        pygame.image.load(os.path.join("Assets/Bird", "Bird2.png"))]

# 장애물 매니저
class ObstacleManager:
    def __init__(self, screen_width):
        self.obstacles = [] # 현재 화면에 있는 장애물 리스트
        self.screen_width = screen_width # 장애물 생성 위치 설정을 위한 화면 너비
        self.fram_counter=0

    def update(self, game_speed):

        # 장애물이 없을 때 새 장애물 생성
        if len(self.obstacles) == 0:
            obstacle_type = random.choice([SmallCactus, LargeCactus, Bird]) #장애물 타입 랜덤 선택
            # 선택된 타입에 따라 새로운 장애물 생성
            if obstacle_type == SmallCactus:
                self.obstacles.append(SmallCactus(SMALL_CACTUS, self.screen_width))
            elif obstacle_type == LargeCactus:
                self.obstacles.append(LargeCactus(LARGE_CACTUS, self.screen_width))
            elif obstacle_type == Bird:
                self.obstacles.append(Bird(BIRD, self.screen_width))

        for obstacle in self.obstacles: # 모든 장애물 업데이트
            obstacle.update(game_speed)
            if obstacle.rect.x < -obstacle.rect.width:# 화면 밖으로 나가면 리스트에서 제거
                self.obstacles.pop(0)

    def draw(self, screen): # 모든 장애물 그리기
        for obstacle in self.obstacles:
            obstacle.draw(screen)

# 장애물 기본 클래스(작은 선인장, 큰 선인장, 새 클래스으 부모 클래스)
class Obstacle:
    def __init__(self, image, type, screen_width):
        self.image = image #장애물 이미지 리스트
        self.type = type #이미지 리스트에 사용할 인덱스
        self.rect = self.image[self.type].get_rect() # 장애물 히트박스 설정
        self.rect.x = screen_width #장애물 초기 x위치

    def update(self, game_speed): #장애물 위치 업데이트
        self.rect.x -= game_speed//2 #장애물의 X좌표를 갑소시켜 왼쪽으로 이동

    def draw(self, screen): #장애물 위치 업데이트
        screen.blit(self.image[self.type], self.rect) #이미지 그리기

# 작은 선인장
class SmallCactus(Obstacle):
    def __init__(self, image, screen_width):
        self.type = random.randint(0, 2) # 선인장 이미지 랜덤 선택
        super().__init__(image, self.type, screen_width) #부모 클래스 초기화
        self.rect.y = 325 # 위치 설정

# 큰 선인장
class LargeCactus(Obstacle):
    def __init__(self, image, screen_width):
        self.type = random.randint(0, 2) # 선인장 이미지 랜덤 선택
        super().__init__(image, self.type, screen_width)#부모 클래스 초기화
        self.rect.y = 300 # 위치 설정

# 새 장애물
class Bird(Obstacle):
    def __init__(self, image, screen_width):
        self.type = 0 # 새 기본 이미지 설정
        super().__init__(image, self.type, screen_width)#부모 클래스 초기화
        self.rect.y = 250 #Y새의 위치
        self.index = 0 #애니메이션 인덱스 초기화

    def draw(self, screen):# 새 애니메이션 그리기
        if self.index >= 9:# 인덱스 범위 넘으면 리셋
            self.index = 0
        screen.blit(self.image[self.index // 5], self.rect) #새의 현재 이미지 그리기
        self.index += 1 # 애니메이션 인덱스 증가

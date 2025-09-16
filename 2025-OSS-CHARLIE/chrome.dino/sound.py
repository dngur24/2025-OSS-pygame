import pygame
import os

class SoundManager:
    def __init__(self):
        pygame.mixer.init()  # 사운드 시스템 초기화
        
        # 배경음악 로드
        self.bgm = pygame.mixer.Sound(os.path.join("Assets/Sounds", "background.mp3"))
        
        # 효과음 로드
        self.jump_sound = pygame.mixer.Sound(os.path.join("Assets/Sounds", "jump.mp3"))
        self.death_sound = pygame.mixer.Sound(os.path.join("Assets/Sounds", "death.mp3"))
        self.point_sound = pygame.mixer.Sound(os.path.join("Assets/Sounds", "score-earning.mp3"))
        self.damage_sound = pygame.mixer.Sound(os.path.join("Assets/Sounds", "damaged.mp3"))
        self.slide_sound = pygame.mixer.Sound(os.path.join("Assets/Sounds", "slide.mp3"))
        self.slide_channel = None
        
        # 기본 볼륨 설정
        self.bgm_volume = 0.2
        self.sfx_volume = 0.2
        
        # 볼륨 적용
        self.bgm.set_volume(self.bgm_volume)
        self.jump_sound.set_volume(self.sfx_volume)
        self.death_sound.set_volume(self.sfx_volume)
        self.point_sound.set_volume(self.sfx_volume)
        self.damage_sound.set_volume(self.sfx_volume)
        self.slide_sound.set_volume(self.sfx_volume)
        
        self.bgm_playing = False
        self.is_sliding = False
    
    def play_bgm(self):
        #배경음악을 재생
        if not self.bgm_playing:
            self.bgm.play(-1)  # -1은 무한 반복
            self.bgm_playing = True
    
    def stop_bgm(self):
        #배경음악을 중지
        self.bgm.stop()
        self.bgm_playing = False
    
    def play_jump(self):
        #점프 효과음을 재생
        self.jump_sound.play()
    
    def play_death(self):
        #사망 효과음을 재생
        self.death_sound.play()
    
    def play_point(self):
        #점수 획득 효과음을 재생
        self.point_sound.play()

    def play_damage(self):
        #피해 효과음 재생
        self.damage_sound.play()

    def play_slide(self):
        #슬라이드 효과음 재생
        self.slide_sound.play()

    def stop_slide(self):
        #슬라이드 효과음 정지
        self.slide_sound.stop()
    
    def set_bgm_volume(self, volume):
        #배경음악 볼륨을 설정 (0.0 ~ 1.0)
        self.bgm_volume = max(0.0, min(1.0, volume))
        self.bgm.set_volume(self.bgm_volume)
    
    def set_sfx_volume(self, volume):
        #효과음 볼륨을 설정 (0.0 ~ 1.0)
        self.sfx_volume = max(0.0, min(1.0, volume))
        self.jump_sound.set_volume(self.sfx_volume)
        self.death_sound.set_volume(self.sfx_volume)
        self.point_sound.set_volume(self.sfx_volume)
        self.damage_sound.set_volume(self.sfx_volume)
        self.slide_sound.set_volume(self.sfx_volume)
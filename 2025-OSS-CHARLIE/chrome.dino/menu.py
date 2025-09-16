import pygame
import os
from config import *
import json
# from sound import * 
from basic import main
from highscore import high_scores

# sound_manager = SoundManager()


class Menu:
    def __init__(self):
        # 화면 설정 가져오기
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Dinosaur Game")
        self.screen_width = SCREEN_WIDTH
        self.screen_height = SCREEN_HEIGHT
        # BGM볼륨 초기화 (0.0 ~ 1.0)
        self.bgm_volume = 1.0
        self.sfx_volume = 1.0
        # 테마 기본 설정
        self.theme = "day"

        # 시작 버튼 설정
        self.button_width = 350
        self.button_height = 50
        self.button_spacing = 20  # 버튼 간격 설정

        # 시작 버튼 위치
        self.button_x = self.screen_width // 2 - self.button_width // 2
        self.button_y = self.screen_height // 2

        # 설정 버튼 위치
        self.settings_button_x = self.button_x
        self.settings_button_y = self.button_y + self.button_height + self.button_spacing

        # 폰트 설정
        self.title_font = pygame.font.Font('freesansbold.ttf', 48)
        self.button_font = pygame.font.Font('freesansbold.ttf', 36)
        self.settings_font = pygame.font.Font('freesansbold.ttf', 24)

        # 색상 설정
        self.button_color = (100, 149, 237)
        self.button_hover_color = (130, 179, 255)
        self.text_color = (255, 255, 255)
        self.slider_color = (200, 200, 200)
        self.slider_handle_color = (50, 50, 50)

        # 테마 색상 조정
        self.day_color = {
            'background':(255, 255, 255),
            'text':(25, 25, 112),
            'button':(135, 206, 250),
            'button_hover':(130, 179, 255),
            'slider_bg':(200,200,200),
            'slider_handle':(50,50,50)
        }
        self.night_color = {
            'background': (40, 40, 60),
            'text': (220, 220, 220),
            'button': (70, 70, 90),
            'button_hover': (100, 100, 100),
            'slider_bg': (100, 100, 120),
            'slider_handle': (180, 180, 200)
        }
        self.current_color = self.day_color

        # 공룡 이미지 로드
        self.dino_image = pygame.image.load(os.path.join("Assets/Dino", "DinoRun1.png"))
        self.dino_rect = self.dino_image.get_rect()
        self.dino_rect.center = (self.screen_width // 2, self.screen_height // 2.5)

        # BGM, SFX 볼륨 및 테마 초기화
        self.bgm_volume = 1.0
        self.sfx_volume = 1.0
        self.theme = "day"

        # 로드 및 적용
        self.load_settings()
        self.apply_settings()

        # 랭킹 버튼 설정
        self.ranking_button_x = self.button_x
        self.ranking_button_y = self.settings_button_y + self.button_height + self.button_spacing

    def draw_button(self, text, x, y, width, height, color):
        # 버튼 그리기
        pygame.draw.rect(self.screen, color, (x, y, width, height))
        text_surface = self.button_font.render(text, True, self.text_color)
        text_rect = text_surface.get_rect(center=(x + width // 2, y + height // 2))
        self.screen.blit(text_surface, text_rect)
        # 버튼 경계선 추가
        pygame.draw.rect(self.screen, self.text_color, (x, y, width, height), 2)
        return pygame.Rect(x, y, width, height)

    def draw_slider(self, x, y, width, value, text):
        # 슬라이더 배경
        pygame.draw.rect(self.screen, self.slider_color, (x, y, width, 10))
        # 슬라이더 핸들
        handle_pos = x + (width * value)
        pygame.draw.circle(self.screen, self.slider_handle_color,
                           (int(handle_pos), y + 5), 10)
        # 텍스트
        text_surface = self.settings_font.render(text, True, (0, 0, 0))
        text_rect = text_surface.get_rect(bottomleft=(x, y - 5))
        self.screen.blit(text_surface, text_rect)
        # 값 표시
        value_text = self.settings_font.render(f"{int(value * 100)}%", True, (0, 0, 0))
        value_rect = value_text.get_rect(bottomright=(x + width, y - 5))
        self.screen.blit(value_text, value_rect)

        return pygame.Rect(x - 10, y - 10, width + 20, 20)

    def draw_theme_toggle(self, x, y):
        text = self.settings_font.render("theme:", True, (0, 0, 0))
        self.screen.blit(text, (x, y))

        theme_rect = pygame.Rect(x + 100, y, 100, 30)
        pygame.draw.rect(self.screen, self.button_color, theme_rect)

        theme_text = self.settings_font.render(
            "night" if self.theme == "day" else "day",
            True,
            self.current_color['text']
        )
        theme_text_rect = theme_text.get_rect(center=theme_rect.center)
        self.screen.blit(theme_text, theme_text_rect)

        return theme_rect

    def show_settings(self):
        running = True
        slider_width = 300
        dragging = None  # 현재 드래그 중인 슬라이더 추적

        # 슬라이더 위치
        bgm_slider_x = self.screen_width // 2 - slider_width // 2
        bgm_slider_y = self.screen_height // 3
        sfx_slider_y = bgm_slider_y + 60
        theme_toggle_y = sfx_slider_y + 60

        while running:
            mouse_pos = pygame.mouse.get_pos()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return True

                if event.type == pygame.MOUSEBUTTONDOWN:
                    theme_rect = self.draw_theme_toggle(bgm_slider_x, theme_toggle_y)
                    if theme_rect.collidepoint(mouse_pos):
                        self.theme = "night" if self.theme == "day" else "day"  # 테마 변경
                        self.apply_settings()
                        self.save_settings()

                    bgm_slider_rect = pygame.Rect(bgm_slider_x, bgm_slider_y, slider_width, 20)
                    sfx_slider_rect = pygame.Rect(bgm_slider_x, sfx_slider_y, slider_width, 20)

                    if bgm_slider_rect.collidepoint(mouse_pos):
                        dragging = "bgm"

                    elif sfx_slider_rect.collidepoint(mouse_pos):
                        dragging = "sfx"

                if event.type == pygame.MOUSEBUTTONUP:
                    if dragging:
                        self.save_settings()
                        self.apply_settings()
                    dragging = None

                if dragging and pygame.mouse.get_pressed()[0]:
                    rel_x = mouse_pos[0] - bgm_slider_x
                    new_value = max(0, min(1, rel_x / slider_width))

                    if dragging == "bgm":
                        self.bgm_volume = new_value
                    elif dragging == "sfx":
                        self.sfx_volume = new_value

                    self.apply_settings()

            # 화면 그리기
            if self.theme == "day":
                self.screen.fill((255, 255, 255))
            else:
                self.screen.fill((50, 50, 50))

            # 테마 업데이트
            self.screen.fill(self.current_color['background'])

            # 설정 제목
            title_text = self.title_font.render("settings", True, self.current_color['text'])
            title_rect = title_text.get_rect(center=(self.screen_width // 2, self.screen_height // 6))
            self.screen.blit(title_text, title_rect)

            # 슬라이더 그리기
            self.draw_slider(bgm_slider_x, bgm_slider_y, slider_width, self.bgm_volume, "bgm volume")
            self.draw_slider(bgm_slider_x, sfx_slider_y, slider_width, self.sfx_volume, "sfx volume")

            # 테마 토글 그리기
            self.draw_theme_toggle(bgm_slider_x, theme_toggle_y)

            # ESC 안내 메시지
            esc_text = self.settings_font.render("Press ESC to return to Home", True, (100, 100, 100))
            esc_rect = esc_text.get_rect(center=(self.screen_width // 2, self.screen_height - 50))
            self.screen.blit(esc_text, esc_rect)

            pygame.display.update()

            # 설정 변경시 저장
            # if event.type == pygame.MOUSEBUTTONDOWN:
            # self.save_settings()

        return True

    # show_settings 메서드에서 볼륨 및 테마 변경 시
    def apply_settings(self):
        # sound_manager.set_bgm_volume(self.bgm_volume)
        # sound_manager.set_sfx_volume(self.sfx_volume)

        if self.theme == "day":
            self.current_color = self.day_color
            self.button_color = self.day_color['button']
            self.button_hover_color = self.day_color['button_hover']
            self.text_color = self.day_color['text']
        else:
            self.current_color = self.night_color
            self.button_color = self.night_color['button']
            self.button_hover_color = self.night_color['button_hover']
            self.text_color = self.night_color['text']

        # 설정 후 상태에 맞게 적용
        # if sound_manager.bgm_playing:
        #     sound_manager.stop_bgm()
        #     sound_manager.play_bgm()

    # 설정 저장
    def save_settings(self):
        # 저장할 정보 딕셔너리
        settings = {
            "bgm_volume": self.bgm_volume,
            "sfx_volume": self.sfx_volume,
            "theme": self.theme
        }
        try:
            # game_settings.json 파일에 설정 저장
            with open("game_settings.json", "w") as f:
                json.dump(settings, f)
        except Exception as e:
            print(f"설정 저장 중 오류 발생: {e}")

    def load_settings(self):
        try:
            # game_settings.json 파일 읽기
            with open("game_settings.json", "r") as f:
                settings = json.load(f)
                self.bgm_volume = settings.get("bgm_volume", 1.0)  # 기본 값
                self.sfx_volume = settings.get("sfx_volume", 1.0)  # 기본 값
                self.theme = settings.get("theme", "day")
        except FileNotFoundError:
            # 파일이 없으면 기본 설정 유지
            self.bgm_volume = 1.0
            self.sfx_volume = 1.0
            self.theme = "day"
        except json.JSONDecodeError:
            # json형식이 잘못됐을 경우 기본값 사용
            self.bgm_volume = 1.0
            self.sfx_volume = 1.0
            self.theme = "day"
        except Exception as e:
            print(f"설정 로드 중 오류 발생: {e}")
            self.bgm_volume = 1.0
            self.sfx_volume = 1.0
            self.theme = "day"

    def show_ranking(self, from_game_over = False):
        running = True
        # 상위 5위까지 점수 표시
        sorted_scores = sorted(high_scores.items(), key=lambda x: x[1], reverse=True)[:5]

        # 화면 설정
        running = True
        while running:
            mouse_pos = pygame.mouse.get_pos()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        if from_game_over:
                            return "game_over"  # game over으로 돌아가기
                        return True  # 메인 메뉴로 돌아가기

            # 화면 그리기
            self.screen.fill(self.current_color['background'])

            # 타이틀 그리기
            title_text = self.title_font.render("Top 5 High Scores", True, self.current_color['text'])
            title_rect = title_text.get_rect(center=(self.screen_width // 2, self.screen_height // 6))
            self.screen.blit(title_text, title_rect)

            # 랭킹 리스트 그리기
            y_offset = self.screen_height // 4
            for i, (name, score) in enumerate(sorted_scores):
                if i == 0:
                    rank_color = (255, 215, 0)  # 1st: 금색
                    rank_text = f"1st place: {name} - {score}"
                elif i == 1:
                    rank_color = (192, 192, 192)  # 2nd: 은색
                    rank_text = f"2nd place: {name} - {score}"
                elif i == 2:
                    rank_color = (205, 127, 50)  # 3rd: 동색
                    rank_text = f"3rd place: {name} - {score}"
                else:
                    rank_color = (139, 69, 19)  # 4th, 5th: 어두운 갈색
                    rank_text = f"{i + 1}th place: {name} - {score}"

                # 랭킹 텍스트 그리기
                rank_text_surface = self.settings_font.render(rank_text, True, rank_color)
                rank_rect = rank_text_surface.get_rect(center=(self.screen_width // 2, y_offset + i * 40))
                self.screen.blit(rank_text_surface, rank_rect)

            esc_text = self.settings_font.render("Press ESC to return to game over" if from_game_over else "Press ESC to return to Home",
                True,
                self.current_color['text'])

            esc_rect = esc_text.get_rect(center=(self.screen_width // 2, self.screen_height - 50))
            self.screen.blit(esc_text, esc_rect)

            pygame.display.update()

        return True

    def show_menu(self):
        # 디스플레이가 초기화되지 않았다면 다시 초기화
        if not pygame.display.get_init():
            pygame.display.init()
            self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
            pygame.display.set_caption("Dinosaur Game")

        running = True
        while running:
            mouse_pos = pygame.mouse.get_pos()

            # 버튼의 영역 정의
            button_rect = pygame.Rect(self.button_x, self.button_y,
                                      self.button_width, self.button_height)
            settings_button_rect = pygame.Rect(self.settings_button_x, self.settings_button_y,
                                               self.button_width, self.button_height)
            ranking_button_rect = pygame.Rect(self.ranking_button_x, self.ranking_button_y,
                                              self.button_width, self.button_height)

            # 마우스가 버튼 위에 있는지 확인
            button_color = self.button_hover_color if button_rect.collidepoint(mouse_pos) else self.button_color
            settings_button_color = self.button_hover_color if settings_button_rect.collidepoint(
                mouse_pos) else self.button_color
            ranking_button_color = self.button_hover_color if ranking_button_rect.collidepoint(
                mouse_pos) else self.button_color

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if button_rect.collidepoint(mouse_pos):
                        return True  # 게임 시작 신호만 반환
                    elif settings_button_rect.collidepoint(mouse_pos):
                        self.show_settings()  # 설정 메뉴 표시
                    elif ranking_button_rect.collidepoint(mouse_pos):
                        self.show_ranking()  # 랭킹 메뉴 표시

            # 화면 그리기
            self.screen.fill(self.current_color['background'])

            # 타이틀 그리기
            title_text = self.title_font.render("Dinosaur Game", True, self.current_color['text'])
            title_rect = title_text.get_rect(center=(self.screen_width // 2, self.screen_height // 4))
            self.screen.blit(title_text, title_rect)

            # 공룡 이미지 그리기
            self.screen.blit(self.dino_image, self.dino_rect)

            # 시작 화면 버튼 그리기
            self.draw_button("Game Start", self.button_x, self.button_y,
                             self.button_width, self.button_height, button_color)
            self.draw_button("Settings", self.settings_button_x, self.settings_button_y,
                             self.button_width, self.button_height, settings_button_color)
            self.draw_button("Ranking", self.ranking_button_x, self.ranking_button_y,
                             self.button_width, self.button_height, ranking_button_color)

            pygame.display.update()

        return False


def start_game(menu_instance):
    return menu_instance.show_menu()


if __name__ == "__main__":
    pygame.init()
    start_game()
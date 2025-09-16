import pygame
from menu import Menu, start_game
from basic import main

def run_game():
    pygame.init()
    while True:
        menu_instance = Menu()
        if start_game(menu_instance):  # 게임 시작 버튼이 눌렸다면
            main(menu_instance)  # 메인 게임 함수 호출
        else:
            break  # 게임 종료

if __name__ == "__main__":
    run_game()
from tkinter import *
import time
import math
import random
import sys
import pygame
import time
import os

# 실행 경로 설정
def resource_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller"""
    try:
        # PyInstaller 사용 시
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

window = Tk()
window.title("종강을 향해 쏴라!")  # 게임 이름
window.resizable(0, 0)
canvas = Canvas(window, width=640, height=640, bg="White")  # 창 생성

objects, enemyObjects, score, grade = set(), set(), 0, 'F'  # 오브젝트 세트, 점수 선언

class Game:
    def __init__(self):
        global objects, enemyObjects, score
        self.keys = set()  # 버튼 세트 생성
        self.mx, self.my = 0, 0  # 마우스 좌표 초기화
        self.grade = 'F'  # 학점을 인스턴스 변수로 설정
        self.runtime, self.spontime = 0, 300  # 런타임, 스폰타임
        self.hp_before, self.score_before = 0, 0  # 갱신용 지역변수
        
        self.enemyvalue = [[50, "orange"], [30, "gray"], [15, "brown"], [10, "black"]]  # 적 정보
        window.bind("<KeyPress>", self.keyPressHandler)  # 키보드 입력 처리
        window.bind("<KeyRelease>", self.keyReleaseHandler)  # 키보드 입력 해제 처리
        canvas.bind("<Motion>", self.mouseMove)  # 마우스 이동 추적
        canvas.pack()

        story = [
            "A 학점으로 학기를 마무리할 수 있게 도와줘!"
        ]
        canvas.delete("all")
        x, y = 320, 300
        for line in story:
            for i in range(len(line)):
                text = canvas.create_text(x, y, text=line[:i + 1], fill="Black", font=("둥근모꼴", 18))
                window.update()
                time.sleep(0.05)  # 글자가 천천히 출력되도록 설정
                canvas.delete(text)
            canvas.create_text(x, y, text=line, fill="Black", font=("둥근모꼴", 18))
            y += 70
        window.update()
        time.sleep(1)  # 스토리 끝나고 잠시 대기

        canvas.delete("all")

        item_heart = PhotoImage(file=resource_path("pygame/item_heart.png"))
        item_star = PhotoImage(file=resource_path("pygame/item_star.png"))
        item_dalnim = PhotoImage(file=resource_path("pygame/item_dalnim.png"))

        # 텍스트 배경 사각형 추가
        canvas.create_rectangle(100, 40, 540, 80, fill="lightpink", outline="lightpink")  # 사각형 배경
        canvas.create_text(320, 60, text="😕종강을 향해 쏴라!🔫", fill="Black", font=("둥근모꼴", 28))
        canvas.create_rectangle(100, 200, 135, 235, fill="lightgreen", outline="Black");
        canvas.create_text(117, 217, text="A", fill="Black", font=("둥근모꼴", 16))
        canvas.create_rectangle(143, 200, 178, 235, fill="lightgreen", outline="Black");
        canvas.create_text(160, 217, text="S", fill="Black", font=("둥근모꼴", 16))
        canvas.create_rectangle(186, 200, 221, 235, fill="lightgreen", outline="Black");
        canvas.create_text(203, 217, text="D", fill="Black", font=("둥근모꼴", 16))
        canvas.create_rectangle(143, 157, 178, 192, fill="lightgreen", outline="Black");
        canvas.create_text(160, 174, text="W", fill="Black", font=("둥근모꼴", 16))
        canvas.create_text(160, 270, text="< 플레이어(학생) >", fill="Black", font=("둥근모꼴", 12))
 
        canvas.create_image(430, 200, image=item_heart)
        canvas.create_image(485, 200, image=item_star)
        canvas.create_image(550, 200, image=item_dalnim)
        
        canvas.create_text(480, 270, text="< 아이템 >", fill="Black", font=("둥근모꼴", 12))
        canvas.create_text(300, 400, text="    공격해오는 과제들을 피해 해치우는 게임입니다!\n\n    시간이 지날수록 과제가 더 강해집니다! ", fill="slategray",
                          font=("둥근모꼴", 12))
        canvas.create_text(300, 400, text="\n\n\n\n\n\n\n\n\n\n\n\n   2025-2 OSS class", fill="cornflowerblue",
                          font=("둥근모꼴", 10))

        # 게임 시작 대기 화면
        self.textblinker()

        # 배경 이미지 로드 및 설정
        try:
            self.bg_image = PhotoImage(file=resource_path("pygame/school_background.png"))  # 배경 이미지 파일 경로
            canvas.create_image(320, 320, image=self.bg_image)  # 캔버스 중앙에 배경 이미지 추가
        except Exception as e:
            print("배경 이미지 로드 실패:", e)
        #배경 음악 추가
        try:
            pygame.mixer.init()
            self.bg_music = pygame.mixer.music.load(resource_path("songs\......已至。-12-塞壬唱片-MSR & 秋田真典.mp3"))
            pygame.mixer.music.play(loops=-1, start =0.0)
        #에러 발생시 대처 (try except)        
        except pygame.error as e:
            print("pygame error",e)

        except Exception as e:
            print("can't play music now. please check again",e)
        

        
        # 캐릭터(플레이어) 생성
        obj_main = object_main(316, 316, 8, 8, "purple")  # 플레이어 객체 생성

        # 점수와 HP 표시
        score_view = canvas.create_text(540, 15, text="SCORE: " + str(score), fill="Black", font=("Arial", 16))
        canvas.create_rectangle(5, 5, 420, 25, fill="White")  # HP바 바탕 드로우
        hpbar = canvas.create_rectangle(5, 5, 420, 25, fill="White", width=0)
        hptext = canvas.create_text(200, 15, text="HP: (" + str(obj_main.hp) + " / 1000)", font=("Arial", 8))

        # 게임 메인 루프
        while obj_main in objects:
    # 아이템 생성 로직
            if self.runtime % 1200 == 0:  # 1200 틱마다 하트 아이템 생성
                obj_item_heart = object_item(
                    random.randint(50, 590),
                    random.randint(50, 590),
                    16, 16,
                    "pink",
                    obj_main,
                    item_type="heart"
                )

    # 별 효과 종료 처리
            current_time = time.time()
            if current_time > obj_main.star_effect_end and obj_main.attack_power > 20:
                # 별 효과 종료, 공격력을 기본값으로 복구
                obj_main.attack_power = 20

            if self.runtime % 1000 == 0:  # 1000 틱마다 별 아이템 생성
                obj_item_star = object_item(
                    random.randint(50, 590),
                    random.randint(50, 590),
                    16, 16,
                    "yellow",
                    obj_main,
                    item_type="star"
                )

            if self.runtime % 1500 == 0:  # 1500 틱마다 달님 아이템 생성
                obj_item_dalnim = object_item(
                    random.randint(50, 590),
                    random.randint(50, 590),
                    16, 16,
                    "blue",
                    obj_main,
                    item_type="dalnim"
                )

            if score >= 14000:
                canvas.delete("all")
                self.show_game_over_screen(score)

                self.textblinker("Exit")  # 종료 대기

                time.sleep(2)  # 종료 전 잠시 대기
                window.destroy()


            for key in self.keys:
                if key == ord('A') and obj_main.x_accel > -3: obj_main.x_accel -= 1  # A
                if key == ord('D') and obj_main.x_accel < 3: obj_main.x_accel += 1  # D
                if key == ord('W') and obj_main.y_accel > -3: obj_main.y_accel -= 1  # W
                if key == ord('S') and obj_main.y_accel < 3: obj_main.y_accel += 1  # S

            # 마우스 클릭 없이 자동으로 투사체 발사
            if obj_main.coolt == obj_main.cool:
                obj_attack = object_attack(
                    canvas.coords(obj_main.canvas_id)[0] + 8,
                    canvas.coords(obj_main.canvas_id)[1] + 8,
                    3, 3,  # 크기
                    "purple",  # 색상
                    120,  # 수명
                    obj_main  # 플레이어 객체 전달
                )

                obj_attack.x_accel, obj_attack.y_accel = self.movePoint(
                    canvas.coords(obj_attack.canvas_id)[0] + 10,
                    canvas.coords(obj_attack.canvas_id)[1] + 10,
                    self.mx, self.my, 25)
                obj_main.coolt = 0  # 쿨타임 초기화

            if self.hp_before != obj_main.hp:  # hp 갱신
                   canvas.delete(hpbar);
                   canvas.delete(hptext)
                   hpbar = canvas.create_rectangle(5, 5, 420 * obj_main.hp / obj_main.mhp, 25, fill="pink",
                                                   width=0)
                   hptext = canvas.create_text(200, 15, text="HP: (" + str(obj_main.hp) + " / 1000)",
                                               font=("둥근모꼴", 12))
                   self.hp_before = obj_main.hp
            if self.score_before != score:  # 점수 갱신
                   canvas.itemconfig(score_view, text="SCORE: " + str(score))
                   self.score_before = score
            
            if score >= 10000: self.grade = 'A'
            elif score >= 5000: self.grade = 'B'
            elif score >= 3000: self.grade = 'C'
            else: self.grade = 'F'

                   

            self.runtime += 1  # 런타임 증가

            if len(enemyObjects) < 25:  # 적 개체 수 제한
                if self.runtime % self.spontime == 0:  # 100 루프마다 적 생성
                    for i in range(4):
                        if self.runtime % (self.spontime * (i + 1) ** 2) == 0: obj_enemy = object_enemy(
                            random.choice([-100, 740]) + random.randrange(-50, 50),
                            random.choice([-100, 740]) + random.randrange(-50, 50), self.enemyvalue[i][0],
                            self.enemyvalue[i][0], self.enemyvalue[i][1], obj_main, i)  # enemy 오브젝트 스폰

                    self.spontime = max([random.randrange(self.spontime - 2, self.spontime), 50])  # 스폰시간 초기화

                for obj in enemyObjects.copy():
                    degree = math.atan2(canvas.coords(obj_main.canvas_id)[0] - canvas.coords(obj.canvas_id)[0],
                                        canvas.coords(obj_main.canvas_id)[1] - canvas.coords(obj.canvas_id)[1])
                    obj.x_accel, obj.y_accel = -obj.enemy_stat[obj.enemy_type][1] * math.cos(degree), 5 * math.sin(
                        degree)  # main 오브젝트 공전
                    if obj.coolt == obj.cool:
                        obj_enemyAttack = object_enemyAttack(
                            canvas.coords(obj.canvas_id)[0] + (obj.size_x - obj.enemy_stat[obj.enemy_type][3]) / 2,
                            canvas.coords(obj.canvas_id)[1] + (obj.size_y - obj.enemy_stat[obj.enemy_type][3]) / 2,
                            obj.enemy_stat[obj.enemy_type][3], obj.enemy_stat[obj.enemy_type][3], obj.color, 100,
                            obj_main, obj.enemy_stat[obj.enemy_type][5])  # obj_enemyAttack 생성
                        obj_enemyAttack.x_accel, obj_enemyAttack.y_accel = self.movePoint(
                            canvas.coords(obj_enemyAttack.canvas_id)[0] + random.randrange(-5, 5),
                            canvas.coords(obj_enemyAttack.canvas_id)[1] + random.randrange(-5, 5),
                            canvas.coords(obj_main.canvas_id)[0] + 10, canvas.coords(obj_main.canvas_id)[1] + 10,
                            obj.enemy_stat[obj.enemy_type][4])
                        obj.coolt = 0

            for obj in list(objects):  # objects의 복사본 사용
                if not hasattr(obj, 'canvas_id') or obj.canvas_id is None:
                    continue  # 이미 삭제된 객체는 건너뜀
                obj.move()
                obj.step()
                
            if not obj_main in objects:
                canvas.delete("all");
                break
            window.update(); # ui 변경사항 즉시 저장
            time.sleep(0.01)  # 0.01초 만큼 sleep
            
        self.show_game_over_screen(score)

    def show_game_over_screen(self, score):
        # 종료 화면 배경 이미지 삽입
        try:
            self.bg_image = PhotoImage(file=resource_path("memo_image.png"))  # 이미지 로드
            canvas.create_image(320, 320, image=self.bg_image)  # 배경 이미지를 중앙에 배치
        except Exception as e:
            print("이미지 로드 실패:", e)

        # 종료 화면과 점수 등급 표시
        canvas.create_text(320, 260, text="Game Over...\n", fill="Black", font=("둥근모꼴", 38))
        canvas.create_text(320, 320, text=str(score) + " 점", fill="Black", font=("둥근모꼴", 28))

        # 점수에 따른 등급과 메시지 출력
        if self.grade == 'A':
            canvas.create_text(320, 430, text="최종학점 A\n", fill="Crimson", font=("둥근모꼴", 30))
            canvas.create_text(320, 450, text="무사히 종강하셨습니다! 당신은 이제 대학원으로!", fill="Crimson", font=("둥근모꼴", 20))
            pygame.mixer.init()
            pygame.mixer.music.load(resource_path('MP_Ta Da.mp3'))
            pygame.mixer.music.play(loops=1, start=0.0)
        elif self.grade == 'B':
            canvas.create_text(320, 430, text="최종학점 B\n", fill="Crimson", font=("둥근모꼴", 30))
            canvas.create_text(320, 450, text="무사히 종강하셨습니다! 노력은 하셨네요...", fill="Crimson", font=("둥근모꼴", 20))
            pygame.mixer.init()
            pygame.mixer.music.load(resource_path('pygame/MP_와우 (단체).mp3'))
            pygame.mixer.music.play(loops=1, start=0.0)
        elif self.grade == 'C':
            canvas.create_text(320, 420, text="최종학점 C\n", fill="Crimson", font=("둥근모꼴", 30))
            canvas.create_text(320, 450, text="무사히 종강하셨습니다! 종강만 하셨네요!", fill="Crimson", font=("둥근모꼴", 20))
            pygame.mixer.init()
            pygame.mixer.music.load(resource_path('pygame/MP_Dun Dun Dun.mp3'))
            pygame.mixer.music.play(loops=1, start=0.0)
        else:
            canvas.create_text(320, 430, text="최종학점 F\n", fill="Crimson", font=("둥근모꼴", 30))
            canvas.create_text(320, 450, text="재수강 힘내세요..", fill="Crimson", font=("둥근모꼴", 20))
            pygame.mixer.init()
            pygame.mixer.music.load(resource_path('pygame/MP_Sad Trombone.mp3'))
            pygame.mixer.music.play(loops=1, start=0.0)

        self.textblinker("Exit")  # 종료 대기
        sys.exit(1)

    def keyPressHandler(self, event):  # 버튼 세트에 버튼추가
       self.keys.add(event.keycode)

    def keyReleaseHandler(self, event):  # 버튼 세트에 버튼 제거
       if event.keycode in self.keys: self.keys.discard(event.keycode)


    def mouseMove(self, event):
        self.mx, self.my = event.x, event.y  # 마우스 이동 시 좌표 갱신

    def movePoint(self, x1, y1, x2, y2, spd):  # 해당 좌표로 이동
       return (x2 - x1) * spd / math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2), (y2 - y1) * spd / math.sqrt(
           (x2 - x1) ** 2 + (y2 - y1) ** 2)

    def textblinker(self, sentance="start"):  # 대기 텍스트
        menuToggle = True;
        blinkerText = canvas.create_text(320, 580, text="< Please press spacebar to " + sentance + ". >", fill="red",
                                        font=("둥근모꼴", 12))  # 깜박이 canvas 생성
        while (True):  # 대기
            self.runtime += 1
            for key in self.keys:  # spacebar 누를시 다음으로
                if key == 32:
                    canvas.delete("all");
                    return
            if self.runtime % 60 == 0:
                if menuToggle == True:
                    canvas.itemconfig(blinkerText, text="");
                    menuToggle = False
                else:
                    canvas.itemconfig(blinkerText, text="< Please press spacebar to " + sentance + ". >");
                    menuToggle = True
            window.update();
            time.sleep(0.01)

# 오브젝트 클래스 정의 및 이하 클래스는 기존 그대로 유지
class element:
    def collision(self, obj):
    # 현재 객체가 유효하지 않으면 False 반환
        if not hasattr(self, 'canvas_id') or self.canvas_id is None:
            return False
    # 대상 객체가 유효하지 않으면 False 반환
        if not hasattr(obj, 'canvas_id') or obj.canvas_id is None:
            return False

    # 객체 좌표를 가져와 충돌 여부 확인
        self_coords = canvas.coords(self.canvas_id)
        obj_coords = canvas.coords(obj.canvas_id)

    # 좌표가 유효하지 않으면 False 반환
        if len(self_coords) < 4 or len(obj_coords) < 4:
            return False

    # 충돌 여부 검사
        return (
            self_coords[0] < obj_coords[2] and
            self_coords[2] > obj_coords[0] and
            self_coords[1] < obj_coords[3] and
            self_coords[3] > obj_coords[1]
        )



    def __init__(self, x, y, size_x, size_y, color):
        self.x, self.y = x, y  # 생성 위치
        self.size_x, self.size_y = size_x, size_y  # 크기
        self.color = color  # 색
        self.x_accel, self.y_accel = 0, 0  # 가속도
        objects.add(self)  # 오브젝트 세트에 자신 등록
        self.canvas_id = canvas.create_oval(x, y, x + self.size_x, y + self.size_y, fill=self.color,
                                                width=0)  # 캠버스 추가

    def destroy(self):
        if hasattr(self, 'canvas_id') and self.canvas_id is not None:
            objects.discard(self)  # objects에서 제거
            canvas.delete(self.canvas_id)  # Canvas에서 삭제
            self.canvas_id = None  # 삭제된 상태로 표시
        del self  # 객체 제거


    def move(self):
        if hasattr(self, 'canvas_id') and self.canvas_id is not None:
            x_value, y_value = self.x_accel, self.y_accel
            if x_value != 0 or y_value != 0:
                coords = canvas.coords(self.canvas_id)
                if coords:
                    if coords[0] + x_value < 0: x_value, self.x_accel = -coords[0], -self.x_accel
                    if coords[1] + y_value < 30: y_value, self.y_accel = 30 - coords[1], -self.y_accel
                    if coords[2] + x_value > 640: x_value, self.x_accel = 640 - coords[2], -self.x_accel
                    if coords[3] + y_value > 640: y_value, self.y_accel = 640 - coords[3], -self.y_accel
                    canvas.move(self.canvas_id, x_value, y_value)
                    self.x_accel, self.y_accel = self.x_accel * 0.98, self.y_accel * 0.98

    def step(self):
        pass  # 빈 함수로 정의 (다른 객체에서 상속하여 사용)

class object_main(element):  # main 오브젝트
    def __init__(self, x, y, size_x, size_y, color):
        super().__init__(x, y, 25, 25, color)  # 상속
        self.mhp, self.hp = 1000, 1000  # 체력
        self.cool, self.coolt = 10, 0  # 쿨타임
        self.attack_power = 20  # 기본 공격력
        self.star_effect_end = 0  # 별 효과 종료 시간 (초 단위)



    def step(self):  # 스텝 함수
        if self.coolt < self.cool:
            self.coolt += 1  # 쿨타임 감소
        if self.hp <= 0:
            self.destroy()  # HP <= 0 일시 제거


class object_enemy(element):  # enemy 오브젝트
    def __init__(self, x, y, size_x, size_y, color, obj_main, enemy_type):
        super().__init__(x, y, size_x, size_y, color)  # 상속
        self.enemy_stat = [[100, 2, 30, 3, 10, 40], [500, 1, 75, 5, 11, 60], [150, 3, 10, 3, 15, 80],
                           [2500, 1, 30, 6, 12, 100]]  # HP, 속도, 공격속도, 투사체 크기, 투사체 속도, 데미지
        self.enemy_type = enemy_type
        self.mhp = self.enemy_stat[self.enemy_type][0]
        self.hp = self.mhp  # 체력
        self.cool, self.coolt = self.enemy_stat[self.enemy_type][2], 0  # 쿨타임
        enemyObjects.add(self)  # enemy 오브젝트 세트에 자신 등록
        self.obj_main = obj_main  # obj_main 오브젝트 받기
        self.label = "과제" if random.random() < 0.5 else "수업"
        self.label_id = canvas.create_text(self.x + size_x // 2, self.y + size_y // 2, text=self.label, fill="blue", font=("Arial", 12))
        self.hp_text = canvas.create_text(self.x + size_x // 2, self.y - 10, text=str(self.hp), fill="red", font=("Arial", 10))

    def step(self):  # 스텝 함수
        if not hasattr(self, 'canvas_id') or self.canvas_id is None:
            return  # 이미 삭제된 객체는 처리하지 않음

        if self.coolt < self.cool: 
            self.coolt += 1  # 쿨타임 감소
        if self.hp <= 0:  # HP <= 0일시 제거
            global score
            self.destroy()
            enemyObjects.discard(self)
            score += self.mhp
        else:
            if hasattr(self, 'hp_text') and self.hp_text is not None:
                canvas.coords(self.hp_text, canvas.coords(self.canvas_id)[0] + self.size_x // 2, canvas.coords(self.canvas_id)[1] - 10)
                canvas.itemconfig(self.hp_text, text=str(self.hp))
            if hasattr(self, 'label_id') and self.label_id is not None:
                canvas.coords(self.label_id, canvas.coords(self.canvas_id)[0] + self.size_x // 2, canvas.coords(self.canvas_id)[1] + self.size_y // 2)


    def destroy(self):
        if hasattr(self, 'canvas_id') and self.canvas_id is not None:
            canvas.delete(self.canvas_id)  # Canvas에서 적 객체 삭제
            self.canvas_id = None
        if hasattr(self, 'hp_text') and self.hp_text is not None:
            canvas.delete(self.hp_text)  # HP 표시 삭제
            self.hp_text = None
        if hasattr(self, 'label_id') and self.label_id is not None:
            canvas.delete(self.label_id)  # 라벨 삭제
            self.label_id = None
        enemyObjects.discard(self)  # 적 객체 집합에서 제거
        objects.discard(self)  # 모든 오브젝트 집합에서도 제거


class object_attack(element):  # attack 오브젝트
    def __init__(self, x, y, size_x, size_y, color, livetime, obj_main):
        super().__init__(x, y, 6, 6, color)  
        self.livetime, self.fortime = livetime/1.5, 0  # 동작 시간
        self.obj_main = obj_main  # 플레이어 객체


    def step(self):  # 스텝 함수
        for obj_s in enemyObjects:
            if self.collision(obj_s):  # 충돌 시
                obj_s.hp -= self.obj_main.attack_power  # 공격력 반영
                self.destroy()
                break
        if self.livetime <= self.fortime:  # 지속시간 초과 시 파괴
            self.destroy()
        self.fortime += 1
        

class object_enemyAttack(element):  # enemyAttack 오브젝트
    def __init__(self, x, y, size_x, size_y, color, livetime, obj_main, damage):
        super().__init__(x, y, 8, 8, color)  # 적 총알 크기를 8x8으로 설정
        self.livetime, self.fortime = livetime, 0  # 동작 시간
        self.obj_main = obj_main  # obj_main 받기
        self.damage = damage  # 데미지

    def step(self):  # 스텝 함수
        if self.obj_main in objects and self.collision(self.obj_main):
            self.obj_main.hp -= self.damage
            self.destroy()
        if not hasattr(self, 'canvas_id') or self.canvas_id is None:
            return  # 이미 삭제된 객체는 처리하지 않음

        if self.livetime <= self.fortime:  # 지속시간 초과 시 파괴
            self.destroy()
        self.fortime += 1

    def move(self):
        x_value, y_value = self.x_accel * 0.5, self.y_accel * 0.5
        coords = canvas.coords(self.canvas_id)
        canvas.move(self.canvas_id, x_value, y_value)

class object_item(element):
    def __init__(self, x, y, size_x, size_y, color, obj_main, item_type="heart"):
        super().__init__(x, y, size_x, size_y, color)
        self.obj_main = obj_main
        self.img = None  # 이미지 객체 초기화
        self.image_id = None  # 이미지 캔버스 ID
        self.item_type = item_type  # 아이템 종류 

        try:
            # 아이템 이미지 로드
            if self.item_type == "heart":
                self.img = PhotoImage(file=resource_path("pygame/item_heart.png"))
            elif self.item_type == "star":
                self.img = PhotoImage(file=resource_path("pygame/item_star.png"))
            elif self.item_type == "dalnim":
                self.img = PhotoImage(file=resource_path("pygame/item_dalnim.png"))

            # 이미지를 중앙에 표시
            self.image_id = canvas.create_image(x + size_x // 2, y + size_y // 2, image=self.img)
        except Exception as e:
            print(f"{self.item_type.capitalize()} 이미지 로드 실패:", e)
            # 이미지 로드 실패 시 기본 사각형 생성
            self.image_id = canvas.create_rectangle(
                x, y, x + size_x, y + size_y, fill=color, outline=""
            )

    def step(self):
        global score
        # 플레이어와 충돌 시 효과 적용
        if self.collision(self.obj_main):
            if self.item_type == "heart":
                # 체력 20% 회복
                self.obj_main.hp = min(self.obj_main.hp + int(self.obj_main.mhp * 0.2), self.obj_main.mhp)
            elif self.item_type == "star":
                # 별 효과 중첩 및 시간 연장
                current_time = time.time()
                if current_time < self.obj_main.star_effect_end:
                    # 이미 효과가 활성화된 경우 남은 시간에 5초 추가
                    self.obj_main.star_effect_end += 5
                else:
                    # 새로운 효과 시작 (현재 시간 + 5초)
                    self.obj_main.star_effect_end = current_time + 5
                    # 공격력 30% 증가
                    self.obj_main.attack_power = int(self.obj_main.attack_power * 1.3)
            elif self.item_type == "dalnim":
                item_sound = pygame.mixer.Sound(resource_path('pygame/item_sound.wav'))
                item_sound.play()
                # 화면에 있는 모든 적 제거
                for enemy in list(enemyObjects):
                    if hasattr(enemy, 'mhp'):
                        score += enemy.mhp  # 적의 최대 HP를 점수에 추가
                    enemy.destroy()
                enemyObjects.clear()  # 적 집합 초기화
            self.destroy()  # 아이템 제거


    def destroy(self):
        # 이미지와 사각형 모두 제거
        if hasattr(self, 'image_id') and self.image_id:
            canvas.delete(self.image_id)
        super().destroy()


    def destroy(self):
        # 이미지와 사각형 모두 제거
        if hasattr(self, 'image_id') and self.image_id:
            canvas.delete(self.image_id)
        super().destroy()

Game()

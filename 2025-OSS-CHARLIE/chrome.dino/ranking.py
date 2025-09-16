class Ranking:
    def __init__(self, filename='highscore.py'):
        self.filename = filename  # 하이스코어를 저장할 Python 파일
        self.high_scores = {}  # 하이스코어 데이터를 저장하는 딕셔너리

    # 하이스코어 데이터를 highscore.py 파일에 저장
    def save_high_scores_to_file(self):
        try:
            with open(self.filename, 'w') as file:
                # highscore.py 파일에 Python 코드 형식으로 저장
                file.write("# This file contains the high scores\n")
                file.write("high_scores = {\n")
                for user_id, score in self.high_scores.items():
                    file.write(f"    '{user_id}': {score},\n")
                file.write("}\n")
        except Exception as e:
            print(f"Error saving high scores: {e}")

    # highscore.py 파일에서 하이스코어 데이터 불러오기
    def load_high_scores_from_file(self):
        try:
            # highscore.py 파일을 실행해서 high_scores 변수 가져오기
            with open(self.filename, 'r') as file:
                exec(file.read(), globals())
                self.high_scores = globals().get('high_scores', {})
        except FileNotFoundError:
            print(f"File {self.filename} not found. Initializing empty high scores.")
            self.high_scores = {}  # 파일 없으면 초기화
        except Exception as e:
            print(f"Error loading high scores: {e}")

    # 최고 기록 업데이트 함수
    def update_high_score(self, user_id, score):
        if user_id not in self.high_scores or score > self.high_scores[user_id]:
            self.high_scores[user_id] = score
            print(f"High score updated for {user_id}: {score}")
        else:
            print(f"No update needed for {user_id}, current score: {self.high_scores[user_id]}")

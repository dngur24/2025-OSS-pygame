# pygame-alpha-mine-sweeper

<br/>

<div align="center">
  <img src="https://github.com/user-attachments/assets/767385d1-f697-425b-b602-7b11c56fb7cd" alt="image">
</div>

<div align="center">
  
# 🎯 SKHU-OSS-2024 윷놀이 게임 제작

</div>

**2024년 성공회대학교 [오픈소스SW개발] 강의** 내 이루어진 게임 제작 프로젝트입니다. 저희 `alpha` 팀은 모두가 쉽게 즐길 수 있는 `윷놀이` 게임을 주제로 정하였습니다. `윷`과 `윷판`이 없어도 언제 어디서든 친구 혹은 가족과 즐기실 수 있도록 제작하였습니다.

<br/>
<br/>

### 0. 목차

- [1. 개요](#1-개요)
- [2. 설치 방법](#2-설치-방법)
- [3. 게임 설명](#3-게임-설명)
- [4. 게임 플레이 방식](#4-게임-플레이-방식)

<br/>
<br/>

### 1. 개요

- 프로젝트명 : pygame-alpha-mine-sweeper
- 프로젝트 기간 : 2024.09.26 - ing
- 개발 엔진 및 언어 : Python-pygame
- 팀원
  - 20학번 김정협(PM)
  - 22학번 이소연
  - 23학번 윤미래
  - 23학번 박혜미

<br/>
<br/>

### 2. 설치 방법

#### install python

- `python 3`을 사용하였습니다.
- download link : https://www.python.org/downloads/

<br/>

#### install pygame

- `pygame 2.6.0`을 사용하였습니다.

```bash
pip install pygame
```

<br/>

#### 실행

1. `src` 폴더에 위치하는 `main.py` 코드를 실행
2. `윷놀이_v1.0_beta.zip`의 압축을 풀고 `YootNoRi.exe` 파일 실행

<br/>
<br/>

### 3. 게임 설명

| 시작 화면 | 게임 화면 |
| :-------: | :-------: |
| ![image](https://github.com/user-attachments/assets/fdb59c85-a189-46cb-9dbb-f42475381fb2) | ![image](https://github.com/user-attachments/assets/300dd680-82b2-4550-bb0a-0232987b25a9) |
| 플레이어의 인원을 2~4명까지 선택할 수 있습니다. | 빨강 팀이 [윷 던지기] 버튼을 눌러 게임을 시작합니다. |

<br/>
<br/>

### 4. 게임 플레이 방식

#### 🕹️ 조작 방법

- 마우스를 사용해 버튼을 눌러 조작합니다.

<br/>

#### 🏆 게임 플레이

|                          게임 설정                           |                           게임 룰                            |
| :----------------------------------------------------------: | :----------------------------------------------------------: |
| - PvP 형식입니다.<br />- Player는 2~4명입니다. <br />- 윷놀이의 말은 4개입니다.<br />- 말의 첫 시작 위치는 우측 하단입니다.<br />- 도착 지점을 초과해야 골인됩니다.<br />- 먼저 말이 4개 도착한 Player가 승리합니다. | - Player 1이 윷을 던집니다.<br />- Player 1이 나온 윷 만큼 이동합니다.<br />- Player 2가 윷을 던집니다.<br />- Player 2가 나온 윷 만큼 이동합니다.<br />- 윷 또는 모가 나올 경우 윷을 한 번 더 던집니다.<br />- 적군의 말을 잡을 경우 윷을 한 번 더 던집니다.<br />- 아군의 말과 마주친 경우 업힙니다.<br />- 윷판의 각 모서리, 혹은 정중앙에 도착할 경우 꺾어 움직일 수 있습니다.<br />- 윷판에 아군의 말이 존재할 경우 새로운 말을 꺼낼 건지, 본래 있던 말을 움직일 건지 선택할 수 있습니다. |

<br/>
<br/>

#### 🖲️ 진행 순서

<div align="center">
  <img width="400" src="https://github.com/user-attachments/assets/25c777b7-ee55-4af9-a487-6f8508401c1b" alt="image">
</div>

1. [윷 던지기] 버튼을 클릭하여 윷을 던집니다.
   - [윷] 또는 [모]가 나올 경우, 말을 이동시키기 전 윷을 한 번 더 던집니다.

<br/>

<div align="center">
  <img width="400" src="https://github.com/user-attachments/assets/075769ad-e5c4-4128-b3a1-03d8b4abcd8d" alt="image">
</div>

2-1. 새로운 말을 출전시킬 거라면 [새 말] 버튼을 클릭하고 이동시킬 결과(빽도~모) 버튼을 클릭합니다.(해당 버튼은 숫자로 표기되어 있습니다. 사진을 참고하세요.

<br/>

<div align="center">
  <img width="400" src="https://github.com/user-attachments/assets/66431050-d64c-4ac6-84de-c9e1de3f4f52" alt="image">
</div>

2-2. 이미 출전되어 있는 말을 움직일 거라면 [말 선택] 우측에 위치해 있는 이동시킬 말 번호를 클릭하고 이동시킬 결과(빽도~모) 버튼을 클릭합니다.(해당 버튼은 숫자로 표기되어 있습니다. 사진을 참고하세요.)

<br/>

<div align="center">
  <img width="400" src="https://github.com/user-attachments/assets/b24ee97e-385e-4fc2-965f-76d5b5b5d98a" alt="image">
</div>

3. 이동시킬 결과 버튼을 클릭하면 말이 갈 수 있는 위치에 주황색으로 표기됩니다. 이동하고 싶은 주황색 위치를 클릭하면 말이 움직입니다.
  - 이 때에도 움직일 말을 변경하고 싶은 경우 2번을 참고하여 변경할 수 있습니다.

<br/>

<div align="center">
  <img width="400" src="https://github.com/user-attachments/assets/d36a2afd-e9d3-41b1-81eb-7e15d491bcdd" alt="image">
</div>

4. [출발] 지점 대각선의 위치하는 주황색 버튼을 클릭하면 골인할 수 있습니다.

<br/>

<div align="center">
  <img width="400" src="https://github.com/user-attachments/assets/2b04a497-46a2-4928-9b4d-6d82fecd1c39" alt="image">
</div>

5. 골인할 경우 우측에 존재하는 스코어가 올라갑니다.

<br/>

6. 1~5번을 반복하여 먼저 4개의 말을 골인시킨 플레이어가 승리합니다.

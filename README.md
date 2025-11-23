# 🎮 도티 피하기 (Doti Dodge)

📖 **프로젝트 소개 (Introduction)**
이 프로젝트는 키보드만으로 즐길 수 있는 캐주얼 아케이드 게임으로, 떨어지는 “도티(도 / 티)”를 피하면서 가능한 한 오래 버티는 **반응 속도 & 집중력 테스트 게임**입니다.

플레이어는 단순한 좌우 이동만으로 끊임없이 떨어지는 장애물을 회피하며,
시간이 지날수록 점점 빨라지는 속도와 늘어나는 개수 속에서 **최고 점수(High Score)**에 도전하게 됩니다.
게임 오버 시에는 실제 API를 통해 가져온 **랜덤 영어 명언(Advice)**을 보여주어, 가볍게 웃고 다시 도전할 수 있도록 돕습니다.

---

## ✨ 주요 기능 (Key Features)

### 1. 점점 빨라지는 난이도 (Dynamic Difficulty Scaling)

게임이 진행될수록 시간이 경과함에 따라:

* 플레이어 이동 속도 증가
* 장애물 낙하 속도 증가
* 장애물 생성 주기 단축

```text
elapsed_time = (현재 시간 - 시작 시간)

player_speed      = 기본 속도 + elapsed_time / 10
obstacle_speed    = 기본 낙하 속도 + elapsed_time / 8
obstacle_add_rate = max(최소 값, 초기 생성 주기 - 경과 시간 비례 감소)
```

단순한 회피 게임이지만, 시간이 지날수록 손에 땀을 쥐는 **난이도 커브**를 느낄 수 있습니다.

---

### 2. 텍스트 기반 캐릭터 & 도티 장애물 (Minimalistic Style)

* 플레이어: `"나"` 라는 텍스트를 파란색으로 렌더링하여 캐릭터로 사용
* 장애물: `"도"` / `"티"` 두 줄로 이루어진 텍스트 블록
* 별도의 이미지 리소스 없이 **폰트만으로 구현된 미니멀 UI/UX**

이미지 없이도 직관적인 **레트로 감성 텍스트 게임** 분위기를 살렸습니다.

---

### 3. 랜덤 명언 시스템 (Advice Slip API Integration)

게임 오버 시 다음과 같은 과정을 거칩니다.

* [Advice Slip API](https://api.adviceslip.com/advice)에 HTTP 요청
* 성공 시: 랜덤 영어 명언 출력
* 실패 시(오프라인, 응답 오류 등):

  * `"오늘의 교훈: 인터넷 연결을 확인하세요."`
  * 혹은 `"오늘의 교훈: 휴식도 중요합니다."`
    와 같은 기본 메시지로 대체

```python
response = requests.get("https://api.adviceslip.com/advice")
data = response.json()
lesson = data["slip"]["advice"]
```

게임을 망쳐(?)도 마지막에 하나쯤은 건져갈 수 있는, **작은 인생 조언 한 줄**.

---

### 4. High Score 영구 저장 (Persistent High Score)

* `highscore.txt` 파일에 최고 점수를 저장
* 게임 종료 후 다시 실행해도 최고 점수가 유지됩니다.
* 파일이 없거나 깨져있으면 자동으로 0점부터 시작

```text
High Score: 1234
```

끊임없이 자신의 기록을 갱신하는 **기록형 게임 플레이**를 즐길 수 있습니다.

---

### 5. “호잇짜!!” & 최고기록 이펙트 (In-game Feedback)

#### ✔ 100점 단위 마일스톤 이펙트

* 100점, 200점, 300점... 마다
* 화면 중앙에 `"XXX점 호잇짜!!"` 텍스트가 **커졌다 작아지는 애니메이션**으로 표시

#### ✔ 최고기록 갱신 중 이펙트

* 현재 점수가 저장된 High Score를 넘어서면
* 화면 중앙에 `"와... 너 지금" / "최고기록 갱신중이야"` 문구가
  **빨강/파랑 번갈아 깜빡이며 표시**

게임 실력 향상에 따른 **즉각적인 시각 피드백**으로 몰입감을 높였습니다.

---

## 🛠 기술 스택 (Tech Stack)

* **Language**: Python 3.10+
* **Game Framework**: `pygame`
* **HTTP / API**: `requests` (Advice Slip API 호출)
* **Standard Library**: `sys`, `os`, `random`, `json`, `traceback`

---

## 🚀 설치 및 실행 (Installation & Usage)

### 1. 저장소 클론

```bash
git clone [Repository URL]
cd [Repository Name]
```

### 2. 의존성 설치

```bash
pip install pygame requests
```

### 3. 실행

```bash
python main.py
```

* `highscore.txt` 파일은 게임 실행 중 자동 생성됩니다.
* Windows 환경에서는 `C:/Windows/Fonts/malgun.ttf` 폰트를 사용해 한글을 렌더링합니다.

  * 해당 폰트가 없거나 다른 OS를 사용할 경우, 자동으로 기본 폰트를 사용합니다.
  * 필요 시 코드 상단의 `KOREAN_FONT_PATH`를 수정하여 원하는 폰트를 지정할 수 있습니다.

---

## 🎮 게임 방법 (How to Play)

1. **게임 시작**

   * 프로그램 실행 후
   * START 화면에서 `START` 버튼을 마우스로 클릭하면 게임이 시작됩니다.

2. **조작법**

   * `←` : 왼쪽으로 이동
   * `→` : 오른쪽으로 이동
   * 캐릭터 `"나"`가 화면 밖으로 나가지 않도록 자동으로 경계 체크가 됩니다.

3. **플레이 목표**

   * 위에서 떨어지는 `"도 / 티"` 장애물을 피하면서
   * **가능한 오래 살아남아 높은 점수(Score)**를 얻는 것이 목표입니다.
   * 점수는 **경과 시간에 비례**하여 증가합니다. (`Score = floor(경과 시간 × 10)`)

4. **게임 오버**

   * `"나"`와 도티 장애물이 충돌하면 게임 오버
   * 게임 오버 화면에서:

     * 이번 점수(`Your Score`)
     * 최고 점수(`High Score`)
     * 오늘의 영어 명언(Advice)
   * 하단의 `RESTART` 버튼을 클릭하면 다시 시작할 수 있습니다.

---

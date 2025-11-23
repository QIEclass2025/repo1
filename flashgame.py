import sys
import os
import traceback
import pygame
import random
import requests
import json
import platform

# --- 초기화 ---
pygame.init()

# --- 화면 설정 ---
SCREEN_WIDTH = 405
SCREEN_HEIGHT = 720
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("도티 피하기")

# --- 색상 ---
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LIGHT_GRAY = (211, 211, 211)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# --- 폰트 설정 (한글 지원) ---
KOREAN_FONT_PATH = None
try:
    if platform.system() == "Windows":
        font_path = "C:/Windows/Fonts/malgun.ttf"
    elif platform.system() == "Darwin":
        font_path = "/System/Library/Fonts/AppleSDGothicNeo.ttc"
    else:
        font_path = None # 다른 OS를 위한 기본값

    if not (font_path and os.path.exists(font_path)):
        font_path = None # 경로에 파일이 없으면 None으로 설정

    KOREAN_FONT_PATH = font_path
    
    # 폰트 로딩. 경로가 None이면 pygame이 기본 폰트를 사용합니다.
    start_font = pygame.font.Font(KOREAN_FONT_PATH, 60)
    score_font = pygame.font.Font(KOREAN_FONT_PATH, 36)
    high_score_font = pygame.font.Font(KOREAN_FONT_PATH, 40)
    lesson_font = pygame.font.Font(KOREAN_FONT_PATH, 20)
    player_font = pygame.font.Font(KOREAN_FONT_PATH, 60)
    obstacle_font = pygame.font.Font(KOREAN_FONT_PATH, 30)
    hoitzza_font = pygame.font.Font(KOREAN_FONT_PATH, 80)

except (FileNotFoundError, pygame.error):
    # 한글 폰트 로딩 실패 시 영문 기본 폰트로 대체
    KOREAN_FONT_PATH = None # 에러 발생 시 경로를 None으로 확실히 설정
    start_font = pygame.font.Font(None, 74)
    score_font = pygame.font.Font(None, 36)
    high_score_font = pygame.font.Font(None, 40)
    lesson_font = pygame.font.Font(None, 24)
    player_font = pygame.font.Font(None, 70)
    obstacle_font = pygame.font.Font(None, 35)
    hoitzza_font = pygame.font.Font(None, 90)

# --- 게임 설정 ---
clock = pygame.time.Clock()
FPS = 60
HIGHSCORE_FILE = "dotti_avoidance_highscore.txt"

# --- API 및 텍스트 래핑 함수 ---
def get_random_advice():
    """
    Advice Slip API를 호출하여 무작위 조언을 가져옵니다.
    """
    try:
        response = requests.get("https://api.adviceslip.com/advice")
        if response.status_code == 200:
            data = response.json()
            return data['slip']['advice']
        else:
            return "오늘의 교훈: 인터넷 연결을 확인하세요."
    except (requests.exceptions.RequestException, json.JSONDecodeError, KeyError):
        return "오늘의 교훈: 휴식도 중요합니다."

def draw_text(surface, text, pos, font, color, max_width):
    """
    주어진 최대 너비에 맞게 텍스트를 래핑하여 그립니다.
    """
    words = text.split(' ')
    lines = []
    current_line = ''
    for word in words:
        test_line = current_line + word + ' '
        if font.size(test_line)[0] < max_width:
            current_line = test_line
        else:
            lines.append(current_line)
            current_line = word + ' '
    lines.append(current_line)

    y_offset = 0
    for line in lines:
        line_surface = font.render(line, True, color)
        surface.blit(line_surface, (pos[0], pos[1] + y_offset))
        y_offset += font.get_linesize()

def create_multiline_surface(text, font, color, max_width):
    """
    주어진 최대 너비에 맞게 래핑된 텍스트를 포함하는 새 Surface를 만듭니다.
    """
    words = text.split(' ')
    lines = []
    current_line = ''
    for word in words:
        test_line = current_line + word + ' '
        if font.size(test_line)[0] < max_width:
            current_line = test_line
        else:
            lines.append(current_line)
            current_line = word + ' '
    lines.append(current_line)

    line_height = font.get_linesize()
    surface_height = len(lines) * line_height
    
    surface_width = 0
    for line in lines:
        line_width = font.size(line)[0]
        if line_width > surface_width:
            surface_width = line_width
            
    text_surface = pygame.Surface((surface_width, surface_height), pygame.SRCALPHA)
    text_surface.fill((0,0,0,0)) # Transparent background

    y_offset = 0
    for line in lines:
        line_surface = font.render(line, True, color)
        text_surface.blit(line_surface, ((surface_width - line_surface.get_width()) / 2, y_offset)) # Centered
        y_offset += line_height
        
    return text_surface

# --- 게임 함수 ---
def load_high_score():
    if os.path.exists(HIGHSCORE_FILE):
        with open(HIGHSCORE_FILE, 'r') as f:
            try: return int(f.read())
            except ValueError: return 0
    return 0

def save_high_score(score):
    with open(HIGHSCORE_FILE, 'w') as f: f.write(str(score))

def start_screen(high_score):
    start_button = pygame.Rect(SCREEN_WIDTH / 2 - 100, SCREEN_HEIGHT / 2 + 50, 200, 80)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.collidepoint(event.pos):
                    return
        
        screen.fill(WHITE)
        title_text = start_font.render("도티 피하기", True, BLACK)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 150))
        screen.blit(title_text, title_rect)
        
        high_score_text = high_score_font.render(f"High Score: {high_score}", True, BLACK)
        high_score_rect = high_score_text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 50))
        screen.blit(high_score_text, high_score_rect)
        
        pygame.draw.rect(screen, (200, 200, 200), start_button)
        
        start_text = score_font.render("START", True, BLACK)
        start_text_rect = start_text.get_rect(center=start_button.center)
        screen.blit(start_text, start_text_rect)
        
        pygame.display.flip()
        clock.tick(15)

def game_over_screen(score, high_score):
    """
    게임 오버 화면을 표시합니다.
    """
    lesson = get_random_advice()
    restart_button = pygame.Rect(SCREEN_WIDTH / 2 - 100, SCREEN_HEIGHT - 150, 200, 80)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if restart_button.collidepoint(event.pos):
                    return

        screen.fill(WHITE)

        # "Game Over" 텍스트
        game_over_text = start_font.render("GAME OVER", True, BLACK)
        game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 4))
        screen.blit(game_over_text, game_over_rect)

        # 점수 표시
        score_text = high_score_font.render(f"Your Score: {score}", True, BLACK)
        score_rect = score_text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 50))
        screen.blit(score_text, score_rect)

        highscore_text = high_score_font.render(f"High Score: {high_score}", True, BLACK)
        highscore_rect = highscore_text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))
        screen.blit(highscore_text, highscore_rect)

        # 오늘의 교훈 표시
        lesson_title_text = lesson_font.render("오늘의 명언(영어):", True, BLACK)
        screen.blit(lesson_title_text, (20, SCREEN_HEIGHT / 2 + 80))
        draw_text(screen, lesson, (20, SCREEN_HEIGHT / 2 + 80 + lesson_font.get_linesize()), lesson_font, BLACK, SCREEN_WIDTH - 40)

        # 다시 시작 버튼
        pygame.draw.rect(screen, (200, 200, 200), restart_button)
        restart_text = score_font.render("RESTART", True, BLACK)
        restart_text_rect = restart_text.get_rect(center=restart_button.center)
        screen.blit(restart_text, restart_text_rect)

        pygame.display.flip()
        clock.tick(15)

def game_loop(high_score):
    # 플레이어 설정
    player_img = player_font.render("나", True, BLUE)
    player_rect = player_img.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT - 40))
    player_speed_initial = 3
    player_speed = player_speed_initial

    # 장애물 설정
    line1 = obstacle_font.render("도", True, RED)
    line2 = obstacle_font.render("티", True, RED)
    obstacle_width = max(line1.get_width(), line2.get_width())
    obstacle_height = line1.get_height() + line2.get_height()
    obstacle_img = pygame.Surface((obstacle_width, obstacle_height), pygame.SRCALPHA)
    obstacle_img.blit(line1, ((obstacle_width - line1.get_width()) / 2, 0))
    obstacle_img.blit(line2, ((obstacle_width - line2.get_width()) / 2, line1.get_height()))

    obstacle_speed_initial = 2
    obstacle_speed = obstacle_speed_initial
    obstacle_add_rate_initial = 50
    obstacle_add_rate = obstacle_add_rate_initial
    obstacle_add_counter = 0
    obstacles = []
    score = 0
    start_time = pygame.time.get_ticks()
    game_over = False

    # 대각선 장애물 설정
    diagonal_obstacles = []
    pending_diagonal_obstacles = []
    diagonal_obstacle_speed = 10
    diagonal_obstacle_add_rate = 150
    diagonal_obstacle_add_counter = 0
    DIAGONAL_OBSTACLE_WARNING_TIME = 2000
    LIGHT_RED = (255, 150, 150)

    # "호잇짜!!" 애니메이션 설정
    milestone_score = 100
    hoitzza_animation_timer = None

    # 배경 명언 설정
    try:
        advice_font = pygame.font.Font(KOREAN_FONT_PATH, 24)
    except (NameError, FileNotFoundError, pygame.error):
        advice_font = pygame.font.Font(None, 30)

    try:
        advice_text_str = get_random_advice()
    except Exception:
        advice_text_str = "Keep trying!"

    advice_surface = create_multiline_surface(advice_text_str, advice_font, LIGHT_GRAY, SCREEN_WIDTH - 100)
    advice_rect = advice_surface.get_rect(center=(random.randint(150, SCREEN_WIDTH - 150), random.randint(150, SCREEN_HEIGHT - 150)))
    advice_x, advice_y = float(advice_rect.x), float(advice_rect.y)
    advice_dx = random.choice([-0.5, 0.5])
    advice_dy = random.choice([-0.5, 0.5])


    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]: player_rect.x -= player_speed
        if keys[pygame.K_RIGHT]: player_rect.x += player_speed

        if player_rect.left < 0: player_rect.left = 0
        if player_rect.right > SCREEN_WIDTH: player_rect.right = SCREEN_WIDTH

        elapsed_time = (pygame.time.get_ticks() - start_time) / 1000
        player_speed = player_speed_initial + elapsed_time // 10
        obstacle_speed = obstacle_speed_initial + elapsed_time // 8
        obstacle_add_rate = max(10, obstacle_add_rate_initial - (elapsed_time // 5) * 2)

        obstacle_add_counter += 1
        if obstacle_add_counter >= obstacle_add_rate:
            obstacle_add_counter = 0
            obstacle_x = random.randint(0, SCREEN_WIDTH - obstacle_width)
            obstacles.append(pygame.Rect(obstacle_x, -obstacle_height, obstacle_width, obstacle_height))

        if score > 300:
            diagonal_obstacle_add_counter += 1
            if diagonal_obstacle_add_counter >= diagonal_obstacle_add_rate and not pending_diagonal_obstacles:
                diagonal_obstacle_add_counter = 0
                if random.choice([True, False]):
                    start_pos = (-obstacle_width, random.uniform(0, SCREEN_HEIGHT * 0.5))
                    end_pos = (random.uniform(0, SCREEN_WIDTH), SCREEN_HEIGHT + obstacle_height)
                else:
                    start_pos = (SCREEN_WIDTH, random.uniform(0, SCREEN_HEIGHT * 0.5))
                    end_pos = (random.uniform(0, SCREEN_WIDTH), SCREEN_HEIGHT + obstacle_height)
                pending_diagonal_obstacles.append({'path_line': (start_pos, end_pos), 'spawn_time': pygame.time.get_ticks() + DIAGONAL_OBSTACLE_WARNING_TIME})

        for obs in obstacles[:]:
            obs.y += obstacle_speed
            if obs.top > SCREEN_HEIGHT: obstacles.remove(obs)

        current_time = pygame.time.get_ticks()
        for pending in pending_diagonal_obstacles[:]:
            if current_time >= pending['spawn_time']:
                start_pos, end_pos = pending['path_line']
                dist_x = end_pos[0] - start_pos[0]
                dist_y = end_pos[1] - start_pos[1]
                distance = (dist_x**2 + dist_y**2)**0.5
                dir_x = dist_x / distance if distance else 0
                dir_y = dist_y / distance if distance else 0
                diagonal_obstacles.append({'rect': pygame.Rect(start_pos[0], start_pos[1], obstacle_width, obstacle_height), 'dir': (dir_x, dir_y)})
                pending_diagonal_obstacles.remove(pending)

        for diag_obs in diagonal_obstacles[:]:
            diag_obs['rect'].x += diag_obs['dir'][0] * diagonal_obstacle_speed
            diag_obs['rect'].y += diag_obs['dir'][1] * diagonal_obstacle_speed
            if not screen.get_rect().colliderect(diag_obs['rect']):
                diagonal_obstacles.remove(diag_obs)

        # 배경 명언 위치 업데이트
        advice_x += advice_dx
        advice_y += advice_dy
        advice_rect.x = int(advice_x)
        advice_rect.y = int(advice_y)

        if advice_rect.left < 0 or advice_rect.right > SCREEN_WIDTH:
            advice_dx *= -1
        if advice_rect.top < 0 or advice_rect.bottom > SCREEN_HEIGHT:
            advice_dy *= -1

        for obs in obstacles:
            if player_rect.colliderect(obs.inflate(-20, -20)): game_over = True
        for diag_obs in diagonal_obstacles:
            if player_rect.colliderect(diag_obs['rect'].inflate(-20, -20)): game_over = True
        if game_over: break

        score = int(elapsed_time * 10)
        screen.fill(WHITE)
        
        # 배경 명언 그리기
        screen.blit(advice_surface, advice_rect)

        for pending in pending_diagonal_obstacles:
            pygame.draw.line(screen, LIGHT_RED, pending['path_line'][0], pending['path_line'][1], 5)

        screen.blit(player_img, player_rect)
        for obs in obstacles: screen.blit(obstacle_img, obs)
        for diag_obs in diagonal_obstacles: screen.blit(obstacle_img, diag_obs['rect'])
        
        score_text = score_font.render(f"Score: {score}", True, BLACK)
        screen.blit(score_text, (10, 10))

        if score > high_score and high_score > 0:
            time_ms = pygame.time.get_ticks()
            flash_color = RED if (time_ms // 250) % 2 == 0 else BLUE
            line1_surface = high_score_font.render("와... 너 지금", True, flash_color)
            line2_surface = high_score_font.render("최고기록 갱신중이야", True, flash_color)
            line1_rect = line1_surface.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 20))
            line2_rect = line2_surface.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 20))
            screen.blit(line1_surface, line1_rect)
            screen.blit(line2_surface, line2_rect)

        if score >= milestone_score:
            hoitzza_animation_timer = pygame.time.get_ticks()
            milestone_score += 100
        
        if hoitzza_animation_timer:
            animation_elapsed = pygame.time.get_ticks() - hoitzza_animation_timer
            if animation_elapsed < 500:
                progress = animation_elapsed / 500.0
                scale = (progress * 2) if progress < 0.5 else ((1.0 - progress) * 2)
                scale = max(0.01, scale)
                hoitzza_text_surface = hoitzza_font.render(f"{milestone_score - 100}점 호잇짜!!", True, LIGHT_GRAY)
                scaled_width = int(hoitzza_text_surface.get_width() * scale)
                scaled_height = int(hoitzza_text_surface.get_height() * scale)
                scaled_surface = pygame.transform.scale(hoitzza_text_surface, (scaled_width, scaled_height))
                scaled_rect = scaled_surface.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))
                screen.blit(scaled_surface, scaled_rect)
            else:
                hoitzza_animation_timer = None
        
        pygame.display.flip()
        clock.tick(FPS)
        
    if game_over:
        screen_copy = screen.copy()
        shake_start_time = pygame.time.get_ticks()
        while pygame.time.get_ticks() - shake_start_time < 1000:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            offset_x = random.randint(-7, 7)
            offset_y = random.randint(-7, 7)
            screen.fill(WHITE)
            screen.blit(screen_copy, (offset_x, offset_y))
            pygame.display.flip()
            clock.tick(FPS)

    return score

def main():
    high_score = load_high_score()
    while True:
        start_screen(high_score)
        current_score = game_loop(high_score)
        if current_score > high_score:
            high_score = current_score
            save_high_score(high_score)
        game_over_screen(current_score, high_score)

if __name__ == "__main__":
    main()
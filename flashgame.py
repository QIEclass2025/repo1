import sys
import os
import traceback
import pygame
import random
import requests
import json

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
try:
    KOREAN_FONT_PATH = "C:/Windows/Fonts/malgun.ttf"
    start_font = pygame.font.Font(KOREAN_FONT_PATH, 60)
    score_font = pygame.font.Font(KOREAN_FONT_PATH, 36)
    high_score_font = pygame.font.Font(KOREAN_FONT_PATH, 40)
    lesson_font = pygame.font.Font(KOREAN_FONT_PATH, 20)
except FileNotFoundError:
    start_font = pygame.font.Font(None, 74)
    score_font = pygame.font.Font(None, 36)
    high_score_font = pygame.font.Font(None, 40)
    lesson_font = pygame.font.Font(None, 24)

# --- 게임 설정 ---
clock = pygame.time.Clock()
FPS = 60
HIGHSCORE_FILE = "highscore.txt"

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
    try:
        player_font = pygame.font.Font(KOREAN_FONT_PATH, 60)
    except (NameError, FileNotFoundError):
        player_font = pygame.font.Font(None, 70)
    player_img = player_font.render("나", True, BLUE)
    player_rect = player_img.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT - 40))
    player_speed_initial = 3
    player_speed = player_speed_initial

    # 장애물 설정
    try:
        obstacle_font = pygame.font.Font(KOREAN_FONT_PATH, 30)
    except (NameError, FileNotFoundError):
        obstacle_font = pygame.font.Font(None, 35)
    
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

    # "호잇짜!!" 애니메이션 설정
    milestone_score = 100
    hoitzza_animation_timer = None
    try:
        hoitzza_font = pygame.font.Font(KOREAN_FONT_PATH, 80)
    except (NameError, FileNotFoundError):
        hoitzza_font = pygame.font.Font(None, 90)

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

        for obs in obstacles[:]:
            obs.y += obstacle_speed
            if obs.top > SCREEN_HEIGHT: obstacles.remove(obs)

        for obs in obstacles:
            if player_rect.colliderect(obs.inflate(-20, -20)):
                game_over = True

        score = int(elapsed_time * 10)

        # 배경 그리기
        screen.fill(WHITE)

        # 캐릭터 및 장애물 그리기
        screen.blit(player_img, player_rect)
        for obs in obstacles: screen.blit(obstacle_img, obs)
        
        score_text = score_font.render(f"Score: {score}", True, BLACK)
        screen.blit(score_text, (10, 10))

        # 최고기록 갱신 또는 "호잇짜!!" 애니메이션
        if score > high_score and high_score > 0:
            # 최고기록 갱신 효과
            time_ms = pygame.time.get_ticks()
            if (time_ms // 250) % 2 == 0:
                flash_color = RED
            else:
                flash_color = BLUE

            line1_surface = high_score_font.render("와... 너 지금", True, flash_color)
            line2_surface = high_score_font.render("최고기록 갱신중이야", True, flash_color)

            line1_rect = line1_surface.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 20))
            line2_rect = line2_surface.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 20))

            screen.blit(line1_surface, line1_rect)
            screen.blit(line2_surface, line2_rect)
        else:
            # "호잇짜!!" 애니메이션 트리거
            if score >= milestone_score:
                hoitzza_animation_timer = pygame.time.get_ticks()
                milestone_score += 100
            
            # "호잇짜!!" 애니메이션 렌더링
            if hoitzza_animation_timer:
                animation_elapsed = pygame.time.get_ticks() - hoitzza_animation_timer
                if animation_elapsed < 500:
                    progress = animation_elapsed / 500.0
                    if progress < 0.5:
                        scale = progress * 2
                    else:
                        scale = (1.0 - progress) * 2
                    
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
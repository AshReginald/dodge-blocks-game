# Trò chơi "Dodge the Blocks" - Né tránh các khối rơi để ghi điểm
# Người chơi điều khiển khối vuông bên dưới để tránh các vật thể rơi từ trên xuống
# Các event đặc biệt xảy ra để tăng độ khó hoặc gây bất ngờ

import os
import pygame
import random
import time

# Khởi tạo pygame
pygame.init()
WIDTH, HEIGHT = 400, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))  # Màn hình game
pygame.display.set_caption("\U0001F6A7 Dodge the Blocks")  # Tiêu đề cửa sổ
clock = pygame.time.Clock()
FPS = 60  # Số khung hình mỗi giây

# Màu sắc cơ bản
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PLAYER_COLOR = (0, 128, 255)
BLOCK_COLOR = (255, 0, 0)
WARNING_COLOR = (255, 0, 0)

# Font chữ hiển thị
font = pygame.font.SysFont("Arial", 24)
large_font = pygame.font.SysFont("Arial", 36)

# Hằng số game
PLAYER_SIZE = 50
BLOCK_SIZE = 50
INIT_BLOCK_SPEED = 4
INIT_PLAYER_SPEED = 5
BLOCK_SPAWN_INTERVAL = 1000  # Tạo khối mỗi 1000ms (1s)

# Đọc điểm cao từ file
SAVE_FILE = "highscore.txt"
if os.path.exists(SAVE_FILE):
    with open(SAVE_FILE, "r") as f:
        HIGH_SCORE = int(f.read())
else:
    HIGH_SCORE = 0

# Hàm vẽ chữ ra giữa màn hình
def draw_text_center(text, font, color, y):
    render = font.render(text, True, color)
    rect = render.get_rect(center=(WIDTH // 2, y))
    screen.blit(render, rect)

# Vòng lặp chính của game
def game_loop():
    global HIGH_SCORE

    # Khởi tạo người chơi và các thông số ban đầu
    player_x = WIDTH // 2 - PLAYER_SIZE // 2
    player_y = HEIGHT - PLAYER_SIZE - 10
    player_speed = INIT_PLAYER_SPEED
    blocks = []
    block_speed = INIT_BLOCK_SPEED
    block_size = BLOCK_SIZE
    score = 0
    game_over = False

    # Thời gian và màu nền ban đầu
    start_time = time.time()
    bg_color = WHITE
    score_multiplier = 1

    # Tạo sự kiện rơi khối
    spawn_event = pygame.USEREVENT + 1
    pygame.time.set_timer(spawn_event, BLOCK_SPAWN_INTERVAL)

    # Quản lý sự kiện đặc biệt
    active_events = {}
    last_event_time = 0
    next_event_trigger = time.time() + random.randint(8, 15)
    warning_text = ""
    warning_timer = 0

    # Hàm xử lý kết thúc game
    def end_game():
        nonlocal game_over
        global HIGH_SCORE
        game_over = True
        if score > HIGH_SCORE:
            HIGH_SCORE = score
            with open(SAVE_FILE, "w") as f:
                f.write(str(HIGH_SCORE))

    while True:
        screen.fill(bg_color)

        # Nếu game over thì hiển thị và chờ nhấn phím R để chơi lại
        if game_over:
            draw_text_center("GAME OVER", large_font, BLACK, HEIGHT // 2 - 60)
            draw_text_center(f"Score: {score}", font, BLACK, HEIGHT // 2 - 20)
            draw_text_center(f"High Score: {HIGH_SCORE}", font, BLACK, HEIGHT // 2 + 10)
            draw_text_center("Press [R] to Play Again", font, BLACK, HEIGHT // 2 + 60)
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                    return game_loop()
            continue

        # Bắt sự kiện người dùng
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == spawn_event:
                x_pos = random.randint(0, WIDTH - block_size)
                blocks.append(pygame.Rect(x_pos, 0, block_size, block_size))

        # Điều khiển nhân vật: nếu có MIRROR_MODE thì đảo chiều phím
        keys = pygame.key.get_pressed()
        control_dir = -1 if "MIRROR_MODE" in active_events else 1
        if keys[pygame.K_LEFT] and player_x > 0:
            player_x -= player_speed * control_dir
        if keys[pygame.K_RIGHT] and player_x < WIDTH - PLAYER_SIZE:
            player_x += player_speed * control_dir

        # Giới hạn người chơi trong màn hình
        player_x = max(0, min(WIDTH - PLAYER_SIZE, player_x))

        # Vẽ người chơi
        player_rect = pygame.Rect(player_x, player_y, PLAYER_SIZE, PLAYER_SIZE)
        pygame.draw.rect(screen, PLAYER_COLOR, player_rect)

        # Di chuyển và vẽ các khối
        for block in blocks[:]:
            block.y += block_speed
            if block.colliderect(player_rect):
                end_game()
            elif block.y > HEIGHT:
                blocks.remove(block)
                score += 1 * score_multiplier
            else:
                # Các điều kiện để ẩn block
                if "HIDDEN_BLOCKS" in active_events and block.y > HEIGHT // 2:
                    continue
                if "GHOST_BLOCKS" in active_events and random.random() < 0.3:
                    continue
                pygame.draw.rect(screen, BLOCK_COLOR, block)

        # Kích hoạt sự kiện đặc biệt khi đủ điểm và đủ thời gian
        if score >= 20 and time.time() > next_event_trigger and len(active_events) == 0:
            event = random.choice([
                "BIG_BLOCKS", "SLOW_PLAYER", "FAST_BLOCKS", "COLOR_CHANGE",
                "HIDDEN_BLOCKS", "MIRROR_MODE", "GHOST_BLOCKS", "MAGNET_PULL", "BLOCK_RAIN"])
            active_events[event] = time.time()
            warning_text = f"\u26a0\ufe0f {event.replace('_', ' ')}!"
            warning_timer = time.time()
            next_event_trigger = time.time() + random.randint(10, 20)

            # Tùy loại event mà thay đổi trạng thái
            if event == "BIG_BLOCKS":
                block_size = int(BLOCK_SIZE * 1.5)
            elif event == "SLOW_PLAYER":
                player_speed = INIT_PLAYER_SPEED * 0.5
            elif event == "FAST_BLOCKS":
                block_speed += 3
                score_multiplier += 1
            elif event == "COLOR_CHANGE":
                bg_color = tuple(random.randint(100, 255) for _ in range(3))
            elif event == "BLOCK_RAIN":
                for _ in range(10):
                    x_pos = random.randint(0, WIDTH - block_size)
                    blocks.append(pygame.Rect(x_pos, 0, block_size, block_size))

        # Sau 6 giây, tắt hiệu ứng event và trả trạng thái về bình thường
        to_remove = []
        for evt, start in active_events.items():
            if time.time() - start > 6:
                to_remove.append(evt)
                if evt == "BIG_BLOCKS":
                    block_size = BLOCK_SIZE
                elif evt == "SLOW_PLAYER":
                    player_speed = INIT_PLAYER_SPEED
                elif evt == "FAST_BLOCKS":
                    block_speed = INIT_BLOCK_SPEED
                    score_multiplier = 1
                elif evt == "COLOR_CHANGE":
                    bg_color = WHITE
                score += 10  # thưởng điểm khi sống sót qua sự kiện

        for evt in to_remove:
            del active_events[evt]

        # Hiển thị điểm số và cảnh báo
        screen.blit(font.render(f"Score: {score}", True, BLACK), (10, 10))
        if warning_text and time.time() - warning_timer < 2:
            draw_text_center(warning_text, large_font, WARNING_COLOR, HEIGHT // 2)

        # Cập nhật màn hình
        pygame.display.flip()
        clock.tick(FPS)

# Bắt đầu game
game_loop()

# Trò chơi "Dodge the Blocks" - Phiên bản nâng cao với 18 sự kiện đặc biệt
# Người chơi điều khiển khối vuông bên dưới để tránh các vật thể rơi từ trên xuống
# Phiên bản này bao gồm nhiều sự kiện thú vị và power-ups để tăng độ hấp dẫn

import os
import pygame
import random
import time
import math

# ===== KHỞI TẠO PYGAME =====
pygame.init()
WIDTH, HEIGHT = 400, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("🚧 Dodge the Blocks - Enhanced Edition")
clock = pygame.time.Clock()
FPS = 60

# ===== ĐỊNH NGHĨA MÀU SẮC =====
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 128, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 255)
ORANGE = (255, 128, 0)
CYAN = (0, 255, 255)
PINK = (255, 0, 128)

# ===== CÁC HẰNG SỐ GAME =====
PLAYER_SIZE = 50
BLOCK_SIZE = 50
POWERUP_SIZE = 30
INIT_BLOCK_SPEED = 4
INIT_PLAYER_SPEED = 5
BLOCK_SPAWN_INTERVAL = 1000  # milliseconds

# ===== FONT CHỮ =====
font_small = pygame.font.SysFont("Arial", 16)
font_medium = pygame.font.SysFont("Arial", 24)
font_large = pygame.font.SysFont("Arial", 36)

# ===== ĐỌC/GHI ĐIỂM CAO =====
SAVE_FILE = "highscore.txt"
if os.path.exists(SAVE_FILE):
    with open(SAVE_FILE, "r") as f:
        HIGH_SCORE = int(f.read())
else:
    HIGH_SCORE = 0

def save_high_score(score):
    """Lưu điểm cao vào file"""
    global HIGH_SCORE
    if score > HIGH_SCORE:
        HIGH_SCORE = score
        with open(SAVE_FILE, "w") as f:
            f.write(str(HIGH_SCORE))

# ===== CLASSES CHO GAME OBJECTS =====

class Player:
    """Class đại diện cho người chơi"""
    def __init__(self):
        self.x = WIDTH // 2 - PLAYER_SIZE // 2
        self.y = HEIGHT - PLAYER_SIZE - 10
        self.width = PLAYER_SIZE
        self.height = PLAYER_SIZE
        self.speed = INIT_PLAYER_SPEED
        self.color = BLUE
        
        # Trạng thái đặc biệt
        self.shield_active = False
        self.shield_timer = 0
        self.speed_boost_active = False
        self.speed_boost_timer = 0
        self.invisible = False
        
    def update(self, keys, mirror_mode=False):
        """Cập nhật vị trí người chơi dựa trên input"""
        # Xử lý mirror mode (đảo ngược điều khiển)
        direction = -1 if mirror_mode else 1
        
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.x -= self.speed * direction
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.x += self.speed * direction
            
        # Giới hạn trong màn hình
        self.x = max(0, min(WIDTH - self.width, self.x))
        
        # Cập nhật timer cho các hiệu ứng
        current_time = time.time() * 1000
        if self.shield_active and current_time > self.shield_timer:
            self.shield_active = False
        if self.speed_boost_active and current_time > self.speed_boost_timer:
            self.speed_boost_active = False
            self.speed = INIT_PLAYER_SPEED
    
    def draw(self, screen, earthquake_offset=(0, 0)):
        """Vẽ người chơi lên màn hình"""
        x_offset, y_offset = earthquake_offset
        
        # Vẽ shield nếu đang active
        if self.shield_active:
            pygame.draw.circle(screen, CYAN, 
                             (int(self.x + self.width//2 + x_offset), 
                              int(self.y + self.height//2 + y_offset)), 
                             self.width//2 + 10, 3)
        
        # Màu sắc thay đổi khi có speed boost
        color = ORANGE if self.speed_boost_active else self.color
        
        # Độ trong suốt khi invisible
        if self.invisible:
            # Tạo surface tạm với alpha
            temp_surface = pygame.Surface((self.width, self.height))
            temp_surface.set_alpha(80)  # 80/255 = ~30% opacity
            temp_surface.fill(color)
            screen.blit(temp_surface, (self.x + x_offset, self.y + y_offset))
        else:
            pygame.draw.rect(screen, color, 
                           (self.x + x_offset, self.y + y_offset, self.width, self.height))
    
    def get_rect(self):
        """Trả về pygame.Rect cho collision detection"""
        return pygame.Rect(self.x, self.y, self.width, self.height)

class Block:
    """Class đại diện cho khối rơi"""
    def __init__(self, x, y, size=BLOCK_SIZE, speed=INIT_BLOCK_SPEED):
        self.x = x
        self.y = y
        self.width = size
        self.height = size
        self.speed = speed
        self.color = RED
        self.original_x = x  # Lưu vị trí gốc cho spiral effect
        self.creation_time = time.time()
        
    def update(self, active_events, player_x):
        """Cập nhật vị trí khối dựa trên các event đang active"""
        # Di chuyển cơ bản
        move_x = 0
        move_y = self.speed
        
        # Xử lý các event đặc biệt
        if "GRAVITY_FLIP" in active_events:
            move_y = -abs(self.speed)  # Bay lên thay vì rơi xuống
            
        if "SPIRAL_BLOCKS" in active_events:
            # Di chuyển theo hình xoắn ốc
            time_factor = (time.time() - self.creation_time) * 3
            move_x = math.sin(time_factor) * 2
            
        if "MAGNET_PULL" in active_events:
            # Bị hút về phía người chơi
            player_center = player_x + PLAYER_SIZE // 2
            block_center = self.x + self.width // 2
            attraction = (player_center - block_center) * 0.05
            move_x += attraction
            
        if "TELEPORT_BLOCKS" in active_events:
            # Ngẫu nhiên dịch chuyển
            if random.random() < 0.005:  # 0.5% chance mỗi frame
                self.x = random.randint(0, WIDTH - self.width)
        
        # Áp dụng di chuyển
        self.x += move_x
        self.y += move_y
        
        # Giữ trong màn hình (trục X)
        self.x = max(0, min(WIDTH - self.width, self.x))
    
    def draw(self, screen, active_events, earthquake_offset=(0, 0)):
        """Vẽ khối lên màn hình với các hiệu ứng đặc biệt"""
        x_offset, y_offset = earthquake_offset
        
        # Kiểm tra các hiệu ứng ẩn
        if "HIDDEN_BLOCKS" in active_events and self.y > HEIGHT // 2:
            return  # Không vẽ nếu ở nửa dưới màn hình
            
        if "GHOST_BLOCKS" in active_events and random.random() < 0.3:
            # Tạo hiệu ứng trong suốt
            temp_surface = pygame.Surface((self.width, self.height))
            temp_surface.set_alpha(80)
            temp_surface.fill(self.color)
            screen.blit(temp_surface, (self.x + x_offset, self.y + y_offset))
        else:
            pygame.draw.rect(screen, self.color, 
                           (self.x + x_offset, self.y + y_offset, self.width, self.height))
    
    def get_rect(self):
        """Trả về pygame.Rect cho collision detection"""
        return pygame.Rect(self.x, self.y, self.width, self.height)

class PowerUp:
    """Class đại diện cho power-up"""
    def __init__(self, x, y, power_type):
        self.x = x
        self.y = y
        self.width = POWERUP_SIZE
        self.height = POWERUP_SIZE
        self.speed = 2
        self.type = power_type
        self.collected = False
        
        # Màu sắc theo loại
        if power_type == "shield":
            self.color = CYAN
            self.symbol = "S"
        elif power_type == "speed":
            self.color = PURPLE
            self.symbol = "+"
        elif power_type == "score":
            self.color = YELLOW
            self.symbol = "*"
    
    def update(self):
        """Cập nhật vị trí power-up"""
        self.y += self.speed
    
    def draw(self, screen):
        """Vẽ power-up lên màn hình"""
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))
        # Vẽ ký hiệu
        text = font_medium.render(self.symbol, True, BLACK)
        text_rect = text.get_rect(center=(self.x + self.width//2, self.y + self.height//2))
        screen.blit(text, text_rect)
    
    def get_rect(self):
        """Trả về pygame.Rect cho collision detection"""
        return pygame.Rect(self.x, self.y, self.width, self.height)

class Particle:
    """Class cho hiệu ứng particle khi thu thập power-up"""
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.vx = random.uniform(-3, 3)
        self.vy = random.uniform(-3, 3)
        self.color = color
        self.life = 60  # 60 frames = 1 giây ở 60 FPS
        self.max_life = 60
        self.size = random.randint(2, 5)
    
    def update(self):
        """Cập nhật particle"""
        self.x += self.vx
        self.y += self.vy
        self.life -= 1
        # Giảm tốc độ dần
        self.vx *= 0.98
        self.vy *= 0.98
    
    def draw(self, screen):
        """Vẽ particle với alpha dựa trên life"""
        if self.life > 0:
            alpha = int(255 * (self.life / self.max_life))
            temp_surface = pygame.Surface((self.size * 2, self.size * 2))
            temp_surface.set_alpha(alpha)
            pygame.draw.circle(temp_surface, self.color, (self.size, self.size), self.size)
            screen.blit(temp_surface, (self.x - self.size, self.y - self.size))

# ===== GAME MANAGER CLASS =====

class GameManager:
    """Class quản lý toàn bộ game logic"""
    def __init__(self):
        self.reset_game()
        
    def reset_game(self):
        """Reset game về trạng thái ban đầu"""
        self.player = Player()
        self.blocks = []
        self.powerups = []
        self.particles = []
        
        # Game stats
        self.score = 0
        self.level = 1
        self.block_speed = INIT_BLOCK_SPEED
        self.block_size = BLOCK_SIZE
        self.score_multiplier = 1
        
        # Timing
        self.last_block_spawn = 0
        self.last_powerup_spawn = 0
        self.last_event_time = 0
        self.next_event_time = time.time() + random.randint(8, 15)
        
        # Events
        self.active_events = {}
        self.event_end_times = {}
        self.warning_text = ""
        self.warning_timer = 0
        
        # Visual effects
        self.bg_color = BLACK
        self.earthquake_offset = (0, 0)
        self.laser_y = -100  # Vị trí laser beam
        
        # Game state
        self.game_over = False
        self.paused = False
    
    def spawn_block(self):
        """Tạo khối mới"""
        x = random.randint(0, WIDTH - self.block_size)
        block = Block(x, -self.block_size, self.block_size, self.block_speed)
        self.blocks.append(block)
    
    def spawn_powerup(self):
        """Tạo power-up mới"""
        x = random.randint(0, WIDTH - POWERUP_SIZE)
        power_type = random.choice(["shield", "speed", "score"])
        powerup = PowerUp(x, -POWERUP_SIZE, power_type)
        self.powerups.append(powerup)
    
    def trigger_event(self):
        """Kích hoạt sự kiện đặc biệt ngẫu nhiên"""
        # Danh sách tất cả 18 events
        events = [
            "BIG_BLOCKS", "TINY_BLOCKS", "FAST_BLOCKS", "SLOW_MOTION",
            "MIRROR_MODE", "BLOCK_RAIN", "GHOST_BLOCKS", "COLOR_CHANGE",
            "GRAVITY_FLIP", "MAGNET_PULL", "INVISIBLE_PLAYER", "DOUBLE_SCORE",
            "FREEZE_BLOCKS", "SPIRAL_BLOCKS", "EARTHQUAKE", "LASER_BEAM",
            "SHIELD_RAIN", "TELEPORT_BLOCKS"
        ]
        
        event = random.choice(events)
        current_time = time.time()
        
        # Đặt thời gian kết thúc event (6 giây)
        self.active_events[event] = current_time
        self.event_end_times[event] = current_time + 6
        
        # Hiển thị warning
        self.warning_text = event.replace("_", " ")
        self.warning_timer = current_time
        
        # Đặt thời gian cho event tiếp theo
        self.next_event_time = current_time + random.randint(10, 20)
        
        # Xử lý logic riêng cho từng event
        if event == "BIG_BLOCKS":
            self.block_size = int(BLOCK_SIZE * 1.8)
        elif event == "TINY_BLOCKS":
            self.block_size = int(BLOCK_SIZE * 0.6)
        elif event == "FAST_BLOCKS":
            self.block_speed += 3
            self.score_multiplier = 3
        elif event == "SLOW_MOTION":
            self.block_speed = max(1, int(self.block_speed * 0.3))
            self.player.speed = int(INIT_PLAYER_SPEED * 0.5)
        elif event == "COLOR_CHANGE":
            # Đổi màu nền ngẫu nhiên
            colors = [BLUE, GREEN, PURPLE, ORANGE, PINK]
            self.bg_color = random.choice(colors)
        elif event == "BLOCK_RAIN":
            # Tạo nhiều khối cùng lúc
            for i in range(12):
                pygame.time.set_timer(pygame.USEREVENT + 2, i * 80)
        elif event == "INVISIBLE_PLAYER":
            self.player.invisible = True
        elif event == "DOUBLE_SCORE":
            self.score_multiplier = 4
        elif event == "FREEZE_BLOCKS":
            self.block_speed = 0
        elif event == "LASER_BEAM":
            self.laser_y = HEIGHT * 0.7  # Laser ở 70% chiều cao màn hình
        elif event == "SHIELD_RAIN":
            # Tạo nhiều shield power-ups
            for i in range(3):
                pygame.time.set_timer(pygame.USEREVENT + 3, i * 500)
    
    def end_event(self, event):
        """Kết thúc một event và trả về trạng thái bình thường"""
        if event == "BIG_BLOCKS" or event == "TINY_BLOCKS":
            self.block_size = BLOCK_SIZE
        elif event == "FAST_BLOCKS":
            self.block_speed = INIT_BLOCK_SPEED + self.level
            self.score_multiplier = 1
        elif event == "SLOW_MOTION":
            self.block_speed = INIT_BLOCK_SPEED + self.level
            self.player.speed = INIT_PLAYER_SPEED
        elif event == "COLOR_CHANGE":
            self.bg_color = BLACK
        elif event == "GRAVITY_FLIP":
            self.block_speed = abs(self.block_speed)
        elif event == "INVISIBLE_PLAYER":
            self.player.invisible = False
        elif event == "DOUBLE_SCORE":
            self.score_multiplier = 1
        elif event == "FREEZE_BLOCKS":
            self.block_speed = INIT_BLOCK_SPEED + self.level
        elif event == "LASER_BEAM":
            self.laser_y = -100
        
        # Thưởng điểm khi sống sót qua event
        self.score += 15
    
    def update(self, keys):
        """Cập nhật toàn bộ game logic"""
        if self.game_over or self.paused:
            return
            
        current_time = time.time()
        
        # Cập nhật player
        mirror_mode = "MIRROR_MODE" in self.active_events
        self.player.update(keys, mirror_mode)
        
        # Kiểm tra và kết thúc events
        events_to_remove = []
        for event, end_time in self.event_end_times.items():
            if current_time > end_time:
                events_to_remove.append(event)
                self.end_event(event)
        
        for event in events_to_remove:
            del self.active_events[event]
            del self.event_end_times[event]
        
        # Spawn blocks
        if current_time * 1000 - self.last_block_spawn > max(1000 - self.level * 50, 300):
            self.spawn_block()
            self.last_block_spawn = current_time * 1000
        
        # Spawn power-ups
        if current_time * 1000 - self.last_powerup_spawn > 8000 + random.randint(0, 7000):
            self.spawn_powerup()
            self.last_powerup_spawn = current_time * 1000
        
        # Trigger events
        if (self.score >= 50 and current_time > self.next_event_time and 
            len(self.active_events) == 0):
            self.trigger_event()
        
        # Cập nhật blocks
        blocks_to_remove = []
        for i, block in enumerate(self.blocks):
            block.update(self.active_events, self.player.x)
            
            # Kiểm tra va chạm
            if block.get_rect().colliderect(self.player.get_rect()):
                if not self.player.shield_active:
                    self.game_over = True
                    save_high_score(self.score)
                    return
            
            # Xóa blocks ra khỏi màn hình
            if "GRAVITY_FLIP" in self.active_events:
                if block.y < -block.height:
                    blocks_to_remove.append(i)
                    self.score += self.score_multiplier
            else:
                if block.y > HEIGHT:
                    blocks_to_remove.append(i)
                    self.score += self.score_multiplier
        
        # Xóa blocks (từ cuối lên để không ảnh hưởng index)
        for i in reversed(blocks_to_remove):
            del self.blocks[i]
        
        # Cập nhật power-ups
        powerups_to_remove = []
        for i, powerup in enumerate(self.powerups):
            powerup.update()
            
            # Kiểm tra thu thập
            if powerup.get_rect().colliderect(self.player.get_rect()):
                powerups_to_remove.append(i)
                
                # Tạo particle effect
                for _ in range(8):
                    particle = Particle(powerup.x + powerup.width//2, 
                                       powerup.y + powerup.height//2, 
                                       powerup.color)
                    self.particles.append(particle)
                
                # Áp dụng hiệu ứng power-up
                if powerup.type == "shield":
                    self.player.shield_active = True
                    self.player.shield_timer = current_time * 1000 + 5000
                elif powerup.type == "speed":
                    self.player.speed_boost_active = True
                    self.player.speed_boost_timer = current_time * 1000 + 5000
                    self.player.speed = int(INIT_PLAYER_SPEED * 1.5)
                elif powerup.type == "score":
                    self.score += 50
            
            # Xóa power-ups ra khỏi màn hình
            elif powerup.y > HEIGHT:
                powerups_to_remove.append(i)
        
        # Xóa power-ups
        for i in reversed(powerups_to_remove):
            del self.powerups[i]
        
        # Cập nhật particles
        particles_to_remove = []
        for i, particle in enumerate(self.particles):
            particle.update()
            if particle.life <= 0:
                particles_to_remove.append(i)
        
        for i in reversed(particles_to_remove):
            del self.particles[i]
        
        # Kiểm tra laser beam collision
        if "LASER_BEAM" in self.active_events:
            player_rect = self.player.get_rect()
            if (player_rect.bottom > self.laser_y - 5 and 
                player_rect.top < self.laser_y + 5 and 
                not self.player.shield_active):
                self.game_over = True
                save_high_score(self.score)
                return
        
        # Cập nhật level
        new_level = self.score // 100 + 1
        if new_level > self.level:
            self.level = new_level
            self.block_speed = INIT_BLOCK_SPEED + self.level
        
        # Earthquake effect
        if "EARTHQUAKE" in self.active_events:
            self.earthquake_offset = (random.randint(-5, 5), random.randint(-5, 5))
        else:
            self.earthquake_offset = (0, 0)
    
    def draw(self, screen):
        """Vẽ toàn bộ game lên màn hình"""
        # Xóa màn hình với màu nền
        screen.fill(self.bg_color)
        
        # Vẽ laser beam
        if "LASER_BEAM" in self.active_events:
            pygame.draw.rect(screen, RED, (0, self.laser_y - 5, WIDTH, 10))
        
        # Vẽ tất cả game objects
        for block in self.blocks:
            block.draw(screen, self.active_events, self.earthquake_offset)
        
        for powerup in self.powerups:
            powerup.draw(screen)
        
        for particle in self.particles:
            particle.draw(screen)
        
        self.player.draw(screen, self.earthquake_offset)
        
        # Vẽ UI
        self.draw_ui(screen)
    
    def draw_ui(self, screen):
        """Vẽ giao diện người dùng"""
        # Score và Level
        score_text = font_medium.render(f"Score: {self.score}", True, WHITE)
        level_text = font_medium.render(f"Level: {self.level}", True, WHITE)
        screen.blit(score_text, (10, 10))
        screen.blit(level_text, (10, 40))
        
        # Active events
        y_offset = 70
        for event in self.active_events:
            event_text = font_small.render(f"⚡ {event.replace('_', ' ')}", True, YELLOW)
            screen.blit(event_text, (10, y_offset))
            y_offset += 20
        
        # Player status
        if self.player.shield_active:
            shield_text = font_small.render("🛡️ Shield Active", True, CYAN)
            screen.blit(shield_text, (10, y_offset))
            y_offset += 20
        
        if self.player.speed_boost_active:
            speed_text = font_small.render("⚡ Speed Boost", True, PURPLE)
            screen.blit(speed_text, (10, y_offset))
            y_offset += 20
        
        # Warning text
        if self.warning_text and time.time() - self.warning_timer < 2:
            warning_surface = font_large.render(f"⚠️ {self.warning_text}", True, RED)
            warning_rect = warning_surface.get_rect(center=(WIDTH//2, HEIGHT//2))
            screen.blit(warning_surface, warning_rect)
        
        # Pause text
        if self.paused:
            pause_surface = font_large.render("PAUSED", True, WHITE)
            pause_rect = pause_surface.get_rect(center=(WIDTH//2, HEIGHT//2))
            pygame.draw.rect(screen, BLACK, pause_rect.inflate(20, 20))
            screen.blit(pause_surface, pause_rect)

def draw_text_center(screen, text, font, color, y):
    """Hàm tiện ích để vẽ text ở giữa màn hình"""
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(WIDTH // 2, y))
    screen.blit(text_surface, text_rect)

def show_menu(screen):
    """Hiển thị menu chính"""
    screen.fill(BLACK)
    
    # Title
    draw_text_center(screen, "🚧 DODGE BLOCKS", font_large, WHITE, HEIGHT//2 - 100)
    draw_text_center(screen, "Enhanced Edition", font_medium, YELLOW, HEIGHT//2 - 60)
    
    # High score
    draw_text_center(screen, f"High Score: {HIGH_SCORE}", font_medium, GREEN, HEIGHT//2 - 20)
    
    # Instructions
    draw_text_center(screen, "Press SPACE to Start", font_medium, WHITE, HEIGHT//2 + 20)
    draw_text_center(screen, "Press I for Instructions", font_small, WHITE, HEIGHT//2 + 50)
    draw_text_center(screen, "Use ← → or A/D to move", font_small, WHITE, HEIGHT//2 + 80)
    
    pygame.display.flip()

def show_instructions(screen):
    """Hiển thị hướng dẫn chi tiết"""
    screen.fill(BLACK)
    
    instructions = [
        "🎮 GAME INSTRUCTIONS",
        "",
        "CONTROLS:",
        "← → or A/D: Move left/right",
        "SPACE: Pause/Resume",
        "ESC: Back to menu",
        "",
        "POWER-UPS:",
        "🛡️ Shield (S): Protection for 5 seconds",
        "⚡ Speed (+ ): Faster movement for 5 seconds",
        "⭐ Score (*): Instant +50 points",
        "",
        "SPECIAL EVENTS (18 total):",
        "• Big/Tiny Blocks • Fast/Slow Motion",
        "• Mirror Mode • Block Rain • Ghost Blocks",
        "• Gravity Flip • Magnet Pull • Invisible Player",
        "• Double Score • Freeze Blocks • Spiral Blocks",
        "• Earthquake • Laser Beam • Shield Rain",
        "• Teleport Blocks • Color Change",
        "",
        "Press ESC to return to menu"
    ]
    
    y = 50
    for line in instructions:
        if line.startswith("🎮"):
            draw_text_center(screen, line, font_large, YELLOW, y)
        elif line == "":
            pass  # Skip empty lines
        elif line.endswith(":"):
            draw_text_center(screen, line, font_medium, GREEN, y)
        else:
            draw_text_center(screen, line, font_small, WHITE, y)
        y += 25
    
    pygame.display.flip()

def show_game_over(screen, final_score):
    """Hiển thị màn hình game over"""
    screen.fill(BLACK)
    
    # Game Over text
    draw_text_center(screen, "GAME OVER", font_large, RED, HEIGHT//2 - 80)
    
    # Scores
    draw_text_center(screen, f"Final Score: {final_score}", font_medium, WHITE, HEIGHT//2 - 40)
    draw_text_center(screen, f"High Score: {HIGH_SCORE}", font_medium, YELLOW, HEIGHT//2 - 10)
    
    # New high score notification
    if final_score == HIGH_SCORE and final_score > 0:
        draw_text_center(screen, "🎉 NEW HIGH SCORE! 🎉", font_medium, GREEN, HEIGHT//2 + 20)
    
    # Instructions
    draw_text_center(screen, "Press R to Play Again", font_medium, WHITE, HEIGHT//2 + 60)
    draw_text_center(screen, "Press ESC for Menu", font_small, WHITE, HEIGHT//2 + 90)
    
    pygame.display.flip()

# ===== MAIN GAME LOOP =====

def main():
    """Hàm chính của game"""
    game_manager = GameManager()
    
    # Game states
    STATE_MENU = 0
    STATE_INSTRUCTIONS = 1
    STATE_PLAYING = 2
    STATE_GAME_OVER = 3
    
    current_state = STATE_MENU
    running = True
    
    # Event timers
    pygame.time.set_timer(pygame.USEREVENT + 1, BLOCK_SPAWN_INTERVAL)
    
    while running:
        # Xử lý events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            elif event.type == pygame.KEYDOWN:
                if current_state == STATE_MENU:
                    if event.key == pygame.K_SPACE:
                        game_manager.reset_game()
                        current_state = STATE_PLAYING
                    elif event.key == pygame.K_i:
                        current_state = STATE_INSTRUCTIONS
                
                elif current_state == STATE_INSTRUCTIONS:
                    if event.key == pygame.K_ESCAPE:
                        current_state = STATE_MENU
                
                elif current_state == STATE_PLAYING:
                    if event.key == pygame.K_SPACE:
                        game_manager.paused = not game_manager.paused
                    elif event.key == pygame.K_ESCAPE:
                        current_state = STATE_MENU
                
                elif current_state == STATE_GAME_OVER:
                    if event.key == pygame.K_r:
                        game_manager.reset_game()
                        current_state = STATE_PLAYING
                    elif event.key == pygame.K_ESCAPE:
                        current_state = STATE_MENU
            
            # Custom events cho spawning
            elif event.type == pygame.USEREVENT + 2:  # Block rain
                game_manager.spawn_block()
            elif event.type == pygame.USEREVENT + 3:  # Shield rain
                x = random.randint(0, WIDTH - POWERUP_SIZE)
                powerup = PowerUp(x, -POWERUP_SIZE, "shield")
                game_manager.powerups.append(powerup)
        
        # Game logic dựa trên state
        if current_state == STATE_MENU:
            show_menu(screen)
        
        elif current_state == STATE_INSTRUCTIONS:
            show_instructions(screen)
        
        elif current_state == STATE_PLAYING:
            # Lấy input
            keys = pygame.key.get_pressed()
            
            # Cập nhật game
            game_manager.update(keys)
            
            # Kiểm tra game over
            if game_manager.game_over:
                current_state = STATE_GAME_OVER
            
            # Vẽ game
            game_manager.draw(screen)
            pygame.display.flip()
        
        elif current_state == STATE_GAME_OVER:
            show_game_over(screen, game_manager.score)
        
        clock.tick(FPS)
    
    pygame.quit()

# ===== CHẠY GAME =====
if __name__ == "__main__":
    main()
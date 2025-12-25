import pygame
import sys
import math
import random

# =========================
# INISIALISASI
# =========================
pygame.init()
WIDTH, HEIGHT = 900, 650
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("🏡 Mini Scene Grafika 2D - Enhanced Edition")
clock = pygame.time.Clock()

# Warna Extended
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)
GREEN = (0, 180, 0)
DARK_GREEN = (0, 100, 0)
BROWN = (139, 69, 19)
GRAY = (120, 120, 120)
DARK_GRAY = (80, 80, 80)
SKY_BLUE = (135, 206, 235)
NIGHT_BLUE = (25, 25, 112)
RED = (200, 50, 50)
PINK = (255, 182, 193)
LIGHT_YELLOW = (255, 255, 224)
CLOUD_WHITE = (240, 248, 255)

# =========================
# PLOT PIXEL
# =========================
def plot(x, y, color=BLACK):
    if 0 <= int(x) < WIDTH and 0 <= int(y) < HEIGHT:
        screen.set_at((int(x), int(y)), color)

# =========================
# GARIS DDA
# =========================
def line_dda(x1, y1, x2, y2, color=BLACK):
    dx = x2 - x1
    dy = y2 - y1
    steps = int(max(abs(dx), abs(dy)))
    if steps == 0:
        plot(x1, y1, color)
        return
    x_inc = dx / steps
    y_inc = dy / steps
    x, y = x1, y1
    for _ in range(steps):
        plot(round(x), round(y), color)
        x += x_inc
        y += y_inc

# =========================
# GARIS BRESENHAM
# =========================
def line_bresenham(x1, y1, x2, y2, color=BLACK):
    x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
    dx = abs(x2 - x1)
    dy = abs(y2 - y1)
    sx = 1 if x1 < x2 else -1
    sy = 1 if y1 < y2 else -1
    err = dx - dy
    
    while True:
        plot(x1, y1, color)
        if x1 == x2 and y1 == y2:
            break
        e2 = 2 * err
        if e2 > -dy:
            err -= dy
            x1 += sx
        if e2 < dx:
            err += dx
            y1 += sy

# =========================
# LINGKARAN MIDPOINT
# =========================
def circle_midpoint(xc, yc, r, color=BLACK):
    x = 0
    y = r
    p = 1 - r
    while x <= y:
        plot(xc + x, yc + y, color)
        plot(xc - x, yc + y, color)
        plot(xc + x, yc - y, color)
        plot(xc - x, yc - y, color)
        plot(xc + y, yc + x, color)
        plot(xc - y, yc + x, color)
        plot(xc + y, yc - x, color)
        plot(xc - y, yc - x, color)
        x += 1
        if p < 0:
            p += 2 * x + 1
        else:
            y -= 1
            p += 2 * (x - y) + 1

# =========================
# LINGKARAN TERISI (SCANLINE)
# =========================
def filled_circle(xc, yc, r, color):
    for y in range(-r, r + 1):
        x_width = int(math.sqrt(r * r - y * y))
        for x in range(-x_width, x_width + 1):
            plot(xc + x, yc + y, color)

# =========================
# POLYGON
# =========================
def polygon(points, color=BLACK):
    n = len(points)
    for i in range(n):
        x1, y1 = points[i]
        x2, y2 = points[(i + 1) % n]
        line_dda(x1, y1, x2, y2, color)

# =========================
# POLYGON TERISI
# =========================
def filled_polygon(points, color):
    if len(points) < 3:
        return
    min_y = int(min(p[1] for p in points))
    max_y = int(max(p[1] for p in points))
    
    for y in range(min_y, max_y + 1):
        intersections = []
        n = len(points)
        for i in range(n):
            x1, y1 = points[i]
            x2, y2 = points[(i + 1) % n]
            if y1 == y2:
                continue
            if y < min(y1, y2) or y > max(y1, y2):
                continue
            x = x1 + (y - y1) * (x2 - x1) / (y2 - y1)
            intersections.append(x)
        
        intersections.sort()
        for i in range(0, len(intersections) - 1, 2):
            x_start = int(intersections[i])
            x_end = int(intersections[i + 1])
            for x in range(x_start, x_end + 1):
                plot(x, y, color)

# =========================
# TRANSFORMASI
# =========================
def translate(points, tx, ty):
    return [(x + tx, y + ty) for x, y in points]

def rotate(points, angle, cx, cy):
    rad = math.radians(angle)
    cos_a = math.cos(rad)
    sin_a = math.sin(rad)
    result = []
    for x, y in points:
        x_new = cos_a * (x - cx) - sin_a * (y - cy) + cx
        y_new = sin_a * (x - cx) + cos_a * (y - cy) + cy
        result.append((x_new, y_new))
    return result

def scale(points, sx, sy, cx, cy):
    result = []
    for x, y in points:
        x_new = sx * (x - cx) + cx
        y_new = sy * (y - cy) + cy
        result.append((x_new, y_new))
    return result

# =========================
# OBJEK SCENE
# =========================
class Cloud:
    def __init__(self, x, y, speed):
        self.x = x
        self.y = y
        self.speed = speed
    
    def draw(self):
        filled_circle(int(self.x), int(self.y), 20, CLOUD_WHITE)
        filled_circle(int(self.x + 25), int(self.y), 25, CLOUD_WHITE)
        filled_circle(int(self.x + 50), int(self.y), 20, CLOUD_WHITE)
    
    def update(self):
        self.x += self.speed
        if self.x > WIDTH + 60:
            self.x = -60

class Star:
    def __init__(self):
        self.x = random.randint(0, WIDTH)
        self.y = random.randint(0, 200)
        self.brightness = random.randint(150, 255)
    
    def draw(self):
        color = (self.brightness, self.brightness, self.brightness)
        plot(self.x, self.y, color)
        plot(self.x + 1, self.y, color)
        plot(self.x, self.y + 1, color)

class Bird:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.angle = 0
    
    def draw(self):
        # V-shape bird
        line_bresenham(self.x - 10, self.y, self.x, self.y + 5, BLACK)
        line_bresenham(self.x, self.y + 5, self.x + 10, self.y, BLACK)
    
    def update(self):
        self.x += 2
        self.y += math.sin(self.angle) * 0.5
        self.angle += 0.1
        if self.x > WIDTH + 20:
            self.x = -20
            self.y = random.randint(50, 150)

class Windmill:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.angle = 0
    
    def draw(self):
        # Tower (trapesium)
        tower = [(self.x - 15, self.y), (self.x + 15, self.y), 
                 (self.x + 10, self.y - 80), (self.x - 10, self.y - 80)]
        filled_polygon(tower, GRAY)
        polygon(tower, BLACK)
        
        # Center hub
        filled_circle(self.x, self.y - 80, 8, DARK_GRAY)
        circle_midpoint(self.x, self.y - 80, 8, BLACK)
        
        # Blades (4 blades with rotation)
        for i in range(4):
            blade_angle = self.angle + i * 90
            blade = self.create_blade(blade_angle)
            filled_polygon(blade, WHITE)
            polygon(blade, BLACK)
    
    def create_blade(self, angle):
        # Create rotated blade
        cx, cy = self.x, self.y - 80
        blade_points = [
            (cx - 5, cy),
            (cx + 5, cy),
            (cx + 3, cy - 40),
            (cx - 3, cy - 40)
        ]
        return rotate(blade_points, angle, cx, cy)
    
    def update(self):
        self.angle += 2  # Rotation speed

class Flower:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.scale = 1.0
        self.target_scale = 1.0
        self.is_clicked = False
    
    def check_click(self, mouse_x, mouse_y):
        # Check if mouse is near flower
        distance = math.sqrt((mouse_x - self.x) ** 2 + (mouse_y - self.y) ** 2)
        if distance < 20:
            self.is_clicked = True
            self.target_scale = 1.8
            return True
        return False
    
    def draw(self):
        # Smooth scale transition
        if self.is_clicked:
            if self.scale < self.target_scale:
                self.scale += 0.05
        else:
            if self.scale > 1.0:
                self.scale -= 0.05
            else:
                self.scale = 1.0
        
        # Batang
        line_dda(self.x, self.y, self.x, self.y - 20 * self.scale, DARK_GREEN)
        
        # Kelopak (5 petals) dengan skala
        petal_radius = int(5 * self.scale)
        for i in range(5):
            angle = i * 72
            rad = math.radians(angle)
            px = self.x + math.cos(rad) * 8 * self.scale
            py = self.y - 20 * self.scale + math.sin(rad) * 8 * self.scale
            filled_circle(int(px), int(py), petal_radius, self.color)
        
        # Tengah bunga
        filled_circle(self.x, int(self.y - 20 * self.scale), int(4 * self.scale), YELLOW)
    
    def reset_click(self):
        self.is_clicked = False
        self.target_scale = 1.0

# =========================
# GAMBAR OBJEK
# =========================
def draw_sun(x, y, time_factor):
    # Sun with rays
    radius = 35
    color = YELLOW if time_factor > 0.3 else ORANGE
    filled_circle(int(x), int(y), radius, color)
    circle_midpoint(int(x), int(y), radius, ORANGE)
    
    # Rays
    for i in range(8):
        angle = i * 45
        rad = math.radians(angle)
        x1 = x + math.cos(rad) * (radius + 5)
        y1 = y + math.sin(rad) * (radius + 5)
        x2 = x + math.cos(rad) * (radius + 15)
        y2 = y + math.sin(rad) * (radius + 15)
        line_dda(x1, y1, x2, y2, color)

def draw_moon(x, y):
    filled_circle(int(x), int(y), 30, LIGHT_YELLOW)
    circle_midpoint(int(x), int(y), 30, WHITE)
    # Craters
    filled_circle(int(x - 8), int(y - 5), 4, GRAY)
    filled_circle(int(x + 10), int(y + 8), 3, GRAY)

def draw_house(x, y, scale_factor=1):
    # Dinding dengan filling
    wall = [(x, y), (x + 200 * scale_factor, y), 
            (x + 200 * scale_factor, y + 100), (x, y + 100)]
    filled_polygon(wall, RED)
    polygon(wall, BLACK)
    
    # Atap dengan filling
    roof = [(x - 20, y), (x + 220 * scale_factor, y), (x + 100 * scale_factor, y - 70)]
    filled_polygon(roof, BROWN)
    polygon(roof, BLACK)
    
    # Pintu
    door = [(x + 80 * scale_factor, y + 50), (x + 120 * scale_factor, y + 50),
            (x + 120 * scale_factor, y + 100), (x + 80 * scale_factor, y + 100)]
    filled_polygon(door, BROWN)
    polygon(door, BLACK)
    
    # Gagang pintu
    filled_circle(int(x + 110 * scale_factor), int(y + 75), 3, BLACK)
    
    # Jendela kiri
    window1 = [(x + 30, y + 30), (x + 60, y + 30), (x + 60, y + 60), (x + 30, y + 60)]
    filled_polygon(window1, LIGHT_YELLOW)
    polygon(window1, BLACK)
    line_dda(x + 45, y + 30, x + 45, y + 60, BLACK)
    line_dda(x + 30, y + 45, x + 60, y + 45, BLACK)
    
    # Jendela kanan
    window2 = [(x + 140, y + 30), (x + 170, y + 30), (x + 170, y + 60), (x + 140, y + 60)]
    filled_polygon(window2, LIGHT_YELLOW)
    polygon(window2, BLACK)
    line_dda(x + 155, y + 30, x + 155, y + 60, BLACK)
    line_dda(x + 140, y + 45, x + 170, y + 45, BLACK)
    
    # Cerobong asap
    chimney = [(x + 150, y - 50), (x + 170, y - 50), (x + 170, y - 20), (x + 150, y - 20)]
    filled_polygon(chimney, BROWN)
    polygon(chimney, BLACK)

def draw_tree(x, y, swing_angle=0):
    # Batang dengan tekstur
    trunk = [(x - 15, y - 70), (x + 15, y - 70), (x + 15, y), (x - 15, y)]
    filled_polygon(trunk, BROWN)
    polygon(trunk, BLACK)
    
    # Tekstur batang
    for i in range(5):
        line_dda(x - 10, y - 15 * i - 10, x + 10, y - 15 * i - 5, DARK_GRAY)
    
    # Daun berlapis (3 lingkaran)
    filled_circle(x, int(y - 90), 35, GREEN)
    filled_circle(x - 20, int(y - 75), 30, DARK_GREEN)
    filled_circle(x + 20, int(y - 75), 30, DARK_GREEN)
    
    circle_midpoint(x, int(y - 90), 35, DARK_GREEN)
    circle_midpoint(x - 20, int(y - 75), 30, DARK_GREEN)
    circle_midpoint(x + 20, int(y - 75), 30, DARK_GREEN)

def draw_flower(x, y, color):
    # Batang
    line_dda(x, y, x, y - 20, DARK_GREEN)
    
    # Kelopak (5 petals)
    petal_radius = 5
    for i in range(5):
        angle = i * 72
        rad = math.radians(angle)
        px = x + math.cos(rad) * 8
        py = y - 20 + math.sin(rad) * 8
        filled_circle(int(px), int(py), petal_radius, color)
    
    # Tengah bunga
    filled_circle(x, y - 20, 4, YELLOW)

def draw_windmill(x, y, angle):
    # Tower (trapesium)
    tower = [(x - 15, y), (x + 15, y), 
             (x + 10, y - 80), (x - 10, y - 80)]
    filled_polygon(tower, GRAY)
    polygon(tower, BLACK)
    
    # Center hub
    filled_circle(x, y - 80, 8, DARK_GRAY)
    circle_midpoint(x, y - 80, 8, BLACK)
    
    # Blades (4 blades with rotation)
    for i in range(4):
        blade_angle = angle + i * 90
        blade = create_windmill_blade(x, y - 80, blade_angle)
        filled_polygon(blade, WHITE)
        polygon(blade, BLACK)

def create_windmill_blade(cx, cy, angle):
    # Create rotated blade
    blade_points = [
        (cx - 5, cy),
        (cx + 5, cy),
        (cx + 3, cy - 40),
        (cx - 3, cy - 40)
    ]
    return rotate(blade_points, angle, cx, cy)

def draw_car(x, y, sun_x, sun_y, is_day):
    # Calculate shadow based on sun position
    if is_day:
        # Shadow direction and length based on sun position
        shadow_offset_x = (x + 40 - sun_x) * 0.3
        shadow_offset_y = 15
        
        # Draw shadow (skewed ellipse)
        shadow_points = [
            (x + shadow_offset_x, y + 20 + shadow_offset_y),
            (x + 80 + shadow_offset_x, y + 20 + shadow_offset_y),
            (x + 85 + shadow_offset_x, y + 25 + shadow_offset_y),
            (x - 5 + shadow_offset_x, y + 25 + shadow_offset_y)
        ]
        filled_polygon(shadow_points, (50, 50, 50, 100))  # Semi-transparent shadow
        
        # Draw simple oval shadow
        for i in range(int(shadow_offset_y)):
            alpha = 1 - (i / shadow_offset_y)
            for dx in range(-40, 40):
                if dx * dx / 1600 + i * i / (shadow_offset_y * shadow_offset_y) < 1:
                    shadow_x = int(x + 40 + shadow_offset_x + dx)
                    shadow_y = int(y + 20 + i)
                    if 0 <= shadow_x < WIDTH and 0 <= shadow_y < HEIGHT:
                        plot(shadow_x, shadow_y, (70, 70, 70))
    
    # Badan mobil
    body = [(x, y), (x + 80, y), (x + 80, y + 20), (x, y + 20)]
    filled_polygon(body, RED)
    polygon(body, BLACK)
    
    # Atap mobil
    roof = [(x + 15, y - 20), (x + 55, y - 20), (x + 65, y), (x + 10, y)]
    filled_polygon(roof, DARK_GRAY)
    polygon(roof, BLACK)
    
    # Roda
    filled_circle(x + 20, y + 25, 8, BLACK)
    filled_circle(x + 20, y + 25, 5, GRAY)
    filled_circle(x + 60, y + 25, 8, BLACK)
    filled_circle(x + 60, y + 25, 5, GRAY)

# =========================
# SCENE MANAGER
# =========================
def draw_scene(time, clouds, stars, birds, car_x, windmill, flowers):
    # Sky gradient based on time
    time_factor = (math.sin(time / 100) + 1) / 2
    
    if time_factor > 0.5:  # Day
        sky_color = SKY_BLUE
        is_day = True
    else:  # Night
        r = int(25 + (SKY_BLUE[0] - 25) * time_factor * 2)
        g = int(25 + (SKY_BLUE[1] - 25) * time_factor * 2)
        b = int(112 + (SKY_BLUE[2] - 112) * time_factor * 2)
        sky_color = (r, g, b)
        is_day = False
    
    screen.fill(sky_color)
    
    # Stars at night
    if not is_day:
        for star in stars:
            star.draw()
    
    # Clouds during day
    if is_day:
        for cloud in clouds:
            cloud.draw()
            cloud.update()
    
    # Sun/Moon
    celestial_x = 100 + time_factor * 700
    celestial_y = 100 + abs(math.sin(time / 100)) * 50
    
    if is_day:
        draw_sun(celestial_x, celestial_y, time_factor)
    else:
        draw_moon(celestial_x, celestial_y)
    
    # Birds
    if is_day:
        for bird in birds:
            bird.draw()
            bird.update()
    
    # Ground
    ground = [(0, 450), (WIDTH, 450), (WIDTH, HEIGHT), (0, HEIGHT)]
    filled_polygon(ground, GREEN)
    
    # Road
    road = [(0, 480), (WIDTH, 480), (WIDTH, 530), (0, 530)]
    filled_polygon(road, DARK_GRAY)
    polygon(road, BLACK)
    
    # Road markings
    for i in range(0, WIDTH, 40):
        line_dda(i, 505, i + 20, 505, WHITE)
    
    # Flowers (with scaling)
    for flower in flowers:
        flower.draw()
    
    # Trees (multiple)
    draw_tree(150, 450)
    draw_tree(750, 450)
    
    # Windmill with rotation
    windmill.draw()
    windmill.update()
    
    # House
    draw_house(300, 350)
    
    # Moving car with shadow
    draw_car(car_x, 485, celestial_x, celestial_y, is_day)
    
    # UI Info
    font = pygame.font.Font(None, 24)
    time_text = "DAY" if is_day else "NIGHT"
    text = font.render(f"Time: {time_text} | FPS: {int(clock.get_fps())} | Click flowers to scale!", True, BLACK if is_day else WHITE)
    screen.blit(text, (10, 10))

# =========================
# LOOP UTAMA
# =========================
time = 0
car_x = -100

# Initialize objects
clouds = [Cloud(100, 80, 0.5), Cloud(400, 120, 0.3), Cloud(700, 60, 0.7)]
stars = [Star() for _ in range(50)]
birds = [Bird(-20, 80), Bird(-100, 120), Bird(-180, 100)]
windmill = Windmill(600, 450)
flowers = [
    Flower(50, 475, PINK),
    Flower(200, 475, RED),
    Flower(350, 475, PINK),
    Flower(500, 475, RED),
    Flower(650, 475, PINK)
]

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Check if any flower is clicked
            mouse_x, mouse_y = pygame.mouse.get_pos()
            clicked = False
            for flower in flowers:
                if flower.check_click(mouse_x, mouse_y):
                    clicked = True
                    break
        elif event.type == pygame.MOUSEBUTTONUP:
            # Reset all flowers when mouse released
            for flower in flowers:
                flower.reset_click()
    
    # Update time
    time += 1
    
    # Update car position
    car_x += 2
    if car_x > WIDTH:
        car_x = -100
    
    # Draw scene
    draw_scene(time, clouds, stars, birds, car_x, windmill, flowers)
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
import pygame
import random

def load_scaled_image(image_path, scale_factor):
    image = pygame.image.load(image_path)
    width = int(image.get_width() * scale_factor)
    height = int(image.get_height() * scale_factor)
    return pygame.transform.scale(image, (width, height))

# Инициализация Pygame
pygame.init()

# Настройки экрана
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))

# Заголовок и иконка
pygame.display.set_caption("Космический шутер")

# Цвета
black = (0, 0, 0)
white = (255, 255, 255)

# Классы кораблей
class Spaceship:
    def __init__(self, x, y, image_path, scale_factor=0.05):
        self.x = x
        self.y = y
        self.image = load_scaled_image(image_path, scale_factor)
        self.attack = 100
        self.shield = 100
        self.weapon_type = 'rocket'
        self.health = 100

    def draw(self, surface):
        surface.blit(self.image, (self.x, self.y))

    def fire(self):
        pass

class Star:
    def __init__(self, x, y, speed):
        self.x = x
        self.y = y
        self.speed = speed

    def update(self):
        self.y += self.speed
    def draw(self, surface):
        pygame.draw.circle(surface, white, (self.x, self.y), 1)

class Meteor:
    def __init__(self):
        self.size = random.randint(10, 15)
        self.x = random.randint(0, screen_width)
        self.y = 0  # Метеориты появляются в верхней части экрана
        self.speed = random.randint(5, 15)
        self.durability = random.randint(1, 100)

    def update(self):
        self.y += self.speed

    def draw(self, surface):
        pygame.draw.circle(surface, (139, 69, 19), (self.x, self.y), self.size)

# Инициализация корабля игрока
player = Spaceship(400, 500, "images/player.png")

# Инициализация метеоритов
meteors = []
for _ in range(5):  # Ограничение по количеству метеоритов на экране
    meteors.append(Meteor())

# Инициализация Звезды
stars = []
for _ in range(100):
    x = random.randint(0, screen_width)
    y = random.randint(0, screen_height)
    speed = random.randint(1, 10)
    stars.append(Star(x, y, speed))

frameCounter = 0
frameStep = 60 # Скорость звезды

# Главный игровой цикл
running = True
while running:
    screen.fill(black)  # Очистка экрана
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.fire()

    for star in stars:
        if frameCounter == frameStep:
            star.update()
        star.draw(screen)
        # Перезапуск звезд, если они ушли за пределы экрана
        if star.y > screen_height:
            star.y = 0
            star.x = random.randint(0, screen_width)

    for meteor in meteors:
        if frameCounter == frameStep:
            meteor.update()
        meteor.draw(screen)
        if meteor.y > screen_height:
            meteors.remove(meteor)

    if frameCounter >= frameStep:
        frameCounter = 0  # Сброс frameCounter
    # Движение и отрисовка всех объектов
    player.draw(screen)
    pygame.display.update()  # Обновление экрана
    frameCounter += 1

pygame.quit()
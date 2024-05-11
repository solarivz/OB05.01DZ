import pygame
import random
import time

# Функция масштабирования изображений игровых обектов
def load_scaled_image(image_path, scale_factor):
    image = pygame.image.load(image_path)
    width = int(image.get_width() * scale_factor)
    height = int(image.get_height() * scale_factor)
    return pygame.transform.scale(image, (width, height))

# Настройки экрана
screen_width = 800
screen_height = 600
FPS = 30 # частота кадров в секунду

# Инициализация Pygame
pygame.init()
# Инициализация звука
pygame.mixer.init()

# Вывод или инициализация(поготовка?) на дисплей окна и заголовка
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Космический шутер")

clock = pygame.time.Clock()

# Цвета
black = (0, 0, 0)
white = (255, 255, 255)

# Классы кораблей
class Spaceship:
    def __init__(self, x, y, image_path):
        self.x = x
        self.y = y
        self.scale_factor = 0.3
        self.image = load_scaled_image(image_path, self.scale_factor)
        self.attack = 100
        self.shield = 100
        self.health = 100
        self.rect = self.image.get_rect(center=(x, y))
        self.bullets = []

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def move(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy

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
    def __init__(self, x, y, speed, image_path_meteor):
        self.x = x
        self.y = y # Метеориты появляются в верхней части экрана y = 0
        self.size = random.randint(1, 5)
        self.scale_factor = self.size / 50
        self.image = load_scaled_image(image_path_meteor, self.scale_factor)
        self.health = (random.randint(10, 100))
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = speed
        self.speed = random.randint(1, 10)
        self.durability = (random.randint(50, 100)) * self.scale_factor

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def update(self):
        self.rect.y += self.speed

# Инициализация корабля игрока
player = Spaceship(400, 500, "images/player.png")

# Инициализация метеоритов
meteors = []

for _ in range(6):  # Ограничение по количеству метеоритов на экране
    x = random.randint(15, screen_width - 15)
    speed = random.randint(1, 5)
    meteors.append(Meteor(x, 0, speed, "images/meteor.png"))
next_meteor_time = time.time()
random_interval = random.randint(1, 5)

# Инициализация Звезды
stars = []
for _ in range(100):
    x = random.randint(0, screen_width)
    y = random.randint(0, screen_height)
    speed = random.randint(1, 10)
    stars.append(Star(x, y, speed))

frameCounter = 0
frameStep = 0 # Скорость звезды

# Главный игровой цикл
running = True
start_time = time.time()  # Записываем время начала игры
while running:
    elapsed_time = time.time() - start_time  # Считаем прошедшее время
    seconds = int(elapsed_time)  # Преобразуем время в целое количество секунд

    clock.tick(FPS)
    screen.fill(black)  # Очистка экрана

    current_time = time.time()
    if len(meteors) < 1 and current_time > next_meteor_time:
        x = random.randint(15, screen_width - 15)
        speed = random.randint(1, 5)
        meteors.append(Meteor(x, 0, speed, "images/meteor.png"))

        next_meteor_time = current_time + random_interval
        random_interval = 10 if random_interval != 10 else random.randint(5, 10)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pressed_keys = pygame.key.get_pressed()
    if pressed_keys[pygame.K_LEFT] and player.rect.x > 0:
        player.move(-10, 0)
    if pressed_keys[pygame.K_RIGHT] and player.rect.x < screen_width - 70:
        player.move(10, 0)
    if pressed_keys[pygame.K_UP] and player.rect.y > 0:
        player.move(0, -10)
    if pressed_keys[pygame.K_DOWN] and player.rect.y < screen_height - 90:
        player.move(0, 10)

    # Обработка движения звезд
    for star in stars:
        if frameCounter == frameStep:
            star.update()
        star.draw(screen)
        # Перезапуск звезд, если они ушли за пределы экрана
        if star.y > screen_height:
            star.y = 0
            star.x = random.randint(0, screen_width)

    # Работа frameCounter (звезды и метеориты)
    if frameCounter == frameStep:
        frameCounter = 0
    else:
        frameCounter += 1

    for meteor in meteors:
        meteor.update()
        meteor.draw(screen)
        if meteor.rect.colliderect(pygame.Rect(0, screen_height, screen_width, 1)):
            meteors.remove(meteor)

    # Движение и отрисовка всех объектов
    player.draw(screen)
    # Выводим время на экран
    font = pygame.font.Font(None, 36)
    text = font.render("Time: " + str(seconds), True, white)
    screen.blit(text, (10, 10))
    pygame.display.update()  # Обновление экрана

pygame.quit()

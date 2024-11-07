import pygame
import random

# Инициализация Pygame
pygame.init()

# Настройка экрана
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Space Shooter")

# Цвета
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

# Частота кадров
FPS = 60
clock = pygame.time.Clock()

# Шрифт для отображения текста
font_name = pygame.font.match_font('arial')
def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)

# Функция экрана инструкции
def show_instructions():
    screen.fill(BLACK)
    draw_text(screen, "Space Shooter", 64, width // 2, height // 4)
    draw_text(screen, "Управление:", 32, width // 2, height // 2 - 50)
    draw_text(screen, "Стрелки влево и вправо - перемещение", 24, width // 2, height // 2)
    draw_text(screen, "Пробел - стрельба", 24, width // 2, height // 2 + 30)
    draw_text(screen, "Нажмите любую клавишу, чтобы начать игру", 18, width // 2, height * 3 // 4)
    pygame.display.flip()
    
    # Ожидание нажатия клавиши для старта игры
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False  # Выход из игры
            elif event.type == pygame.KEYUP:
                waiting = False  # Начинаем игру
    return True  # Переход к игровой логике

# Функция экрана окончания игры
def game_over_screen():
    global high_score
    # Обновляем максимальный рекорд, если текущий счёт больше
    if score > high_score:
        high_score = score

    screen.fill(BLACK)
    draw_text(screen, "GAME OVER", 64, width // 2, height // 4)
    draw_text(screen, f"Score: {score}", 24, width // 2, height // 2)
    draw_text(screen, f"High Score: {high_score}", 24, width // 2, height // 2 + 40)
    draw_text(screen, "Press any key to play again", 18, width // 2, height * 3 // 4)
    pygame.display.flip()
    
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False  # Выход из игры
            elif event.type == pygame.KEYUP:
                waiting = False  # Перезапуск игры
    return True  # Перезапуск игры

# Загрузка изображений
player_image = pygame.image.load("spaceship.png")  # Замените на путь к вашему изображению
player_image = pygame.transform.scale(player_image, (50, 50))  # Изменяем размер

enemy_image = pygame.Surface((40, 30))  # Прямоугольник для врагов
enemy_image.fill(RED)

bullet_image = pygame.Surface((10, 20))  # Прямоугольник для снарядов
bullet_image.fill(YELLOW)

# Класс игрока
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = player_image
        self.rect = self.image.get_rect()
        self.rect.centerx = width // 2
        self.rect.bottom = height - 10
        self.speed_x = 0
        self.health = 3  # Количество жизней
        self.shoot_delay = 250  # Задержка между выстрелами (в миллисекундах)
        self.last_shot_time = pygame.time.get_ticks()  # Время последнего выстрела

    def update(self):
        # Обработка движения
        self.speed_x = 0
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.speed_x = -5
        if keys[pygame.K_RIGHT]:
            self.speed_x = 5

        # Обновляем позицию игрока
        self.rect.x += self.speed_x

        # Ограничиваем движение игрока рамками экрана
        if self.rect.right > width:
            self.rect.right = width
        if self.rect.left < 0:
            self.rect.left = 0

        # Автоматическая стрельба при удержании пробела
        if keys[pygame.K_SPACE]:
            self.shoot()

    def shoot(self):
        # Проверяем, прошло ли достаточно времени с момента последнего выстрела
        current_time = pygame.time.get_ticks()
        if current_time - self.last_shot_time > self.shoot_delay:
            self.last_shot_time = current_time
            bullet = Bullet(self.rect.centerx, self.rect.top)
            all_sprites.add(bullet)
            bullets.add(bullet)

# Класс врага
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = enemy_image
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, width - self.rect.width)
        self.rect.y = random.randint(-100, -40)
        self.speed_y = random.randint(1, 5)

    def update(self):
        self.rect.y += self.speed_y
        if self.rect.top > height:
            self.rect.x = random.randint(0, width - self.rect.width)
            self.rect.y = random.randint(-100, -40)
            self.speed_y = random.randint(1, 5)

# Класс снаряда
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = bullet_image
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speed_y = -10  # Снаряд летит вверх

    def update(self):
        self.rect.y += self.speed_y
        if self.rect.bottom < 0:
            self.kill()

# Функция для перезапуска игры
def new_game():
    global all_sprites, enemies, bullets, player, score, last_score_update
    all_sprites = pygame.sprite.Group()
    enemies = pygame.sprite.Group()
    bullets = pygame.sprite.Group()

    player = Player()
    all_sprites.add(player)

    for i in range(8):
        enemy = Enemy()
        all_sprites.add(enemy)
        enemies.add(enemy)

    score = 0
    last_score_update = pygame.time.get_ticks()

# Основной игровой цикл
high_score = 0  # Переменная для хранения максимального рекорда
game_over = False
show_instructions()  # Показ инструкции перед началом игры
new_game()

while True:
    if game_over:
        if not game_over_screen():
            break  # Выход из игры, если игрок закрыл окно
        new_game()
        game_over = False

    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True

    all_sprites.update()

    # Каждую секунду добавляем 2 очка
    current_time = pygame.time.get_ticks()
    if current_time - last_score_update >= 400:  # 1 секунда = 1000 мс
        score += 1
        last_score_update = current_time

    # Проверка столкновений снарядов и врагов
    hits = pygame.sprite.groupcollide(enemies, bullets, True, True)
    for hit in hits:
        score += 10
        enemy = Enemy()
        all_sprites.add(enemy)
        enemies.add(enemy)

    # Проверка столкновений игрока и врагов
    hits = pygame.sprite.spritecollide(player, enemies, True)
    for hit in hits:
        player.health -= 1
        if player.health <= 0:
            game_over = True

    # Отрисовка на экране
    screen.fill(BLACK)
    all_sprites.draw(screen)

    # Отображение текста (очки, жизни)
    draw_text(screen, f"Score: {score}", 18, width // 2, 10)
    draw_text(screen, f"Lives: {player.health}", 18, width - 100, 10)

    pygame.display.flip()

pygame.quit()

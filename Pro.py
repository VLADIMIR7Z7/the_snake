import pygame
import random

# Константы
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
CELL_SIZE = 20
FPS = 10

# Цвета
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
DARK_GREEN = (0, 128, 0)  # Цвет контуров сегментов змейки
RED = (255, 0, 0)
BLUE = (0, 0, 255)  # Цвет головы змейки
WHITE = (255, 255, 255)  # Цвет текста

class GameObject:
    """Базовый класс для всех игровых объектов."""
    
    def __init__(self, position):
        self.position = position

    def draw(self, surface):
        """Метод для отрисовки объекта на экране."""
        pass

class Apple(GameObject):
    """Класс, представляющий яблоко."""
    
    def __init__(self):
        self.body_color = RED
        self.randomize_position()

    def randomize_position(self):
        """Устанавливает случайное положение яблока на игровом поле."""
        self.position = (random.randint(0, (SCREEN_WIDTH // CELL_SIZE) - 1) * CELL_SIZE,
                         random.randint(0, (SCREEN_HEIGHT // CELL_SIZE) - 1) * CELL_SIZE)

    def draw(self, surface):
        """Отрисовывает яблоко на игровом поле."""
        pygame.draw.rect(surface, self.body_color, (self.position[0], self.position[1], CELL_SIZE, CELL_SIZE))

class Snake(GameObject):
    """Класс, представляющий змейку."""
    
    def __init__(self):
        self.body_color = GREEN
        self.head_color = BLUE  # Цвет головы змейки
        self.length = 15  # Начальная длина змейки
        self.positions = [(CELL_SIZE * i, CELL_SIZE) for i in range(self.length)]  # Начальная позиция
        self.direction = (CELL_SIZE, 0)  # Движение вправо
        self.next_direction = None

    def update_direction(self, new_direction):
        """Обновляет направление движения змейки."""
        if (new_direction[0] * -1, new_direction[1] * -1) != self.direction:
            self.next_direction = new_direction

    def move(self):
        """Обновляет позицию змейки."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

        new_head = (self.positions[0][0] + self.direction[0], self.positions[0][1] + self.direction[1])
        
        # Обработка границ
        new_head = (new_head[0] % SCREEN_WIDTH, new_head[1] % SCREEN_HEIGHT)
        
        if new_head in self.positions[1:]:
            self.reset()
            return False  # Возвращаем False, если произошла столкновение

        self.positions.insert(0, new_head)

        if len(self.positions) > self.length:
            self.positions.pop()

        return True  # Возвращаем True, если движение прошло успешно

    def draw(self, surface):
        """Отрисовывает змейку на игровом поле."""
        for i, pos in enumerate(self.positions):
            if i == 0:  # Голова змейки
                pygame.draw.rect(surface, self.head_color, (pos[0], pos[1], CELL_SIZE, CELL_SIZE))
            else:  # Остальные сегменты змейки
                pygame.draw.rect(surface, self.body_color, (pos[0], pos[1], CELL_SIZE, CELL_SIZE))
                pygame.draw.rect(surface, DARK_GREEN, (pos[0], pos[1], CELL_SIZE, CELL_SIZE), 1)

    def get_head_position(self):
        """Возвращает позицию головы змейки."""
        return self.positions[0]

    def reset(self):
        """Сбрасывает змейку в начальное состояние."""
        self.length = 15
        self.positions = [(CELL_SIZE * i, CELL_SIZE) for i in range(self.length)]
        self.direction = (CELL_SIZE, 0)

def handle_keys(snake):
    """Обрабатывает нажатия клавиш для управления змейкой."""
    for event in pygame.event.get ():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                snake.update_direction((0, -CELL_SIZE))
            elif event.key == pygame.K_DOWN:
                snake.update_direction((0, CELL_SIZE))
            elif event.key == pygame.K_LEFT:
                snake.update_direction((-CELL_SIZE, 0))
            elif event.key == pygame.K_RIGHT:
                snake.update_direction((CELL_SIZE, 0))
            elif event.key == pygame.K_ESCAPE:  # Выход из игры
                pygame.quit()
                exit()

def main():
    """Основной игровой цикл."""
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Изгиб Питона")
    clock = pygame.time.Clock()
    
    # Инициализация шрифта
    font = pygame.font.Font(None, 36)
    score = 0  # Переменная для хранения счета

    snake = Snake()
    apple = Apple()

    while True:
        handle_keys(snake)
        if not snake.move():  # Проверяем, произошло ли столкновение
            score = 0  # Обнуляем счет при столкновении
            apple.randomize_position()  # Перемещаем яблоко

        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position()
            score += 1  # Увеличиваем счет при поедании яблока

        screen.fill(BLACK)
        snake.draw(screen)
        apple.draw(screen)

        # Отрисовка счета
        score_text = font.render(f"Счет: {score}", True, WHITE)
        screen.blit(score_text, (SCREEN_WIDTH - 150, 10))  # Позиция текста в правом верхнем углу

        pygame.display.update()
        clock.tick(FPS)

if __name__ == "__main__":
    main()
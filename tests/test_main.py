import pygame
import random
from pygame.time import Clock

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвета
BOARD_BACKGROUND_COLOR = (0, 0, 0)
BORDER_COLOR = (93, 216, 228)
APPLE_COLOR = (255, 0, 0)
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 10

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
pygame.display.set_caption('Змейка')
clock = pygame.time.Clock()


class GameObject:
    """
    Базовый класс для всех игровых объектов.
    """

    def __init__(self, position=(0, 0)):
        self.position = position

    def draw(self, surface):
        """
        Метод для отрисовки объекта на экране.
        """
        pass


class Apple(GameObject):
    """
    Класс, представляющий яблоко.
    """

    def __init__(self):
        super().__init__(self.randomize_position())

    def randomize_position(self):
        """
        Устанавливает случайное положение яблока на игровом поле.
        """
        self.position = (
            random.randint(0, GRID_WIDTH - 1) * GRID_SIZE,
            random.randint(0, GRID_HEIGHT - 1) * GRID_SIZE
        )
        return self.position

    def draw(self, surface):
        """
        Отрисовывает яблоко на игровом поле.
        """
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(surface, APPLE_COLOR, rect)
        pygame.draw.rect(surface, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """
    Класс, представляющий змейку.
    """

    def __init__(self):
        self.body_color = SNAKE_COLOR
        self.length = 1
        self.positions = [(GRID_SIZE * 5, GRID_SIZE * 5)]
        self.direction = RIGHT
        self.next_direction = None

    def update_direction(self, new_direction):
        """
        Обновляет направление движения змейки.
        """
        if (new_direction[0] * -1, new_direction[1] * -1) != self.direction:
            self.next_direction = new_direction

    def move(self):
        """
        Обновляет позицию змейки.
        """
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

        new_head = (self.positions[0][0] + self.direction[0] * GRID_SIZE,
                    self.positions[0][1] + self.direction[1] * GRID_SIZE)

        new_head = (new_head[0] % SCREEN_WIDTH, new_head[1] % SCREEN_HEIGHT)

        if new_head in self.positions:
            self.reset()
            return False

        self.positions.insert(0, new_head)

        if len(self.positions) > self.length:
            self.positions.pop()

        return True

    def draw(self, surface):
        """
        Отрисовывает змейку на игровом поле.
        """
        for pos in self.positions:
            rect = pygame.Rect(pos, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(surface, self.body_color, rect)
            pygame.draw.rect(surface, BORDER_COLOR, rect, 1)

    def reset(self):
        """
        Сбрасывает змейку в начальное состояние.
        """
        self.length = 1
        self.positions = [(GRID_SIZE * 5, GRID_SIZE * 5)]
        self.direction = RIGHT

    def get_head_position(self):
        """
        Возвращает позицию головы змейки.
        """
        return self.positions[0]


def handle_keys(snake):
    """
    Обрабатывает нажатия клавиш для управления змейкой.
    """
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                snake.update_direction(UP)
            elif event.key == pygame.K_DOWN:
                snake.update_direction(DOWN)
            elif event.key == pygame.K_LEFT:
                snake.update_direction(LEFT)
            elif event.key == pygame.K_RIGHT:
                snake.update_direction(RIGHT)
            elif event.key == pygame.K_ESCAPE:
                pygame.quit()
                exit()


def main():
    """
    Основной игровой цикл.
    """
    pygame.init()
    apple = Apple()
    snake = Snake()

    while True:
        clock.tick(SPEED)
        handle_keys(snake)

        if not snake.move():
            apple.randomize_position()

        if snake.positions[0] == apple.position:
            snake.length += 1
            apple.randomize_position()

        screen.fill(BOARD_BACKGROUND_COLOR)
        snake.draw(screen)
        apple.draw(screen)

        pygame.display.update()


if __name__ == '__main__':
    main()

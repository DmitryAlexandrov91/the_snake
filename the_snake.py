from random import choice, randint
import pygame as pg

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

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Цвет камня
STONE_COLOR = (140, 134, 111)

# Скорость движения змейки:
SPEED = 10

# Настройка игрового окна:
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pg.display.set_caption('Змейка')

# Настройка времени:
clock = pg.time.Clock()


class GameObject:
    """Родительский класс, шаблон игрового объекта."""

    def __init__(self,
                 body_color=SNAKE_COLOR):
        """Инициализатор игрового шаблона."""
        self.body_color = body_color  # Цвет игрового элемента.
        self.position = (
            (SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2)
        )  # Позиция на экране, по умолчанию центр.

    def draw(self):
        """Будет переопределён в дочерних классах."""
        pass

    def draw_cell(self, position, body_color):
        """Убирает повторы кода в отрисовке объектов."""
        rect = pg.Rect(position, (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, body_color, rect)
        pg.draw.rect(screen, BORDER_COLOR, rect, 1)

    def randomize_position(self, *positions):
        """Задаёт рандомные координаты игрового объекта."""
        while True:
            position = (
                randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                randint(0, GRID_HEIGHT - 1) * GRID_SIZE
            )
            if position not in positions:
                self.position = position
                break


class Apple(GameObject):
    """Игровой объект яблоко."""

    def __init__(self,
                 body_color=APPLE_COLOR):
        """Инициализатор класса Apple."""
        super().__init__(body_color)
        #  Координаты генерятся в main().

    def draw(self):
        """Отрисовывает яблоко на игровом поле."""
        self.draw_cell(self.position, self.body_color)


class Stone(GameObject):
    """Игровой объект камень.

    Условия появления в цикле игры.
    """

    def __init__(self,
                 body_color=STONE_COLOR, position=None, value=0):
        """Инициализатор камня."""
        super().__init__(body_color)
        self.position = position
        self.value = value

    def draw(self):
        """Отрисовывает камень на игровом поле."""
        self.draw_cell(self.position, self.body_color)


class Snake(GameObject):
    """Игровой объект змейка."""

    def __init__(self,
                 body_color=SNAKE_COLOR):
        """Инициализатор класа Snake.

        Змейка всегда начинает движение в разном направлении.
        """
        super().__init__(body_color)
        self.reset()  # Метод выступает в роли инициализатора.

    def update_direction(self):
        """Обновление направления движения змейки."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def reset(self):
        """Рестарт игры, в случае если змейка съест сама себя.

        Или вляпается в камень.
        Также используется в инициализаторе класса.
        """
        screen.fill(BOARD_BACKGROUND_COLOR)
        self.length = 1
        self.position = (
            (SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2)
        )
        self.positions = [(self.position)]
        directions = (UP, DOWN, LEFT, RIGHT)
        self.direction = choice(directions)
        self.next_direction = None
        self.last = None

    def move(self):
        """Метод, отвечающий за движение змейки."""
        head_position = self.get_head_position()
        self.position = (
            (head_position[0] + self.direction[0] * GRID_SIZE) % SCREEN_WIDTH,
            (head_position[1] + self.direction[1] * GRID_SIZE) % SCREEN_HEIGHT
        )
        #  Проверяем, столкнулась ли змейка сама с собой
        if head_position in self.positions[1:-1]:
            self.reset()
        #  Проверяем, превышает ли длина змейки максимально допустимую длину.
        if len(self.positions) >= self.length:
            #  Создаём атрибут last для затирки последнего сегмента.
            self.last = self.positions[-1]
            #  Удаляем последний элемент змеи.
            self.positions.pop()
        self.positions.insert(0, self.position)

    def get_head_position(self):
        """Возвращает координаты головы змеи."""
        return self.positions[0]

    def draw(self):
        """Отрисовка змейки на игровом поле."""
        for position in self.positions[:-1]:
            self.draw_cell(self.position, self.body_color)
        # Отрисовка головы змейки
        self.draw_cell(self.get_head_position(), self.body_color)
        # Затирание последнего сегмента
        if self.last:
            last_rect = pg.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pg.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)


def handle_keys(game_object):
    """Задаёт направление движение змеи нажатиями клавиш."""
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            raise SystemExit
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pg.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pg.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pg.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def main():
    """Запускаем игру."""
    pg.init()
    apple = Apple()
    snake = Snake()
    stone = Stone()
    apple.randomize_position(snake.position)

    while True:  # Основной игровой цикл.
        clock.tick(SPEED)
        handle_keys(snake)
        snake.update_direction()
        snake.move()
        snake.draw()
        apple.draw()
        if snake.position == apple.position:  # Проверка, съела ли змея яблоко.
            #  Генерим новые координаты яблока.
            apple.randomize_position(snake.positions, stone.position)
            snake.length += 1
            snake.draw()
            apple.draw()
        #  Если змея врезается в камень.
        if snake.position == stone.position:
            snake.reset()
            stone.value = 0
        #   Условие, при котором появляется камень.
        if snake.length >= 10 and stone.value != 1:
            stone.value = 1
            #  Генерим координаты камня.
            stone.randomize_position(apple.position, snake.positions)
            stone.draw()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                break
        pg.display.update()


if __name__ == '__main__':
    main()

import pygame # ЕСЛИ КОД НЕ ГРУЗИТСЯ ВЫДАЕТ ОШИБКУ УСТАНОВИТЕ БИБЛИОТЕКУ "pygame" "datetime"
import datetime # ЕСЛИ КОД НЕ ГРУЗИТСЯ ВЫДАЕТ ОШИБКУ УСТАНОВИТЕ БИБЛИОТЕКУ "pygame" "datetime"
import sys

# Инициализация Pygame
pygame.init()

# Настройки дисплея
WIDTH, HEIGHT = 1920, 1080
DISPLAYSURF = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Самолётик')

# Цвета
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
# ------------------- ФОРМА "ОСНОВНАЯ" --------------------------
BACKGROUND_IMAGE_PATH = 'background.jpg'
BACKGROUND = pygame.image.load(BACKGROUND_IMAGE_PATH)
BACKGROUND = pygame.transform.scale(BACKGROUND, (WIDTH, HEIGHT))
# ------------------- ФОРМА "ОБ ИГРЕ" --------------------------
INFO_BACKGROUND_IMAGE_PATH = 'space_background.jpg'
info_background = pygame.image.load(INFO_BACKGROUND_IMAGE_PATH)
info_background = pygame.transform.scale(info_background, (WIDTH, HEIGHT))

# Скорость самолёта (точки)
SPEED = 5

# Флаги состояния игры
game_started = False
game_paused = False
show_info_screen = False

# Эталонная траектория и границы
REF_LINE_Y = HEIGHT // 1.39 # НАСТРОЙКА ПОЛОСЫ ЗЕЛЁНОЙ ТРАЕКТОРИИ / UPDATE CODE
BOUNDARY_OFFSET = 53 # НАСТРОЙКА ПОЛОСЫ СЕРОЙ ТРАЕКТОРИИ / UPDATE CODE
HEADER_HEIGHT = 78

# Функция отображения заголовка и авторства
def draw_header():
    DISPLAYSURF.fill(BLACK, (0, 0, WIDTH, HEADER_HEIGHT))
    font = pygame.font.SysFont('Arial', 24)
    title_surf = font.render('Самолётик - Игра про посадку самолёта', True, WHITE)
    author_surf = font.render('Разработано: Татьяной', True, WHITE)
    DISPLAYSURF.blit(title_surf, (WIDTH // 2 - title_surf.get_width() // 2, 10))
    DISPLAYSURF.blit(author_surf, (WIDTH // 2 - author_surf.get_width() // 2, 40))

def draw_datetime():
    now = datetime.datetime.now()
    date_time_string = now.strftime("%Y-%m-%d %H:%M:%S")
    font = pygame.font.SysFont('Arial', 17)
    date_time_surf = font.render(date_time_string, True, WHITE)
    # Позиционирование в правом верхнем углу
    date_time_position = (WIDTH - date_time_surf.get_width() - 1400, 24)
    DISPLAYSURF.blit(date_time_surf, date_time_position)

# Класс кнопки
class Button:
    def __init__(self, text, x, y, action):
        self.text = text
        self.x = x
        self.y = y
        self.action = action
        self.font = pygame.font.SysFont('Arial', 20)
        self.rendered_text = self.font.render(text, True, WHITE)
        self.rect = self.rendered_text.get_rect(topleft=(x, y))
        self.hover = False

    def draw(self):
        button_color = BLACK if not self.hover else (40, 40, 40)
        pygame.draw.rect(DISPLAYSURF, button_color, self.rect)
        DISPLAYSURF.blit(self.rendered_text, self.rect.topleft)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.action()
        elif event.type == pygame.MOUSEMOTION:
            self.hover = self.rect.collidepoint(event.pos)

# Функции для кнопок
def start_game():
    global game_started, game_paused
    game_started = True
    game_paused = False

def pause_game():
    global game_paused
    game_paused = not game_paused

def show_game_info():
    global show_info_screen
    show_info_screen = True

def hide_game_info():
    global show_info_screen
    show_info_screen = False

def erase_path():
    global plane_path, plane_pos
    plane_path = []  # Очищаем трек самолёта
    plane_pos = (WIDTH // 1.4, HEIGHT // 1.39)  # Устанавливаем самолёт в центр экрана !!!КНОПКА СТЕРЕТЬ!!!

def quit_game():  # КНОПКА ВЫХОДА
    pygame.quit()
    sys.exit()

# Создание кнопок
start_button = Button('Старт', 65, 10, start_game)
pause_button = Button('Пауза', 65, 40, pause_game)
info_button = Button('Об игре', WIDTH - 150, 10, show_game_info)
back_button = Button('Назад', WIDTH // 2 - 30, HEIGHT // 2, hide_game_info)
erase_button = Button('Стереть', WIDTH - 150, 40, erase_path)
exit_button = Button('X', WIDTH - 45, 5, quit_game)

# Отрисовка самолёта и его трека
def draw_plane(plane_pos, plane_path):
    for point in plane_path:
        pygame.draw.circle(DISPLAYSURF, RED, point, 3)
    pygame.draw.circle(DISPLAYSURF, YELLOW, plane_pos, 10)

# Отрисовка траектории
def draw_trajectory_lines():
    pygame.draw.line(DISPLAYSURF, GREEN, (0, REF_LINE_Y), (WIDTH, REF_LINE_Y), 2)
    pygame.draw.line(DISPLAYSURF, WHITE, (0, REF_LINE_Y - BOUNDARY_OFFSET), (WIDTH, REF_LINE_Y - BOUNDARY_OFFSET), 1)
    pygame.draw.line(DISPLAYSURF, WHITE, (0, REF_LINE_Y + BOUNDARY_OFFSET), (WIDTH, REF_LINE_Y + BOUNDARY_OFFSET), 1)

# Отображение сообщения о необходимости коррекции траектории
def display_correction_message(message):
    font = pygame.font.SysFont(None, 22)
    text_surface = font.render(message, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.center = (WIDTH // 2, HEIGHT // 11) # НАСТРОЙКА ТЕКСТА ОТОБРАЖЕНИЯ ОТКЛОНЕНИЙ ТРАЕКТОРИИ/ UPDATE CODE
    DISPLAYSURF.blit(text_surface, text_rect)

# Проверка положения самолёта и отображение предупреждений
def check_plane_position(plane_pos):
    deviation = plane_pos[1] - REF_LINE_Y
    if abs(deviation) > BOUNDARY_OFFSET:
        message = 'Отклонение: {} метров'.format(abs(deviation))
        if deviation < 0:
            message += '. Вы поднимайтесь!'
        else:
            message += '. Вы опускайтесь!' # исправленние поправка занчений
        display_correction_message(message)

# Отрисовка экрана информации
def draw_info_screen():
    DISPLAYSURF.blit(info_background, (0, 0))  # Фон экрана информации
    font = pygame.font.SysFont('Arial', 24)
    lines = [
        "Игра 'Самолётик'",
        "Версия 1.0",
        "Дата создания: Ноябрь 2023",
        "Разработчик: Татьяна",
        "Цель игры - управлять самолётом, не выходя за границы траектории."
    ]
    for i, line in enumerate(lines):
        draw_text_with_outline(DISPLAYSURF, line, (WIDTH // 2, 300 + i * 40), font, WHITE, BLACK)
    back_button.draw()
def draw_text_with_outline(surface, text, position, font, color, outline_color):
    text_surface = font.render(text, True, color)
    outline_surface = font.render(text, True, outline_color)

    outline_rect = text_surface.get_rect()
    outline_rect.center = (position[0] + 2, position[1] + 2.1)
    surface.blit(outline_surface, outline_rect)

    text_rect = text_surface.get_rect()
    text_rect.center = position
    surface.blit(text_surface, text_rect)

# Основной цикл приложения
def main():
    global game_started, game_paused, show_info_screen, plane_path, plane_pos
    plane_pos = (WIDTH // 1.4, HEIGHT // 1.39)  # Начальное положение самолёта
    plane_path = []

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit_button.draw()
                sys.exit()
            if not show_info_screen:
                if event.type == pygame.MOUSEMOTION:
                    mouse_x, mouse_y = event.pos
                    if not game_paused and game_started and mouse_y > HEADER_HEIGHT:
                        plane_pos = event.pos
                        plane_path.append(plane_pos)
                start_button.handle_event(event)
                pause_button.handle_event(event)
                info_button.handle_event(event)
                erase_button.handle_event(event)
                exit_button.handle_event(event)
            else:
                back_button.handle_event(event)
                # Обработка событий для кнопки выхода
                exit_button.handle_event(event)

        if not show_info_screen:
            DISPLAYSURF.fill(BLACK)  # Очистка экрана
            DISPLAYSURF.blit(BACKGROUND, (0, 0))
            draw_header()
            start_button.draw()
            pause_button.draw()
            info_button.draw()
            erase_button.draw()
            exit_button.draw()
            draw_datetime()
            if not game_started:
                display_correction_message('Необходимо начать игру!')
            elif game_paused:
                display_correction_message('Игра на паузе!')
            else:
                draw_trajectory_lines()
                draw_plane(plane_pos, plane_path)
                check_plane_position(plane_pos)
        else:
            draw_info_screen()

        pygame.display.update()
        pygame.time.Clock().tick(60) # Настройка фпс / UPDATE CODE

# это основной файл, запускаем игру :D
if __name__ == "__main__":
    main()

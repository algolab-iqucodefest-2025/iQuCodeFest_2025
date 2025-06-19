import pygame
import math
import sys

pygame.init()

# Screen setup
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("QDutch")

FONT = pygame.font.SysFont(None, 40)
clock = pygame.time.Clock()

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
BLUE = (100, 149, 237)
GREEN = (0, 128, 0)

# Game states
MENU = "menu"
SELECT_PLAYERS = "select_players"
ENTER_NAMES = "enter_names"
GAME_STARTED = "game_started"

# Player seat order based on number of players
PLAYER_POSITIONS = {
    2: [0, 2],         # Bottom, Top
    3: [0, 1, 2],      # Bottom, Left, Top
    4: [0, 1, 2, 3]    # Bottom, Left, Top, Right
}

state = MENU
num_players = 0
player_names = []
name_inputs = []
active_input = -1

# Button class
class Button:
    def __init__(self, text, x, y, w, h, callback):
        self.text = text
        self.rect = pygame.Rect(x, y, w, h)
        self.callback = callback

    def draw(self, screen):
        pygame.draw.rect(screen, BLUE, self.rect)
        txt = FONT.render(self.text, True, WHITE)
        screen.blit(txt, (self.rect.x + 10, self.rect.y + 10))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos):
            self.callback()

# Input box class
class InputBox:
    def __init__(self, x, y, w, h, text=''):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = GRAY
        self.text = text
        self.txt_surface = FONT.render(text, True, BLACK)
        self.active = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.active = self.rect.collidepoint(event.pos)
            self.color = BLUE if self.active else GRAY
        if event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            elif event.key == pygame.K_RETURN:
                self.active = False
                self.color = GRAY
            else:
                self.text += event.unicode
            self.txt_surface = FONT.render(self.text, True, BLACK)

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect, 2)
        screen.blit(self.txt_surface, (self.rect.x + 5, self.rect.y + 5))

# Callbacks
def start_game():
    global state
    state = SELECT_PLAYERS

def choose_players(n):
    global num_players, state, name_inputs
    num_players = n
    state = ENTER_NAMES
    name_inputs = [InputBox(300, 150 + i*70, 200, 40) for i in range(num_players)]

def quit_game():
    pygame.quit()
    sys.exit()

def back_to_menu():
    global state
    state = MENU

def back_to_select_players():
    global state
    state = SELECT_PLAYERS

def launch_game():
    global state, player_names
    player_names = [box.text.strip() for box in name_inputs]
    state = GAME_STARTED

def compute_rotated_rects(rects, w, h, rotation, target_x, target_y):
    new_rects = []
    for r in rects:
        cx = r.x + r.w / 2 - w / 2
        cy = r.y + r.h / 2 - h / 2
        angle = math.radians(rotation)
        rx = cx * math.cos(angle) - cy * math.sin(angle)
        ry = cx * math.sin(angle) + cy * math.cos(angle)
        final_x = int(rx + w / 2 + target_x - r.w / 2)
        final_y = int(ry + h / 2 + target_y - r.h / 2)
        new_rects.append(pygame.Rect(final_x, final_y, r.w, r.h))
    return new_rects

# Drawing player area with rotation
def draw_player_area(name, position):
    card_w, card_h = 60, 90
    spacing = 15
    area_w = card_w * 4 + spacing * 3
    area_h = card_h + 40

    player_surface = pygame.Surface((area_w, area_h), pygame.SRCALPHA)
    player_surface.fill((0, 0, 0, 0))

    slot_rects = []
    for i in range(4):
        x = i * (card_w + spacing)
        y = 10
        rect = pygame.Rect(x, y, card_w, card_h)
        pygame.draw.rect(player_surface, GRAY, rect)
        pygame.draw.rect(player_surface, BLACK, rect, 2)
        slot_rects.append(rect)

    name_text = FONT.render(name, True, WHITE)
    player_surface.blit(name_text, ((area_w - name_text.get_width()) // 2, card_h + 15))

    if position == 0:
        screen.blit(player_surface, (WIDTH // 2 - area_w // 2, HEIGHT - area_h))
        base_x = WIDTH // 2 - area_w // 2
        base_y = HEIGHT - area_h
        return [pygame.Rect(base_x + r.x, base_y + r.y, r.w, r.h) for r in slot_rects]
    elif position == 1:
        rotated = pygame.transform.rotate(player_surface, 270)
        screen.blit(rotated, (0, HEIGHT // 2 - rotated.get_height() // 2))
        return compute_rotated_rects(slot_rects, area_w, area_h, rotation=270, target_x=0, target_y=HEIGHT // 2 - rotated.get_height() // 2)
    elif position == 2:
        rotated = pygame.transform.rotate(player_surface, 180)
        screen.blit(rotated, (WIDTH // 2 - rotated.get_width() // 2, 0))
        return compute_rotated_rects(slot_rects, area_w, area_h, rotation=180, target_x=WIDTH // 2 - rotated.get_width() // 2, target_y=0)
    elif position == 3:
        rotated = pygame.transform.rotate(player_surface, 90)
        screen.blit(rotated, (WIDTH - rotated.get_width(), HEIGHT // 2 - rotated.get_height() // 2))
        return compute_rotated_rects(slot_rects, area_w, area_h, rotation=90, target_x=WIDTH - rotated.get_width(), target_y=HEIGHT // 2 - rotated.get_height() // 2)


# Screen drawing
def draw_menu():
    screen.fill(WHITE)
    title = FONT.render("Main Menu", True, BLACK)
    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 50))
    play_button.draw(screen)
    quit_button.draw(screen)

def draw_player_select():
    screen.fill(WHITE)
    title = FONT.render("Select Number of Players", True, BLACK)
    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 50))
    for btn in player_buttons:
        btn.draw(screen)
    back_button_select.draw(screen)

def draw_name_entry():
    screen.fill(WHITE)
    title = FONT.render("Enter Player Names", True, BLACK)
    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 50))
    for box in name_inputs:
        box.draw(screen)
    back_button_names.draw(screen)
    if all(box.text.strip() for box in name_inputs):
        confirm = FONT.render("(Press Enter to continue)", True, GRAY)
        screen.blit(confirm, (WIDTH // 2 - confirm.get_width() // 2, 500))

def draw_game():
    screen.fill(GREEN)
    positions = PLAYER_POSITIONS.get(num_players, [0])
    for i, pos in enumerate(positions):
        draw_player_area(player_names[i], pos)

# Buttons
play_button = Button("Play", WIDTH // 2 - 75, 250, 150, 50, start_game)
quit_button = Button("Quit", WIDTH // 2 - 75, 320, 150, 50, quit_game)
player_buttons = [
    Button("2 Players", 325, 175, 150, 50, lambda: choose_players(2)),
    Button("3 Players", 325, 250, 150, 50, lambda: choose_players(3)),
    Button("4 Players", 325, 325, 150, 50, lambda: choose_players(4)),
]
back_button_select = Button("Back", 50, 50, 100, 40, back_to_menu)
back_button_names = Button("Back", 50, 50, 100, 40, back_to_select_players)

# Main loop
running = True
while running:
    screen.fill(WHITE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif state == MENU:
            play_button.handle_event(event)
            quit_button.handle_event(event)
        elif state == SELECT_PLAYERS:
            for btn in player_buttons:
                btn.handle_event(event)
            back_button_select.handle_event(event)
        elif state == ENTER_NAMES:
            for box in name_inputs:
                box.handle_event(event)
            back_button_names.handle_event(event)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                if all(box.text.strip() for box in name_inputs):
                    launch_game()

    if state == MENU:
        draw_menu()
    elif state == SELECT_PLAYERS:
        draw_player_select()
    elif state == ENTER_NAMES:
        draw_name_entry()
    elif state == GAME_STARTED:
        draw_game()

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()

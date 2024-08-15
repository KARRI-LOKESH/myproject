import pygame
import random

pygame.init()

GRID_SIZE = 4
TILE_SIZE = 100
MARGIN = 10
SCREEN_SIZE = GRID_SIZE * TILE_SIZE + (GRID_SIZE + 1) * MARGIN
FONT_SIZE = 60

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)

WORD_LIST = ["PYTHON", "GAME", "CODE", "HANGMAN", "GRID", "TILES"]

screen = pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE))
pygame.display.set_caption("2048 Hangman")
font = pygame.font.Font(None, FONT_SIZE)
clock = pygame.time.Clock()

def new_tile():
    return random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ")

def draw_grid(grid):
    screen.fill(BLACK)
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            value = grid[row][col]
            rect = pygame.Rect(
                col * TILE_SIZE + (col + 1) * MARGIN,
                row * TILE_SIZE + (row + 1) * MARGIN,
                TILE_SIZE,
                TILE_SIZE,
            )
            pygame.draw.rect(screen, GRAY, rect)
            if value:
                text = font.render(value, True, WHITE)
                screen.blit(
                    text,
                    (
                        rect.centerx - text.get_width() / 2,
                        rect.centery - text.get_height() / 2,
                    ),
                )
    pygame.display.update()

def slide_tiles(grid, direction):
    moved = False
    for _ in range(GRID_SIZE - 1):
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                if direction == "UP" and row > 0:
                    if grid[row - 1][col] == "":
                        grid[row - 1][col], grid[row][col] = grid[row][col], ""
                        moved = True
                elif direction == "DOWN" and row < GRID_SIZE - 1:
                    if grid[row + 1][col] == "":
                        grid[row + 1][col], grid[row][col] = grid[row][col], ""
                        moved = True
                elif direction == "LEFT" and col > 0:
                    if grid[row][col - 1] == "":
                        grid[row][col - 1], grid[row][col] = grid[row][col], ""
                        moved = True
                elif direction == "RIGHT" and col < GRID_SIZE - 1:
                    if grid[row][col + 1] == "":
                        grid[row][col + 1], grid[row][col] = grid[row][col], ""
                        moved = True
    return moved

def check_word(grid, word):
    for row in grid:
        if "".join(row).find(word) != -1:
            return True
    for col in range(GRID_SIZE):
        column = "".join([grid[row][col] for row in range(GRID_SIZE)])
        if column.find(word) != -1:
            return True
    return False

grid = [["" for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
grid[random.randint(0, GRID_SIZE - 1)][random.randint(0, GRID_SIZE - 1)] = new_tile()
target_word = random.choice(WORD_LIST)
game_over = False

while not game_over:
    draw_grid(grid)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True
        elif event.type == pygame.KEYDOWN:
            moved = False
            if event.key == pygame.K_UP:
                moved = slide_tiles(grid, "UP")
            elif event.key == pygame.K_DOWN:
                moved = slide_tiles(grid, "DOWN")
            elif event.key == pygame.K_LEFT:
                moved = slide_tiles(grid, "LEFT")
            elif event.key == pygame.K_RIGHT:
                moved = slide_tiles(grid, "RIGHT")

            if moved:
                empty_tiles = [(r, c) for r in range(GRID_SIZE) for c in range(GRID_SIZE) if grid[r][c] == ""]
                if empty_tiles:
                    row, col = random.choice(empty_tiles)
                    grid[row][col] = new_tile()

            if check_word(grid, target_word):
                print("You found the word:", target_word)
                game_over = True

    clock.tick(10)

pygame.quit()

import pygame
import random
from bot import TetrisBot

screen_width = 400
screen_height = 500
block_size = 20
grid_width = 10
grid_height = 20
white = (255, 255, 255)
black = (0, 0, 0)
paused = False

colors = {
    1: (255, 0, 0),
    2: (0, 255, 0),
    3: (0, 0, 255),
    4: (255, 255, 0),
    5: (255, 165, 0),
    6: (128, 0, 128),
    7: (0, 255, 255)
}

shapes = [
    [[1, 1, 1],
     [0, 1, 0]],
    
    [[0, 2, 2],
     [2, 2, 0]],

    [[3, 3, 0],
     [0, 3, 3]],

    [[4, 0, 0],
     [4, 4, 4]],

    [[0, 0, 5],
     [5, 5, 5]],

    [[6, 6],
     [6, 6]],

    [[7, 7, 7, 7]]
]

pygame.init()
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()
pygame.mixer.music.load('theme1.mid')
pygame.display.set_caption("Tetris - In Game")

def create_shape():
    shape = random.choice(shapes)
    while shape is None or len(shape) == 0:
        shape = random.choice(shapes)
    return shape

def draw_shape(shape, x, y, placed=False):
    if shape is not None:
        for i in range(len(shape)):
            for j in range(len(shape[i])):
                if shape[i][j] != 0:
                    if placed:
                        pygame.draw.rect(screen, colors[shape[i][j]], pygame.Rect((x + j) * block_size, (y + i) * block_size, block_size, block_size))
                    else:
                        pygame.draw.rect(screen, colors[shape[i][j]], pygame.Rect((x + j) * block_size, (y + i) * block_size, block_size, block_size), 1)

def draw_grid(grid):
    border_size = 3
    border_x = -border_size
    border_y = -border_size
    border_width = grid_width * block_size + 2 * border_size
    border_height = grid_height * block_size + 2 * border_size
    pygame.draw.rect(screen, white, pygame.Rect(border_x, border_y, border_width, border_height), border_size)
    for i in range(grid_height):
        for j in range(grid_width):
            if grid[i][j] != 0:
                pygame.draw.rect(screen, colors[grid[i][j]], pygame.Rect(j * block_size, i * block_size, block_size, block_size))


def rotate_shape(shape):
    rotated_shape = [[shape[j][i] for j in range(len(shape))] for i in range(len(shape[0]))]
    rotated_shape = [row[::-1] for row in rotated_shape]
    return rotated_shape

def game_over_screen():
    font = pygame.font.Font(None, 25)
    text = font.render("Game Over. Press SPACE to restart...", True, white)
    text_rect = text.get_rect(center=(screen_width // 2, screen_height - 20))
    pygame.draw.rect(screen, black, (text_rect.x - 10, text_rect.y - 10, text_rect.width + 20, text_rect.height + 20))
    screen.blit(text, text_rect)

def check_loosing_condition(grid,shape,x,y):
    for i in range(len(shape)):
        for j in range (len(shape)):
            if shape[i][j] != 0:
                if y + i < 0:
                    return True
                if grid [y + i][x + j] != 0:
                    return True
    return False

def draw_preview(shape, x, y, grid):
    if shape is not None:
        preview_color = (150, 150, 150)
        preview_alpha = 60
        preview_y = y
        while not check_collision(grid, shape, x, preview_y + 1):
            preview_y += 1
        
        for i in range(len(shape)):
            for j in range(len(shape[i])):
                if shape[i][j] != 0:
                    if y + i < grid_height and (x + j >= 0 and x + j < grid_width) and grid[y + i][x + j] == 0:
                        pygame.draw.rect(screen, (preview_color[0], preview_color[1], preview_color[2], preview_alpha),
                                        pygame.Rect((x + j) * block_size, (preview_y + i) * block_size, block_size, block_size))
                    else:
                        pygame.draw.rect(screen, (colors[shape[i][j]][0], colors[shape[i][j]][1], colors[shape[i][j]][2]),
                                        pygame.Rect((x + j) * block_size, (preview_y + i) * block_size, block_size, block_size))
                    
def read_bot_status():
    try:
        with open("bot_settings.txt", "r") as f:
            bot_status = bool(int(f.readline()))
            return bot_status == True
    except FileNotFoundError:
        return False

def main():
    next_shapes = []
    try:
        with open("volume_settings.txt", "r") as f:
            volume = float(f.readline())
    except FileNotFoundError:
        volume = 0.5
    
    pygame.mixer.music.set_volume(volume)
    running = True
    game_over = False
    grid = [[0] * grid_width for _ in range(grid_height)]
    shape = create_shape()
    if not next_shapes:
        next_shapes = [create_shape() for _ in range(2)]
    x, y = 4, 0
    move_down_time = 0
    placed_instantly = False
    score = 0
    lines_cleared = 0
    level = 1
    speed = 0.5
    bot_enabled = read_bot_status()
    bot = TetrisBot(grid, shape,x,y)
    pygame.mixer.music.play(-1)

    while running:
        if shape is None:
            shape = create_shape()
            if not shape:
                continue

        screen.fill(black)

        if not game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT and not placed_instantly:
                        if not check_collision(grid, shape, x - 1, y):
                            x -= 1
                    elif event.key == pygame.K_RIGHT and not placed_instantly:
                        if not check_collision(grid, shape, x + 1, y):
                            x += 1
                    elif event.key == pygame.K_UP and not placed_instantly:
                        rotated_shape = rotate_shape(shape)
                        if not check_collision(grid, rotated_shape, x, y):
                            shape = rotated_shape
                        elif not check_collision(grid, rotated_shape, x - 1, y):
                            x -= 1
                            shape = rotated_shape
                        elif not check_collision(grid, rotated_shape, x + 1, y):
                            x += 1
                            shape = rotated_shape
                    elif event.key == pygame.K_DOWN and not placed_instantly:
                        rotated_shape = rotate_shape(shape)
                        if not check_collision(grid, shape, x, y + 1):
                            y += 1
                    elif event.key == pygame.K_SPACE:
                        while not check_collision(grid, shape, x, y + 1):
                            y += 1
                        placed_instantly = True
                        

            current_time = pygame.time.get_ticks()
            if current_time - move_down_time > speed * 1000:
                if bot_enabled == True:
                    best_rotation, best_x = bot.find_best_move()
                    shape = best_rotation
                    x = best_x
                else:
                    if not check_collision(grid, shape, x, y + 1):
                        y += 1
                    else:
                        for i in range(len(shape)):
                            for j in range(len(shape[i])):
                                if shape[i][j] != 0:
                                    grid[y + i][x + j] = shape[i][j]
                        lines, multiple_clear = clear_lines(grid)
                        lines_cleared += lines
                        if lines > 0:
                            score += lines * 100
                            if multiple_clear:
                                score += 100 * (2 ** (lines - 1))
                        if lines_cleared >= 10:
                            level += 1
                            lines_cleared -= 10
                            speed *= 0.8
                        shape = next_shapes.pop(0)
                        next_shapes.append(create_shape())
                        x, y = 4, 0
                        placed_instantly = False
                        if check_loosing_condition(grid, shape, x, y):
                            game_over = True
     
                    move_down_time = current_time

        else:
            game_over_screen()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        game_over = False
                        grid = [[0] * grid_width for _ in range(grid_height)]
                        shape = create_shape()
                        next_shapes = [create_shape() for _ in range(2)]
                        x, y = 4, 0
                        move_down_time = 0
                        placed_instantly = False
                        score = 0
                        level = 1
                        speed = 0.5

        draw_grid(grid)
        draw_preview(shape, x, y, grid)
        draw_shape(shape, x, y, placed=False)
        for idx, next_shape in enumerate(next_shapes):
            draw_shape(next_shape, grid_width + 2, 5 + (idx * 8), placed=True)

        draw_score(score)
        draw_level(level)
        pygame.display.flip()
        clock.tick(30)

    pygame.quit()

def check_collision(grid, shape, x, y):
    for i in range(len(shape)):
        for j in range(len(shape[i])):
            if shape[i][j] != 0:
                if (y + i >= len(grid) or x + j < 0 or x + j >= len(grid[0]) or
                        grid[y + i][x + j] != 0):
                    return True
    return False

def clear_lines(grid):
    full_lines = []
    for i in range(len(grid)):
        if all(grid[i]):
            full_lines.append(i)
    for row in full_lines:
        del grid[row]
        grid.insert(0, [0] * grid_width)
    multiple_line_clear = len(full_lines) > 1
    return len(full_lines), multiple_line_clear

def draw_score(score):
    font = pygame.font.Font(None, 25)
    text = font.render(f"Score: {score}", True, white)
    screen.blit(text,(screen_width - text.get_width() - 10, 30))

def draw_level(level):
    font = pygame.font.Font(None, 25)
    text = font.render(f"Level: {level}", True, white)
    screen.blit(text, (screen_width - text.get_width() - 10, 10))

if __name__ == "__main__":
    main()

import pygame
import sys

white = (255,255,255)
black = (0,0,0)

screen_width = 400
screen_height = 500
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()

def main_menu():
    pygame.init()
    pygame.display.set_caption("Tetris - Main Menu")

    font = pygame.font.Font(None, 36)
    start_text = font.render("Start Game", True, white)
    quit_text = font.render("Quit", True, white)
    settings_text = font.render("Settings", True, white)

    start_rect = start_text.get_rect(center=(screen_width // 2, screen_height // 2 - 100))
    settings_rect = settings_text.get_rect(center=(screen_width // 2, screen_height // 2))
    quit_rect = quit_text.get_rect(center=(screen_width // 2, screen_height // 2 + 100))

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if start_rect.collidepoint(event.pos):
                    running = False
                elif settings_rect.collidepoint(event.pos):
                    adjust_settings()
                elif quit_rect.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()
        screen.fill(black)
        screen.blit(start_text, start_rect)
        screen.blit(settings_text, settings_rect)
        screen.blit(quit_text, quit_rect)
        pygame.display.flip()
        clock.tick(30)

    return True

def adjust_settings():
    try:
        with open("volume_settings.txt", "r") as f:
            volume = float(f.readline())
    except FileNotFoundError:
        volume = 0.5

    try:
        with open("bot_settings.txt", "r") as f:
            bot_enabled = bool(int(f.readline()))
    except FileNotFoundError:
        bot_enabled = False
    
    pygame.mixer.music.set_volume(volume)

    slider_width = 200
    slider_height = 20
    slider_x = (screen_width - slider_width) // 2
    slider_y = (screen_height - slider_height) // 2
    slider_handle_width = 10
    slider_handle_height = 30
    slider_handle_x = slider_x + int((pygame.mixer.music.get_volume() * slider_width) - slider_handle_width / 2)
    slider_handle_y = slider_y - (slider_handle_height - slider_height) // 2

    dragging = False

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if pygame.Rect(slider_handle_x, slider_handle_y, slider_handle_width, slider_handle_height).collidepoint(event.pos):
                        dragging = True
                    elif back_button_rect.collidepoint(event.pos):
                        running = False
                    elif bot_toggle_rect.collidepoint(event.pos):
                        bot_enabled = not bot_enabled
                        with open("bot_settings.txt", "w") as f:
                            f.write("1" if bot_enabled else "0")
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    dragging = False
            elif event.type == pygame.MOUSEMOTION:
                if dragging:
                    slider_handle_x = min(max(event.pos[0] - slider_handle_width // 2, slider_x), slider_x + slider_width - slider_handle_width)
                    volume = (slider_handle_x - slider_x) / slider_width
                    pygame.mixer.music.set_volume(volume)

        screen.fill(black)
        pygame.draw.rect(screen, white, pygame.Rect(slider_x, slider_y, slider_width, slider_height))
        pygame.draw.rect(screen, (100, 100, 100), pygame.Rect(slider_handle_x, slider_handle_y, slider_handle_width, slider_handle_height))
        font = pygame.font.Font(None, 36)
        volume_text = font.render(f"Music Volume: {int(pygame.mixer.music.get_volume() * 100)}%", True, white)
        volume_rect = volume_text.get_rect(center=(screen_width // 2, screen_height // 2.5))
        screen.blit(volume_text, volume_rect)
        back_button_text = font.render("Back", True, white)
        back_button_rect = back_button_text.get_rect(center=(screen_width // 2, screen_height - 50))
        screen.blit(back_button_text, back_button_rect)
        bot_toggle_text = font.render("Bot Enabled: " + ("On" if bot_enabled else "Off"), True, white)
        bot_toggle_rect = bot_toggle_text.get_rect(center=(screen_width // 2, screen_height // 2 + 50))
        screen.blit(bot_toggle_text,bot_toggle_rect)
        pygame.display.flip()
        clock.tick(30)
    
    with open("volume_settings.txt", "w") as f:
        f.write(str(volume))

if __name__ == "__main__":
    if main_menu():
        import game
        game.main()
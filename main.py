import pygame
import random

# Define basic colors
noir = (0, 0, 0)
blanc = (220, 220, 220)
rouge = (255, 0, 0)

EVENT_PER_SECOND = pygame.USEREVENT + 1
GAME_MAX_TIME = 30
SIZE_APPLE: int = 100
WINDOW_WIDTH: int = 800
WINDOW_HEIGHT: int = 600

vec = pygame.math.Vector2
ACCELERATION = 0.5
FRICTION = -0.03
GRAVITY = 0.3


class Apple:
    def __init__(self):
        self.sprite = pygame.image.load("assets/apple.png").convert_alpha()
        self.sprite = pygame.transform.scale(self.sprite, (SIZE_APPLE, SIZE_APPLE))
        self.rect = self.sprite.get_rect()
        self.pos = vec(0, 0)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.reset_pos()

    def reset_pos(self):
        self.pos = vec(random.randint(0, WINDOW_WIDTH - SIZE_APPLE), random.randint(0, WINDOW_HEIGHT - SIZE_APPLE))
        self.vel.y = -10
        if self.pos.x < WINDOW_WIDTH / 2:
            self.vel.x = 10
        else:
            self.vel.x = -10

        self.acc = vec(0, 0)
        self.rect = self.sprite.get_rect()
        self.rect.x = self.pos.x
        self.rect.y = self.pos.y

    def move(self):
        self.acc = vec(0, GRAVITY)
        self.acc.x += self.vel.x * FRICTION
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc

        self.rect = self.sprite.get_rect()
        self.rect.x = self.pos.x
        self.rect.y = self.pos.y


def main():
    # Initialize Pygame
    pygame.init()

    # Create game window
    window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Shoot the fruits!")

    # Setup internal clocks
    clock = pygame.time.Clock()
    pygame.time.set_timer(EVENT_PER_SECOND, 1000, 0)

    # Game variables
    running: bool = False
    score: int = 0
    remaining_time: int = GAME_MAX_TIME
    game_over: bool = False
    apple = Apple()

    # Sound assets
    start_sound = pygame.mixer.Sound("assets/game-start.ogg")
    start_sound.set_volume(1.25)
    shooting_sound = pygame.mixer.Sound("assets/retro-laser-shot.wav")
    shooting_sound.set_volume(0.50)
    game_over_sound = pygame.mixer.Sound("assets/game-over.wav")
    game_over_sound.set_volume(1.25)
    game_over_sound_already_played = False
    clock_ticking_sound = pygame.mixer.Sound("assets/clock-ticking.wav")
    clock_ticking_sound_played = False

    pos_mouse = (0, 0)

    font = pygame.font.Font(pygame.font.get_default_font(), 24)
    big_font = pygame.font.Font("assets/Barlow-Bold.ttf", 72)

    pygame.mixer.Sound.play(start_sound)

    # Game main loop
    while not running:
        # Capture user's event
        mouse_clicked = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = True
            if not game_over:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos_mouse = pygame.mouse.get_pos()
                    buttons_mouse = pygame.mouse.get_pressed()
                    mouse_clicked = buttons_mouse[0]
                if event.type == EVENT_PER_SECOND:
                    remaining_time = remaining_time - 1

        # Update internal logic
        if mouse_clicked:
            pygame.mixer.Sound.play(shooting_sound)
            if apple.rect.collidepoint(pos_mouse):
                apple.reset_pos()
                score = score + 1

        # Move the apple
        apple.move()
        if apple.rect.centery > WINDOW_HEIGHT:
            apple.reset_pos()

        if remaining_time == 5:
            if not clock_ticking_sound_played:
                pygame.mixer.Sound.play(clock_ticking_sound)
                clock_ticking_sound_played = True

        if remaining_time == 0:
            if not game_over_sound_already_played:
                clock_ticking_sound.stop()
                pygame.mixer.Sound.play(game_over_sound)
                game_over_sound_already_played = True
            game_over = True

        # Prepare scoring text
        score_surface = font.render("Score: " + str(score), True, blanc)
        score_rect = score_surface.get_rect()
        score_rect.x = 5
        score_rect.y = 5

        # Prepare timing text
        temps_surface = font.render("Remaining time: " + str(remaining_time), True, blanc)
        temps_rect = temps_surface.get_rect()
        temps_rect.x = WINDOW_WIDTH - temps_rect.width - 5
        temps_rect.y = 5

        # Prepare timing gauge
        gauge_width = 225
        gauge_height = 15
        gauge_size = ((gauge_width - 2) / GAME_MAX_TIME) * (GAME_MAX_TIME - remaining_time)
        gauge_surface = pygame.surface.Surface((gauge_width, 15))
        pygame.draw.rect(gauge_surface, blanc, (0, 0, gauge_width, gauge_height), 1)
        pygame.draw.rect(gauge_surface, blanc, (1 + gauge_size, 1, gauge_width - 2, gauge_height - 2), 0)

        gauge_surface_rect = gauge_surface.get_rect()
        gauge_surface_rect.x = WINDOW_WIDTH - gauge_surface_rect.width - 5
        gauge_surface_rect.y = 5 + 5 + temps_rect.height

        game_over_surface = big_font.render("Time's up!", True, blanc)
        game_over_rect = game_over_surface.get_rect()
        game_over_rect.centerx = WINDOW_WIDTH / 2
        game_over_rect.centery = WINDOW_HEIGHT / 2

        # Update the screen
        window.fill(noir)
        if game_over:
            window.blit(game_over_surface, game_over_rect)
        else:
            window.blit(apple.sprite, apple.rect)
        window.blit(score_surface, score_rect)
        window.blit(temps_surface, temps_rect)
        window.blit(gauge_surface, gauge_surface_rect)

        # Update the screen 60x per second
        pygame.display.flip()
        clock.tick(60)

    # End of game
    pygame.quit()


if __name__ == "__main__":
    main()

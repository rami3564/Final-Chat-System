import pygame
import time
import random

pygame.init()


def run_snake_games():
    # Initialize sound mixer
    pygame.mixer.init()

    # Load sound effects
    eat_sound = pygame.mixer.Sound('eat_sound.wav')
    collision_sound = pygame.mixer.Sound('collision_sound.wav')
    game_over_sound = pygame.mixer.Sound('game_over_sound.wav')

    # Window size
    window_x = 720
    window_y = 480


    # Initialize game window
    game_window = pygame.display.set_mode((window_x, window_y))
    pygame.display.set_caption('ICSDS Project: Snakes')

    # Load background image
    background = pygame.image.load('background.jpg')
    background = pygame.transform.scale(background, (window_x, window_y))

    # Load snake texture
    snake_texture = pygame.image.load('snake_texture.jpeg')
    snake_texture = pygame.transform.scale(snake_texture, (10, 10))

    # Colors
    black = pygame.Color(0, 0, 0)
    white = pygame.Color(255, 255, 255)
    red = pygame.Color(255, 0, 0)
    green = pygame.Color(0, 255, 0)
    blue = pygame.Color(0, 0, 255)

    # Snake speed
    snake_speed = 15

    # FPS controller
    fps = pygame.time.Clock()

    # Snake default position
    snake_position = [100, 50]

    # Snake body
    snake_body = [
        [100, 50],
        [90, 50],
        [80, 50],
        [70, 50]
    ]

    # Fruit position
    fruit_position = [random.randrange(1, (window_x // 10)) * 10,
                      random.randrange(1, (window_y // 10)) * 10]

    # Snake direction
    direction = 'RIGHT'
    change_to = direction

    # Score
    score = 0

    # Display score function
    def show_score(choice, color, font, size):
        score_font = pygame.font.SysFont(font, size)
        score_surface = score_font.render('Score: ' + str(score), True, color)
        game_window.blit(score_surface, (10, 10))

    # Game over function
    def game_over():
        my_font = pygame.font.SysFont('times new roman', 50)
        game_over_surface = my_font.render('Your Score is: ' + str(score), True, red)
        game_over_rect = game_over_surface.get_rect()
        game_over_rect.midtop = (window_x / 2, window_y / 4)
        game_window.blit(game_over_surface, game_over_rect)
        pygame.display.flip()
        time.sleep(3)
        pygame.quit()
        quit()

    # Main loop
    fruit_spawn = True
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    change_to = 'UP'
                elif event.key == pygame.K_DOWN:
                    change_to = 'DOWN'
                elif event.key == pygame.K_LEFT:
                    change_to = 'LEFT'
                elif event.key == pygame.K_RIGHT:
                    change_to = 'RIGHT'

        # Update direction
        if change_to == 'UP' and direction != 'DOWN':
            direction = 'UP'
        if change_to == 'DOWN' and direction != 'UP':
            direction = 'DOWN'
        if change_to == 'LEFT' and direction != 'RIGHT':
            direction = 'LEFT'
        if change_to == 'RIGHT' and direction != 'LEFT':
            direction = 'RIGHT'

        # Move the snake
        if direction == 'UP':
            snake_position[1] -= 10
        if direction == 'DOWN':
            snake_position[1] += 10
        if direction == 'LEFT':
            snake_position[0] -= 10
        if direction == 'RIGHT':
            snake_position[0] += 10

        # Snake body growing mechanism
        snake_body.insert(0, list(snake_position))
        if snake_position[0] == fruit_position[0] and snake_position[1] == fruit_position[1]:
            score += 1
            fruit_spawn = False
            eat_sound.play()  # Play eat sound effect
        else:
            snake_body.pop()

        if not fruit_spawn:
            fruit_position = [random.randrange(1, (window_x // 10)) * 10,
                              random.randrange(1, (window_y // 10)) * 10]
        game_window.blit(background, (0, 0))

        for pos in snake_body:
            game_window.blit(snake_texture, (pos[0], pos[1]))

        pygame.draw.rect(game_window, red, pygame.Rect(
            fruit_position[0], fruit_position[1], 10, 10))

        # Game Over conditions
        if snake_position[0] < 0 or snake_position[0] > window_x - 10:
            game_over_sound.play()  # Play game over sound effect
            game_over()
        if snake_position[1] < 0 or snake_position[1] > window_y - 10:
            game_over_sound.play()  # Play game over sound effect
            game_over()

        # Touching the snake body
        for block in snake_body[1:]:
            if snake_position[0] == block[0] and snake_position[1] == block[1]:
                collision_sound.play()  # Play collision sound effect
                game_over()

        # Display score
        show_score(1, blue, 'times new roman', 20)

        # Refresh game screen
        pygame.display.update()

        # FPS / Refresh Rate
        fps.tick(snake_speed)

if __name__ == "__main__":
    run_snake_games()

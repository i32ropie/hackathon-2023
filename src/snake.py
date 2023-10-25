import sys, os, random
import pygame


# Initialize Pygame
pygame.init()
pygame.mixer.init()

#Eat sound
eat_sound_file = os.path.join(os.path.dirname(__file__), "../sounds/eat_sound.mp3")
eat_sound = pygame.mixer.Sound(eat_sound_file)


# Set up the game window
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Snake")

# Set up the game clock
clock = pygame.time.Clock()

# Set up the snake
SNAKE_SIZE = 20
snake = [pygame.Rect(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2, SNAKE_SIZE, SNAKE_SIZE)]
snake_direction = "right"
HEAD_COLOR = (0, 128, 0)  # Dark green
BODY_COLOR = (144, 238, 144)  # Light green
TAIL_COLOR = (255, 255, 0)  # Yellow


FOOD_SIZE = 20
food_image_file = os.path.join(os.path.dirname(__file__), "../imgs/apple.png")
food_image = pygame.image.load(food_image_file).convert_alpha()
food = pygame.Rect(random.randint(0, WINDOW_WIDTH - FOOD_SIZE), random.randint(0, WINDOW_HEIGHT - FOOD_SIZE), FOOD_SIZE, FOOD_SIZE)

# Set up the score
score = 0
font = pygame.font.SysFont(None, 30)

# Set up the music from "../sounds/music.mp3" using os library
def play_music():
    music_file = os.path.join(os.path.dirname(__file__), "../sounds/music.mp3")
    pygame.mixer.music.load(music_file)
    pygame.mixer.music.play(-1)

def stop_music():
    pygame.mixer.music.stop()


# Function to display the Game Over screen
def game_over():
    stop_music()
    game_over_text = font.render("Game Over", True, (255, 0, 0))
    window.blit(game_over_text, (WINDOW_WIDTH // 2 - 60, WINDOW_HEIGHT // 2))
    pygame.display.flip()
    #Death sound
    death_sound_file = os.path.join(os.path.dirname(__file__), "../sounds/death_sound.mp3")
    death_sound_file = pygame.mixer.Sound(death_sound_file)
    death_sound_file.play()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

# Function to generate food at a random location
def generate_food():
    return pygame.Rect(random.randint(0, WINDOW_WIDTH - SNAKE_SIZE), random.randint(0, WINDOW_HEIGHT - SNAKE_SIZE), SNAKE_SIZE, SNAKE_SIZE)


# Set up the initial food
food = generate_food()

play_music()

# Main menu
def main_menu():
    menu_font = pygame.font.SysFont(None, 50)
    title_text = menu_font.render("Snake Game", True, (255, 255, 255))
    easy_text = menu_font.render("Press 'E' for Easy", True, (255, 255, 255))
    medium_text = menu_font.render("Press 'M' for Medium", True, (255, 255, 255))
    hard_text = menu_font.render("Press 'H' for Hard", True, (255, 255, 255))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_e:
                    return 5  # Easy mode (5 pieces of food)
                elif event.key == pygame.K_m:
                    return 3  # Medium mode (3 pieces of food)
                elif event.key == pygame.K_h:
                    return 1  # Hard mode (1 piece of food)

        # Fondo del menu
        bgdtile = pygame.image.load(os.path.join(os.path.dirname(__file__), "../imgs/bgimage.png")).convert()
        SCREENRECT = pygame.Rect(0, 0, 800, 600)
        background = pygame.Surface(SCREENRECT.size)
        for x in range(0, SCREENRECT.width, bgdtile.get_width()):
            background.blit(bgdtile, (x, 0))
        window.blit(background, (0, 0))

        window.blit(title_text, (WINDOW_WIDTH // 2 - 90, 100))
        window.blit(easy_text, (WINDOW_WIDTH // 2 - 120, 200))
        window.blit(medium_text, (WINDOW_WIDTH // 2 - 140, 250))
        window.blit(hard_text, (WINDOW_WIDTH // 2 - 110, 300))

        pygame.display.flip()


# Get the selected difficulty
food_count = main_menu()

# Set up the food based on the selected difficulty
if food_count == 5:  # Easy mode
    FOOD_COUNT = 5
elif food_count == 3:  # Medium mode
    FOOD_COUNT = 3
else:                   # Hard mode
    FOOD_COUNT = 1

food_list = [generate_food() for _ in range(FOOD_COUNT)]

# Set up the snake movement speed (milliseconds per movement)
SNAKE_SPEED = 50  # Adjust this value to control the snake's speed
last_move_time = 0

while True:
    # Setupt background for each difficulty
    if food_count == 5:
        bgdtile = pygame.image.load(os.path.join(os.path.dirname(__file__), "../imgs/easyBack.png")).convert()
    elif food_count == 3:  # Medium mode
        bgdtile = pygame.image.load(os.path.join(os.path.dirname(__file__), "../imgs/mediumBack.png")).convert()
    else:                   # Hard mode
        bgdtile = pygame.image.load(os.path.join(os.path.dirname(__file__), "../imgs/hardBack.png")).convert()

    SCREENRECT = pygame.Rect(0, 0, 800, 600)
    background = pygame.Surface(SCREENRECT.size)
    for x in range(0, SCREENRECT.width, bgdtile.get_width()):
        background.blit(bgdtile, (x, 0))
    window.blit(background, (0, 0))

    current_time = pygame.time.get_ticks()

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Reset has_eaten
    has_eaten = False

    # Move the snake
    if current_time - last_move_time >= SNAKE_SPEED:
        last_move_time = current_time
        if snake_direction == "right":
            new_head = pygame.Rect(snake[-1].x + SNAKE_SIZE, snake[-1].y, SNAKE_SIZE, SNAKE_SIZE)
        elif snake_direction == "left":
            new_head = pygame.Rect(snake[-1].x - SNAKE_SIZE, snake[-1].y, SNAKE_SIZE, SNAKE_SIZE)
        elif snake_direction == "up":
            new_head = pygame.Rect(snake[-1].x, snake[-1].y - SNAKE_SIZE, SNAKE_SIZE, SNAKE_SIZE)
        elif snake_direction == "down":
            new_head = pygame.Rect(snake[-1].x, snake[-1].y + SNAKE_SIZE, SNAKE_SIZE, SNAKE_SIZE)

        # Check if the snake hit the wall
        if new_head.left < 0:
            new_head.left = WINDOW_WIDTH - SNAKE_SIZE
        elif new_head.right > WINDOW_WIDTH:
            new_head.left = 0
        elif new_head.top < 0:
            new_head.top = WINDOW_HEIGHT - SNAKE_SIZE
        elif new_head.bottom > WINDOW_HEIGHT:
            new_head.top = 0

        # Check if the snake hit itself
        if new_head in snake:
            game_over()  # Call the Game Over function
            break

        # Check if the snake ate the food
        for food in food_list:
            if new_head.colliderect(food):
                food_list.remove(food)
                food_list.append(generate_food())
                score += 1
                has_eaten = True
                eat_sound.play()  # Play the eat sound

        # Add the new head to the snake
        snake.append(new_head)

        # If the snake hasn't eaten, remove the tail segment
        if not has_eaten:
            snake.pop(0)

    # Handle input
    keys = pygame.key.get_pressed()
    if keys[pygame.K_RIGHT] and snake_direction != "left":
        snake_direction = "right"
    elif keys[pygame.K_LEFT] and snake_direction != "right":
        snake_direction = "left"
    elif keys[pygame.K_UP] and snake_direction != "down":
        snake_direction = "up"
    elif keys[pygame.K_DOWN] and snake_direction != "up":
        snake_direction = "down"

    # Draw the snake and food  
    for segment in snake:
        pygame.draw.rect(window, (255, 255, 255), segment)
    # Draw the snake
    for i, segment in enumerate(snake):
        if i == 0:
            # Draw the head
            pygame.draw.rect(window, TAIL_COLOR, pygame.Rect(segment[0], segment[1], SNAKE_SIZE, SNAKE_SIZE))
        elif i == len(snake) - 1:
            # Draw the tail
            pygame.draw.rect(window, HEAD_COLOR, pygame.Rect(segment[0], segment[1], SNAKE_SIZE, SNAKE_SIZE))
        else:
            # Draw the body
            pygame.draw.rect(window, BODY_COLOR, pygame.Rect(segment[0], segment[1], SNAKE_SIZE, SNAKE_SIZE))

    # Draw food
    for food in food_list:
        window.blit(food_image, food)

    # Draw the score
    score_text = font.render("Score: " + str(score), True, (255, 255, 255))
    window.blit(score_text, (10, 10))

    # Update the display
    pygame.display.flip()

    # Limit the frame rate
    clock.tick(60)  # Set the frame rate to a reasonable value (e.g., 60 FPS)

import pygame
import random
import serial

ser = serial.Serial('COM24', 115200, timeout=1)  # Adjust 'COM24' to match your serial port

pygame.init()
counter = 0

# Size of display
WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 600
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Envole-toi, Petit Lapin!')

# Load game icon
icon_image = pygame.image.load('./images/Turbo_Lapin.png')  # Replace 'your_icon_image.png' with the path to your icon image
pygame.display.set_icon(icon_image)

# Load character images
bird_image = pygame.image.load('./images/Turbo_Lapin.png')
bird_image = pygame.transform.scale(bird_image, (50, 50))  # Reduce the size of the bird image

# Define a variable to keep track of the background's x-coordinate
background_x = 0
background_image = None
background_image = pygame.image.load('./images/tree.png').convert()
background_image = pygame.transform.scale(background_image, (WINDOW_WIDTH, WINDOW_HEIGHT))

# Define bird variables
bird_lowest_y = WINDOW_HEIGHT - bird_image.get_height()  # Lowest position of the bird
bird_highest_y = 100  # Adjusted starting position of the bird
lapin_y_range = bird_lowest_y - bird_highest_y  # Range of possible bird positions
lapin_y = bird_lowest_y  # Initialize bird's vertical position
bird_rect = bird_image.get_rect()

# Define tube variables
tube_image = pygame.image.load('./images/pipe.png')
tube_x = WINDOW_WIDTH - tube_image.get_width()  # Initial x-coordinate of the tubes
tube_gap = 300  # Gap between the upper and lower tubes
tube_speed = 1  # Decreased tube speed
tube_width = tube_image.get_width()
tube_height = tube_image.get_height()

game_over = False  # Flag to track game state
score = 0  # Initialize score
game_started = False  # Flag to track whether the game has started

font = pygame.font.SysFont(None, 50)  # Font for displaying score

def draw_text(text, font, color, surface, x, y):
    # Render the text with a black shadow
    textobj_shadow = font.render(text, True, (0, 0, 0))  # Black color for shadow
    textrect_shadow = textobj_shadow.get_rect()
    textrect_shadow.centerx = surface.get_rect().centerx + 2  # Offset the shadow slightly to the right
    textrect_shadow.y = y + 2  # Offset the shadow slightly downwards
    surface.blit(textobj_shadow, textrect_shadow)
    
    # Render the text with the desired color
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect()
    textrect.centerx = surface.get_rect().centerx  # Center the text horizontally
    textrect.y = y  # Set the y-coordinate
    surface.blit(textobj, textrect)

def draw_tube(x, y, gap_y):
    upper_tube_y = y # position of upper tube
    lower_tube_y = gap_y + tube_gap 
    
    #draw tubes
    window.blit(tube_image, (x, upper_tube_y))  # Upper tube
    window.blit(pygame.transform.flip(tube_image, False, True), (x  + 70 , lower_tube_y))  # Lower tube

def check_collision(x , y, gap_y):
    global bird_rect, tube_x, tube_gap , tube_width, tube_height

    # Update tube positions
    upper_tube_rect = pygame.Rect(tube_x, y, tube_width , tube_height)
    lower_tube_rect = pygame.Rect(tube_x + 70, gap_y + tube_gap , tube_width, tube_height)

    # Draw collision boxes
    pygame.draw.rect(window, (255, 0, 0), upper_tube_rect, 2)  # Red rectangle for upper tube
    pygame.draw.rect(window, (255, 0, 0), lower_tube_rect, 2)  # Red rectangle for lower tube

    return bird_rect.colliderect(upper_tube_rect) or bird_rect.colliderect(lower_tube_rect)

def start_screen():
    global background_image

    if not game_over:
        window.blit(background_image, (0, 0))
        draw_text('Press space to start', font, (255, 255, 255), window, 250, 250)
        pygame.display.flip()
    else:
        # Load the new background image    
        file_path = './images/{}.png'.format(counter)  # Construct the file path using string formatting
        background_image = pygame.image.load(file_path).convert()
        background_image = pygame.transform.scale(background_image, (WINDOW_WIDTH, WINDOW_HEIGHT))
        window.blit(background_image, (0, 0))

        # load score
        draw_text('Best Score : ' + str(score), font, (255, 255, 255), window, 250, 220)
        draw_text('Press space to try again!', font, (255, 255, 255), window, 250, 280)
  
        pygame.display.flip()  

def game_screen():
    global tube_x, tube_y, tube_gap, tube_speed, score, game_over, background_x, counter

    tube_x -= tube_speed
    background_x -= (tube_speed - 1) # Move the background along with the tubes
        
    if tube_x < -tube_width:
        tube_x = WINDOW_WIDTH
        tube_gap = random.randint(20, 346)  # Randomize gap between tubes
        tube_y = random.randint(-2, 20) * 10
        tube_speed += 0.1
        score += 1

    # If the background has scrolled completely, reset its position
    if background_x <= -WINDOW_WIDTH:
        background_x = 0

    # Draw the background at its current position
    window.blit(background_image, (background_x, 0))
    window.blit(background_image, (background_x + WINDOW_WIDTH, 0))

    # Draw the bird and tubes
    window.blit(bird_image, (bird_rect.x, lapin_y))
    bird_rect.x = 0
    bird_rect.y = lapin_y
    draw_tube(tube_x, tube_y, WINDOW_HEIGHT // 2)

    # Check for collision
    if check_collision(tube_x, tube_y, WINDOW_HEIGHT // 2):
        game_over = True
        counter = 1 if counter == 8 else counter + 1

    # Draw the score
    draw_text('Score: ' + str(score), font, (255, 255, 255), window, 10, 10)

    pygame.display.flip()

# Game loop
running = True
while running:

    line = ser.readline().decode().strip()

    if line.startswith("Average Period:"):
        average_period = int(line.split(":")[1])
        value = bird_lowest_y - int((average_period - 350) / 250 * lapin_y_range) # initial position
        lapin_y = 0 if value < 0 else value # top position limit
        bird_rect.y = lapin_y # colision

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if not game_started or game_over:
                    game_started = True
                    game_over = False
                    lapin_y = bird_lowest_y
                    tube_x = WINDOW_WIDTH - tube_image.get_width()
                    tube_y = 0
                    tube_gap = 200
                    tube_speed = 4
                    score = 0
                    bird_rect = bird_image.get_rect()
        
    if not game_started:
        start_screen() # Show start game screen
    else:
        game_screen() if not game_over else start_screen()  # Show game over screen

    pygame.display.update()

pygame.quit()
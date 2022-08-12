## Imports
import sys, pygame, random

## Functions
def rot_center(image, angle):
    """rotate an image while keeping its center and size"""
    orig_rect = image.get_rect()
    rot_image = pygame.transform.rotate(image, angle)
    rot_rect = orig_rect.copy()
    rot_rect.center = rot_image.get_rect().center
    rot_image = rot_image.subsurface(rot_rect).copy()
    return rot_image

## Main
pygame.init()

# Vars and Inits
size = width, height = 1600, 900
speed = [0, 1] # A définir
angle = 0
tick_rate = 120
acceleration = 0.1 # A définir
enable_hitbox = False
score = 0
player_dead = False

# Screen and Images
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock() # nb frames
ball = pygame.image.load("intro_ball.gif")
background = pygame.image.load("beach3d.jpg")
panel = pygame.image.load("panel.png")

# Create and Render font
score_font = pygame.font.SysFont("Colibri", 98)
button_font = pygame.font.SysFont("Comic sans ms", 130)

# Get Rectangle of Ball
ballrect = ball.get_rect(center=(random.randint(int(ball.get_width()/2), width - ball.get_width()), ball.get_height()/2 ))
# Get Rectangle of Panel
panelrect = panel.get_rect(center=(panel.get_width()/2 + 150, height - panel.get_height()/2 - 90))

# Game Loop
while True:
    # Logs
    # print("Player:" , pygame.mouse.get_pos(),"; Ball's Speed:", speed[1], "; Ball's Left/Right:", (ballrect.left, ballrect.right), "; Ball's Top/Bottom:", (ballrect.top, ballrect.bottom))

    # Parametres balles
    if not player_dead:
        speed[1] += acceleration
        angle += speed[1] * 0.25
        ballrect = ballrect.move(speed)
        r_ball = rot_center(ball, angle)

        # Score Actualisation
        score_text = score_font.render(("Score: " + str(score)), True, (255, 255, 255))
        rscore_text = pygame.transform.rotate(score_text, -7.5)

    # Affichage
    screen.blit(background, (0, 0)) 
    screen.blit(panel, panelrect)
    screen.blit(rscore_text, (panelrect.left + 25, panelrect.top + 45))
    screen.blit(r_ball, ballrect)
    # Hitbox
    if enable_hitbox:
        pygame.draw.rect(screen, (255, 0, 0), ballrect, 2)
    # Death Screen
    if player_dead:
        # Death Fade
        death_screen = pygame.Surface((width, height), pygame.SRCALPHA)
        death_screen.fill((0,0,0,150))
        screen.blit(death_screen, (0,0))
        # Button Rect Algebra
        play_again_rect = [width/4, height/4 - 50, 2*width/4, height/4]
        quit_rect = [width/4, 2*height/4 + 50, 2*width/4, height/4]
        # Button Draw [ Left (x axis), Top (y axis), width, height]
        pygame.draw.rect(screen, (44, 44, 84), play_again_rect , border_radius=24, border_top_left_radius=0)
        pygame.draw.rect(screen, (179, 57, 57), quit_rect , border_radius=24, border_bottom_right_radius=0)
        # Button Text & Blit
        play_again_text = button_font.render("REJOUER", True, (255,255,255))
        quit_text = button_font.render("QUITTER", True, (255,255,255))
        screen.blit(play_again_text, (play_again_rect[0] + 100, play_again_rect[1] + 20))
        screen.blit(quit_text, (quit_rect[0] + 90, quit_rect[1] + 20))
    # Clock & Display
    clock.tick(tick_rate)
    pygame.display.flip()

    # Death Check
    if ballrect.top > width:
        player_dead = True

    # Event Loop
    for event in pygame.event.get():
        # Exit Game
        if event.type == pygame.QUIT:
            sys.exit()
        
        # Show Hitbox
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_F3:
                if enable_hitbox:
                    enable_hitbox = False
                else:
                    enable_hitbox = True

        # Catch event
        if event.type == pygame.MOUSEBUTTONUP:
            player_x, player_y = pygame.mouse.get_pos()
            # Click Buttons
            if player_dead:

                # Replay Button
                if player_x > play_again_rect[0] and player_x < play_again_rect[0] + play_again_rect[2]:
                    if player_y > play_again_rect[1] and player_y < play_again_rect[1] + play_again_rect[3]:
                        player_dead = False
                        ballrect = ball.get_rect(center=(random.randint(int(ball.get_width()/2), width - ball.get_width()), ball.get_height()/2 ))
                        speed = [0, 1]
                        angle = 0
                        score = 0

                # Quit Button
                if player_x > quit_rect[0] and player_x < quit_rect[0] + quit_rect[2]:
                    if player_y > quit_rect[1] and player_y < quit_rect[1] + quit_rect[3]:
                        sys.exit()

            # Catch the Ball
            elif player_x > ballrect.left and player_x < ballrect.right:
                if player_y > ballrect.top and player_y < ballrect.bottom:
                    speed[1] = -speed[1] * (1 + acceleration)
                    score += 1

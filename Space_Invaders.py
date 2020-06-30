''' Space Invaders by Akshay Jain '''

import pygame
import random
from pygame import mixer

# Initializing the game
pygame.init()

# Creating a screen : SCREENWIDTH X SCREENHEIGHT
screen = pygame.display.set_mode((800,600))
background = pygame.image.load("background.png")

# Title and icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load("ufo.png")
pygame.display.set_icon(icon)


def mainScreen():
    # Global Variables
    global background, playerX, playerY, playerX_change, playerY_change, playerImg

    # mainRunning is true if mainScreen is showing
    mainRunning = True
    show = True

    # MAINSCREEN Image
    main = pygame.image.load("main.png")
    
    while mainRunning:

        # Blitting background
        screen.blit(background, (0,0))

        if show :
            # display main screen
            screen.blit(main, (0,0))

        # display the player
        player(playerX, playerY)

        # Checking for events
        for event in pygame.event.get():
            # Quitting the Game
            if event.type == pygame.QUIT:
                mainRunning = False
                return "QUIT"
            
            # Starting game
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    show = False

        if not show:
            playerY += playerY_change
            if playerY + playerImg.get_height() < 0:
                playerY = 480
                return "RUN"
                    
        # Updating the screen
        pygame.display.update()



# Score
score_value = 0
font = pygame.font.Font("freesansbold.ttf", 30)
scoreX = 10
scoreY = 10
def show_score():
    score = font.render("Score : " + str(score_value), True, (0,255,0))
    screen.blit(score, (scoreX, scoreY))

# Player
playerImg = pygame.image.load("player.png")
playerX = (800 - playerImg.get_width()) // 2
playerY = 480
playerX_change = 0
playerY_change = -4
def player(x,y):
    screen.blit(playerImg, (x,y))

# Enemy
enemyNo = 5
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
for i in range(enemyNo):
    enemyImg.append(pygame.image.load("enemy.png"))
    enemyX.append(random.randint(0,800 - enemyImg[i].get_width()))
    enemyY.append(random.randint(20,150)) # Some random height
    enemyX_change.append(5)
    enemyY_change.append(40)
def enemy(x,y,i):
    screen.blit(enemyImg[i], (x,y))

# Bullet
bulletImg = pygame.image.load("bullet.png")
bulletX = playerX + (playerImg.get_width() - bulletImg.get_width()) // 2
bulletY = playerY - bulletImg.get_height()
bulletX_change = 0
bulletY_change = -15
bulletState = "ready" # If ready bullet can be fired
def fire_bullet(x,y):
    global bulletState
    bulletState = "fire"
    screen.blit(bulletImg, (x,y))

# Check if bullet hits the enemy
def isCollide(enemyX, enemyY, bulletX, bulletY):
    differenceX = bulletX - enemyX
    differenceY = bulletY - enemyY
    if differenceX > 0 and differenceX < enemyImg[0].get_width() :
        if differenceY > 0 and differenceY < enemyImg[0].get_height() :
            return True
    return False


def game():

    # Global Variables
    global background, score_value, font, scoreX, scoreY, playerImg, playerX, playerY, playerX_change, enemyNo, enemyImg, enemyX, enemyY, enemyX_change, enemyY_change, bulletImg, bulletX, bulletY, bulletX_change, bulletY_change, bulletState


    # gameRunning is true if game is running
    gameRunning = True

    # Game Starts
    while gameRunning :

        # Blitting background
        screen.blit(background, (0,0))


        # Checking for events
        for event in pygame.event.get():
            # Quitting the Game
            if event.type == pygame.QUIT:
                gameRunning = False
                return "QUIT"

            if event.type == pygame.KEYDOWN:
                # Moving the spaceship
                if event.key == pygame.K_LEFT:
                    playerX_change = -5
                elif event.key == pygame.K_RIGHT:
                    playerX_change = 5
                # Firing the bullet
                if event.key == pygame.K_SPACE:
                    if bulletState == "ready":
                        bulletSound = mixer.Sound("laser.wav")
                        bulletSound.play()
                        bulletX = playerX + (playerImg.get_width() - bulletImg.get_width()) // 2
                        fire_bullet(bulletX, bulletY)
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    playerX_change = 0


        # Setting boundaries
        if playerX < 0 :
            playerX = 0
        elif playerX + playerImg.get_width() > 800 :
            playerX = 800 - playerImg.get_width()
        
        # Enemy functioning
        for i in range(enemyNo):
            # Checking for boundaries
            if enemyX[i] < 0 :
                enemyX[i] = 0
                enemyX_change[i] = -enemyX_change[i]
                enemyY[i] += enemyY_change[i]
            elif enemyX[i] + enemyImg[i].get_width() > 800 :
                enemyX[i] = 800 - enemyImg[i].get_width()
                enemyX_change[i] = -enemyX_change[i]
                enemyY[i] += enemyY_change[i]

            # Blitting enemy
            enemyX[i] += enemyX_change[i]
            enemy(enemyX[i], enemyY[i], i)
            
            # Check for Game Over
            if enemyY[i] >= 480 - playerImg.get_height() - bulletImg.get_height():
                gameRunning = False
            
            # Check for collision
            collide = isCollide(enemyX[i], enemyY[i], bulletX, bulletY)
            if collide :        
                collisionSound = mixer.Sound("explosion.wav")
                collisionSound.play()
                bulletY = playerY - bulletImg.get_height()
                bulletState = "ready"
                score_value += 1
                enemyX[i] = random.randint(0,800 - enemyImg[i].get_width())
                enemyY[i] = random.randint(20,150)

                # Increasing game complexity : Enemy increases as Score increases by 25
                if score_value%25 == 0:
                    enemyNo += 1
                    enemyImg.append(pygame.image.load("enemy.png"))
                    enemyX.append(random.randint(0,800 - enemyImg[i].get_width()))
                    enemyY.append(random.randint(20,150)) # Some random height
                    enemyX_change.append(5)
                    enemyY_change.append(40)
            

        # Blitting player
        playerX += playerX_change
        player(playerX, playerY)

        # Blitting bullet
        if bulletY<0: # Multiple bullets
            bulletY = playerY - bulletImg.get_height()
            bulletState = "ready"
        if bulletState == "fire":
            fire_bullet(bulletX, bulletY)
            bulletY += bulletY_change

        # Blitting scores
        show_score()

        # Updating the screen
        pygame.display.update()
    
    # After Game is over
    return "OVER"


# Main Function
if __name__ == "__main__":

    # Background music
    mixer.music.load("background.wav")
    mixer.music.play(-1)

    # Displaying main Screen
    run = mainScreen()

    if run == "RUN":
        # Running Game
        over = game()

        # Game Over
        if over == "OVER":

            overRunning = True
            gameOver = pygame.image.load("over.png")
            show = False
            while overRunning:

                # Blitting background
                screen.blit(background, (0,0))

                # display the player
                player(playerX, playerY)

                if show:
                    # Blitting Game Over Message
                    screen.blit(gameOver, (0,0))

                    # Checking for events
                    for event in pygame.event.get():
                        # Quitting the Game
                        if event.type == pygame.QUIT:
                            overRunning = False
                        
                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_q:
                                overRunning = False
                
                if not show:
                    playerY += playerY_change
                    if playerY + playerImg.get_height() < 0:
                        show = True

                # Updating the screen
                pygame.display.update()
    print("GoodBye Pilot :)")
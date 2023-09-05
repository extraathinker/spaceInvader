import pygame
import random
import math
from pygame import mixer

# initializing the pygame
pygame.init()
mixer.init()
# create the screen
screen = pygame.display.set_mode((800, 600))

# background
background = pygame.image.load('3.jpg')

# title and icon
pygame.display.set_caption('Space Invaders')
icon = pygame.image.load('spaceship.png')
pygame.display.set_icon(icon)

#player
playerImg = pygame.image.load('001-spaceship.png')
playerX = 370
playerY = 480
playerChangeX = 0
playerChangeY = 0

#enemy
enemyImg = []
enemyX = []
enemyY = []
enemyChangeX = []
enemyChangeY = []
numEnemies = 6

for i in range(numEnemies):
    enemyImg.append(pygame.image.load('002-alien.png'))
    enemyX.append(random.randint(0, 735))
    enemyY.append(random.randint(50,150))
    enemyChangeX.append(0.3)
    enemyChangeY.append(40)

#bullet
bulletImg = pygame.image.load('001-bullet.png')
bulletX = 370
bulletY = 480
bulletChangeX = 0.1
bulletChangeY = 0.8
bulletState = 'ready'

score = 0
font = pygame.font.Font('freesansbold.ttf',32)

textX = 10
textY = 10

overfont = pygame.font.Font('freesansbold.ttf',64)

def showScore(x, y):
    scor = font.render('Score :' + str(score), True, (250,0,0))
    screen.blit(scor, (x, y))

def gameOver():
    overText = overfont.render('GAME OVER', True, (250,255,0))
    screen.blit(overText, (200, 250))

def player(x,y):
    screen.blit(playerImg,(x, y))

def enemy(x,y, i):
    screen.blit(enemyImg[i],(x, y))

def fire_bullet(x,y):
    global bulletState
    bulletState = 'fire'
    screen.blit(bulletImg,(x + 16, y + 10))

def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt(math.pow(enemyX - bulletX,2) + math.pow(enemyY - bulletY,2))
    if distance < 27:
        return True
    else:
        return False    

# game loop
running = True
while running:

    # RGB - Red, Green, Blue
    screen.fill((0, 0, 0))

    # background image
    screen.blit(background,(0,0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerChangeX = -0.3
            if event.key == pygame.K_RIGHT:
                playerChangeX = 0.3
            if event.key == pygame.K_UP:
                playerChangeY = -0.1
            if event.key == pygame.K_DOWN:
                playerChangeY = 0.1
            if event.key == pygame.K_SPACE:
                if bulletState == 'ready':
                    bulletSound = mixer.Sound('laser.mp3')
                    bulletSound.play()
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                playerChangeX = 0
            if event.key == pygame.K_RIGHT:
                playerChangeX = 0 
            if event.key == pygame.K_UP:
                playerChangeY = 0
            if event.key == pygame.K_DOWN:
                playerChangeY = 0 

    playerX += playerChangeX
    playerY += playerChangeY
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736
    
    for i in range(numEnemies):

        # Game Over
        if enemyY[i] > 440:
            for j in range(numEnemies):
                enemyY[j] = 2000
            gameOver()
            break

        enemyX[i] += enemyChangeX[i]
        if enemyX[i] <= 0:
            enemyY[i] += enemyChangeY[i]
            enemyChangeX[i] = 0.3   
        elif enemyX[i] >= 736:
            enemyY[i] += enemyChangeY[i]
            enemyChangeX[i] = -0.3
        
        collision = isCollision(enemyX[i],enemyY[i],bulletX,bulletY)
        if collision:
            explosion = mixer.Sound('explosion.mp3')
            explosion.play()
            bulletY = 480
            bulletState = 'ready'
            score += 1
            
            enemyX[i] = random.randint(0, 735)
            enemyY[i] = random.randint(50,150)

        enemy(enemyX[i], enemyY[i], i)
    
    if bulletY <= 0:
        bulletY = 480
        bulletState = 'ready'

    if bulletState is 'fire':
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletChangeY

    


    player(playerX, playerY)
    showScore(textX, textY)

    # updating the display
    pygame.display.update()
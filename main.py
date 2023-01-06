import random
import sys
import pygame as pg
from pygame.locals import *

#Global Variables
FPS = 30
screenwidth = 310
screenheight = 512
SCREEN = pg.display.set_mode((screenwidth,screenheight))
groundy = screenheight*0.8
game_sprites={}
game_sounds={}
player = 'gallery/sprites/fish.png'
background = 'gallery/sprites/background.jpg'
over= 'gallery/sprites/gameover.png'
PIPE = 'gallery/sprites/pipe.png'

def isCollide(playerx,playery,upperPipes,lowerPipes):
    if playery> (groundy-66) or playery<0:
        game_sounds['hit'].play()
        return True

    for pipe in upperPipes:
        pipeHeight = game_sprites['pipe'][0].get_height()
        if(playery < (pipeHeight +pipe['y'])/1.2 and abs(playerx-pipe['x'])<game_sprites['pipe'][0].get_width()):
            game_sounds['hit'].play() 
            return True  
    for pipe in lowerPipes:
        if(playery + (game_sprites['player'].get_height())/1.2 > pipe['y'] and abs(playerx-pipe['x'])<game_sprites['pipe'][0].get_width()):
            game_sounds['hit'].play() 
            return True 
 
    return False


def getRandomPipe():

    #generate positions of two pipes
    pipeHeight = game_sprites['pipe'][0].get_height()
    offset = screenheight/3
    y2= offset + random.randrange(0,int(screenheight - game_sprites['base'].get_height() -1.2*offset))
    pipeX = screenwidth+10
    y1=pipeHeight-y2+offset
    pipes = [
        {'x':pipeX, 'y': -y1},
        {'x':pipeX, 'y': y2}
           
    ]
    return pipes

def welcomeScreen():

    #shows welcome message

    playerx= int(screenwidth/5)
    playery= int((screenheight - game_sprites['player'].get_height())/1.5)
    messagex= int((screenwidth - game_sprites['message'].get_width())/2)
    messagey = int(screenheight*0.03)
    basex = 0
    while True:
        for event in pg.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key== K_ESCAPE):
                pg.quit()
                sys.exit()
            elif event.type==KEYDOWN and (event.key==K_SPACE or event.key==K_UP):
                return
            else:
                SCREEN.blit(game_sprites['background'],(0,0))
                SCREEN.blit(game_sprites['player'],(playerx,playery))
                SCREEN.blit(game_sprites['message'],(messagex,messagey))
                SCREEN.blit(game_sprites['base'],(basex,groundy))
                pg.display.update()
                fpsclock.tick(FPS)

def mainGame():
    score =0
    playerx = int(screenwidth/5)
    playery=int(screenheight/2)
    basex =0

    #creating pipes
    newPipe1 = getRandomPipe()
    newPipe2 = getRandomPipe()

    #list of upper pipes
    upperPipes = [
        {'x': screenwidth+200,'y':newPipe1[0]['y']},
        {'x': screenwidth+200+(screenwidth/2),'y':newPipe2[0]['y']},
    ]
    #list of lower pipes
    lowerPipes = [
        {'x': screenwidth+200,'y':newPipe1[1]['y']},
        {'x': screenwidth+200+(screenwidth/2),'y':newPipe2[1]['y']},
    ]  
    

    speedpipe = -4

    playerVelY = -9
    playerMaxVelY = 10
    playerMinVelY = -8
    playerAccY = 1

    playerFlapAccV = -8 #velocity while flapping
    playerFlapped = False #it is true only when the bird is flapping

    while True:
        for event in pg.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pg.quit()
                sys.exit()

            if event.type == KEYDOWN and (event.key == K_SPACE or event.key==K_UP):
                if playery > 0:
                    playerVelY = playerFlapAccV
                    playerFlapped = True
                    game_sounds['wing'].play()


        crashTest= isCollide(playerx,playery,upperPipes,lowerPipes)
        if crashTest:
            return

        #CHECK FOR SCORE AND INCREMENT IN SPEED
        playerMidPos = playerx + game_sprites['player'].get_width()/2
        for pipe in upperPipes:
            pipeMidPos = pipe['x'] + game_sprites['pipe'][0].get_width()/2
            if pipeMidPos<= playerMidPos < pipeMidPos+(-speedpipe):
                score +=1
                if score%10==0:
                    speedpipe=speedpipe-1.5
                print(f"Your score is {score}")
                game_sounds['point'].play()

        if playerVelY < playerMaxVelY and not playerFlapped:
            playerVelY += playerAccY

        if playerFlapped:
             playerFlapped= False
        playerHeight = game_sprites['player'].get_height()
        playery = playery + playerVelY

        #move pipes to left
        for upperPipe , lowerPipe in zip(upperPipes, lowerPipes):
            upperPipe['x'] += speedpipe
            lowerPipe['x'] += speedpipe

        #add a new piep when the first is about to leave
        if 0<upperPipes[0]['x']<(-speedpipe+1):
            newpipe = getRandomPipe()
            upperPipes.append(newpipe[0])
            lowerPipes.append(newpipe[1])


        #remove pipe if out of the screen
        if upperPipes[0]['x'] < -game_sprites['pipe'][0].get_width():
            upperPipes.pop(0)
            lowerPipes.pop(0)

        #lets blit our sprites now
        SCREEN.blit(game_sprites['background'],(0,0))
        #blit pipes
        for upperPipe, lowerPipe in zip(upperPipes, lowerPipes):
            SCREEN.blit(game_sprites['pipe'][0],(upperPipe['x'],upperPipe['y']))
            SCREEN.blit(game_sprites['pipe'][1],(lowerPipe['x'],lowerPipe['y']))

        SCREEN.blit(game_sprites['base'],(basex,groundy))
        SCREEN.blit(game_sprites['player'],(playerx,playery))

        myDigits = [int(x) for x in list(str(score))]
        width = 0
        for digit in myDigits:
            width += game_sprites['numbers'][digit].get_width()

        Xoffset = (screenwidth - width)/2
        for digit in myDigits:
            SCREEN.blit(game_sprites['numbers'][digit],(Xoffset, screenheight*0.12))
            Xoffset += game_sprites['numbers'][digit].get_width()
        pg.display.update()
        fpsclock.tick(FPS)

def gameover():

    #shows welcome message

    playerx= int(screenwidth/5)
    playery= int((screenheight - game_sprites['player'].get_height())/1.5)
    messagex= int((screenwidth - game_sprites['message'].get_width())/2)
    messagey = int(screenheight*0.03)
    basex = 0
    while True:
        for event in pg.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key== K_ESCAPE):
                pg.quit()
                sys.exit()
            elif event.type==KEYDOWN and (event.key==K_SPACE or event.key==K_UP):
                return
            else:
                SCREEN.blit(game_sprites['background'],(0,0))
                SCREEN.blit(game_sprites['player'],(playerx,playery))
                SCREEN.blit(game_sprites['over'],(messagex,messagey))
                SCREEN.blit(game_sprites['base'],(basex,groundy))
                pg.display.update()
                fpsclock.tick(FPS)

if __name__ == "__main__":
    pg.init() #initialize pygame modules
    fpsclock= pg.time.Clock()
    pg.display.set_caption("Flying Fish")

    #game sprites
    game_sprites['numbers'] = (
        pg.image.load('gallery/sprites/0.png').convert_alpha(),
        pg.image.load('gallery/sprites/1.png').convert_alpha(),
        pg.image.load('gallery/sprites/2.png').convert_alpha(),
        pg.image.load('gallery/sprites/3.png').convert_alpha(),
        pg.image.load('gallery/sprites/4.png').convert_alpha(),
        pg.image.load('gallery/sprites/5.png').convert_alpha(),
        pg.image.load('gallery/sprites/6.png').convert_alpha(),
        pg.image.load('gallery/sprites/7.png').convert_alpha(),
        pg.image.load('gallery/sprites/8.png').convert_alpha(),
        pg.image.load('gallery/sprites/9.png').convert_alpha(),
    )
    game_sprites['message'] = pg.image.load("gallery/sprites/message.png").convert_alpha()
    game_sprites['over'] = pg.image.load("gallery/sprites/gameover.png").convert_alpha()
    game_sprites['pipe'] = (
        pg.transform.rotate(pg.image.load(PIPE).convert_alpha(),180),
        pg.image.load(PIPE).convert_alpha()
    )
    game_sprites['background']= pg.image.load(background).convert()
    game_sprites['player'] = pg.image.load(player).convert_alpha()
    game_sprites['base']=pg.image.load("gallery/sprites/base.png").convert_alpha()

    #game sounds
    game_sounds['die'] = pg.mixer.Sound("gallery/audio/die.wav")
    game_sounds['hit'] = pg.mixer.Sound("gallery/audio/hit.wav")
    game_sounds['point'] = pg.mixer.Sound("gallery/audio/point.wav")
    game_sounds['swoosh'] = pg.mixer.Sound("gallery/audio/swoosh.wav")
    game_sounds['wing'] = pg.mixer.Sound("gallery/audio/wing.wav")

    while True:
        welcomeScreen()
        mainGame()
        gameover()


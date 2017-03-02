import time
import random
import pygame
import math
import shelve
from collections import deque
import pygame.font, pygame.event, pygame.draw, string
from pygame.locals import *
import operator


#########################################################################
#########################################################################
###### CONSTANTS ######
#########################################################################
#########################################################################
WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (200,20,0)
GREEN = (0, 220,10)
BLUE = (50, 50, 150)
FPS = 10
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600
SCREEN_SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT)
SCALE = 40
#########################################################################
#########################################################################
#########################################################################
#################  SNAKE GAME  ##########################################
#########################################################################
#########################################################################
class SnakeGame(object):
    #########################################################################
    # INITIALIZE ############################################################
    #########################################################################

    def __init__(self):
        self.SNAKE_ALIVE = True
        self.gameExit = False
        self.gameOver = False
        self.score = 0
        self.snake = Snake()

        self.showScores = False
        self.showGameOver = False

        self.apples = [Apple(), Apple(), Apple(), Apple(), Apple(), Apple()]
        self.snake.grow()

        self.powerUp = pygame.mixer.Sound('Powerup1.wav')
        self.hurt = pygame.mixer.Sound('Hurt.wav')
        self.image = pygame.Surface([SCREEN_WIDTH, SCREEN_HEIGHT])

        # Fetch the rectangle object that has the dimensions of the image
        # Update the position of this object by setting the values of rect.x and rect.y
        self.image = pygame.image.load("SpaceBackground.gif").convert_alpha()
        self.image = pygame.transform.scale(self.image, (SCREEN_WIDTH, SCREEN_HEIGHT))
        #
        self.scoreFont = pygame.font.SysFont(None, 40)

        self.eventQueue = deque()




    #########################################################################
    ##### EVENT HANDLING  ##########################
    #########################################################################
    def process_events(self, screen):
        # SNAKE CRASHED



        if self.SNAKE_ALIVE:
            if self.snake.snake_body[0].rect.x + SCALE/2 >= SCREEN_WIDTH or self.snake.snake_body[0].rect.x + 5< 0:
                print ('x crash')
                self.gameOver = True
                self.hurt.play()
            if self.snake.snake_body[0].rect.y + SCALE/2 >= SCREEN_HEIGHT or self.snake.snake_body[0].rect.y + 5 < 0:
                self.SNAKE_ALIVE = False
                print ('y crash')
                self.gameOver = True
                self.hurt.play()
                self.SNAKE_ALIVE = False
            if self.snake.die():
                print ('snake hit itself')
                self.gameOver = True
                self.hurt.play()
                self.SNAKE_ALIVE = False

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    self.eventQueue.append(event)

            if self.eventQueue:
                event = self.eventQueue.popleft()
                print(event)
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    if self.snake.snake_body[0].x_vel == 0:
                        self.snake.setVelocity(-1 * SCALE, 0)
                    # break
                elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    if self.snake.snake_body[0].x_vel == 0:
                            self.snake.setVelocity(SCALE, 0)
                            #     break
                elif event.key == pygame.K_UP or event.key == pygame.K_w:
                    if self.snake.snake_body[0].y_vel == 0:
                            self.snake.setVelocity(0, -1 * SCALE)
                    # break
                elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    if self.snake.snake_body[0].y_vel == 0 and self.snake.snake_body[0].x_vel != 0:
                       self.snake.setVelocity(0, SCALE)
                            #      break

            for i in range(len(self.apples)):
                dist = Distance(self.snake.snake_body[0].rect.x, self.apples[i].x_pos, self.snake.snake_body[0].rect.y, self.apples[i].y_pos)
                if dist < SCALE:
                    self.powerUp.play()
                    self.snake.grow()
                    self.snake.grow()
                    self.apples[i].respawn()


        Bigfont = pygame.font.SysFont(None, 150)
        Medfont = pygame.font.SysFont(None, 50)
        Score = (len(self.snake.snake_body)-1)/2




        if self.SNAKE_ALIVE == False:
            screen.fill(GREEN)
            self.DrawScores(screen)



            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.gameExit = True
                    self.gameOver = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        self.gameExit = True
                        self.gameOver = False
                    if event.key == pygame.K_s:
                        user_Name = self.ask(screen, "NAME")
                        self.EnterScore(user_Name, Score)
                    if event.key == pygame.K_r:
                        self.SNAKE_ALIVE = True
                        self.__init__()
            screen.blit(Medfont.render("S to save highscores!", True, RED), [302, 79])









        pygame.display.flip()

    def display_box(self, screen, name):
        fontobject = pygame.font.Font(None, 30)

        # NAME BOX
        pygame.draw.rect(screen, (0, 0, 0),
                         (302, 79,
                          300, 30), 0)
        pygame.draw.rect(screen, WHITE,
                          (300, 77,
                          304, 34), 1)

        if len(name) != 0:
            screen.blit(fontobject.render(name, 1, (255, 255, 255)),
                        (302, 85))
        pygame.display.flip()

    def ask(self, screen, question1):
        pygame.font.init()
        name = []
        self.display_box(screen, question1 + "-> " + string.join(name, ""))
        while 1:
            inkey = get_key()
            if inkey == K_BACKSPACE:
                name = name[0:-1]
            elif inkey == K_RETURN:
                break
            elif inkey == K_MINUS:
                name.append("_")
            elif inkey <= 127:
                name.append(chr(inkey))
            elif inkey <= 127:
                name.append(chr(inkey))
            print("DISPLAYBOXIN")
            self.display_box(screen, question1 + "-> " + string.join(name, ""))

        return string.join(name, "")

    def run_logic(self):

        self.snake.move()

    #########################################################################
    def display_frame(self, screen):
        if not self.gameOver:

            screen.blit(self.image, (0,0))
            # screen.fill(GREEN)

            Score = "SCORE:  " + str((len(self.snake.snake_body)-1)/2)
            self.scoreText = self.scoreFont.render(Score, True, RED)

            for x in range(len(self.apples)):
                self.apples[x].draw(screen)
            self.snake.draw(screen)
            screen.blit(self.scoreText, [50, SCREEN_HEIGHT-50])
            self.drawBorders(screen)


        else:
            screen.fill(BLACK)

    def drawBorders(self, screen):
        pygame.draw.rect(screen, (255,22,0),(0, 0, SCREEN_WIDTH, 10), 10)
        pygame.draw.rect(screen, (255,22,0),(0, SCREEN_HEIGHT-10, SCREEN_WIDTH, 10), 10)
        pygame.draw.rect(screen, (255,22,0),(0, 0, 10, SCREEN_HEIGHT), 10)
        pygame.draw.rect(screen, (255,22,0),(SCREEN_WIDTH-10, 0, 10, SCREEN_HEIGHT), 10)


    def DrawScores(self, screen):
        Bigfont = pygame.font.SysFont(None, 75)
        Medfont = pygame.font.SysFont(None, 35)

        d = self.LoadScores()
        sorted_d = sorted(d.items(), key=operator.itemgetter(1))
        HighScore_text = Bigfont.render("HIGH SCORES: ", True, BLACK)
        screen.blit(HighScore_text, [SCREEN_WIDTH/4, 20])
        sorted_d.reverse()
        for x in range(len(sorted_d)):
            screen.blit(Medfont.render(str(x+1), True, BLACK), [(SCREEN_WIDTH-160)/4, 100 + (x+1)*30])
            screen.blit(Medfont.render(sorted_d[x][0], True, RED), [SCREEN_WIDTH/4, 100 + (x+1)*30])
            screen.blit(Medfont.render(str(sorted_d[x][1]), True, RED), [SCREEN_WIDTH/4+ 400, 100 + (x+1)*30])


    def EnterScore(self, name, score):
        d = shelve.open('score.txt') # here you will save the score variable
        d[name] = score         # thats all, now it is saved on disk.
        d.close()


    def LoadScores(self):
        d = shelve.open('score.txt')
        return d





#########################################################################
#########################################################################

#########################################################################
###########################  SNAKE  #####################################
#########################################################################
#########################################################################
class Snake(object):

    def __init__(self):
        self.all_sprites = pygame.sprite.Group()

        self.block = Block(SCREEN_WIDTH/2, SCREEN_HEIGHT/2, True)

        self.all_sprites.add(self.block)
        self.BlockCount = 0
        self.snake_body = [self.block]
        #self.snake_body = [Block(SCREEN_WIDTH/2, SCREEN_HEIGHT/2)]
    def move(self):

        for i in reversed(range(1, self.BlockCount + 1)):
            if self.snake_body[0].x_vel == 0 and self.snake_body[0].y_vel == 0:
                break
            self.snake_body[i].rect.x = int(round(self.snake_body[i-1].rect.x, -1))
            self.snake_body[i].rect.y = int(round(self.snake_body[i-1].rect.y, -1))

        self.snake_body[0].move()


    def setVelocity(self, x, y):

        self.snake_body[0].setVelocity(x, y)


    def draw(self, screen):


        background = pygame.Surface(screen.get_size())
        background = background.convert()
        for i in range(self.BlockCount + 1):
            self.all_sprites.add(self.snake_body[i])
        self.all_sprites.update()
        self.all_sprites.draw(screen)

    def grow(self):
        oreintation = self.findOrirentation(self.snake_body[self.BlockCount].x_vel, self.snake_body[self.BlockCount].y_vel)
        x_increment = 0
        y_increment = 0

        if oreintation == 0:
            y_increment = SCALE
        elif oreintation == 1:
            x_increment = -1 * SCALE
        elif oreintation == 2:
            y_increment = -1 * SCALE
        elif oreintation == 3:
            x_increment = SCALE


        self.snake_body.append(Block(self.snake_body[self.BlockCount].rect.x + x_increment,self.snake_body[self.BlockCount].rect.y + y_increment))
        self.BlockCount += 1
    def printcoordinates(self):
        pass
        #   for i in range(self.BlockCount+1):
        #print 'block: ', i
        # print 'x',  self.snake_body[i].rect.x
        # print 'y',  self.snake_body[i].rect.y
    def findOrirentation(self, x, y):
        # NORTH = 0
        # EAST = 1
        # SOUTH = 2
        # WEST = 3


        if(x ==0 and y == 0):
            return 0
        if(x == 0 and y < 0):
            return 0
        if(x > 0 and y  == 0):
            return 1
        if(x == 0 and y > 0):
            return 2
        if(x < 0 and y == 0):
            return 3


    def die(self):
        for i in range(5, self.BlockCount):
            if Distance(self.snake_body[0].rect.x + SCALE/2, self.snake_body[i].rect.x + SCALE/2,self.snake_body[0].rect.y + SCALE/2 ,self.snake_body[i].rect.y + SCALE/2) < 2:
                print ("0 hit " + str(i))
                return True
        return False


class Block(pygame.sprite.Sprite):

    def __init__(self, x_cord, y_cord, head = False):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([SCALE, SCALE])

        if head == True:
            self.image = pygame.image.load("GlorpHead.png").convert_alpha()
        else:
            self.image = pygame.image.load("GlorpBody.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (SCALE, SCALE))
        self.rect = self.image.get_rect()
        self.rect.x = int(round(x_cord, -1))
        self.rect.y = int(round(y_cord, -1))


        self.x_cord = int(round(x_cord, -1))
        self.y_cord = int(round(y_cord, -1))
        self.x_vel = 0
        self.y_vel = 0

    def move(self):
        self.rect.x += self.x_vel
        self.rect.y += self.y_vel
        self.rect.x = int(round(self.rect.x, -1))
        self.rect.y = int(round(self.rect.y, -1))

    def setVelocity(self, x, y):
        self.x_vel = x
        self.y_vel = y

def Distance(x1, x2, y1, y2):
    delta_x = ((x1-x2)**2)
    delta_y = ((y1-y2)**2)
    return math.sqrt((delta_x+delta_y))

#########################################################################
#########################################################################
######################  APPLE  ##########################################
#########################################################################


class Apple(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.x_pos = int(round(random.randrange(10, SCREEN_WIDTH-SCALE), -1))
        self.y_pos = int(round(random.randrange(10, SCREEN_HEIGHT-SCALE), -1))

        self.image = pygame.Surface([SCALE, SCALE])
        self.image = pygame.image.load("GlorpBall.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (SCALE+10, SCALE+10))
        self.rect = self.image.get_rect()
        self.rect.x = self.x_pos
        self.rect.y = self.y_pos
    def spawn(self, x, y):
        self.x_pos = int(round(x, -1))
        self.y_pos = int(round(y, -1))
    def respawn(self):
        self.x_pos = int(round(random.randrange(10, SCREEN_WIDTH-SCALE), -1))
        self.y_pos = int(round(random.randrange(10, SCREEN_HEIGHT-SCALE), -1))

    def draw(self, screen):
        #pass
        #pygame.draw.rect(screen, WHITE, [self.x_pos, self.y_pos, SCALE, SCALE])
        # pygame.draw.rect(screen, WHITE, [self.x_pos, self.y_pos, SCALE, SCALE])
        screen.blit(self.image, (self.x_pos, self.y_pos))

#########################################################################
#########################################################################

def get_key():
    while 1:
        event = pygame.event.poll()
        if event.type == KEYDOWN:
            return event.key
        else:
            pass

#########################################################################
##########################  MAIN  #######################################
#########################################################################
#########################################################################
def main():
    pygame.mixer.pre_init(44100, -16, 2, 2048) # setup mixer to avoid sound lag
    pygame.init()
    screen = pygame.display.set_mode(SCREEN_SIZE)
    pygame.display.set_caption('~~~~~ IM A SNAKE IM A SNAKE IM A SNAKE ~~~~~')
    pygame.mouse.set_visible(False)

    clock = pygame.time.Clock()
    game = SnakeGame()
    pygame.mixer.music.load('Sandstorm.ogg')

    #  pygame.mixer.music.play(-1, 30)
    while not game.gameExit:


        #   game.snake.printcoordinates()
        # Process events
        game.process_events(screen)
        # Update object positions, check for collisions
        game.run_logic()
        # Draw the curent frame
        game.display_frame(screen)
        clock.tick(FPS)
    pygame.quit()

#########################################################################
#########################################################################
#########################################################################
#########################################################################
#########################################################################
#########################################################################


main()






import pygame
from pygame.locals import *
import time 
pygame.init()

screen_width=1100
screen_height=800

screen = pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption('Platformer Ball Game')

#load images

# sun_img = pygame.image.loaf('Images/sun.png')
bg_img=pygame.image.load('Images/bg_img.jpeg')

def drawGridWithTileSize(tile_size):
    # draw vertical lines
    N_ver= round(screen_width/tile_size) - 1
    white=(255,255,255)
    for i in range(0,N_ver):
        start_pos=(tile_size*(i+1),0)
        end_pos=(tile_size*(i+1),screen_height)
        pygame.draw.line(screen,white,start_pos,end_pos,1)
    N_hor= round(screen_height/tile_size) - 1
    for i in range(0,N_hor):
        start_pos=(0,tile_size*(i+1))
        end_pos=(screen_width,tile_size*(i+1))
        pygame.draw.line(screen,white,start_pos,end_pos,1)
tile_Size=100
# world_data =      

run = True  
while run:
    #screen.blit() => a function to paint a picture on the screen
    screen.blit(bg_img,(0,0)) # start_x, start_y
    drawGridWithTileSize(tile_Size) 
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            run=False
    pygame.display.update()
pygame.quit()

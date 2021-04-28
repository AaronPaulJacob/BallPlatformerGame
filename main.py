import pygame
from pygame.locals import *
import time 
pygame.init()

screen_width= 1000      # default = 1100
screen_height=800      # default = 800
tile_Size=100   #default 100
screen = pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption('Platformer Ball Game')

#load images
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
    # draw horizontal lines
    for i in range(0,N_hor):
        start_pos=(0,tile_size*(i+1))
        end_pos=(screen_width,tile_size*(i+1))
        pygame.draw.line(screen,white,start_pos,end_pos,1)

class World():
    def __init__(self):
        self.tile_list = []  # will store list of images and their rectangle objects (storing coordinate informations)
        #load images
        wall_bg = pygame.image.load('Images/wall.png')
        grass_bg=pygame.image.load('Images/Grass.jpeg')
        row_count=0
        # for row in data:
        #     col_count=0
        #     for tile in row:
        #         if tile ==1 : # 1 => Ground grass 
        #             grass = pygame.transform.scale(grass_bg,(tile_Size,tile_Size))
        #             grass_rect=grass.get_rect()
        #             grass_rect.x = col_count * tile_Size
        #             grass_rect.y = row_count * tile_Size
        #             self.tile_list.append( (grass,grass_rect) )
        #         elif tile == 3 : # 1 => Side wall 
        #             wall = pygame.transform.scale(wall_bg,(tile_Size,tile_Size))
        #             wall_rect=wall.get_rect()
        #             wall_rect.x = col_count * tile_Size
        #             wall_rect.y = row_count * tile_Size
        #             self.tile_list.append( (wall,wall_rect) )
        #         col_count += 1
        #     row_count += 1
    def draw(self):
        for tile in self.tile_list:
            img = tile[0]
            pos = tile[1]
            screen.blit(img,pos)




# world_data = [
# [3,3,3,3,3],
# [3,0,0,0,3],
# [3,0,0,0,3],
# [3,0,0,0,3],
# [3,3,3,3,3]
# ]     

world = World()
run = True  
while run:
    #screen.blit() => a function to paint a picture on the screen
    screen.blit(bg_img,(0,0)) # start_x, start_y
    world.draw()
    # drawGridWithTileSize(tile_Size) 
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            run=False
    pygame.display.update()
pygame.quit()

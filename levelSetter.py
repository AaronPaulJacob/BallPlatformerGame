import pygame 
import pickle
from os import path
import os
pygame.init()
clock = pygame.time.Clock()
fps = 60
# gameWindow
screen_width= 1000     # default = 1100
screen_height=800      # default = 800
tile_Size=100          #default 100

screen = pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption("Level Maker")

#load images
bg_img=pygame.image.load('Images/bg_img.jpeg')
entries = os.listdir('./Images')
img_List=[]
for i in range(1,len(entries)):
    c_path='Images/'
    c_path+=entries[i]
    curr_img=pygame.image.load(c_path)
    # print(entries[i])
    img_List.append(curr_img)


#define game variables
clicked = False
level = 1

white = (255,255,255)
green = (144,201,120)

font = pygame.font.SysFont('Futura',24)

#create empty tile list
world_data= []
N_row= round(screen_height/tile_Size)
N_col= round(screen_width/tile_Size)

for row in range(N_row):
    r = [0] * N_col
    world_data.append(r)

#create Boundary
# row boundary
for x in range(N_col):
    world_data[0][x]= 1 #black boundary
    world_data[N_row-1][x]=2 # grass boundary
for y in range(N_row):
    world_data[y][0] = 1
    world_data[y][N_col-1] = 1

def draw_text(text,font,col,x,y):
    img = font.render(text, True, col)
    screen.blit(img, (x,y))

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


def draw_world():
    for row in range(N_row):
        for col in range(N_col):
            if world_data[row][col] > 0 :
                # traverse over all the images and see if it matches any image
                for i in range(len(img_List)):
                    if world_data[row][col] == i+1:
                        img = pygame.transform.scale(img_List[i],(tile_Size,tile_Size))
                        screen.blit(img,(col*tile_Size,row*tile_Size)) 

class Button():
    def __init__(self, x,y,image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft= (x,y)
        self.clicked = False
    def draw(self):
        action = False # ?
        # get mouse position 
        pos = pygame.mouse.get_pos()

        #check mouseover and clicked conditions
        if self.rect.collidepoint(pos): # checking if mouse position is on the button
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                action = True
                self.clicked = True
        if pygame.mouse.get_pressed()[0] == 0 :
            self.clicked = False
        
        #draw button
        screen.blit(self.image,(self.rect.x,self.rect.y))
        return action

loadBtn = pygame.image.load('Buttons/loadBtn.png')
saveBtn = pygame.image.load('Buttons/saveBtn.png')

# create load and save buttons
save_button = Button(screen_width // 2 - 150, screen_height-80,saveBtn)
load_button = Button(screen_width // 2 + 50, screen_height-80, loadBtn)

run = True

while run:
    clock.tick(fps) # ?

    #draw background
    screen.fill(green)
    screen.blit(bg_img,(0,0))

    #load and save level
    if save_button.draw(): # returns if the button was clicked by determining the mouse postion coordinates
        pickle_out = open(f'level{level}_data', 'wb')
        pickle.dump(world_data, pickle_out)
        pickle_out.close()
    
    if load_button.draw():
        #load in level data
        if path.exists(f'level{level}_data'):
            pickle_in = open(f'level{level}_data', 'rb')
            world_data = pickle.load(pickle_in)

    draw_world()
    drawGridWithTileSize(tile_Size)

    #text showing current level
    draw_text(f'Level: {level}', font, white, tile_Size, screen_height - 60)
    draw_text('Press UP or DOWN to change level', font, white, tile_Size, screen_height - 40)

    for event in pygame.event.get():
        # quit game
        if event.type == pygame.QUIT:
            run = False
        
        #mouseclicks to change tiles
        if event.type == pygame.MOUSEBUTTONDOWN and clicked == False:
            clicked= True
            pos = pygame.mouse.get_pos()
            x = pos[0] // tile_Size
            y = pos[1] // tile_Size
            # check that the coordinates are within the tile area
            if x < N_col and y < N_row :
                if pygame.mouse.get_pressed()[0] == 1:
                    world_data[y][x] = (world_data[y][x]+1)%(len(img_List)+1) # will cycle over all the images
                elif pygame.mouse.get_pressed()[2] == 1:
                    world_data[y][x] -= 1
                    if(world_data[y][x]<0):
                        world_data[y][x]=len(img_List)
            if event.type == pygame.MOUSEBUTTONUP:
                clicked = False
		#up and down key presses to change level number
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                level += 1
            elif event.key == pygame.K_DOWN and level > 1:
                level -= 1
    #update game display window
    pygame.display.update()
    
pygame.quit()          
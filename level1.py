import pygame 
import pickle
from os import path
import os
pygame.init()
level=1


# gameWindow
screen_width= 1000     # default = 1100
screen_height=800      # default = 800
tile_Size=50          #default 100

screen = pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption("Level "+str(level))

img_List=[]
#load images
bg_img=pygame.image.load('Images/bg_img.jpeg')
wall_idx=0
def loadImages():
    entries = os.listdir('./Images')
    # print(entries[1])
    for i in range(0,len(entries)):
        if entries[i]=='bg_img.jpeg' or entries[i] == '.DS_Store':
            continue 
        if entries[i] == 'SideWall.png':
            wall_idx=len(img_List)
        c_path='Images/'
        c_path+=entries[i]
        curr_img=pygame.image.load(c_path)
        # print(entries[i])
        img_List.append(curr_img)
    print("Number of images loaded:"+ str(len(img_List)))
loadImages()

#define game variables
clicked = False
white = (255,255,255)
font = pygame.font.SysFont('Futura',24)

#create empty tile list
world_data= []
N_row= round(screen_height/tile_Size)
N_col= round(screen_width/tile_Size)
# for row in range(N_row):
#     r = [0] * N_col
#     world_data.append(r)
#Loading level1 world data from the file
if path.exists(f'level{level}_data'):
            pickle_in = open(f'level{level}_data', 'rb')
            world_data = pickle.load(pickle_in)
def draw_text(text,font,col,x,y):
    img = font.render(text, True, col)
    screen.blit(img, (x,y))


class World():
    def __init__(self,data):
        self.tile_list = []  # will store list of images and their rectangle objects (storing coordinate informations)
        #load images
        for row in range(N_row):
            for col in range(N_col):
                # traverse over all the images and see if it matches any image
                for i in range(len(img_List)):
                    if world_data[row][col] == i+1:
                        img = pygame.transform.scale(img_List[i],(tile_Size,tile_Size))
                        img_rect=img.get_rect()
                        img_rect.x = col * tile_Size
                        img_rect.y = row * tile_Size
                        self.tile_list.append( (img,img_rect) )
    def draw(self):
        for tile in self.tile_list:
            img = tile[0]
            pos = tile[1]
            screen.blit(img,pos)

class Player():
    def __init__(self, x ,y):
        img = pygame.image.load('Images/red_ball.png')
        self.image = pygame.transform.scale(img,(tile_Size,tile_Size))
        self.rect= self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.vel_y = 0 # upward velocity on pressing space
        self.jumped = False # Have I jumped or not by pressing the space button

    def update(self):
        dx = 0
        dy = 0
        #get keypresses
        key = pygame.key.get_pressed()
        if key[pygame.K_SPACE] and self.jumped == False :  # to allow only 1 jump
            self.vel_y = -15
            self.jumped = True 
        if key[pygame.K_SPACE] ==  False: 
            self.jumped = False

        if key[pygame.K_LEFT]:
            dx -= 5
        if key[pygame.K_RIGHT]:
            dx += 5
        #calculate new player position and check collision at new position 

        #adding gravity
        self.vel_y += 1
        if self.vel_y >10:
            self.vel_y=10 # setting a limit to gravity i.e. falling down
        dy += self.vel_y
        #check collision

        #update player coordinates
        # print("shift")
        self.rect.x += dx
        self.rect.y += dy

        if self.rect.bottom > screen_height-tile_Size :
            self.rect.bottom = screen_height-tile_Size
            dy=0
            self.vel_y=0

        #draw player on screen
        screen.blit(self.image,self.rect)


world = World(world_data)
player = Player(2*tile_Size,screen_height-2*tile_Size)        
run = True
count = 0
print("Openeing Game Window")
while run:
    #draw background
    screen.blit(bg_img,(0,0))
    count +=1
    world.draw()
    player.update()

    for event in pygame.event.get():
        # quit game
        if event.type == pygame.QUIT:
            run = False

    #update game display window
    pygame.display.update()

print("Count:"+str(count))
pygame.quit()          
import pygame 
import pickle
from os import path
import os
pygame.init()
level=1

clock = pygame.time.Clock()
fps = 80

# gameWindow
screen_width= 1000     # default = 1100
screen_height=800      # default = 800
tile_Size=50          #default 100
main_menu=True

# buttons



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
game_over=0

#create empty tile list
world_data= []
N_row= round(screen_height/tile_Size)
N_col= round(screen_width/tile_Size)
# for row in range(N_row):
#     r = [0] * N_col
#     world_data.append(r)
#Loading level1 world data from the file
# if path.exists(f'level{level}_data'):
#             pickle_in = open(f'level{level}_data', 'rb')
#             world_data = pickle.load(pickle_in)
#             print(world_data)
world_data = [[2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
              [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2], 
              [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8, 0, 2], 
              [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 2], 
              [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 2], 
              [2, 0, 0, 0, 0, 0, 0, 0, 0, 5, 1, 0, 0, 0, 0, 0, 0, 0, 0, 2], 
              [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2], 
              [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 11, 11, 1, 1, 1, 1, 1, 2], 
              [2, 0, 11, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2], 
              [2, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2], 
              [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 9, 9, 9, 0, 0, 0, 0, 0, 0, 2], 
              [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 6, 6, 6, 0, 0, 0, 1, 1, 1, 2], 
              [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2], 
              [2, 1, 1, 1, 1, 1, 0, 0, 1, 1, 0, 0, 0, 0, 1, 1, 1, 0, 0, 2], 
              [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2], 
              [2, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 2]]

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
                # for i in range(len(img_List)):
                idx_blk=world_data[row][col]
                if idx_blk !=0 :
                    img = pygame.transform.scale(img_List[idx_blk-1],(tile_Size,tile_Size))
                    img_rect=img.get_rect()
                    img_rect.x = col * tile_Size
                    img_rect.y = row * tile_Size
                    self.tile_list.append( (img,img_rect) )
    def draw(self):
        for tile in self.tile_list:
            img = tile[0]
            pos = tile[1]
            screen.blit(img,pos)
            # pygame.draw.rect(screen,(255,255,255),pos,2)

class Player():
    def __init__(self, x ,y):
        # creating a series of images for moving animation 
        self.images_right = []
        self.images_left = []
        self.index=0
        self.counter=0 # speed of player animaion
        for num in range(1,9):
            img_right =  pygame.image.load(f'Ball/redBall{num}.png')
            img_right = pygame.transform.scale(img_right,(tile_Size,tile_Size))
            img_left = pygame.transform.flip(img_right, True,False) # flip the image across x axis but not across y axis
            self.images_right.append(img_right)
            self.images_left.append(img_left)
        print(len(self.images_left))
        print(len(self.images_right))
        self.image = self.images_right[self.index]
        self.direction = 0
        #************************ end of animation
              
        # img = pygame.image.load('Images/red_ball.png')
        # self.image = pygame.transform.scale(img,(tile_Size,tile_Size))
        # print("Image")
        # print(self.image)
        self.rect= self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        # print(self.rect)
        self.vel_y = 0 # upward velocity on pressing space
        self.jumped = False # Have I jumped or not by pressing the space button

    def update(self,game_over):
        dx = 0
        dy = 0
        walk_cooldown = 1

        if game_over == 0:
            #get keypresses
            key = pygame.key.get_pressed()
            if key[pygame.K_SPACE] and self.jumped == False and self.in_air == False :  # to allow only 1 jump 
                self.vel_y = -15
                self.jumped = True 
            if key[pygame.K_SPACE] ==  False: 
                self.jumped = False
            if key[pygame.K_LEFT]:
                dx -= 5
                self.direction = -1
                self.counter += 1   # cycle through images only when the left or right keys are pressed 
                # if counter is incremented and exceedds the walk_cooldown only then the image index will be incremented
            if key[pygame.K_RIGHT]:
                dx += 5
                self.counter += 1
                self.direction = 1
            # if key[pygame.K_LEFT] == False and key[pygame.K_RIGHT] == False:
            #     self.counter=0
            #     if self. direction == 1:
            #         self.image = self.images_right[self.index]
            #     if self.direction == -1:
            #         self.image = self.images_left[self.index]
            #     self.index=0    # so that animation returns to begining image
                
            #handle animation
            # print(self.counter)
            if self.counter > walk_cooldown:
                self.counter=0
                self.index =(self.index+1)%(len(self.images_right)) # cycling through the images
                if self.direction == 1:
                    self.image = self.images_right[self.index]
                if self.direction == -1:
                    self.image = self.images_left[self.index]
            #calculate new player position and check collision at new position 

            #adding gravity
            self.vel_y += 1
            if self.vel_y >10:
                self.vel_y=10 # setting a limit to gravity i.e. falling down
            dy += self.vel_y
            

            #check collision
            self.in_air = True
            for tile in world.tile_list:
                #check for collision in x direction
                if tile[1].colliderect(self.rect.x+dx ,self.rect.y ,self.width, self.height):
                    dx = 0
                #check for collision in y direction
                if tile[1].colliderect(self.rect.x ,self.rect.y+dy ,self.width, self.height):
                    # if collision is taking place then check
                    
                    # check if below the ground i.e. jumping
                    if self.vel_y < 0:
                        dy = tile[1].bottom - self.rect.top # resetting the change dy so that it may not go above the block
                        self.vel_y = 0
                    #check ig above the ground i.e. falling
                    elif self.vel_y >= 0 :
                        dy = tile[1].top - self.rect.bottom
                        self.vel_y = 0
                        self.in_air = False

            #update player coordinates
            self.rect.x += dx
            self.rect.y += dy

            # checking player does not fall of the screen due to gravity
            if self.rect.bottom > screen_height-tile_Size :
                self.rect.bottom = screen_height-tile_Size
                dy=0
                self.vel_y=0
        
        #draw player on screen
        screen.blit(self.image,self.rect)
        # pygame.draw.rect(screen,(255,255,255),self.rect,2)
        return game_over

class Button():
	def __init__(self, x, y, image):
		self.image = image
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y
		self.clicked = False

	def draw(self):
		action = False

		#get mouse position
		pos = pygame.mouse.get_pos()

		#check mouseover and clicked conditions
		if self.rect.collidepoint(pos):
			if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
				action = True
				self.clicked = True

		if pygame.mouse.get_pressed()[0] == 0:
			self.clicked = False


		#draw button
		screen.blit(self.image, self.rect)

		return action


world = World(world_data)
player = Player(2*tile_Size,screen_height-2*tile_Size)        
run = True
count = 0
print("Opening Game Window")

#Load button images
restart_img = pygame.image.load('Static_Img/restart_btn.png')
restart_img = pygame.transform.scale(restart_img,(4*tile_Size,2*tile_Size))
start_img = pygame.image.load('Static_Img/start_btn.png')
start_img = pygame.transform.scale(start_img,(4*tile_Size,2*tile_Size))
exit_img = pygame.image.load('Static_Img/exit_btn.png')
exit_img = pygame.transform.scale(exit_img,(4*tile_Size,2*tile_Size))

#create buttons
restart_button = Button(screen_width // 2 - 50, screen_height // 2 + 100, restart_img)
start_button = Button(screen_width // 2 - 350, screen_height // 2, start_img)
exit_button = Button(screen_width // 2 + 150, screen_height // 2, exit_img)
print('Here')
while run:
    clock.tick(fps)

    #draw background
    screen.blit(bg_img,(0,0))
    count +=1
    
    if main_menu == True:
        if exit_button.draw():
            run = False
        if start_button.draw():
            main_menu = False
    else:
        world.draw()
        game_over=player.update(game_over)

    for event in pygame.event.get():
        # quit game
        if event.type == pygame.QUIT:
            run = False
    print("Here2")
    #update game display window
    pygame.display.update()

print("Count:"+str(count))
pygame.quit()          

import os
entries = os.listdir('./Images')

print(len(entries))
for i in range(1,len(entries)):
    print(entries[i])
    # bg_img=pygame.image.load('Images/bg_img.jpeg')
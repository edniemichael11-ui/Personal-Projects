import pygame  
from os.path import join
import random
#General Setup
pygame.init()
screen = pygame.display.set_mode((800, 320))

#Imports
backround = pygame.image.load(join('assets', 'backround.png')).convert_alpha()
backround = backround.subsurface((0,0,783,318))
backround = pygame.transform.scale(backround, (800,320))
 #Player Animations Import 
left_animation = []
for i in range(8):
    image = pygame.image.load(f"assets/player/left/left_{i}.png").convert_alpha()
    left_animation.append(image)
for index, image in enumerate(left_animation):
    left_animation[index] = pygame.transform.scale(image,(96,96))
right_animation = []
for i in range(8):
    image = pygame.image.load(f"assets/player/right/right_{i}.png").convert_alpha()
    right_animation.append(image)
for index, image in enumerate(right_animation):
    right_animation[index] = pygame.transform.scale(image,(96,96))

#Variables
x=375
y=220
current_frame = 0
animation_speed = 100
last_update = pygame.time.get_ticks()
direction = "right"
Moving = False




def handle_events():
    for event in pygame.event.get():
           if event.type == pygame.QUIT:  #pygame.QUIT it the event when "X" is clicked
            return  True
    return False
def update():
    global x,y, last_update, current_frame, direction,Moving
    current_time = pygame.time.get_ticks()
    if current_time - last_update >= animation_speed:
        current_frame += 1
        if current_frame >= 8: 
            current_frame = 0
        last_update = current_time
    keys = pygame.key.get_pressed()
    #Movement
    Moving = False
    if keys[pygame.K_LEFT]:
        x -= 5
        direction = "left"
        Moving = True
        
    if keys[pygame.K_RIGHT]:
        x += 5
        direction = "right"
        Moving = True
    #Make sure in window
    if x < 0:
        x= 0
    if x > 704:
        x = 704
    

    
def draw():
    screen.blit(backround, (0,0))
    if direction == "left":
        screen.blit(left_animation[current_frame], (x, y))
    else:
        screen.blit(right_animation[current_frame], (x, y))
    pygame.display.update()


clock = pygame.time.Clock()
game_ended = False
while game_ended == False:
    game_ended = handle_events()
    update()
    draw()

    clock.tick(60)
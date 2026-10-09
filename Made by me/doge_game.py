import pygame  
pygame.init()
screen = pygame.display.set_mode((800, 600))
x=375
y=275
def handle_events():
    for event in pygame.event.get():
           if event.type == pygame.QUIT:  #pygame.QUIT it the event when "X" is clicked
            return  True
    return False
def update():
    global x,y
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        x-=5
    elif keys[pygame.K_RIGHT]:
        x+=5
    elif keys[pygame.K_UP]:
        y-=5
    elif keys[pygame.K_DOWN]:
        y+=5
def draw():
    screen.fill((0, 0, 0))
    rec_color = (255, 0, 0)
    pygame.draw.rect(screen, rec_color, (x, y, 50, 50))
    pygame.display.update()

game_ended = False
while game_ended == False:
    game_ended = handle_events()
    update()
    draw()
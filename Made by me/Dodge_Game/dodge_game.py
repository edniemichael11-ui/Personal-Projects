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
    #Make sure in window
    if x < 0:
        x= 0
    if x > 750:
        x = 750
    if y < 0:
        y = 0
    if y > 550:
        y=550
    #Movement
    if keys[pygame.K_LEFT]:
        x -= 5
    
    if keys[pygame.K_RIGHT]:
        x += 5
    
    if keys[pygame.K_UP]:
        y -= 5
    
    if keys[pygame.K_DOWN]:
        y += 5
def draw():
    screen.fill((0, 0, 0))
    rec_color = (0, 0, 255)
    pygame.draw.circle(screen, rec_color, (x + 25, y + 25), 25)
    pygame.display.update()


clock = pygame.time.Clock()
game_ended = False
while game_ended == False:
    game_ended = handle_events()
    update()
    draw()

    clock.tick(60)
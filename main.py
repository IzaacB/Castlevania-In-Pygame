from settings import *
from player import *
from objects import *
from tile_data import *
from map_data import *

window = pygame.display.set_mode((window_width, window_height), pygame.SCALED, vsync=1)#Create a window.

simon = Player()
debug = Tilemap(test_level[0], test_tiles, 0 ,0)
camera = Camera()

#Start main game loop.
running = True
while running:  
    sprite_layer1 = []
    sprite_layer2 = []
    sprite_layer3 = []

    walls = []
    platforms = []
    decor = []

    delta_time = refresh.tick(refresh_rate)/1000#Get the frametime.
    
    #Tap into pygame event handler.
    for event in pygame.event.get():
        if event.type == pygame.QUIT:#If the X in the window bar is pressed.
            running = False

    keys = pygame.key.get_pressed()

    if simon.x > ((window_width/6) * 3 - 16) + camera.x and camera.x <= 48:
        camera.x += abs(simon.accel_x) * delta_time
    if simon.x < ((window_width/6) * 3 - 16) + camera.x and camera.x >= 0:
        camera.x -= abs(simon.accel_x) * delta_time
        
    #Add objects  to sprite layers:
    walls, platforms, decor = debug.render()
    sprite_layer1 += walls + platforms + decor
    sprite_layer1 += [simon.update(walls, platforms, keys, delta_time)]

    #Finalize render with the camera object.
    final_render = camera.render(sprite_layer3 + sprite_layer2 + sprite_layer1)
    #Later this will go through a camera class
            
    #Render:
    window.fill(BLACK)#Clear screen.
    
    #PUT IN RENDER CODE HERE.
    for sprite in final_render:
        window.blit(sprite[2], (sprite[0], sprite[1]))
    
    pygame.display.update()#Update window.

quit()#Once the loop ends, quit out of the game.
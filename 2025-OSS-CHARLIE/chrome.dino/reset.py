import pygame
pygame.init() #this ‘starts up’ pygame

size = width,height = 640, 480#creates tuple called size with width 400  and height 230
gameDisplay= pygame.display.set_mode(size) #creates screen

while True: #gameLoop it draws the frames of the game


  for event in pygame.event.get(): #Check for events
    if event.type == pygame.QUIT:
      pygame.quit() #quits
      quit()

  pygame.display.update() #updates the screen

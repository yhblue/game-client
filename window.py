import pygame
import time
def main():
	win = pygame.display.set_mode((1024,625),0,32)
	background = pygame.image.load("./pic/background.jpg");
    while True:
        screen.blit(background, (0,0))

        pygame.display.update()

        time.sleep(0.01)

if __name__ == "__main__":
    main()
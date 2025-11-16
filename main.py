import pygame
from gameLoop import GameLoop

if __name__ == "__main__":
    print("intializing engine")
    pygame.init()
    info = pygame.display.Info()
    DEVICE_W, DEVICE_H = info.current_w, info.current_h
    # screen = pygame.display.set_mode((DEVICE_W, DEVICE_H), flags=pygame.FULLSCREEN)
    screen = pygame.display.set_mode((800, 640))
    print(DEVICE_W, DEVICE_H)

    gl = GameLoop(screen);
    gl.loop()

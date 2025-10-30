import pygame
from gameLoop import GameLoop

if __name__ == "__main__":
    print("intializing engine")
    pygame.init()

    gl = GameLoop();
    gl.loop()

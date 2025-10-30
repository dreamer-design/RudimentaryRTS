from pygame import display
from pygame import draw
from pygame import Rect

# (0,0) is top left

# Screen settings
WIDTH, HEIGHT = 1900, 1200
TILE, MULT = 64, 3
NW, NH = WIDTH // TILE - 2, HEIGHT // TILE - 2

screen = display.set_mode((NW * TILE, NH * TILE))
print(NW * MULT ,NH * MULT, NW * TILE * MULT, NH * TILE * MULT)

class Renderer:
        def __init__(s, entities):
            s.toDraw = entities

        def render(s):
            screen.fill((100, 100, 100))  # grey

            for entity in s.toDraw:
                color = ( 255, 255, 255)
                r = Rect( entity.x, entity.y, 10, 10)
                draw.rect(screen, color , r)
            # Any other rendering goes here
            display.flip()

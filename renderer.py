from pygame import display

# Screen settings
WIDTH, HEIGHT = 1900, 1200
TILE, MULT = 64, 3
NW, NH = WIDTH // TILE - 2, HEIGHT // TILE - 2

screen = display.set_mode((NW * TILE, NH * TILE))
print(NW * MULT ,NH * MULT, NW * TILE * MULT, NH * TILE * MULT)

class Renderer:
        def __init__(s):
            s.state = 0

        def render(s):
            screen.fill((100, 100, 100))  # Clear the screen to black
            # Any other rendering goes here
            display.flip()

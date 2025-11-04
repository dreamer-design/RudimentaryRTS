from pygame import display
from pygame import draw
from pygame import Rect
import math

from entityManager import Unit, Structure
# (0,0) is top left

# Screen settings
WIDTH, HEIGHT = 1900, 1000
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
                # unit
                if type(entity) == Unit:
                    s.draw_triangle(screen, entity.x, entity.y, entity.size, entity.rotation)
                # structure
                if isinstance(entity, Structure):
                    rect = Rect(entity.x, entity.y, entity.size, entity.size) # x,y, height, width
                    color = (0, 0, 255)
                    draw.rect( screen, color, rect )

            display.flip()

        # Function to rotate a point around the center
        def rotate_point(s, px, py, cx, cy, angle):
            angle_rad = math.radians(angle) # convert degs to rad
            dx = px - cx
            dy = py - cy
            new_x = cx + dx * math.cos(angle_rad) - dy * math.sin(angle_rad)
            new_y = cy + dx * math.sin(angle_rad) + dy * math.cos(angle_rad)
            return new_x, new_y

        # Function to draw an equilateral triangle
        # angle in degrees
        def draw_triangle(s, screen, cx, cy, side_length, angle):
            color = (255, 255, 255)

            # Calculate the 3 points of the equilateral triangle
            height = side_length / (2 * math.sqrt(3))
            top = (cx, cy - height)
            left = (cx - side_length / 2, cy + height)
            right = (cx + side_length / 2, cy + height)

            # Rotate each point by the given angle
            top = s.rotate_point(top[0], top[1], cx, cy, angle)
            left = s.rotate_point(left[0], left[1], cx, cy, angle)
            right = s.rotate_point(right[0], right[1], cx, cy, angle)

            # Draw the triangle
            draw.polygon(screen, color, [top, left, right])
            draw.line(screen, (255, 0 ,0) , left, right )

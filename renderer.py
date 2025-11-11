from pygame import display, Surface
from pygame import draw
from pygame import Rect
from pygame import font
import math

from entityManager import Unit, Structure
# (0,0) is top left

# Screen settings
WIDTH, HEIGHT = 1900, 1000

# screen vars
# screen = display.set_mode((NW * TILE, NH * TILE))
buffer = display.set_mode((WIDTH, HEIGHT))
screen = Surface( (WIDTH*2, HEIGHT*2) )

# Scroll position
screen_width, screen_height = WIDTH, HEIGHT
scroll_x, scroll_y = 0, 0
scroll_speed = 5  # Speed of scrolling
edge_threshold = 50  # Threshold distance from the edge to trigger scrolling


class Renderer:
        def __init__(s, entities):
            s.toDraw = entities
            # Define the font and size
            s.font = font.Font(None, 74)  # None means default font, 74 is the size

        def render(s, selected_unit):
            screen.fill((100, 100, 100))  # grey

            if( selected_unit ):
                pos = (selected_unit.x,selected_unit.y)
                sz = selected_unit.size
                draw.circle(screen, (0, 255, 0), pos, sz) # s, c, center, rad, width

            for entity in s.toDraw:
                # all
                bar_width = entity.size
                health_ratio = entity.hp / entity.max_hp
                draw.rect(screen, (255,0,0), Rect(entity.x -bar_width/2, entity.y - entity.size/2-10, bar_width, 5))
                draw.rect(screen, (0,255,0), Rect(entity.x - bar_width/2, entity.y-entity.size/2-10, bar_width * health_ratio, 5))


                # unit
                if type(entity) == Unit:
                    s.draw_triangle(screen, entity.x, entity.y, entity.size, entity.rotation, entity.color)

                # structure
                if isinstance(entity, Structure):
                    # set to centre of square
                    half = entity.size / 2
                    rect = Rect(entity.x - half, entity.y - half, entity.size, entity.size) # x,y, height, width
                    draw.rect( screen, entity.color, rect )

                    # draw cooldown
                    text_surface = s.font.render( str( round(entity.spawn_timer) ), True, (255, 255, 255) ) # Render the text white
                    screen.blit(text_surface, (entity.x, entity.y) )

                    # Draw spawn point indicator
                    if entity.spawn:
                        sx, sy = entity.spawn
                        draw.circle(screen, (255, 255, 0), (int(sx), int(sy)), 5)

                # Draw the portion of the buffer that we want to show on the screen
            buffer.blit(screen, (0, 0), (scroll_x, scroll_y, screen_width, screen_height))

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
        def draw_triangle(s, screen, cx, cy, side_length, angle, color = (255, 255, 255)):

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

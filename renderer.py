from pygame import display, Surface
from pygame import draw
from pygame import Rect
from pygame import font
import math

from entityManager import Unit, Structure, Node, Projectile
# (0,0) is top left

MINIMAP_SIZE = 200          # pixel size of the minimap square
MINIMAP_SCALE = 0.1         # world-to-minimap scale
MINIMAP_MARGIN = 10         # offset from screen edges

# map vars
MAPW, MAPH = 2000 , 2000
map_buffer = Surface( (MAPW, MAPH) )

class Renderer:
        def __init__(s, screen, manager, entities):
            s.screen = screen
            s.toDraw = entities
            s.manager = manager
            # Define the font and size
            s.font = font.Font(None, 74)  # None means default font, 74 is the size

        def render(s, selected_unit, scroll_x, scroll_y):
            map_buffer.fill((100, 100, 100))  # grey

            # start pylons
            for pos in s.manager.startPylons:
                draw.circle(map_buffer, (200, 200, 200), pos, 5)
                draw.circle(map_buffer, (200, 200, 200), pos, s.manager.buildRadius, width=2)

            if( selected_unit ):
                pos = (selected_unit.x,selected_unit.y)
                sz = selected_unit.size
                draw.circle(map_buffer, (0, 255, 0), pos, sz) # s, c, center, rad, width

            for entity in s.toDraw:
                # all
                if entity.hp < 900:
                    bar_width = entity.size
                    health_ratio = entity.hp / entity.max_hp
                    draw.rect(map_buffer, (255,0,0), Rect(entity.x -bar_width/2, entity.y - entity.size/2-10, bar_width, 5))
                    draw.rect(map_buffer, (0,255,0), Rect(entity.x - bar_width/2, entity.y-entity.size/2-10, bar_width * health_ratio, 5))

                # unit
                if type(entity) == Unit:
                    s.draw_triangle(map_buffer, entity.x, entity.y, entity.size, entity.rotation, entity.color)

                # structure
                if isinstance(entity, Structure):
                    # set to centre of square
                    half = entity.size / 2
                    rect = Rect(entity.x - half, entity.y - half, entity.size, entity.size) # x,y, height, width
                    draw.rect( map_buffer, entity.color, rect )

                    # draw cooldown
                    text_surface = s.font.render( str( round(entity.spawn_timer) ), True, (255, 255, 255) ) # Render the text white
                    map_buffer.blit(text_surface, (entity.x, entity.y) )

                    # Draw spawn point indicator
                    if entity.spawn:
                        sx, sy = entity.spawn
                        draw.circle(map_buffer, (255, 255, 0), (int(sx), int(sy)), 5)

                # Node
                if isinstance(entity, Node):
                    s.draw_triangle(map_buffer, entity.x, entity.y, entity.size, entity.rotation, entity.color)

                # Projectile
                if isinstance(entity, Projectile):
                    draw.circle(map_buffer, (0, 255, 0), (int(entity.x), int(entity.y)), 5)

                # Draw the portion of the buffer that we want to show on the screen
            # s.screen.blit(map_buffer, (0, 0), (scroll_x, scroll_y, screen_width, screen_height))
            s.screen.blit(map_buffer, (0, 0), (scroll_x, scroll_y, s.screen.get_width(), s.screen.get_height() ))

            s.draw_minimap(s.screen, s.toDraw)
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
        def draw_triangle(s, map_buffer, cx, cy, side_length, angle, color = (255, 255, 255)):

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
            draw.polygon(map_buffer, color, [top, left, right])
            draw.line(map_buffer, (255, 0 ,0) , left, right )

        def draw_minimap(self, map_buffer, entities):
            # Position (top-right corner)
            # mx = WIDTH - MINIMAP_SIZE - MINIMAP_MARGIN
            mx = 0
            my = MINIMAP_MARGIN

            # Background rectangle
            draw.rect(map_buffer, (40, 40, 40), Rect(mx, my, MINIMAP_SIZE, MINIMAP_SIZE))

            for e in entities:
                # Only show units and structures
                if not isinstance(e, (Unit, Structure)):
                    continue

                # Convert world → minimap coordinates
                px = mx + e.x * MINIMAP_SCALE
                py = my + e.y * MINIMAP_SCALE

                # Choose team color
                color = (0, 0, 255) if e.team == 0 else (255, 0, 0)

                # Units as small circles; structures as small squares
                if isinstance(e, Unit):
                    draw.circle(map_buffer, color, (int(px), int(py)), 2)
                elif isinstance(e, Structure):
                    draw.rect(map_buffer, color, Rect(px - 2, py - 2, 4, 4))

import pygame
from pygame import display, Surface
from pygame import draw
from pygame import Rect
from pygame import font
import math

import constants as C
from entityManager import Unit, Structure, Node, Projectile
# (0,0) is top left
from ui import Button

class Renderer:
        def __init__(s, screen, manager, entities):
            s.screen = screen
            s.map_buffer = Surface( (C.MAPW, C.MAPH) )
            s.ui_buffer = Surface(s.screen.get_size(), pygame.SRCALPHA)
            s.toDraw = entities
            s.manager = manager
            s.font = font.Font(None, 74)  # None means default font, 74 is the size
            s.build_button = Button( x = C.MINIMAP_SIZE + C.MINIMAP_MARGIN*2, y = C.EDGE_THRESHOLD)

        def render(s, selected_unit, scroll):
            s.map_buffer.fill((100, 100, 100))  # grey

            # start pylons
            for pos in s.manager.startPylons:
                draw.circle(s.map_buffer, (200, 200, 200), pos, 5)
                draw.circle(s.map_buffer, (200, 200, 200), pos, s.manager.buildRadius, width=2)

            if( selected_unit ):
                pos = (selected_unit.x,selected_unit.y)
                sz = selected_unit.size
                draw.circle(s.map_buffer, (0, 255, 0), pos, sz) # s, c, center, rad, width

            for entity in s.toDraw:
                # all
                if entity.hp < 900:
                    bar_width = entity.size
                    health_ratio = entity.hp / entity.max_hp
                    draw.rect(s.map_buffer, (255,0,0), Rect(entity.x -bar_width/2, entity.y - entity.size/2-10, bar_width, 5))
                    draw.rect(s.map_buffer, (0,255,0), Rect(entity.x - bar_width/2, entity.y-entity.size/2-10, bar_width * health_ratio, 5))

                # unit
                if type(entity) == Unit:
                    s.draw_triangle(s.map_buffer, entity.x, entity.y, entity.size, entity.rotation, entity.color)

                # structure
                if isinstance(entity, Structure):
                    # set to centre of square
                    half = entity.size / 2
                    rect = Rect(entity.x - half, entity.y - half, entity.size, entity.size) # x,y, height, width
                    draw.rect( s.map_buffer, entity.color, rect )

                    # draw cooldown
                    text_surface = s.font.render( str( round(entity.spawn_timer) ), True, (255, 255, 255) ) # Render the text white
                    s.map_buffer.blit(text_surface, (entity.x, entity.y) )

                    # Draw spawn point indicator
                    if entity.spawn:
                        sx, sy = entity.spawn
                        draw.circle(s.map_buffer, (255, 255, 0), (int(sx), int(sy)), 5)

                # Node
                if isinstance(entity, Node):
                    s.draw_triangle(s.map_buffer, entity.x, entity.y, entity.size, entity.rotation, entity.color)

                # Projectile
                if isinstance(entity, Projectile):
                    draw.circle(s.map_buffer, (0, 255, 0), (int(entity.x), int(entity.y)), 5)

                # Draw the portion of the buffer that we want to show on the screen
            s.screen.blit(s.map_buffer, (0, 0), (scroll[0], scroll[1], s.screen.get_width(), s.screen.get_height() ))
            s.screen.blit(s.ui_buffer, (0, 0))

            # UI
            s.draw_minimap(s.screen, s.toDraw)
            s.build_button.draw(s.screen)

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
            mx = C.MINIMAP_MARGIN
            my = C.MINIMAP_MARGIN

            # Background rectangle
            draw.rect(map_buffer, (40, 40, 40), Rect(mx, my, C.MINIMAP_SIZE, C.MINIMAP_SIZE))

            for e in entities:
                # Only show units and structures
                if not isinstance(e, (Unit, Structure)):
                    continue

                # Convert world → minimap coordinates
                px = mx + e.x * C.MINIMAP_SCALE
                py = my + e.y * C.MINIMAP_SCALE

                # Choose team color
                color = (0, 0, 255) if e.team == 0 else (255, 0, 0)

                # Units as small circles; structures as small squares
                if isinstance(e, Unit):
                    draw.circle(map_buffer, color, (int(px), int(py)), 2)
                elif isinstance(e, Structure):
                    draw.rect(map_buffer, color, Rect(px - 2, py - 2, 4, 4))

        def draw_silohette(s, mouse):
            mx, my = mouse[0], mouse[1]
            size = 50
            # print(mx, my)
            s.clear_UI()   # transparent

            draw.rect(
                s.ui_buffer,
                (0,255,0),
                Rect(mx, my, size, size),
                width=2
            )

        def clear_UI(s):
            s.ui_buffer.fill((0,0,0,0))   # transparent


from renderer import Renderer

from entityManager import EntityManager, Unit, Structure
from random import randint

from pygame import time
from pygame import event, QUIT
from pygame import key, KEYDOWN, KMOD_SHIFT, K_q, K_a, K_s, K_d, K_w, K_z, K_x, K_c
from pygame import mouse, MOUSEBUTTONDOWN

import renderer as R

clock = time.Clock()

class GameLoop:
    def __init__(s):
        s.running = True
        s.deltaTime = 0
        s.manager = EntityManager()
        s.display = Renderer( s.manager, s.manager.entities )
        s.selected = None # currently selected unit

    def loop(s):
        while s.running:
            # update
            dt = clock.tick(60) / 1000
            s.manager.update(dt)
            s.display.render(s.selected)

            # edge scroll
            # Get mouse position
            mouse_x, mouse_y = mouse.get_pos()
            AMouse_x = mouse_x + R.scroll_x
            AMouse_y = mouse_y + R.scroll_y

            # Check if the mouse is near any edge and scroll accordingly
            if mouse_x < R.edge_threshold:  # Mouse is near the left edge
                R.scroll_x -= R.scroll_speed
            if mouse_x > R.screen_width - R.edge_threshold:  # Mouse is near the right edge
                R.scroll_x += R.scroll_speed
            if mouse_y < R.edge_threshold:  # Mouse is near the top edge
                R.scroll_y -= R.scroll_speed
            if mouse_y > R.screen_height - R.edge_threshold:  # Mouse is near the bottom edge
                R.scroll_y += R.scroll_speed

            # Ensure scrolling doesn't go beyond the map boundaries
            R.scroll_x = max(0, R.scroll_x)                        # left edge
            R.scroll_x = min(R.MAPW - R.screen_width, R.scroll_x)  # right edge
            R.scroll_y = max(0, R.scroll_y)                        # top edge
            R.scroll_y = min(R.MAPH - R.screen_height, R.scroll_y) # bottom edge

            # input handle
            for ev in event.get():
                if ev.type == QUIT:
                    running = False
                if ev.type == KEYDOWN:
                    keys = key.get_pressed()
                    mods = key.get_mods()

                    if keys[K_q]:
                        s.running = False
                    if keys[K_z] and (mods & KMOD_SHIFT):
                        s.manager.addUnit( AMouse_x, AMouse_y, (1500,1500), team=1 )
                    elif keys[K_z]:
                        s.manager.addUnit( AMouse_x, AMouse_y, (500,500), team=0 )
                    if keys[K_x] and (mods & KMOD_SHIFT):
                        s.manager.addStructure( AMouse_x, AMouse_y, team=1 )
                    elif keys[K_x]:
                        s.manager.addStructure( AMouse_x, AMouse_y, team=0 )
                    if keys[K_c]:
                        s.manager.addNode( AMouse_x, AMouse_y)
                if ev.type == MOUSEBUTTONDOWN:
                    if ev.button == 1:  # Left click -> select
                        # s.selected = s.manager.get_entity_at( pos ) # return null/pos
                        s.selected = s.manager.get_entity_at( (AMouse_x, AMouse_y) ) # return null/pos

                    elif ev.button == 3 and s.selected:  # Right click
                        clicked = s.manager.get_entity_at( (AMouse_x, AMouse_y) )

                        if isinstance(s.selected, Unit):
                            # Always move the unit to clicked position
                            s.selected.moveTo = (AMouse_x, AMouse_y)
                            s.selected.point_to_target(AMouse_x, AMouse_y)

                        elif isinstance(s.selected, Structure):
                            if clicked == s.selected:
                                # Right-click on the selected structure -> spawn unit
                                s.selected.spawn_unit(s.manager)
                            else:
                                # Right-click elsewhere -> set spawn point
                                s.selected.set_spawn(AMouse_x, AMouse_y)


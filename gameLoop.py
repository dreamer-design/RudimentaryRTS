from renderer import Renderer

from entityManager import EntityManager, Unit, Structure
from random import randint

from pygame import time
from pygame import event, QUIT
from pygame import key, KEYDOWN, KMOD_SHIFT, K_q, K_a, K_s, K_d, K_w, K_z, K_x, K_c
from pygame import mouse, MOUSEBUTTONDOWN

import renderer as r

clock = time.Clock()

class GameLoop:
    def __init__(s):
        s.running = True
        s.deltaTime = 0
        s.manager = EntityManager()
        s.display = Renderer( s.manager.entities )
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

            # Check if the mouse is near any edge and scroll accordingly
            if mouse_x < r.edge_threshold:  # Mouse is near the left edge
                r.scroll_x -= r.scroll_speed
            if mouse_x > r.screen_width - r.edge_threshold:  # Mouse is near the right edge
                r.scroll_x += r.scroll_speed
            if mouse_y < r.edge_threshold:  # Mouse is near the top edge
                r.scroll_y -= r.scroll_speed
            if mouse_y > r.screen_height - r.edge_threshold:  # Mouse is near the bottom edge
                r.scroll_y += r.scroll_speed

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
                        s.manager.addUnit( *mouse.get_pos(), (500,500), team=1 )
                    elif keys[K_z]:
                        s.manager.addUnit( *mouse.get_pos(), (500,500), team=0 )
                    if keys[K_x] and (mods & KMOD_SHIFT):
                        s.manager.addStructure( *mouse.get_pos(), team=1 )
                    elif keys[K_x]:
                        s.manager.addStructure( *mouse.get_pos(), team=0 )
                    if keys[K_c]:
                        s.manager.addNode( *mouse.get_pos())
                if ev.type == MOUSEBUTTONDOWN:
                    pos = mouse.get_pos()
                    ##### pos = (pos[0] + r.scroll_x, pos[1] + r.scroll_y)  # Adjust for the scrolling
                    if ev.button == 1:  # Left click -> select
                        s.selected = s.manager.get_entity_at( pos ) # return null/pos

                    elif ev.button == 3 and s.selected:  # Right click
                        clicked = s.manager.get_entity_at(pos)

                        if isinstance(s.selected, Unit):
                            # Always move the unit to clicked position
                            s.selected.moveTo = pos
                            s.selected.point_to_target(*pos)

                        elif isinstance(s.selected, Structure):
                            if clicked == s.selected:
                                # Right-click on the selected structure -> spawn unit
                                s.selected.spawn_unit(s.manager)
                            else:
                                # Right-click elsewhere -> set spawn point
                                s.selected.set_spawn(*pos)


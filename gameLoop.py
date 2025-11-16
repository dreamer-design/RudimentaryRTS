import pygame
from pygame import time
from pygame import event, QUIT
from pygame import key, KEYDOWN, KMOD_SHIFT, K_q, K_a, K_s, K_d, K_w, K_z, K_x, K_c
from pygame import mouse, MOUSEBUTTONDOWN, MOUSEWHEEL

from random import randint

import constants as C
from renderer import Renderer
import renderer as R
from entityManager import EntityManager, Unit, Structure

clock = time.Clock()

class GameLoop:
    def __init__(s, screen):
        s.screen = screen
        s.running = True
        s.deltaTime = 0
        s.manager = EntityManager()
        s.display = Renderer( screen, s.manager, s.manager.entities )
        s.selected = None # currently selected unit
        s.scroll_x, s.scroll_y = 750, 500

        s.build_mode = None          # "pylon", "factory", or None
        s.build_types = ["pylon", "factory"]
        s.build_index = 0
        s.build_team = None          # "blue" or "red"


    def loop(s):
        while s.running:
            ### update
            dt = clock.tick(60) / 1000
            s.manager.update(dt)
            s.display.render(s.selected, (s.scroll_x, s.scroll_y)) # main render
            s.display.build_button.update( mouse.get_pos() ) # check button hover

            ### edge scroll
            # Get mouse position
            mouse_x, mouse_y = mouse.get_pos()
            AMouse_x = mouse_x + s.scroll_x
            AMouse_y = mouse_y + s.scroll_y

            # Check if the mouse is near any edge and scroll accordingly
            if mouse_x < C.EDGE_THRESHOLD:  # Mouse is near the left edge
                s.scroll_x -= C.SCROLL_SPEED
            if mouse_x > s.screen.get_width() - C.EDGE_THRESHOLD:  # Mouse is near the right edge
                s.scroll_x += C.SCROLL_SPEED
            if mouse_y < C.EDGE_THRESHOLD:  # Mouse is near the top edge
                s.scroll_y -= C.SCROLL_SPEED
            if mouse_y > s.screen.get_height() - C.EDGE_THRESHOLD:  # Mouse is near the bottom edge
                s.scroll_y += C.SCROLL_SPEED

            # Ensure scrolling doesn't go beyond the map boundaries
            s.scroll_x = max(0, s.scroll_x)                        # left edge
            s.scroll_x = min(C.MAPW - s.screen.get_width(), s.scroll_x)  # right edge
            s.scroll_y = max(0, s.scroll_y)                        # top edge
            s.scroll_y = min(C.MAPH - s.screen.get_height(), s.scroll_y) # bottom edge

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

                # unit handling
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

                # build mode
                if s.build_mode:
                    s.display.draw_silohette( mouse.get_pos() ) # reaches
                    if ev.type == MOUSEBUTTONDOWN:
                        if ev.button == 1:  # Left click -> select
                            s.manager.addStructure( AMouse_x, AMouse_y, team=s.build_team )
                            s.cancel_build_mode()
                            s.display.clear_UI()

                        elif ev.button == 3:  # Right click
                            s.cancel_build_mode()

                ### UI
                # scroll for build cycling
                if ev.type == MOUSEWHEEL:
                    # print(ev.y)
                    if ev.y == 2:    # scroll up
                        s.cycle_build_type(+1)
                    elif ev.y == -2:  # scroll down
                        s.cycle_build_type(-1)

                # Button click
                result = s.display.build_button.handle_event(ev)
                if result == 'left':
                    s.enter_build_mode(team=0)
                elif result == 'right':
                    s.enter_build_mode(team=1)

    def cycle_build_type(self, direction):
        self.build_index = (self.build_index + direction) % len(self.build_types)
        self.build_mode = self.build_types[self.build_index]
        # print( "cycle: ", self.build_mode )

    def enter_build_mode(self, team):
        self.build_team = team
        self.build_mode = self.build_types[self.build_index]   # current type
        # print("build mode: " + self.build_mode + " team: " + str(team) )

    def cancel_build_mode(self):
        self.build_mode = None
        self.build_team = None

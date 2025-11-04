from renderer import Renderer

from entityManager import EntityManager, Unit, Structure
from random import randint

from pygame import time
from pygame import event, QUIT
from pygame import key, KEYDOWN, K_q, K_a, K_s
from pygame import mouse, MOUSEBUTTONDOWN

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

            # input handle
            for ev in event.get():
                if ev.type == QUIT:
                    running = False
                if ev.type == KEYDOWN:
                    keys = key.get_pressed()
                    if keys[K_q]:
                        s.running = False
                    if keys[K_a]:
                        # x = randint(20,300); y = randint(20,300)
                        # r = randint(0,90)       # clockwise
                        s.manager.addUnit( *mouse.get_pos(), (500,500) )
                    if keys[K_s]:
                        # x = randint(20,300); y = randint(20,300)
                        # r = randint(0,90)       # clockwise
                        s.manager.addStructure( *mouse.get_pos() ) # spawn = 0, unused atm
                if ev.type == MOUSEBUTTONDOWN:
                    pos = mouse.get_pos()
                    if ev.button == 1:  # Left click -> select
                        s.selected = s.manager.get_entity_at( pos ) # return null/pos

                    elif ev.button == 3 and s.selected:  # Right click
                        clicked = s.manager.get_entity_at(pos)

                        if isinstance(s.selected, Unit):
                            # Always move the unit to clicked position
                            s.selected.target = pos

                        elif isinstance(s.selected, Structure):
                            if clicked == s.selected:
                                # Right-click on the selected structure -> spawn unit
                                s.selected.spawn_unit(s.manager)
                            else:
                                # Right-click elsewhere -> set spawn point
                                s.selected.set_spawn(*pos)


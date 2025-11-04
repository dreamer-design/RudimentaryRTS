from renderer import Renderer

from entityManager import EntityManager
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
            s.display.render()

            # input handle
            for ev in event.get():
                if ev.type == QUIT:
                    running = False
                if ev.type == KEYDOWN:
                    keys = key.get_pressed()
                    if keys[K_q]:
                        s.running = False
                    if keys[K_a]:
                        x = randint(20,300); y = randint(20,300)
                        r = randint(0,90)       # clockwise
                        s.manager.addUnit( x, y )
                    if keys[K_s]:
                        x = randint(20,300); y = randint(20,300)
                        r = randint(0,90)       # clockwise
                        s.manager.addStructure( x, y, (0,0) ) # spawn = 0, unused atm
                if ev.type == MOUSEBUTTONDOWN:
                    if ev.button == 1:  # Left click -> select
                        s.selected = s.manager.get_entity_at(mouse.get_pos())
                    elif ev.button == 3 and s.selected:  # Right click -> move
                        s.selected.target = mouse.get_pos()
                        # s.selected.point_to_target(*s.selected.target)

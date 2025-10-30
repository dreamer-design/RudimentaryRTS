from renderer import Renderer

from entityManager import EntityManager
from random import randint

from pygame import time
from pygame import event, QUIT
from pygame import key, K_q, K_a, KEYDOWN

clock = time.Clock()

class GameLoop:
    def __init__(s):
        s.running = True
        s.deltaTime = 0
        s.manager = EntityManager()
        s.display = Renderer( s.manager.entities )

    def loop(s):
        while s.running:
            dt = clock.tick(60) / 1000

            s.display.render()

            for ev in event.get():
                if ev.type == QUIT:
                    running = False
                if ev.type == KEYDOWN:
                    keys = key.get_pressed()
                    if keys[K_q]:
                        s.running = False
                    if keys[K_a]:
                        s.manager.addEntity( randint(0,100),randint(0,100) )

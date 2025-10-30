from renderer import Renderer
from entityManager import EntityManager
from pygame import time
from pygame import event, QUIT
from pygame import key, K_q

clock = time.Clock()

class GameLoop:

    def __init__(s):
        s.running = True
        s.deltaTime = 0
        s.manager = EntityManager()
        s.display = Renderer()

    def loop(s):
        while s.running:
            dt = clock.tick(60) / 1000

            s.display.render()

            for ev in event.get():
                if ev.type == QUIT:
                    running = False

            keys = key.get_pressed()
            if keys[K_q]:
                s.running = False

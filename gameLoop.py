from renderer import Renderer
from entityManager import EntityManager

class GameLoop:

    def __init__(s):
        s.isRunning = True
        s.deltaTime = 0
        s.manager = EntityManager()

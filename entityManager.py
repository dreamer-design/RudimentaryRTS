class EntityManager:
    def __init__(s):
        s.entities = []

    def addEntity(s, x, y):
        s.entities.append( Entity(x,y) )

class Entity:
    def __init__(s, x, y):
        print("emit: ", x, y)
        s.x = x
        s.y = y

class Unit(Entity):
        def __init__(s):
            s.shape = "triangle"

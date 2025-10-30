import math

class EntityManager:
    def __init__(s):
        s.entities = []

    def addEntity(s, x, y, rotation=0, size=40):
        s.entities.append( Unit(x,y, rotation, size) )

class Entity:
    def __init__(s, x, y, rotation, size):
        print("emit: ", x, y, rotation, size)
        s.x = x
        s.y = y
        s.rotation = rotation # degs from up
        s.size = size

class Unit(Entity):

        target = (1000, 700)

        def __init__(s, x, y, rotation, size):
            super().__init__(x, y, rotation, size)

            s.rotation = s.point_to_target(*s.target)
            print(s.rotation)
        
        def point_to_target(s, x2, y2):
            # get the clockwise angle of rotation from straight (0) up to the secondary point located to the bottom right of screen
            # somthing like 180 - inverse tan of x2-x1 / y2 -y1
            dx = x2 - s.x
            dy = y2 - s.y
            angle_rad = math.atan2(dx, -dy)        # 0 deg = up, increases clockwise
            angle_deg = math.degrees(angle_rad)
            return angle_deg
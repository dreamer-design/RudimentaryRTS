import math

class EntityManager:
    def __init__(s):
        s.entities = []

    def addEntity(s, x, y, rotation=0, size=40):
        s.entities.append( Unit(x,y, rotation, size) )

    def addUnit(s, x, y, rotation=0, size=40):
        s.entities.append( Unit(x,y, rotation, size) )

    def addStructure(s, x, y, spawn_point):
        s.entities.append( Structure(x,y, spawn_point) )

    def get_entity_at(s, pos):
        x, y = pos
        for e in s.entities:
            if abs(e.x - x) < e.size and abs(e.y - y) < e.size:
                print(str(e) + "selected")
                return e
        return None

    def update(s, dt):
        for e in s.entities:
            if isinstance(e, Unit):
                e.update(dt)


class Entity:
    def __init__(s, x, y, rotation, size):
        print("emit: ", x, y, rotation, size)
        s.x = x
        s.y = y
        s.rotation = rotation # degs from up
        s.size = size


class Unit(Entity):
        def __init__(s, x, y, rotation=0, size=40, T= (1000, 700) ):
            super().__init__(x, y, rotation, size)
            s.target = T
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

        def update(s, dt):
            tx, ty = s.target
            dx, dy = tx - s.x, ty - s.y
            dist = math.hypot(dx, dy)
            if dist > 1:
                s.x += (dx / dist) * 100 * dt  # speed = 100 px/s
                s.y += (dy / dist) * 100 * dt
            # update roation angle
            s.rotation = s.point_to_target(tx,ty)


class Structure(Entity):
        spawn = []

        def __init__(s, x, y, spawn_point):
            super().__init__(x, y, rotation=0, size=80)
            s.spawn = spawn_point

        def set_spawn(s, x, y):
            s.x = x; s.y = y

import math

SPAWN_TIME = 30

class EntityManager:
    def __init__(s):
        s.entities = []

    # def addEntity(s, x, y, rotation=0, size=40, team=0):
    #     s.entities.append( Unit(x,y, rotation, size) )

    def addUnit(s, x, y, spawn, rotation=0, size=40, team=0):
        s.entities.append( Unit(x,y, rotation, size, spawn) )

    def addStructure(s, x, y, spawn_point= (100,100), team=0 ):
        s.entities.append( Structure(x,y, spawn_point) )

    def addNode(s, x, y ):
        s.entities.append( Node(x,y) )

    def get_entity_at(s, pos):
        x, y = pos
        for e in s.entities:
            if abs(e.x - x) < e.size and abs(e.y - y) < e.size:
                print(str(e) + "selected")
                return e
        return None

    def update(s, dt):
        for e in s.entities:
            # if isinstance(e, Unit):
            #     e.update(dt)
            if hasattr(e, "update"):
                e.update(dt)

class Entity:
    def __init__(s, x, y, rotation, size, max_hp=100, team=0):
        print("emit: ", x, y, rotation, size)
        s.x = x
        s.y = y
        s.rotation = rotation # degs from up
        s.size = size
        s.hp = s.max_hp = max_hp
        s.team = team

        if s.team == 0:
            s.color = (0,0,255) # blue team
        elif s.team == 1:
            s.color = (255,0,0) # red team
        else:
            s.color = (255,255,255); # white = neutral

        def take_damage(s, dmg):
            s.hp = max(0, s.hp - dmg)

class Unit(Entity):
        def __init__(s, x, y, rotation=0, size=40, T= (1000, 700) ):
            super().__init__(x, y, rotation, size)
            s.target = T
            s.rotation = s.point_to_target(*s.target)
            print(s.rotation)
            s.range = 100 # radius
            s.fire_rate = 1 # secs?
            s.cooldown = s.fire_rate
        
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
        spawn_timer = 0

        def __init__(s, x, y, spawn_point=(100,100) ):
            super().__init__(x, y, rotation=0, size=80)
            s.spawn = spawn_point
            s.spawn_timer = 0
            s.spawnable = True

        def set_spawn(s, x, y):
            # s.x = x; s.y = y
            s.spawn = (x, y)

        def update(s, dt):
            if not s.spawnable:
                s.spawn_timer -= dt
                if s.spawn_timer <= 0:
                    s.spawnable = True

        def spawn_unit(s, manager):
            if s.spawnable and s.spawn:
                sx, sy = s.x, s.y # Spawn unit at the structure’s center
                unit = manager.addUnit(sx, sy, s.spawn) # set its target to the spawn point

                # Handle cooldown
                s.spawnable = False
                s.spawn_timer = SPAWN_TIME

class Node(Entity):
    types = 0 # resource, health regen, upgrade

    def __init__(s, x, y ):
        super().__init__(x, y, rotation=0, size=80, max_hp=9999, team=None)



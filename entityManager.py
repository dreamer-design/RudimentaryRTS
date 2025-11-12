import math
# import renderer as R

SPAWN_TIME = 30

class EntityManager:
    entities = []
    # startPylons = []
    buildRadius = 500

    def __init__(s):
        # s.startPylons[0], s.startPylons[1] = (0 + s.buildRadius, 0 + s.buildRadius)
        s.startPylons = ( (0 + s.buildRadius, 0 + s.buildRadius), (2000 - s.buildRadius, 2000 - s.buildRadius) )


    # def addEntity(s, e):
    #     s.entities.append( e )

    def addUnit(s, x, y, spawn, rotation=0, size=40, team=0):
        s.entities.append( Unit(x,y, rotation, size, spawn, team) )

    def addStructure(s, x, y, spawn_point= (100,100), team=0 ):
        s.entities.append( Structure(x,y, spawn_point, team) )

    def addNode(s, x, y ):
        s.entities.append( Node(x,y) )

    def addProjectile( s, x, y, target):
        print("here")
        s.entities.append( Projectile(x, y, target) )
        print("here")

    def get_entity_at(s, pos):
        x, y = pos
        for e in s.entities:
            if abs(e.x - x) < e.size and abs(e.y - y) < e.size:
                print(str(e) + "selected")
                return e
        return None

    def update(s, dt):
        for e in s.entities:
            if hasattr(e, "update"):
                e.update(dt, s)

        # Remove dead entities
        # s.entities = [e for e in s.entities if e.hp > 0]

class Entity:
    def __init__(s, x, y, rotation, size, max_hp=100, team=0):
        print("emit: ", x, y, rotation, size, team)
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
        def __init__(s, x, y, rotation=0, size=40, T= (1000, 700), team=0 ):
            super().__init__(x, y, rotation, size, team=team)
            s.x = x
            s.y = y
            s.moveTo = T
            s.rotation = s.point_to_target(*s.moveTo)
            s.range = 200      # radius
            s.fire_rate = 1.0  # secsonds between shots
            s.cooldown = 0     # able to shoot immediately
            s.damage = 1
            s.target = None
        
        def point_to_target(s, x2, y2):
            # get the clockwise angle of rotation from straight (0) up to the secondary point located to the bottom right of screen
            # somthing like 180 - inverse tan of x2-x1 / y2 -y1
            dx = x2 - s.x
            dy = y2 - s.y
            angle_rad = math.atan2(dx, -dy)        # 0 deg = up, increases clockwise
            angle_deg = math.degrees(angle_rad)
            return angle_deg

        def update(s, dt, manager):
            # move
            tx, ty = s.moveTo
            dx, dy = tx - s.x, ty - s.y
            dist = math.hypot(dx, dy)
            if dist > 1:
                s.x += (dx / dist) * 100 * dt  # speed = 100 px/s
                s.y += (dy / dist) * 100 * dt

            # update roation angle
            if s.target != None:
                s.rotation = s.point_to_target( s.target.x, s.target.y )
            else:
                s.rotation = s.point_to_target(s.moveTo[0],s.moveTo[1])

            # cooldown
            if s.cooldown > 0:
                s.cooldown -= dt

            # try to shoot
            if s.cooldown <= 0:
                s.target = s.find_target( EntityManager.entities )

                # instant damage
                if s.target:
                    # s.moveTo = (s.x, s.y) # stop to shoot
                    s.target.take_damage(s.damage)
                    s.cooldown = s.fire_rate
                # add Projectile
                    manager.addProjectile( s.x, s.y, s.target )

        def find_target(s, entities):
            enemies = [e for e in entities if e.team != s.team and e.hp > 0]
            closest = None
            min_dist = float("inf")

            for e in enemies:
                dist = math.hypot(e.x - s.x, e.y - s.y)
                if dist < s.range and dist < min_dist:
                    min_dist = dist
                    closest = e

            return closest

class Structure(Entity):
        spawn = []
        spawn_timer = 0

        def __init__(s, x, y, spawn_point=(100,100), team=0 ):
            super().__init__(x, y, rotation=0, size=80, team=team)
            s.spawn = spawn_point
            s.spawn_timer = 0
            s.spawnable = True

        def set_spawn(s, x, y):
            # s.x = x; s.y = y
            s.spawn = (x, y)

        def update(s, dt, manager):
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

# fixme: projectile has a health bar too.
class Projectile(Entity):
    def __init__(s, x, y, target):
        super().__init__(x, y, rotation=0, size=80, max_hp=9999, team=None)
        s.target = target

    def update(s, dt, manager):
        # move
        tx, ty = s.target.x, s.target.y
        dx, dy = tx - s.x, ty - s.y
        dist = math.hypot(dx, dy)
        if dist > 0:
            s.x += (dx / dist) * 100 * dt  # speed = 100 px/s
            s.y += (dy / dist) * 100 * dt

# obstacle.py
class Obstacle:
    passable     = False
    destructible = False
    color        = (0, 0, 0)

class Empty(Obstacle):
    passable     = True
    destructible = False
    color        = (0, 0, 0)

class Brick(Obstacle):
    passable     = False
    destructible = True
    color        = (180, 80, 20)

class Steel(Obstacle):
    passable     = False
    destructible = False
    color        = (150, 150, 150)

class Water(Obstacle):
    passable     = True
    destructible = False
    color        = (0, 80, 200)

class Forest(Obstacle):
    passable     = True
    destructible = False
    color        = (0, 120, 0)

class Base(Obstacle):
    passable     = False
    destructible = True
    color        = (255, 200, 0)
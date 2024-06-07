from cmu_graphics import *

# Bullet class
class Bullet:
    def __init__(self, app, x, y, xSpeed, ySpeed, owner):
        self.app = app
        self.x = x
        self.y = y
        self.xSpeed = xSpeed
        self.ySpeed = ySpeed
        self.owner = owner  # Owner of the bullet (player or enemy)
        # Add bullet to world elements
        app.worldElements.append(self)

    # Move function
    def move(self):
        self.x += self.xSpeed
        self.y += self.ySpeed

# Bomb class
class Bomb:
    def __init__(self, app, x, y, xSpeed, ySpeed, owner):
        self.app = app
        self.x = x
        self.y = y
        self.xSpeed = xSpeed
        self.ySpeed = ySpeed
        self.owner = owner  # Owner of the bomb (player or enemy)
        # Add bomb to world elements
        app.worldElements.append(self)

    # Move function
    def move(self):
        self.y += 10        
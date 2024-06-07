from cmu_graphics import *
import math
from bulletsbombs import Bullet
from bulletsbombs import Bomb

# Player class
class Player:
    def __init__(self, app):
        self.app = app
        self.planeX = 400
        self.planeY = 300  # Centered starting position
        self.speed = 30  # Speed control
        self.acceleration = 0.15  # Acceleration control
        self.fill = 'blue'
        self.bullets = []  # List to store bullet information
        self.bombs = [] # List to store bomb information
        self.isFiring = False  # Flag to indicate whether spacebar is being held
        self.fireCooldownCounter = 0  # Counter for controlling firing rate
        self.score = 10000  # Player's score
        self.ignoreCollision = False  # Flag to ignore collisions for a brief period after a collision
        self.collisionCooldownCounter = 0  # Counter for collision cooldown
        self.angle = 0 # Initial angle
        self.currentWeaponMode = 'Regular Gun'
        self.machineGunAmmo = 90 # Machine Gun Ammo Limit
        self.bombAmmo = 20 # Bomb Ammo Limit

    def moveTowardsMouse(self, mouseX, mouseY):
        # Calculate the angle between the current and previous mouse positions
        angle = math.atan2(mouseY - self.planeY, mouseX - self.planeX)

        # Accelerate towards the mouse based on the distance
        xSpeed = self.acceleration * math.cos(angle)
        ySpeed = self.acceleration * math.sin(angle)

        # Update the player's plane speed without changing its position
        self.speedX = xSpeed * self.speed
        self.speedY = ySpeed * self.speed

        return (self.speedX, self.speedY)

    def startShooting(self, app):
        bulletSpeed = 20
        fireCooldown = 10 # Control firing rate
        machineGunMode = 'Machine Gun'
        bombMode = 'Bomb'
        regularBulletMode = 'Regular Gun'
        if not app.gameOver:
            if self.currentWeaponMode == regularBulletMode and self.fireCooldownCounter == 0:
                angle = math.atan2(app.mouseY - self.planeY, app.mouseX - self.planeX)
                self.angle = angle  # Update plane's angle
                xSpeed = bulletSpeed * math.cos(angle)
                ySpeed = bulletSpeed * math.sin(angle)
                bullet = Bullet(self.app, self.planeX, self.planeY, xSpeed, ySpeed, owner='player')
                self.bullets.append(bullet)
                self.fireCooldownCounter = fireCooldown
            elif self.currentWeaponMode == machineGunMode and self.machineGunAmmo > 0:
                self.startMachineGunShooting(app)
                self.machineGunAmmo -= 1
                # Reset to default shooting if ammo runs out
                if self.machineGunAmmo == 0:
                    self.currentWeaponMode == regularBulletMode
            elif self.currentWeaponMode == bombMode and self.bombAmmo > 0:
                self.startBombDropping(app)
                self.bombAmmo -= 1
                # Reset to default shooting if ammo runs out
                if self.bombAmmo == 0:
                    self.currentWeaponMode == regularBulletMode

    def startMachineGunShooting(self, app):
        bulletSpeed = 20
        fireCooldown = 10 # Control firing rate
        angle = math.atan2(app.mouseY - self.planeY, app.mouseX - self.planeX)
        self.angle = angle
        bulletSpread = 20
        for i in range(-1, 2):  # Create three rows of bullets
            adjustedAngle = angle + i * math.radians(bulletSpread)
            xSpeed = bulletSpeed * math.cos(adjustedAngle)
            ySpeed = bulletSpeed * math.sin(adjustedAngle)
            bullet = Bullet(self.app, self.planeX, self.planeY, xSpeed, ySpeed, owner='player')
            self.bullets.append(bullet)
            self.fireCooldownCounter = fireCooldown

    def updateBulletPositions(self):
        for bullet in self.bullets:
            bullet.move()

    # Draw bullets
    def drawBullets(self):
        for bullet in self.bullets:
            drawCircle(bullet.x, bullet.y, 5, fill='red')

    def startBombDropping(self, app):
        angle = self.angle
        bombSpeed = 10
        xSpeed = bombSpeed * math.sin(angle)
        ySpeed = bombSpeed * math.cos(angle)
        bomb = Bomb(self.app, self.planeX, self.planeY, xSpeed, ySpeed, owner='player')
        self.bombs.append(bomb)
    
    def updateBombPositions(self):
        for bomb in self.bombs:
            bomb.move()
    
    # Draw bullets
    def drawBombs(self):
        for bomb in self.bombs:
            drawCircle(bomb.x, bomb.y, 5, fill='pink')

    def drawPlane(self):
        # Draw the player's plane as an oriented triangle
        noseX = self.planeX + 30 * math.cos(self.angle)
        noseY = self.planeY + 30 * math.sin(self.angle)
        wing1X = self.planeX + 15 * math.cos(self.angle + math.pi / 2)
        wing1Y = self.planeY + 15 * math.sin(self.angle + math.pi / 2)
        wing2X = self.planeX + 15 * math.cos(self.angle - math.pi / 2)
        wing2Y = self.planeY + 15 * math.sin(self.angle - math.pi / 2)

        drawPolygon(noseX, noseY, wing1X, wing1Y, wing2X, wing2Y, fill=self.fill)
from cmu_graphics import *
import math
import random # Source for all random methods and functions: https://docs.python.org/3/library/random.html
from bulletsbombs import Bullet
from bulletsbombs import Bomb

# Enemy class
class Enemy:
    def __init__(self, app):
        self.app = app
        self.planeX = 300
        self.planeY = 20  # Starting position at the top
        self.speed = 5  # Speed control for the enemy plane
        self.fill = 'red'
        self.bullets = []  # List to store enemy bullet information
        self.bombs = [] # List to store bomb information
        self.fireCooldownCounter = 0  # Counter for controlling firing rate
        self.score = 10000  # Enemy's score
        self.ignoreCollision = False  # Flag to ignore collisions for a brief period after a collision
        self.collisionCooldownCounter = 0  # Counter for collision cooldown
        self.followPlayer = True  # Flag to determine whether the enemy should follow the player
        self.waitCounter = 0
        self.angle = 0
        self.currentWeaponMode = 'Regular Gun'
        self.machineGunAmmo = 90 # Machine Gun Ammo Limit
        self.bombAmmo = 20 # Bomb Ammo Limit
        # Add enemy to world elements
        app.worldElements.append(self)

    def moveTowardsPlayer(self):
        # Move the enemy plane towards the player
        angle = math.atan2(self.app.player.planeY - self.planeY, self.app.player.planeX - self.planeX)
        xSpeed = self.speed * math.cos(angle)
        ySpeed = self.speed * math.sin(angle)

        # Move the enemy plane with adjusted speed
        self.planeX += xSpeed
        self.planeY += ySpeed

    def moveRandomly(self):
        # Move the enemy plane randomly
        angle = random.uniform(0, 2 * math.pi)  # Choose a random angle in radians
        distance = random.uniform(0, self.speed)  # Choose a random distance within the speed range

        # Calculate the new position based on the chosen angle and distance
        self.planeX += distance * math.cos(angle)
        self.planeY += distance * math.sin(angle)

        # Ensure the new position is within the playable area
        self.planeX = max(0, min(self.app.width, self.planeX))
        self.planeY = max(0, min(self.app.height, self.planeY))


    def startShooting(self, app):
        bulletSpeed = 20
        fireCooldown = 10 # Control firing rate
        machineGunMode = 'Machine Gun'
        bombMode = 'Bomb'
        regularBulletMode = 'Regular Gun'
        if self.followPlayer:
            if self.currentWeaponMode == regularBulletMode and self.fireCooldownCounter == 0:
                # Start shooting bullets towards the player
                angle = math.atan2(
                    self.app.player.planeY - self.planeY, 
                    self.app.player.planeX - self.planeX
                )
                self.angle = angle  # Update plane's angle
                xSpeed = bulletSpeed * math.cos(angle)
                ySpeed = bulletSpeed * math.sin(angle)
                bullet = Bullet(self.app, self.planeX, self.planeY, xSpeed, ySpeed, owner='enemy')
                self.bullets.append(bullet)  # Append the bullet to the enemy's bullets list
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
        angle = math.atan2(
                self.app.player.planeY - self.planeY, 
                self.app.player.planeX - self.planeX
            )
        self.angle = angle
        bulletSpread = 20
        for i in range(-1, 2):  # Create three rows of bullets
            adjustedAngle = angle + i * math.radians(bulletSpread)
            xSpeed = bulletSpeed * math.cos(adjustedAngle)
            ySpeed = bulletSpeed * math.sin(adjustedAngle)
            bullet = Bullet(self.app, self.planeX, self.planeY, xSpeed, ySpeed, owner='enemy')
            self.bullets.append(bullet)
            self.fireCooldownCounter = fireCooldown

    def updateBulletPositions(self):
        for bullet in self.bullets:
            bullet.move()  # Move the bullet according to its speed

    def drawBullets(self):
        # Draw the bullets in the redrawAll function
        for bullet in self.bullets:
            drawCircle(bullet.x, bullet.y, 5, fill='green')

    def startBombDropping(self, app):
        angle = self.angle
        bombSpeed = 10
        xSpeed = bombSpeed * math.sin(angle)
        ySpeed = bombSpeed * math.cos(angle)
        bomb = Bomb(self.app, self.planeX, self.planeY, xSpeed, ySpeed, owner='enemy')
        self.bombs.append(bomb)
    
    def updateBombPositions(self):
        for bomb in self.bombs:
            bomb.move() # Move the bomb according to its speed
    
    # Draw bombs
    def drawBombs(self):
        for bomb in self.bombs:
            drawCircle(bomb.x, bomb.y, 5, fill='pink')

    def drawPlane(self):
        # Draw the enemy plane as an oriented triangle
        if self.app.player.planeX - self.planeX != 0:
            angle = math.atan2(self.app.player.planeY - self.planeY, self.app.player.planeX - self.planeX)
        else:
            # Default angle if the player and enemy have the same X-coordinate
            angle = 0

        noseX = self.planeX + 30 * math.cos(angle)
        noseY = self.planeY + 30 * math.sin(angle)
        wing1X = self.planeX + 15 * math.cos(angle + math.pi / 2)
        wing1Y = self.planeY + 15 * math.sin(angle + math.pi / 2)
        wing2X = self.planeX + 15 * math.cos(angle - math.pi / 2)
        wing2Y = self.planeY + 15 * math.sin(angle - math.pi / 2)

        # Draw the plane using these points
        drawPolygon(noseX, noseY, wing1X, wing1Y, wing2X, wing2Y, fill=self.fill)

    def handleCollision(self):
        collisionCooldown = 1000  # Control the collision cooldown duration
        # Set the enemy to move randomly and wait for a cooldown period
        self.followPlayer = False
        self.collisionCooldownCounter = collisionCooldown
        self.fill = 'yellow'

    def update(self):
        # Update the enemy's state and behavior
        if self.followPlayer:
            self.moveTowardsPlayer()
        else:
            self.moveRandomly()

        # Handle collision cooldown
        if self.collisionCooldownCounter > 0:
            self.collisionCooldownCounter -= 1
        else:
            # Reset to follow the player after the cooldown period
            self.followPlayer = True

        # Update enemy state
        self.updateEnemyState()

    def updateEnemyState(self):
        # Change the enemy state by updating the wait counter
        if not self.followPlayer and self.waitCounter > 0:
            self.waitCounter -= 1
        elif not self.followPlayer:
            self.fill = 'red'
            self.followPlayer = True
            self.waitCounter = 100  # Adjust the wait duration as needed
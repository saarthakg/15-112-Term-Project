from cmu_graphics import *
import math
import random # Source for all random methods and functions: https://docs.python.org/3/library/random.html
from PIL import Image
import os, pathlib
from player import Player
from weaponpackages import WeaponPackage
from bulletsbombs import Bullet 
from bulletsbombs import Bomb
from enemy import Enemy
from terrainelements import TerrainElement
from world import World

# Function to create the terrain elements based on some random points
def createRandomTerrain(app):
    terrainElements = []

    # Generate random y points for the hilly terrain
    yPoints = [random.uniform(app.height * 0.7, app.height-20) for _ in range(10)]

    # Generate random x points for the hilly terrain
    xPoints = [random.randrange(10, app.width-10, 60) for _ in range(10)]
    # Ensure the x points are sorted
    xPoints.sort()

    # Create the towers
    for y in yPoints:
        towerX = random.uniform(10, app.width)
        towerY = y
        tower = TerrainElement(app, towerX, towerY, points = None, shapeType='tower', fill='gray', border='black')
        terrainElements.append(tower)

    # Create a continuous polygon for the hill
    hillPoints = [0, app.height, 0, app.height - 100]
    # Interleave the xPoints and yPoints list to make a final points list
    pointsList = interleave(xPoints, yPoints)
    for point in pointsList:
        hillPoints.append(point)
    hillPoints.append(app.width)
    hillPoints.append(app.height - 100)    
    hillPoints.append(app.width)
    hillPoints.append(app.height)
    hill = TerrainElement(app, x = None, y = None, points = hillPoints, shapeType='hill', fill='forestGreen', border='darkOliveGreen')
    terrainElements.append(hill)

    return terrainElements
    
# Recursive function to interleave two lists
def interleave(L, M): # CS Academy Problem (solved by me): https://academy.cs.cmu.edu/exercise/13176
    if L == []:
        return M
    if M == []:
        return L
    else:
        LFirst = L[0]
        LRest = L[1:]
        MFirst = M[0]
        MRest = M[1:]
        return [LFirst,MFirst] + interleave(LRest,MRest)

# Game initialization variables
def onAppStart(app):
    app.stepsPerSecond = 30
    app.width = 800
    app.height = 600
    app.worldElements = []
    app.player = Player(app)
    app.enemy = Enemy(app)
    app.scrollX = 0 # x offset from scrolling
    app.scrollY = 0 # y offset from scrolling
    app.mouseX = 0
    app.mouseY = 0
    app.terrainElements = createRandomTerrain(app)
    app.world = createWorld(app)
    app.packageElements = []
    app.background = 'skyBlue'
    app.gameOver = False
    app.margin = 5
    app.image1 = openImage("images/sky.jpeg") # Image Source: https://unsplash.com/s/photos/starry-sky
    app.image2 = openImage("images/title.jpeg") # Image Source: https://www.steamgriddb.com/game/5326986/grids
    app.image1 = CMUImage(app.image1)
    app.image2 = CMUImage(app.image2)

# Taken from Images Demo File linked from Piazza
def openImage(fileName):
        return Image.open(os.path.join(pathlib.Path(__file__).parent,fileName))

# Mouse movement event
def onMouseMove(app, mouseX, mouseY):
    if not app.gameOver:
        app.mouseX = mouseX
        app.mouseY = mouseY
        # Calculate scrolling based on mouse movement
        app.scrollX, app.scrollY = app.player.moveTowardsMouse(app.mouseX, app.mouseY)
        updateWorldPositions(app, app.scrollX, app.scrollY)

# Key press event
def onKeyPress(app, key):
    if key == 'space':
        app.player.isFiring = True
        app.player.fireCooldownCounter = 0
    elif key == 'r' and app.gameOver:
        resetGame(app)

def resetGame(app):
    app.gameOver = False
    
    # Reset player state
    app.player = Player(app)

    # Reset enemy state
    app.enemy = Enemy(app)

    # Clear bullets, enemy bullets, and other objects
    app.player.bullets.clear()
    app.enemy.bullets.clear()
    app.packageElements.clear()

# Key release event
def onKeyRelease(app, key):
    if key == 'space':
        app.player.isFiring = False
        app.player.fireCooldownCounter = 0

# Step event
def onStep(app):
    fireCooldown = 10 # Control firing rate
    if not app.gameOver:
        # Check for game over conditions
        if app.player.score < -10000:
            app.gameOver = True
            app.gameOverMessage = "You lost! Press 'r' to play again!"
        elif app.enemy.score < -10000:
            app.gameOver = True
            app.gameOverMessage = "You won! Press 'r' to play again!"
        
        # Player actions
        if app.player.isFiring and app.player.fireCooldownCounter == 0:
            app.player.startShooting(app)
            app.player.fireCooldownCounter = fireCooldown
        elif app.player.fireCooldownCounter > 0:
            app.player.fireCooldownCounter -= 1
        app.player.updateBulletPositions()
        app.player.updateBombPositions()

        # Enemy actions
        app.enemy.update()
        if app.enemy.fireCooldownCounter == 0:
            app.enemy.startShooting(app)
            app.enemy.fireCooldownCounter = fireCooldown
        elif app.enemy.fireCooldownCounter > 0:
            app.enemy.fireCooldownCounter -= 1
        app.enemy.updateBulletPositions()
        app.enemy.updateBombPositions()

    # Create falling weapon packages
    machineGunMode = 'Machine Gun'
    bombMode = 'Bomb'
    if random.random() < 0.02:  # Adjust the probability as needed
        weaponType = random.choice([machineGunMode, bombMode])
        weaponPackage = WeaponPackage(app, random.uniform(0, app.width), app.world[1].y - 10, weaponType)
        app.packageElements.append(weaponPackage)

    # Update positions of falling weapon packages
    for element in app.worldElements:
        if isinstance(element, WeaponPackage):
            element.move()

    # Check for collisions between player and weapon packages
    checkWeaponPackageCollisions(app, app.player, app.packageElements)
    checkWeaponPackageCollisions(app, app.enemy, app.packageElements)

    # Check for collisions between bullets and update scores
    checkBulletCollisions(app.player, app.enemy)
    checkBulletCollisions(app.enemy, app.player)
    checkBombCollisions(app.player, app.enemy)

    # Check for collisions between planes and terrain elements and decrement scores
    checkPlaneCollisions(app.player, app.enemy)

    # Handle collision cooldown
    if app.player.collisionCooldownCounter > 0:
        app.player.collisionCooldownCounter -= 1
    if app.enemy.collisionCooldownCounter > 0:
        app.enemy.collisionCooldownCounter -= 1

    # Update scores based on time spent outside the playable area
    updateScoresOutsidePlayableArea(app.player, app.terrainElements, app.world, owner='player')
    updateScoresOutsidePlayableArea(app.enemy, app.terrainElements, app.world, owner='enemy')

# Function to check collisions between player and weapon packages
def checkWeaponPackageCollisions(app, plane, packageElements):
    collectionDistance = 300
    for package in packageElements:
        distance = ((plane.planeX - package.x)**2 + (plane.planeY - package.y)**2)**0.5
        if distance < collectionDistance:
            package.collectPackage(app, plane, package.weaponType)

# Function to check collisions between bullets and update scores
def checkBulletCollisions(attacker, target):
    collisionRadius = 20  # Radius within which collision is considered
    for bullet in attacker.bullets:
        if (
            bullet.owner == 'player'
            and target.planeX - collisionRadius < bullet.x < target.planeX + collisionRadius
            and target.planeY - collisionRadius < bullet.y < target.planeY + collisionRadius
        ):
            # Player's bullet hit the enemy
            attacker.score += 1000
            target.score -= 500
        elif (
            bullet.owner == 'enemy'
            and attacker.planeX - collisionRadius < bullet.x < attacker.planeX + collisionRadius
            and attacker.planeY - collisionRadius < bullet.y < attacker.planeY + collisionRadius
        ):
            # Enemy's bullet hit the player
            attacker.score += 200
            target.score -= 50

# Function to check collisions between bullets and update scores
def checkBombCollisions(attacker, target):
    collisionRadius = 20  # Radius within which collision is considered
    for bomb in attacker.bombs:
        if (
            bomb.owner == 'player'
            and target.planeX - collisionRadius < bomb.x < target.planeX + collisionRadius
            and target.planeY - collisionRadius < bomb.y < target.planeY + collisionRadius
        ):
            # Player's bomb hit the enemy
            attacker.score += 1000
            target.score -= 500
        elif (
            bomb.owner == 'enemy'
            and attacker.planeX - collisionRadius < bomb.x < attacker.planeX + collisionRadius
            and attacker.planeY - collisionRadius < bomb.y < attacker.planeY + collisionRadius
        ):
            # Enemy's bomb hit the player
            attacker.score += 200
            target.score -= 50

# Function to check collisions between planes and decrement scores
def checkPlaneCollisions(player, enemy):
    planeCollisionPenalty = 20  # Score decrement on plane collision
    collisionRadius = 20  # Radius within which collision is considered
    if (
        player.planeX - collisionRadius < enemy.planeX < player.planeX + collisionRadius
        and player.planeY - collisionRadius < enemy.planeY < player.planeY + collisionRadius
        ):
        # Planes collided
        # Decrease player's score
        player.score -= planeCollisionPenalty
        # Decrease enemy's score
        enemy.score -= planeCollisionPenalty
        enemy.handleCollision()

def createWorld(app):
    world = []

    # Create sky
    x3 = app.width / 2
    y3 = - 100
    sky = World(app, x3, y3, shapeType = 'sky', fill='red')
    world.append(sky)

    # Create sea
    x2 = app.width / 2
    y2 = app.height
    sea = World(app, x2, y2, shapeType='sea', fill='royalBlue')
    world.append(sea)

    # Create border
    x1 = app.width / 2
    y1 = app.height / 2
    border = World(app, x1, y1, shapeType='border', fill=None)
    world.append(border)

    return world

# Function to update positions of all world elements
def updateWorldPositions(app, scrollX, scrollY):
    for element in app.worldElements:
        if isinstance(element, Bullet):
            element.x -= scrollX
            element.y -= scrollY

        if isinstance(element, Bomb):
            element.x -= scrollX
            element.y -= scrollY

        elif isinstance(element, Enemy):
            element.planeX -= scrollX
            element.planeY -= scrollY

        elif isinstance(element, TerrainElement):
            if element.shapeType == 'hill':
                for i in range(0, len(element.points), 2):
                    element.points[i] -= scrollX
                    element.points[i+1] -= scrollY
            elif element.shapeType == 'tower':
                element.x -= scrollX
                element.y -= scrollY
        
        elif isinstance(element, World):
            element.x -= scrollX
            element.y -= scrollY

        elif isinstance(element, WeaponPackage):
            element.x -= scrollX
            element.y -= scrollY    

def updateScoresOutsidePlayableArea(plane, terrainElements, worldElements, owner):
    terrainCollisionPenalty = 500 # Score decrement on terrain collision
    collisionRadius = 20  # Radius within which collision is considered
    # Check if the plane is colliding with any terrain element
    for terrainElement in terrainElements:
        if terrainElement.shapeType == 'hill':
            for i in range(0, len(terrainElement.points), 2):
                if (
                    plane.planeX - collisionRadius < terrainElement.points[i] < plane.planeX + collisionRadius
                    and plane.planeY - collisionRadius < terrainElement.points[i+1] < plane.planeY + collisionRadius
                ):
                    # Decrease the plane's score
                    if owner == 'player':
                        plane.score -= terrainCollisionPenalty
                    elif owner == 'enemy':
                        plane.score -= (0.5 * terrainCollisionPenalty)
        elif terrainElement.shapeType == 'tower':
            if (
                plane.planeX - collisionRadius < terrainElement.x < plane.planeX + collisionRadius
                and plane.planeY - collisionRadius < terrainElement.y < plane.planeY + collisionRadius
            ):
                # Decrease the plane's score
                if owner == 'player':
                    plane.score -= terrainCollisionPenalty
                elif owner == 'enemy':
                    plane.score -= (0.5 * terrainCollisionPenalty)
    
    # Check if the plane is colliding with any world element
    for worldElement in worldElements:
        if worldElement.shapeType == 'sea':
            if (
                worldElement.y < plane.planeY
            ):
                # Decrease the plane's score
                if owner == 'player':
                    plane.score -= 10
                elif owner == 'enemy':
                    plane.score -= 5
        elif worldElement.shapeType == 'border':
            if (
                (worldElement.x > plane.planeX) 
                or (worldElement.x + 800 < plane.planeX)
                or  (worldElement.y > plane.planeY)
            ):
                # Decrease the plane's score
                if owner == 'player':
                    plane.score -= 10
                elif owner == 'enemy':
                    plane.score -= 5     

# Redraw event
def redrawAll(app):
    # Draw sky and border
    for worldElement in app.world:
        if worldElement.shapeType == 'sky':
            worldElement.drawSky(app)
        elif worldElement.shapeType == 'border':
            worldElement.drawBorder()
    
    # Draw the player's plane
    app.player.drawPlane()
    # Draw enemy plane
    app.enemy.drawPlane()

    # Draw bullets and bombs
    app.player.drawBullets()
    app.player.drawBombs()
    app.enemy.drawBullets()
    app.enemy.drawBombs()

    # Draw falling weapon packages
    for packageElement in app.packageElements:
        if isinstance(packageElement, WeaponPackage):
            if packageElement.weaponType != 'Regular Gun':
                packageElement.drawPackage()

    # Draw terrain elements
    for terrainElement in app.terrainElements:
        if terrainElement.shapeType == 'tower':
            terrainElement.drawTower()
        elif terrainElement.shapeType == 'hill':
            terrainElement.drawHill()

    # Draw sea
    for worldElement in app.world:
        if worldElement.shapeType == 'sea':
            worldElement.drawSea()

    # Display scores
    drawLabel(f"Player Score: {app.player.score}", 700, 10, size=14, fill='yellow')
    drawLabel(f"Player Weapon: {app.player.currentWeaponMode}", 700, 30, size=14, fill='yellow')
    drawLabel(f"Enemy Score: {app.enemy.score}", 700, 50, size=14, fill='yellow')

    # Check if the game is over
    if app.gameOver:
        drawLabel(app.gameOverMessage, app.width / 2, app.height / 2, size=50, fill='yellow', bold=True)

# Main execution
if __name__ == "__main__":
    runApp(width=800, height=600)

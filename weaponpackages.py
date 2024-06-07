from cmu_graphics import *

# Weapon package class
class WeaponPackage:
    def __init__(self, app, x, y, weaponType):
        self.app = app
        self.x = x
        self.y = y
        self.ySpeed = 5
        self.width = 20
        self.height = 20
        self.weaponType = weaponType  # Type of weapon in the package (machine gun, bomb)
        # Add weapon package to world elements
        app.worldElements.append(self)

    def drawPackage(self):
        machineGunMode = 'Machine Gun'
        bombMode = 'Bomb'
        if self.weaponType == machineGunMode:
            fill = 'navajoWhite'
        elif self.weaponType == bombMode:
            fill = 'mediumOrchid'
        drawRect(self.x - self.width / 2, self.y - 600 - self.height / 2, self.width, self.height, fill=fill, align='center')

    def collectPackage(self, app, plane, weaponType):
        machineGunMode = 'Machine Gun'
        bombMode = 'Bomb'
        machineGunAmmoLimit = 90
        bombAmmoLimit = 20
        if weaponType == machineGunMode:
            plane.currentWeaponMode = machineGunMode
            plane.machineGunAmmo = machineGunAmmoLimit
        elif weaponType == bombMode:
            plane.currentWeaponMode = bombMode
            plane.bombAmmo = bombAmmoLimit

        # Remove the collected package
        if self in app.packageElements:
            app.packageElements.remove(self)
    
    # Move function
    def move(self):
        self.y += self.ySpeed
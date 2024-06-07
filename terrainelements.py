from cmu_graphics import *

# Terrain Elements class
class TerrainElement:
    def __init__(self, app, x, y, points, shapeType, fill, border):
        self.app = app
        self.points = points
        self.shapeType = shapeType
        self.fill = fill
        self.border = border
        self.visible = True
        self.x = x
        self.y = y
        if self.y != None:
            self.height = app.height - self.y
        # Add terrain element to world elements
        app.worldElements.append(self)

    # Draw the hill
    def drawHill(self):
        if self.visible:
            drawPolygon(*self.points, fill=self.fill, border=self.border)

    # Draw the tower
    def drawTower(self):
        if self.visible:
            drawRect(self.x, self.y, 30, self.height, fill=self.fill, border=self.border, align='top')
from cmu_graphics import *

# World Class
class World:
    def __init__(self, app, x, y, shapeType, fill=None):
        self.app = app
        self.x = x
        self.y = y
        self.shapeType = shapeType
        self.fill = fill
        # Add world to world elements
        app.worldElements.append(self)

    def drawBorder(self):
        drawRect(self.x, self.y, 800, 600, fill=self.fill, border='darkRed', borderWidth=10, align='center')

    def drawSea(self):
        drawRect(self.x, self.y, 800*100, 50, fill=self.fill, align='center')

    def drawSky(self, app):
        # Scale image by defining new dimensions 
        newWidth, newHeight = (app.width*3,app.height*3)
        drawImage(app.image1,self.x,self.y,width=newWidth,height=newHeight, align='center')
        
        drawImage(app.image2,self.x,self.y - 150,width=600, height=200, align='center')

        drawLabel('RESTRICTED AIRSPACE', self.x, self.y, size=30, font='monospace', bold=True, fill=self.fill)
        drawLabel('Pick up the falling weapon packages!', self.x, self.y + 30, size=20, font='montserrat', fill='lightGreen')
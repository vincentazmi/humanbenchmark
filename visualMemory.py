from PIL import Image
import pyautogui

class MemoryBot():
    

    def __init__(self,
                 bgColour=None, boxColour=None,
                 topLeft=None,bottomRight=None):
        # Preset Colours
        if bgColour != None and boxColour != None:
            self.bgColour = bgColour
            self.boxColour = boxColour
        # Not preset colours
        else: self.getColours()

        # Preset area
        if topLeft != None and bottomRight != None:
            self.topLeft = topLeft
            self.bottomRight = bottomRight
        # Not preset area
        else:
            topLeft, bottomRight = self.getArea()
            
        self.top = topLeft[1]
        self.left = topLeft[0]
        self.bottom = bottomRight[1]
        self.right = bottomRight[0]

        self.width = self.right - self.left
        self.height = self.bottom - self.top

        self.getBoxValues()

    

        

    # Get area of squares in terms of screen coords
    def getArea(self):
        input('''
Position the cursor:
1. ABOVE the top left box
  AND
2. LEFT of the top left box

Then press enter in this window.
''')
        topLeft = pyautogui.position()

        input('''
Position the cursor:
1. BELOW the bottom right box
  AND
2. RIGHT of the bottom right box

Then press enter in this window.
''')
        bottomRight = pyautogui.position()

        print(topLeft, bottomRight)
    
        return topLeft,bottomRight

    def getColours(self):
        ss = pyautogui.screenshot()
        
        input('''
Position the cursor:
1. Over the background colour

Then press enter in this window.
''')
        x,y = pyautogui.position()
        self.bgColour = ss.getpixel((x,y))
        
        input('''
Position the cursor:
1. Over any dark box.

Then press enter in this window.
''')
        x,y = pyautogui.position()
        self.boxColour = ss.getpixel((x,y))

        print(self.bgColour, self.boxColour)

    # Get the number of boxes
    def getBoxValues(self, DEBUG=False):
        ss = pyautogui.screenshot(region=(self.left,self.top,
                                          self.width, self.height))

        # topLeftCorner will be used to create the perfect screenshot region
        topLeftCorner = (0,0)
        # topY will keep y value of the start of the top box
        # bottomy will keep y value of the end of the bottom box
        topY,bottomY = 0,0
        # boxHeight will hold the start and end y coordinate of the first box
        boxHeight = [0,0]
        
        boxCount = 0
        # inBox is used to count the boxes
        inBox = False

        # For loop goes from left to right, top to bottom
        for x in range(self.width):
            for y in range(self.height):
                px = ss.getpixel((x,y))

                if not inBox and px != self.bgColour:
                    # Box found
                    inBox = True
                    boxCount += 1

                    # DEBUG highlight
                    if DEBUG: ss.putpixel((x, y), (0, 255, 0))

                    # Only run the first time
                    if boxHeight[0] == 0:
                        topLeftCorner = (x,y)
                        boxHeight[0] = y

                    # Only run the first time
                    if topY == 0: topY = y
                    

                elif inBox and px == self.bgColour:
                    # Box ended
                    inBox = False

                    # DEBUG highlight
                    if DEBUG: ss.putpixel((x, y), (255, 0, 0))

                    # Only run the first time
                    if boxHeight[1] == 0: boxHeight[1] = y

                    # Will remember the last box's bottom y coordinate
                    bottomY = y
                    
                    
                    
            
            if boxCount > 0: break
            
        # DEBUG image
        if DEBUG: ss.save("modified_screenshot.png")
        
        self.boxCount = boxCount
        self.boxSize = int(boxHeight[1] - boxHeight[0])
        
        self.gapSize = ((bottomY-topY)-self.boxSize*self.boxCount)/self.boxCount
        
        self.top += topLeftCorner[1]
        self.left += topLeftCorner[0]
        self.right = int(self.left + self.boxSize*self.boxCount + self.gapSize*(self.boxCount-1))
        self.bottom = int(self.top + self.boxSize*self.boxCount + self.gapSize*(self.boxCount-1))
        
        self.width = self.right - self.left
        self.height = self.bottom - self.top

        
        self.boxCount **= 2
        # DEBUG output 9 [12, 120] 108 16.0 12 10 366.0 368.0 356.0 356.0
        if DEBUG:
            print(self.boxCount,boxHeight,self.boxSize,self.gapSize,
                        self.top,self.left,self.right,self.bottom,self.width,self.height)
            ss = pyautogui.screenshot(region=(self.left,self.top,
                                              self.width, self.height))
            ss.save("perfect_screenshot_region.png")
            

    def waitForFlash(self):
        # After start is clicked this method will wait for the level start 'flash'

        white = False
        # gapColour gets the pixel colour halfway between the top left two boxes
        for i in range(1000):
            gapColour = pyautogui.pixel(self.left+(self.boxSize+int(self.gapSize/2)),self.top)

##            print(gapColour)
            
            if gapColour == (62, 184, 255):
                print("WHITE")
                white = True
                
            if white: break
        

        
        

    def getWhiteBoxes(self):
        ss = pyautogui.screenshot(region=(self.left,self.top,
                                          self.width, self.height))

        # Start and step values to get x,y coords of the center of the boxes
        start = int(self.boxSize/2)
        step = int(self.boxSize+(self.gapSize/2))

        
        whiteList = []
        for x in range(start,self.width,step):
            for y in range(start,self.height,step):
                px = ss.getpixel((x,y))
                if px == (255,255,255):
                    whiteList.append(px)

        print("whiteList=",whiteList)
        
                
                
                

'''
Presets
bgColour=(43, 135, 209)
boxColour=(37, 115, 193)
topLeft = (1072, 262)
bottomRight = (1468, 660)
'''

if __name__ == "__main__":
    bgColour=(43, 135, 209)
    boxColour=(37, 115, 193)
    topLeft = (1072, 262)
    bottomRight = (1468, 660)
    bot = MemoryBot(bgColour, boxColour,
                      topLeft, bottomRight)

##    bot.getBoxValues(DEBUG=True)
    input("ready")
    bot.waitForFlash()
                           
    



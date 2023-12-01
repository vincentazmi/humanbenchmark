from PIL import Image
import pyautogui, time

class MemoryBot():
    
    def __init__(self,
                 bgColour=None, boxColour=None,
                 topLeft=None,bottomRight=None,DEBUG=False):
        # Preset Colours
        if bgColour != None and boxColour != None:
            self.bgColour = bgColour
            self.boxColour = boxColour
        # Not preset colours
        else: self.getColours(DEBUG)

        # Preset area
        if topLeft != None and bottomRight != None:
            self.topLeft = topLeft
            self.bottomRight = bottomRight
            
            self.top = topLeft[1]
            self.left = topLeft[0]
            self.bottom = bottomRight[1]
            self.right = bottomRight[0]

            self.width = self.right - self.left
            self.height = self.bottom - self.top
        # Not preset area
        else: self.getBoxArea(DEBUG)

        self.getBoxCount(DEBUG,saveImage=True)

        self.getBoxGapSize(DEBUG)

        self.getPerfectScreenshotRegion(DEBUG)

        input("ready")
        
        if self.waitForFlash(DEBUG):
            self.getWhiteBoxes(DEBUG)
            self.clickWhiteBoxes(DEBUG)
        else: return

        while self.waitForFlash(DEBUG):
            self.getBoxCount(DEBUG)
            self.getBoxGapSize(DEBUG)
            self.getWhiteBoxes(DEBUG)
            self.clickWhiteBoxes(DEBUG)
            

        


    def getColours(self,DEBUG=False):
        ss = pyautogui.screenshot()
        
        input('''
Position the cursor:
1. Over the background.

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

        if DEBUG: print('''
getColours()
bgColour = {}
boxColour = {}
'''.format(self.bgColour,self.boxColour))







    # Get area of squares in terms of screen coords
    def getBoxArea(self, DEBUG=False):
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

        if DEBUG: print('''
getBoxArea()
topLeft = {}
bottomRight = {}
'''.format(topLeft,bottomRight))

        self.top = topLeft[1]
        self.left = topLeft[0]
        self.bottom = bottomRight[1]
        self.right = bottomRight[0]

        self.width = self.right - self.left
        self.height = self.bottom - self.top






    def takeScreenshot(self):
        self.ss = pyautogui.screenshot(region=(self.left,self.top,
                                          self.width, self.height))





    def getBoxCount(self,DEBUG=False,saveImage=False):
        self.takeScreenshot()
        
        boxCount = 0
        # inBox is used to count the boxes
        inBox = False
        
        # For loop goes from left to right, top to bottom
        for x in range(self.width):
            for y in range(self.height):
                px = self.ss.getpixel((x,y))

                if not inBox and px != self.bgColour:
                    # Box found
                    inBox = True
                    boxCount += 1

                    # DEBUG highlight
                    if saveImage: self.ss.putpixel((x, y), (0, 255, 0))
                    

                elif inBox and px == self.bgColour:
                    # Box ended
                    inBox = False

                    # DEBUG highlight
                    if saveImage: self.ss.putpixel((x, y), (255, 0, 0))
                    
            if boxCount > 2:
                boxCount**=2
                break

        if DEBUG: print('''
getBoxCount()
boxCount = {}
'''.format(boxCount))
        if saveImage: self.ss.save("boxCount_screenshot.png")

        
        if boxCount > 8:
            self.boxCount = boxCount





    def getBoxGapSize(self,DEBUG=False):
        self.takeScreenshot()

        lockY,startX,endX = 0,0,0
        boxSize,gapSize = 0,0
        for x in range(self.width):
            for y in range(self.height): # lockY stops this loop
                if lockY != 0: break

                px = self.ss.getpixel((x,y))

                if px != self.bgColour:
                    if lockY == 0:
                        startX = x
                        lockY = y

            # lockY starts here going along x axis now
            if lockY != 0: 
                px = self.ss.getpixel((x,lockY))     

                if boxSize == 0 and px == self.bgColour:
                    # is true when end of box is reached to calculate boxSize
                    endX = x
                    boxSize = endX - startX
                    
                    startX = x # start counting the gap

                if boxSize != 0 and px != self.bgColour:
                    # is true when start of next box is reached to calculate gapSize
                    endX = x
                    gapSize = endX - startX

                if boxSize != 0 and gapSize != 0: break


        if DEBUG: print('''
getBoxGapSize()
boxSize = {}
gapSize = {}
'''.format(boxSize,gapSize))

        if boxSize != 0 and gapSize != 0:
            self.boxSize = boxSize
            self.gapSize = gapSize





    def getPerfectScreenshotRegion(self,DEBUG=False):
        self.takeScreenshot()

        if DEBUG: print("getPerfectScreenshotRegion()")

        newX,newY = 0,0
        for x in range(self.width):
            for y in range(self.height):
                
                try:
                    px = self.ss.getpixel((x,y))

                    if px != self.bgColour:
                        newX = x
                        break
                except IndexError:
                    print('''
x = {}
y = {}
'''.format(x,y))
            if newX != 0: break

        if DEBUG: print("getPerfectScreenshotRegion()")
        
        for y in range(self.height):
            for x in range(self.width):
                try:
                    px = self.ss.getpixel((x,y))

                    if px != self.bgColour:
                        newY = y
                        break
                except IndexError:
                    print('''
IndexError at
y = {}
x = {}
'''.format(y,x))
            if newY != 0: break

        self.left += newX
        
        self.top += newY

        # for a 3x3 grid:
        # (9**0.5 = 3*boxSize) +
        # (9**0.5 = 3-1 = 2*gapSize)
        length = int((self.boxCount**0.5)*self.boxSize)
        length += int((self.boxCount**0.5-1)*self.gapSize)

        self.right = self.left + length
        self.bottom = self.top + length

        self.width = self.right - self.left
        self.height = self.bottom - self.top

        self.takeScreenshot()
        self.ss.save("perfect_screenshot_region.png")
                
        


            
    def waitForFlash(self, DEBUG=False):
        # After start is clicked this method will wait for the level start 'flash'

        if DEBUG: pyautogui.moveTo(self.left,self.top-5)
        
        white = False
        # gapColour gets the pixel above the top left box
        for i in range(1000):
            gapColour = pyautogui.pixel(self.left,self.top-5)
            

##            print(gapColour)
            
            if gapColour == (62, 184, 255):
                if DEBUG: print("WHITE")
                white = True
                
            if white: break
        if white:
            time.sleep(1.4)
            if DEBUG: print("WAIT FOR FLASH NOW**************************************")
            self.takeScreenshot()

            if DEBUG: self.ss.save("white_screenshot.png")
            
            self.whiteScreenshot = self.ss
            return True
        else:
            print("waitForFlash not found")
            return False




        
    def getBoxGridStartStep(self,DEBUG):

        self.gridStart = int(self.left + (self.boxSize/2))

        self.gridStep = int(self.boxSize + self.gapSize)

        

        if DEBUG: print('''
getWhiteBoxes()
gridStart = {}
gridStep = {}
'''.format(self.gridStart,self.gridStep))


    

    def getWhiteBoxes(self,DEBUG=False):
        
        time.sleep(2)
        
        # Start and step values to get x,y coords of the center of the boxes
        self.getBoxGridStartStep(DEBUG)

        whiteList = []
        for x in range(self.gridStart,self.width,self.gridStep):
            for y in range(self.gridStart,self.height,self.gridStep):
                px = self.ss.getpixel((x,y))

                gridX = int((x-start)/step)
                gridY = int((y-start)/step)
                
                if DEBUG: print('''
x = {}
y = {}
RGB = {} {}
'''.format(gridX,
           gridY,
           px,"WHITE" if px == (255,255,255) else ""))
                
                if px == (255,255,255):
                    whiteList.append((gridX,gridY))
                

        if DEBUG: print("whiteList=",whiteList)

        self.whiteList = whiteList



    
        
    def clickWhiteBoxes(self,DEBUG=False):
        time.sleep(2)
        self.getBoxGridStartStep(DEBUG)
        
        for (x,y) in self.whiteList:
            
            if DEBUG: print("click",x*self.gridStep,y*self.gridStep)
            pyautogui.click(x*self.gridStep,y*self.gridStep)

        

'''
Presets
bgColour = (43, 135, 209)
boxColour = (37, 115, 193)
topLeft = (1076, 263)
bottomRight = (1466, 658)
'''

if __name__ == "__main__":
    bgColour = (43, 135, 209)
    boxColour = (37, 115, 193)
    topLeft = (1076, 263)
    bottomRight = (1466, 658)
    bot = MemoryBot(bgColour,boxColour,
                    topLeft,bottomRight,
                    DEBUG=True)
    
                           
    















'''
# Get the number of boxes
    def getBoxValues(self, DEBUG=False):
        if DEBUG: print("BOX VALUES NOW*****************************************")
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
                        print("change box height",x,y)
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
                    if boxHeight[1] == 0:
                        print("change box 2height",x,y)
                        boxHeight[1] = y

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
        self.right = int(self.left + self.boxSize*self.boxCount + self.gapSize*(self.boxCount))
        self.bottom = int(self.top + self.boxSize*self.boxCount + self.gapSize*(self.boxCount))

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
'''


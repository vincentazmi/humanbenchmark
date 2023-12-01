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
            if DEBUG: print('''
__init__()
self.top = {}
self.left = {}
self.bottom = {}
self.right = {}
width = {}
height = {}
'''.format(self.top,
           self.left,
           self.bottom,
           self.right,
           self.width,
           self.height))
        # Not preset area
        else: self.getBoxArea(DEBUG)

        self.boxCount = 99999999999
        self.takeScreenshot(DEBUG)
        
        self.getBoxCount(DEBUG,saveImage=True)

        self.getBoxGapSize(DEBUG)

        self.originalRegion = [self.top,
                               self.left,
                               self.right-self.left,
                               self.bottom-self.top]

        self.getPerfectScreenshotRegion(DEBUG)

        input("ready")
        
        if self.waitForFlash(DEBUG):
            if self.getWhiteBoxes(DEBUG):
                self.clickWhiteBoxes(DEBUG)
        else: return

        while self.waitForFlash(DEBUG):
            self.getBoxCount(DEBUG,saveImage=True)
            self.getBoxGapSize(DEBUG)
            if self.getWhiteBoxes(DEBUG):
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



    def resetScreenshotRegion(self,DEBUG=False):
        self.top = self.originalRegion[0]
        self.left = self.originalRegion[1]
        
        
        self.width = self.originalRegion[2]
        self.height = self.originalRegion[3]

        self.right = self.left + self.height
        self.bottom = self.top + self.width

        if DEBUG: print('''
resetScreenshotRegion()
self.top = {}
self.left = {}
self.bottom = {}
self.right = {}
width = {}
height = {}
'''.format(self.top,
           self.left,
           self.bottom,
           self.right,
           self.width,
           self.height))


    def takeScreenshot(self, DEBUG=False):
        if DEBUG: print("takeScreenshot()")
        self.ss = pyautogui.screenshot(region=(self.left,self.top,
                                          self.width, self.height))





    def getBoxCount(self,DEBUG=False,saveImage=False):
        
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
            if self.boxCount < boxCount:
                # bigger area - need to recalculate perfect screenshot region
                if DEBUG: print("Increased size {} -> {}".format(self.boxCount,
                                                                 boxCount))
                self.resetScreenshotRegion(DEBUG)
                self.getPerfectScreenshotRegion(DEBUG)
            self.boxCount = boxCount





    def getBoxGapSize(self,DEBUG=False):

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
        self.takeScreenshot(DEBUG)
        
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
IndexError at
x = {}
y = {}
'''.format(x,y))
            if newX != 0: break
            
        
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

        if DEBUG: print('''
width = {}
height = {}
'''.format(self.width,self.height))

        self.takeScreenshot(DEBUG)
        self.ss.save("perfect_screenshot_region.png")
                
        


            
    def waitForFlash(self, DEBUG=False):
        # After start is clicked this method will wait for the level start 'flash'

##        if DEBUG: pyautogui.moveTo(self.left,self.top-5)

        if DEBUG: print("waitForFlash()")

        rgbPercent = 0 # 765 = 255,255,255 (100%)
        
        flash = False
        # gapColour gets the pixel above the top left box
        for i in range(1000):
            gapColour = pyautogui.pixel(self.left,self.top-5)

            currentPercent = sum(gapColour)
            if currentPercent == rgbPercent:
                # do nothing
                pass
            elif currentPercent > rgbPercent:
                # going up
                rgbPercent = currentPercent
##                if DEBUG: print("rgbPercent =",rgbPercent)
                
            elif currentPercent < rgbPercent:
                # going down
                flash = True
                if DEBUG: print("FLASH")
                rgbPercent = currentPercent
##                if DEBUG: print("rgbPercent =",rgbPercent)

            if flash and currentPercent == rgbPercent:
                # finished flash
                break
            time.sleep(0.05)
            
        if flash:
            time.sleep(1.5)
            if DEBUG: print("WAIT FOR FLASH NOW**************************************")
            self.takeScreenshot(DEBUG)

            if DEBUG: self.ss.save("white_screenshot.png")
            
            self.whiteScreenshot = self.ss
            return True
        else:
            print("waitForFlash not found")
            return False




        
    def getBoxGridStartStep(self,DEBUG):

        self.gridStart = int(self.boxSize/2)

        self.gridStep = int(self.boxSize + self.gapSize)

        

        if DEBUG: print('''
getBoxGridStartStep()
gridStart = {}
gridStep = {}
'''.format(self.gridStart,self.gridStep))


    

    def getWhiteBoxes(self,DEBUG=False):
        
        time.sleep(2)
        
        # Start and step values to get x,y coords of the center of the boxes
        self.getBoxGridStartStep(DEBUG)

        if DEBUG: print("getBoxGridStartStep()")

        whiteList = []
        for x in range(self.gridStart,self.width,self.gridStep):
            for y in range(self.gridStart,self.height,self.gridStep):
                px = self.ss.getpixel((x,y))

                gridX = int((x-self.gridStart)/self.gridStep)
                gridY = int((y-self.gridStart)/self.gridStep)
                
##                if DEBUG: print('''
##x = {}
##y = {}
##RGB = {} {}
##'''.format(gridX,
##           gridY,
##           px,"WHITE" if px == (255,255,255) else ""))
                
                if px == (255,255,255):
                    whiteList.append((gridX,gridY))
                

        if DEBUG: print('''
whiteList= {}
{} Boxes found
'''.format(whiteList,len(whiteList)))
        if len(whiteList) < 1:
            return False
        
        self.whiteList = whiteList
        return True



    
        
    def clickWhiteBoxes(self,DEBUG=False):
##        time.sleep(2)
        self.getBoxGridStartStep(DEBUG)
        
        for (gridX,gridY) in self.whiteList:
            x = int(self.left + (gridX * self.gridStep) + (self.boxSize/2))
            y = int(self.top + (gridY * self.gridStep) + (self.boxSize/2))
            
##            if DEBUG: print("click",x,y)
            pyautogui.click(x,y)

        

'''
Presets
bgColour = (43, 135, 209)
boxColour = (37, 115, 193)
topLeft = (1060, 260)
bottomRight = (1480, 680)
'''

if __name__ == "__main__":
    if False:
        bgColour = (43, 135, 209)
        boxColour = (37, 115, 193)
        topLeft = (1060, 260)
        bottomRight = (1480, 680)
        bot = MemoryBot(bgColour,boxColour,
                        topLeft,bottomRight,
                        DEBUG=True)

    if True:
        bot = MemoryBot(DEBUG=True)
    
                           
    















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


from PIL import Image
import pyautogui, time

class MemoryBot():
    
    def __init__(self,
                 bgColour=None, boxColour=None,
                 topLeft=None,bottomRight=None,DEBUG=False):
        if DEBUG: print("__init__()")
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
            
            self.left = topLeft[0]
            self.top = topLeft[1]
            self.bottom = bottomRight[1]
            self.right = bottomRight[0]

            self.width = self.right - self.left
            self.height = self.bottom - self.top
            if DEBUG: print('''
bgColour = {}
boxColour = {}
left = {}
top = {}
bottom = {}
right = {}
width = {}
height = {}
'''.format(self.bgColour,
           self.boxColour,
           self.left,
           self.top,
           self.bottom,
           self.right,
           self.width,
           self.height))
        # Not preset area
        else: self.getBoxArea(DEBUG)

        self.originalRegion = [self.left,
                               self.top,
                               self.right-self.left,
                               self.bottom-self.top]

        self.boxCount = 99999999999
        self.takeScreenshot(DEBUG,original=True)
        
        self.getBoxCount(DEBUG,saveImage=True)

        self.getBoxGapSize(DEBUG)

        self.getPerfectScreenshotRegion(DEBUG)

        input("ready")
        self.level = 2
        if self.waitForFlash(DEBUG):
            if self.getWhiteBoxes(DEBUG):
                self.clickWhiteBoxes(DEBUG)
                self.level += 1
                if DEBUG: print("LEVEL",self.level)
        else: return

        while self.waitForFlash(DEBUG):
            self.level += 1
            self.takeScreenshot(DEBUG,original=True)
            self.getBoxCount(DEBUG,saveImage=True)
            self.getBoxGapSize(DEBUG)
            if self.getWhiteBoxes(DEBUG):
                self.clickWhiteBoxes(DEBUG)
            else: break

            if DEBUG: print("LEVEL",self.level)
            

        


    def getColours(self,DEBUG=False):
        if DEBUG: print("getColours()")
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
        if DEBUG: print("getBoxArea()")
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
topLeft = ({}, {})
bottomRight = ({}, {})
'''.format(topLeft[0],topLeft[1],
           bottomRight[0],bottomRight[1]))

        self.left = topLeft[0]
        self.top = topLeft[1]
        self.bottom = bottomRight[1]
        self.right = bottomRight[0]

        self.width = self.right - self.left
        self.height = self.bottom - self.top



    def resetScreenshotRegion(self,DEBUG=False):
        # Not using
        if DEBUG: print("resetScreenshotRegion()")
        self.left = self.originalRegion[0]
        self.top = self.originalRegion[1]
        
        self.width = self.originalRegion[2]
        self.height = self.originalRegion[3]

        self.right = self.left + self.height
        self.bottom = self.top + self.width

        if DEBUG: print('''
left = {}
top = {}
bottom = {}
right = {}
width = {}
height = {}
'''.format(self.left,
           self.top,
           self.bottom,
           self.right,
           self.width,
           self.height))


    def takeScreenshot(self, DEBUG=False,original=False):
        DEBUG = False
        if original:
            if DEBUG: print('''
takeScreenshot() {}
left = {}
top = {}
width = {}
height = {}
'''.format("ORIGINAL",
           self.originalRegion[0],
           self.originalRegion[1],
           self.originalRegion[2],
           self.originalRegion[3]))
            
            self.ss = pyautogui.screenshot(region=(self.originalRegion[0],
                                                   self.originalRegion[1],
                                                   self.originalRegion[2],
                                                   self.originalRegion[3]))
            
        else:
            if DEBUG: print('''
takeScreenshot()
left = {}
top = {}
width = {}
height = {}
'''.format(self.left,
           self.top,
           self.width,
           self.height))
            
            self.ss = pyautogui.screenshot(region=(self.left,self.top,
                                                   self.width, self.height))
        
            
            




    def getBoxCount(self,DEBUG=False,saveImage=False):
        if DEBUG: print("getBoxCount()")
        
        boxCount = 0
        # inBox is used to count the boxes
        inBox = False
        
        # For loop goes from left to right, top to bottom
        for x in range(self.originalRegion[2]):
            for y in range(self.originalRegion[3]):
                px = self.ss.getpixel((x,y))

                if not inBox and px == self.boxColour:
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
boxCount = {}
'''.format(boxCount))
        if DEBUG: print("save boxCount_screenshot.png")
        if saveImage: self.ss.save("boxCount_screenshot.png")


        if boxCount > 8:
            if self.boxCount < boxCount:
                # bigger area - need to recalculate perfect screenshot region
                if DEBUG: print("Increased grid size {} -> {}".format(self.boxCount,
                                                                 boxCount))
                self.takeScreenshot(DEBUG,original=True)
                self.getPerfectScreenshotRegion(DEBUG)
            self.boxCount = boxCount





    def getBoxGapSize(self,DEBUG=False):
        if DEBUG: print("getBoxGapSize()")
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
boxSize = {}
gapSize = {}
'''.format(boxSize,gapSize))

        if boxSize != 0 and gapSize != 0:
            self.boxSize = boxSize
            self.gapSize = gapSize





    def getPerfectScreenshotRegion(self,DEBUG=False):
        if DEBUG: print("getPerfectScreenshotRegion()")
        self.takeScreenshot(DEBUG,original=True)
        
        startX,endX,startY,endY = 0,0,0,0
        # This loop gets first X coord there is a box coloured pixel
        for x in range(self.originalRegion[2]):
            for y in range(self.originalRegion[3]):
                
                try:
                    px = self.ss.getpixel((x,y))

                    if px == self.boxColour:
                        if startX == 0: startX = x
                        else: endX = x
                        
                except IndexError:
                    print('''
IndexError at
x = {}
y = {}
'''.format(x,y))
                    
        # This loop gets first Y coord there is a box coloured pixel
        for y in range(self.originalRegion[3]):
            for x in range(self.originalRegion[2]):
                try:
                    px = self.ss.getpixel((x,y))

                    if px == self.boxColour:
                        if startY == 0: startY = y
                        else: endY = y
                except IndexError:
                    print('''
IndexError at
y = {}
x = {}
'''.format(y,x))
                    
        if DEBUG:
            print('''
startX: {}
endX: {}
startY: {}
endY: {}
'''.format(startX,endX,startY,endY))
            self.ss.putpixel((startX, startY), (0, 255, 0))
            self.ss.putpixel((endX, endY), (255, 0, 0))
            print("save perfect_screenshot_region.png")
            self.ss.save("perfect_screenshot_region.png")

        
        
        self.left = self.originalRegion[0] + startX
        self.top = self.originalRegion[1] + startY
        self.width = endX - startX
        self.height = endY - startY

        self.right = self.left + self.width
        self.bottom = self.top + self.height

        self.gridStartX = startX
        self.gridStartY = startY

        self.gridEndX = endX
        self.gridEndY = endY
        

        self.takeScreenshot(DEBUG)
        if DEBUG: print("save perfect_screenshot_region_crop.png")
        self.ss.save("perfect_screenshot_region_crop.png")
                
        


            
    def waitForFlash(self, DEBUG=False):
        if DEBUG: print("waitForFlash()")
        # After start is clicked this method will wait for the level start 'flash'
        

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
##            if DEBUG: print("sleep 0.05")
            time.sleep(0.05)
            
        if flash:
            if DEBUG: print("sleep 1.5")
            time.sleep(1.5)
            self.takeScreenshot(DEBUG,original=True)

            if DEBUG:
                print("save white_screenshot.png")
                self.ss.save("white_screenshot.png")
                self.whiteScreenshot = self.ss
                
            if DEBUG: print("sleep 1.5")
            time.sleep(1.5)
            return True
        else:
            print("waitForFlash not found")
            return False
        


    

    def getWhiteBoxes(self,DEBUG=False):
        if DEBUG: print("getWhiteBoxes()")

        self.ss = self.whiteScreenshot
        
        
        # Start and step values to get x,y coords of the center of the boxes

##        startX = int(self.left + (self.boxSize/2))
##        endX = int(self.right)
##
##        startY = int(self.top + (self.boxSize/2))
##        endY = int(self.bottom)
        
        self.gridStep = int(self.boxSize + self.gapSize)

        whiteList = []
        for x in range(int(self.gridStartX+self.boxSize/2),self.gridEndX,self.gridStep):
            for y in range(int(self.gridStartY+self.boxSize/2),self.gridEndY,self.gridStep):
##                if DEBUG: print("Pixel",x,y)
                px = self.ss.getpixel((x,y))
                

                gridX = int((x-self.gridStartX)/self.gridStep)
                gridY = int((y-self.gridStartY)/self.gridStep)
                if px == self.bgColour and DEBUG:
                    print('''
gridX = {}
gridY = {}
RGB = {} Background Colour
'''.format(gridX,
             gridY,
             px))
                          
                
##                if DEBUG: print('''
##gridX = {}
##gridY = {}
##RGB = {} {}
##'''.format(gridX,
##           gridY,
##           px,"WHITE" if px == (255,255,255) else
##           "Background Colour***********************" if px == self.bgColour else
##           "Box Colour" if px == self.boxColour else ""))
                
                if px == (255,255,255):
                    whiteList.append((gridX,gridY))
                    if DEBUG: self.ss.putpixel((x, y), (0, 255, 0))
                else:
                    if DEBUG: self.ss.putpixel((x, y), (255, 0, 0))
                

        if DEBUG:

            grid = []
            for z in range(int(self.boxCount**0.5)):
                grid.append('__')
            grid.append('\n')
            for i in range(int(self.boxCount**0.5)):
                
                for j in range(int(self.boxCount**0.5)):
                    if (j,i) in whiteList:
                        grid.append('|*')
                    else:
                        grid.append('| ')
                grid.append('|\n')
                
            for z in range(int(self.boxCount**0.5)):
                grid.append('‾‾')
                

            prettyGrid = ''.join(grid)
            
            print('''
prettyGrid:
{}
{} Boxes found
'''.format(prettyGrid,len(whiteList)))
            if DEBUG: print("save getWhiteBoxes.png")
            self.ss.save("getWhiteBoxes.png")
        if len(whiteList) < 1:
            return False
        
        self.whiteList = whiteList
        return True



    
        
    def clickWhiteBoxes(self,DEBUG=False):
        
        if DEBUG: print("clickWhiteBoxes()")
        
        for (gridX,gridY) in self.whiteList:
            x = int(self.left + (gridX * self.gridStep) + (self.boxSize/2))
            y = int(self.top + (gridY * self.gridStep) + (self.boxSize/2))
            
##            if DEBUG: print("click",x,y)
            pyautogui.click(x,y)

        

'''
Presets
bgColour = (43, 135, 209)
boxColour = (37, 115, 193)
topLeft = (1050, 254)
bottomRight = (1814, 706)
'''

if __name__ == "__main__":
    if False:
        bgColour = (43, 135, 209)
        boxColour = (37, 115, 193)
        topLeft = (1050, 254)
        bottomRight = (1814, 706)
        bot = MemoryBot(bgColour,boxColour,
                        topLeft,bottomRight,
                        DEBUG=True)

    else:
        bot = MemoryBot(DEBUG=True)
    
                           

from PIL import Image
import pyautogui, time, pytesseract

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

class VerbalBot():

    
    def __init__(self,
                 preset=None,
                 DEBUG=False):

        if preset == None:
            self.getPresets(DEBUG)

        else:
            self.seenX, self.seenY = preset[0]
            self.newX, self.newY = preset[1]
            self.topLeft = preset[2]
            self.bottomRight = preset[3]

            self.width = self.bottomRight[0]-self.topLeft[0]
            self.height = self.bottomRight[1]-self.topLeft[1]

        try:
            desiredScore = int(input('''
WARNING: this program never loses
This is an issue for you as you will lose control of your computer

70 (20 Seconds)
100 (28 Seconds)
210 (1 Minute)
1050 (5 Minutes)
2100 (10 Minutes)
9999 (47:39 Minutes)
Please enter the desired score:
'''))
        except:
            print("Undesired input received")
            return

        currentScore = 0
        self.wordsList = []
        startTime = time.time()
        while currentScore < desiredScore:
            self.readWord(DEBUG)
            self.clickButton(DEBUG)
            currentScore += 1
        endTime = time.time()
        totalTime = endTime-startTime
        averageTime = totalTime / currentScore
        print('''
start = {}
end = {}
total = {}
average = {}
'''.format(startTime,endTime,
           totalTime, averageTime))
        print("Score:",currentScore)





    def getPresets(self,DEBUG):
        if DEBUG: print("getPresets()")
        ss = pyautogui.screenshot()
        
        input('''
Position the cursor:
1. In the center of the "SEEN" button

And press enter in this window.
''')
        self.seenX, self.seenY = pyautogui.position()

        input('''
Position the cursor:
1. In the center of the "NEW" button

And press enter in this window.
''')
        self.newX, self.newY = pyautogui.position()

        input('''
Position the cursor:
1. In the center of the middle word

And press enter in this window.
''')
        middleX, middleY = pyautogui.position()

        self.topLeft = (int(middleX-((middleX-self.seenX)*4)),
                        int(middleY-((self.seenY-middleY)/2)))

        self.bottomRight = (int(middleX+((middleX-self.seenX)*4)),
                            int(middleY+((self.seenY-middleY)/2)))

        

        if DEBUG:
            print('''
seenXY = ({},{})
newXY = ({},{})
topLeft = {}
bottomRight = {}
'''.format(self.seenX, self.seenY,
           self.newX, self.newY,
           self.topLeft,
           self.bottomRight))
                  
            ss.putpixel(self.topLeft,(255,0,0))
            ss.putpixel(self.bottomRight,(255,0,0))
            ss.save("screenshot_region.png")

            self.width = self.bottomRight[0]-self.topLeft[0]
            self.height = self.bottomRight[1]-self.topLeft[1]

            ss = pyautogui.screenshot(region=(self.topLeft[0],
                                              self.topLeft[1],
                                              self.width,
                                              self.height))
            
            ss.save("cropped_screenshot_region.png")
            





    def readWord(self,DEBUG=False):
        ss = pyautogui.screenshot(region=(self.topLeft[0],
                                          self.topLeft[1],
                                          self.width,
                                          self.height))

        self.currentWord = pytesseract.image_to_string(ss)
##        print("word=",self.currentWord)


    def clickButton(self,DEBUG=False):
        
        if self.currentWord in self.wordsList:
            if DEBUG: print("Seen",self.currentWord)
            self.seenStreak += 1
            
            pyautogui.click(self.seenX, self.seenY)
            

        else:
            if DEBUG: print("New",self.currentWord)
            self.seenStreak = 0
            
            self.wordsList.append(self.currentWord)
            pyautogui.click(self.newX, self.newY)
        
        


    

'''
PRESETS
seenXY = (1203,511)
newXY = (1339,510)
topLeft = (1071, 379)
bottomRight = (1467, 467)
'''
    
if __name__ == "__main__":
    seenXY = (1203,511)
    newXY = (1339,510)
    topLeft = (1071, 379)
    bottomRight = (1467, 467)
    presets = [seenXY,
               newXY,
               topLeft,
               bottomRight]
    
    if True: # with presets
        
        bot = VerbalBot(presets,DEBUG=False)

    else: # without presets
        bot = VerbalBot(DEBUG=False)
    
                           

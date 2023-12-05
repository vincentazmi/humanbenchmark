from PIL import Image
import pyautogui, time

class RectionBot():

    
    def __init__(self,
                 clickPoint=None,
                 redBG=None,
                 DEBUG=False):
        if DEBUG: print("__init__({}{})".format("" if clickPoint == None else
                                              "clickPoint="+str(clickPoint),
                                                 "" if redBG == None else
                                                 ",redBG="+str(redBG)))
        if clickPoint == None:
            self.getClickPoint()

        else:
            self.x = clickPoint[0]
            self.y = clickPoint[1]
            self.blueBG = pyautogui.pixel(self.x,self.y)

        
            
        if DEBUG: print('''
x = {}
y = {}
blueBG = {}
'''.format(self.x,self.y,self.blueBG))

        
        if redBG != None:
            self.redBG = redBG
            
            runFive = input("Run five times? (y/n)")
            if runFive.lower() == "y":
                for i in range(5):
                    self.start(firstRun=False,DEBUG=DEBUG)
            else:
                self.start(firstRun=False,DEBUG=DEBUG)
                
        else:
            self.start(firstRun=True,DEBUG=DEBUG)
            




    def getClickPoint(self,DEBUG=False):
        if DEBUG: print("getClickPoint()")
        input('''
Position the cursor:
1. Over the blue area

Then press enter in this window.
''')
        self.x,self.y = pyautogui.position()
        
        self.blueBG = pyautogui.pixel(self.x,self.y)

        


        

    def start(self,firstRun=False,DEBUG=False):
        if DEBUG: print("getClickPoint()")
        safety = 10000
        redStart = time.time()
        pyautogui.click(self.x,self.y)
        if firstRun:
            # If after starting self.x,self.y points to white text, move down
            while pyautogui.pixel(self.x,self.y) == (255,255,255):
                self.y += 1

            self.redBG = pyautogui.pixel(self.x,self.y)
        
        while safety and pyautogui.pixel(self.x,self.y) == self.redBG:
            safety -= 1
        
        redEnd = time.time()
        pyautogui.click(self.x,self.y)

        if DEBUG: print('''
safety = {}
Wait time = {}
redBG = {}
'''.format(self.x,self.y,self.redBG))

        if firstRun:
            print('''
Presets to run at full speed:
x = {}
y = {}
redBG = {}
'''.format(self.x,
           self.y,
           self.redBG))
        



'''
PRESETS
x = 1495
y = 347
redBG = (206, 38, 54)
'''
    
if __name__ == "__main__":
    x = 1495
    y = 347
    redBG = (206, 38, 54)
    
    if False:
        
        bot = RectionBot([x,y],redBG,DEBUG=True)

    else:
        # full speed
        bot = RectionBot([x,y],redBG,DEBUG=False)
    
                           

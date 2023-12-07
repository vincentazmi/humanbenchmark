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
                    self.fastRun()
            else:
                self.fastRun()
                
        else:
            self.firstRun(DEBUG=DEBUG)
            




    def getClickPoint(self,DEBUG=False):
        if DEBUG: print("getClickPoint()")
        input('''
Position the cursor:
1. Over the blue area

Then press enter in this window.
''')
        self.x,self.y = pyautogui.position()
        
        self.blueBG = pyautogui.pixel(self.x,self.y)

        


        

    def fastRun(self):
        redStart = time.time()
        pyautogui.click(self.x,self.y)
        
        while pyautogui.pixel(self.x,self.y) == self.redBG: pass
    
        pyautogui.click(self.x,self.y)
        redEnd = time.time()


    def firstRun(self,DEBUG=False):
        if DEBUG: print("firstRun()")
        pyautogui.click(self.x,self.y)
        # If after starting self.x,self.y points to white text, move down
        while pyautogui.pixel(self.x,self.y) == (255,255,255):
            self.y += 1

        self.redBG = pyautogui.pixel(self.x,self.y)
        
        print('''
Presets to run at full speed:
x = {}
y = {}
redBG = {}
Copy the line below
{}#{}#{}
'''.format(self.x,
           self.y,
           self.redBG,
           self.x,
           self.y,
           self.redBG))
        


'''
1101#327#206, 38, 54
'''

    
if __name__ == "__main__":
    DEBUG = False
    
    if input("Do you have presets?(y/n)").lower() == 'y':
##        redBG = (0,0,0)
        x,y,redNew = input("Paste here:\n").split('#')

        redBG = eval(redNew)
        
        # full speed
        bot = RectionBot([int(x),int(y)],redBG,DEBUG=DEBUG)
    else:
        bot = RectionBot(DEBUG=DEBUG)
        
        
    
                           

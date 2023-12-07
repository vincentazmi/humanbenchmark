from PIL import Image
import pyautogui, time, pytesseract

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

class NumberMemory():

    
    def __init__(self,
                 DEBUG=False):
        self.DEBUG = DEBUG
        if self.DEBUG: print("__init__()")

        self.getPresets()

        self.start()



    def getPresets(self):
        if self.DEBUG: print("getPresets()")

        input('''
Position the cursor:
1. Over the "Start" button

And press enter in this window.
''')
        # Start button is in the same position as the next button later
        self.nextX, self.nextY = pyautogui.position()

        pyautogui.click(self.nextX,self.nextY)

        self.blueBG = pyautogui.pixel(self.nextX,self.nextY)

        for y in range(self.nextY,0,-1):
            # Go up from start button until background is not blue
            if pyautogui.pixel(self.nextX,y) != self.blueBG:
                # Keep going past the "load" bar until it is blue again
                for z in range(y,0,-1):
                    if pyautogui.pixel(self.nextX,z) == self.blueBG:
                        bottomY = z
                        break
                break
            
        arbitraryDistance = self.nextY - bottomY
        
        self.left = self.nextX - arbitraryDistance*3
        self.right = self.nextX + arbitraryDistance*3

        self.top = int(bottomY - arbitraryDistance*1.25)
        self.bottom = bottomY

        self.width = self.right - self.left
        self.height = self.bottom - self.top

        if self.DEBUG:
            print('''
left = {}
top = {}
width = {}
height = {}
'''.format(self.left,
           self.top,
           self.width,
           self.height))

        self.takeScreenshot()
        self.getNumber()
        count = 10000
        try:
            while count and pyautogui.locateOnScreen('screenshot_number.png', region=(self.left,
                                                                                      self.top,
                                                                                      self.width,
                                                                                      self.height)):
                count -= 1
            if count == 0: print("count dead")
            
        except:
            pyautogui.write(str(self.currentNumber))
        
        input('''
Position the cursor:
1. Over the "Submit" button

And press enter in this window.
'''.format(self.currentNumber))
        
        self.submitX, self.submitY = pyautogui.position()

        pyautogui.click(self.submitX,self.submitY)

    def takeScreenshot(self):
        self.ss = pyautogui.screenshot(region=(self.left,
                                              self.top,
                                              self.width,
                                              self.height))
        if self.DEBUG: self.ss.save("screenshot_number.png")

    def getNumber(self):
        if self.DEBUG: print("getNumber()")
        self.currentNumber = pytesseract.image_to_string(self.ss, config='--psm 13 --oem 3 -c tessedit_char_whitelist=0123456789')
        try:
            self.currentNumber = int(self.currentNumber.strip())
        except ValueError as e:
            print("cannot get number",self.currentNumber)
            raise e
        
        if self.DEBUG: print("Found",self.currentNumber)
        

    def start(self):
        if DEBUG: print("start()")

        input("Ready when you are (press enter)")


        for i in range(10):
            pyautogui.click(self.nextX,self.nextY)

            time.sleep(0.1)
            self.takeScreenshot()
            self.getNumber()

            count = 10000
            try:
                while count and pyautogui.locateOnScreen('screenshot_number.png', region=(self.left,
                                                                                          self.top,
                                                                                          self.width,
                                                                                          self.height)):
                    count -= 1
                if count == 0: print("count dead")
                
            except:
                pyautogui.write(str(self.currentNumber))
                pyautogui.click(self.submitX,self.submitY)
                time.sleep(0.6)
        




        
    
if __name__ == "__main__":
    DEBUG = True
    
    if False: # with presets
        
        bot = NumberMemory(presets,DEBUG=DEBUG)

    else: # without presets
        bot = NumberMemory(DEBUG=DEBUG)
    
                           

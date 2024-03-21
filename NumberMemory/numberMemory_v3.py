from PIL import Image
import numpy as np
import pyautogui, time, pytesseract, cv2

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

class NumberMemory():

    
    def __init__(self,
                 DEBUG=False):
        self.DEBUG = DEBUG
        if self.DEBUG: print("__init__()")

        # getPresets() aquires:
        # blue colour RGB tuple,
        # screenshot size x,y,width,height tuple
        # x,y locations of submit and next button
        self.getPresets()

##        self.start()



    def getPresets(self):
        if self.DEBUG: print("getPresets()")

        input('''
Position the cursor:
1. Over the "Start" button

Then press enter in this window.
''')
        # Start button is in the same position as the next button later
        self.nextButtonX, self.nextButtonY = pyautogui.position()

        pyautogui.click(self.nextButtonX,self.nextButtonY)
        
        self.blueBG = pyautogui.pixel(self.nextButtonX, self.nextButtonY)
        
        # getScreenshotDefault() sets x,y,width and height of screenshot
        self.getScreenshotSize()

        ##################



    def getScreenshotSize(self):
        full_screenshot = pyautogui.screenshot() # full screen screenshot
        
        if self.DEBUG: full_screenshot.save(r'./full_screenshot.png')

        for x in range(full_screenshot.width):
            for y in range(full_screenshot.height):
                colour = full_screenshot.getpixel((x,y))

                if colour != self.blueBG:
                    full_screenshot.putpixel((x,y),(255,255,255))
                    
        if self.DEBUG: full_screenshot.save(r'./blueFilterImage.png')

        # find blue box and calculate screenshot size
        
        

        


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
    
    
                           

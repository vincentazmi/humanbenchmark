from bs4 import BeautifulSoup
import pyautogui, time, win32clipboard

class TypingBot():

    
    def __init__(self,DEBUG=False):
        if DEBUG: print("__init__()")


        self.getClickXY(DEBUG)

        self.typeCopiedElement(DEBUG)
        

        

    def getClickXY(self,DEBUG=False):
        if DEBUG: print("getClickXY()")

        input('''
Right click in this position:
1. Inside the grey box
2. NOT over any text

Then click inspect and hopfully the following will be highlighted:
<div class="letters notranslate" tabindex="1"> etc...

Right click this and select Copy > Copy element

Then move cursor back to the grey box
Then press enter in this window
''')
        self.left, self.top = pyautogui.position()
        

    def typeCopiedElement(self,DEBUG=False):
        pyautogui.click((self.left,self.top))
        win32clipboard.OpenClipboard()
        data = win32clipboard.GetClipboardData()
        win32clipboard.CloseClipboard()

        soup = BeautifulSoup(data)
        
        if DEBUG: print(soup.text)
        if DEBUG: print(len(soup.text))
        pyautogui.write(soup.text)


    
if __name__ == "__main__":
    
    bot = TypingBot(DEBUG=True)
    
                           

from pynput import keyboard
import pyautogui
import collections
import threading

SCREENSHOT_X, SCREENSHOT_Y = [600, 200]

active = False
inputQueue = collections.deque()
screenshot = None

def updateScreen():
    global screenshot, SCREENSHOT_X, SCREENSHOT_Y
    screenshot = pyautogui.screenshot(region=(SCREENSHOT_X, SCREENSHOT_Y, 1100, 700))

updateScreen()

def onPress(key):
    global active, inputQueue
    try:
        if(active):
            inputQueue.append(key.char)
        else:
            if(key == keyboard.Key.ctrl):
                active = not active
                updateScreen()
                print("ACTIVATE")
    except AttributeError:
        if(key == keyboard.Key.ctrl):
            active = not active
            print("DEACTIVATE")

listener = keyboard.Listener(
    on_press=onPress)
listener.start()

while True:
    if(inputQueue):
        try:
            character = inputQueue.popleft()
            location = pyautogui.locate(f"images/{character}.png", screenshot)
            pyautogui.moveTo(x=location[0]+SCREENSHOT_X, y=location[1]+SCREENSHOT_Y)
            squareLocation = pyautogui.locate("images/emptySquare.png", screenshot)
            pyautogui.dragTo(x=squareLocation[0]+SCREENSHOT_X, y=squareLocation[1]+SCREENSHOT_Y)
        except pyautogui.ImageNotFoundException:
            pass
        updateScreen()
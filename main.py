from pynput import keyboard
import pyautogui
import collections
import threading
import time
import notify2

SCREENSHOT_X, SCREENSHOT_Y = [600, 200]

active = False
inputQueue = collections.deque()
screenshot = None
lastUpdateAt = time.time()
notifier = notify2.init("Alphie Script")

def updateScreen():
    global screenshot, SCREENSHOT_X, SCREENSHOT_Y, lastUpdateAt
    screenshot = pyautogui.screenshot(region=(SCREENSHOT_X, SCREENSHOT_Y, 1100, 800))
    lastUpdateAt = time.time()

updateScreen()

def notify(active):
    global notifier
    if(active):
        n = notify2.Notification("ENABLED")
        n.set_timeout(750)
        n.show()
    else:
        n = notify2.Notification("DISABLED")
        n.set_timeout(750)
        n.show()

def onPress(key):
    global active, inputQueue
    try:
        if(active):
            inputQueue.append(key.char)
        else:
            if(key == keyboard.Key.ctrl):
                active = not active
                updateScreen()
                notify(True)
    except AttributeError:
        if(key == keyboard.Key.ctrl):
            active = not active
            notify(False)

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
        except FileNotFoundError:
            print(f"[WARNING] images/{character}.png not found")
        updateScreen()
    if(time.time()-lastUpdateAt > 0.3 and active):
        updateScreen()
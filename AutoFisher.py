import math
from random import randint, uniform, choice
import sys
import time
import numpy as np
import pyautogui as pag
from itertools import chain
import os

def checkFishingLevel(path):
    """TODO: Mimic behavior of checking progress of fishing level"""
    return

def openInventory(path):
    """TODO: Should open the inventory if not already opened, i.e. after checking xp/level progress"""
    return

def createDropList(path):
    """Using path, will return an array of all items that a player wishes to drop from their inventory"""
    images = []
    for image in os.listdir(path):
        images.append(os.path.join(path, image))
    print(images)
    return images

def dropItem(item):
    """Drop's specified item. This will take a Box(Top, Left, Width, Height) generator"""
    r = randint(28, 32)
    t = uniform(4.8, 7)
    clicktime = t/r
    
    pag.keyDown('shift')
    random_wait(clicktime - .04, clicktime + .04)
    center = pag.center(item)
    random_coordinate(center, item)
    pag.click()
    pag.keyUp('shift')
    return

def clickSpecial(item):
    """Will use special if image is provided"""
    if not item:
        print('inif')
        return False
    r = randint(28, 32)
    t = uniform(4.8, 7)
    clicktime = t/r
    random_wait(clicktime - .04, clicktime + .04)
    myChoice = choice(item)
    center = pag.center(myChoice)
    random_coordinate(center, myChoice)
    pag.click()
    return True

def startFishing(item):
    """Starts fishing given an image of the fishing location"""
    if item is None:
        print('inif')
        return False
    r = randint(28, 32)
    t = uniform(4.8, 7)
    clicktime = t/r
    random_wait(clicktime - .04, clicktime + .04)
    center = pag.center(item)
    random_coordinate(center, item)
    pag.click()
    time.sleep(5)
    return True

def travel_time(x2, y2):
        """Calculates cursor travel time in seconds per 240-270 pixels, based on a variable rate of movement"""
        rate = uniform(0.09, 0.15)
        x1, y1 = pag.position()
        distance = math.sqrt(math.pow(x2-x1, 2)+math.pow(y2-y1, 2))
        return max(uniform(.08, .12), rate * (distance/randint(250, 270)))

def random_coordinate(center, item):
        """Moves cursor to random locaction still above the object to be clicked"""
        x = randint(center[0], center[0]+int(item[2]/4))
        y = randint(center[1], center[1]+int(item[3]/4))
        time = travel_time(x, y)
        print('X:%s,Y:%s' % (x,y))
        return pag.moveTo(x, y, time)

def random_wait(min=0.25, max=0.50):
        """Waits a random number of seconds between two numbers (0.25 and 0.50 default) to mimic human reaction time"""
        return time.sleep(uniform(min, max))

# 2333, 1097 : 2512, 1352
if __name__ == '__main__':
    conf = 0.75
    drops = createDropList('DropItems')
    try:
        while True:
            
            if (pag.locateOnScreen('images\\isFishing.png', confidence=0.95)):
                pass
            else:
                print('NOT FISHING')
                if (pag.locateOnScreen('images\\specialReady.png', confidence=0.95)):
                    special = pag.locateOnScreen('images\\specialReady.png', confidence=0.95)
                    clickSpecial(special)
                #we stopped fishing, drop inventory and restart fishing
                
                inventory = []
                for image in drops:
                    matches = pag.locateAllOnScreen(image, confidence=0.95, grayscale=True)
                    for match in matches:
                        inventory.append(match)
                
                # should sort on closest to current cursor, this can be much better 
                # since image size is factored here
                #toDropSorted = sorted(toDrop, key=lambda a: (pag.center(a).x,pag.center(a).y))
                inventorySorted = sorted(inventory, key=lambda a: (a.top, a.left))
                print(inventorySorted)
                random_wait()
                for drop in inventorySorted:
                    dropItem(drop)
                try:
                    print(conf)
                    fishing = pag.locateAllOnScreen('images\\startFishing.png', confidence=conf, grayscale=True)

                    if (startFishing(list(fishing))):
                        conf = 0.75
                    else:
                        conf = conf - .1
                    if conf < .4:
                        conf = 0.75
                except TypeError:
                    conf = conf -.1
                    pass
    except KeyboardInterrupt:
        sys.exit()
    

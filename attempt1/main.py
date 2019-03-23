import numpy as np
import pyautogui
import cv2 as cv
import pathlib
import time
import math
import sys
time.sleep(2)
def round_to_20(number):
    return math.floor(number/15)*15

def clusterize(points, type):
    if type != "pawn":
        if not points:
            return False, False
        startpt = points[0]
        cluster1 = [startpt]
        cluster2 = []
        if len(points) == 1:
            return points[0], False
        elif len(points) == 0:
            return False, False
        for i in range(1, len(points)):
            currpt = points[i]
            if (startpt[0] - currpt[0])** 2 + (startpt[1] - currpt[1]) ** 2 > 900:
                cluster2.append(currpt)
            else:
                cluster1.append(currpt)
        avg1 = False
        avg2 = False
        if len(cluster1) > 0:
            avg1 = ( int(sum([ k[0] for k in cluster1 ])/len(cluster1)), int(sum([ k[1] for k in cluster1 ])/len(cluster1)) )
        if len(cluster2) > 0:
            avg2 = (int(sum([k[0] for k in cluster2]) / len(cluster1)), int(sum([k[1] for k in cluster2]) / len(cluster1)))
        if avg1 and avg2:
            return avg1, avg2
        elif avg1:
            print("wot")
            print(len(cluster1))
            return avg1, False
        else:
            print("wot")
            print(len(cluster2))
            return False, avg2
    else:
        if len(points) == 0:
            return [False] * 8
        #do the clustering stuff
        center, w, h = currentboard
        bottoml = (center[0] - w//2, center[1] - h//2)
        topr = (center[0] + w//2, center[1] + h//2)
        poses = set()
        for pos in points:
            poses.add(get_rel_pos(pos))
        poses_list = list(poses)
        poses_list += (8 - len(poses_list)) * [False]
        return poses_list


def get_rel_pos(pos):
    center, w, h = currentboard
    bottoml = (center[0] - w//2, center[1] - h//2) #this is absolute position
    rel_pos = (pos[0]-bottoml[0], pos[1] - bottoml[1])
    topr = (w, h) # this is relative position
    # this is on an 8 by 8 grid
    unit = w/8
    x = math.floor(rel_pos[0] / unit)
    y = math.floor(rel_pos[1] / unit)
    return int(x * unit + unit/2 + bottoml[0]), int(y * unit + unit/2 + bottoml[1])


def get_matches(screenshot, color, piece):
    start = time.time()
    positions = set()
    #dark background
    img_gray = cv.cvtColor(screenshot, cv.COLOR_BGR2GRAY)
    template = cv.imread(str(  pathlib.Path(__file__).parent / 'chess pieces' / str(color+'_pieces') /
                               str(color+"_"+piece+"_1.png")  ), 0)
    w, h = template.shape[::-1]
    res = cv.matchTemplate(img_gray, template, cv.TM_CCOEFF_NORMED)
    threshold = 0.6
    loc = np.where(res >= threshold)

    for pt in zip(*loc[::-1]):
        x, y = round_to_20(pt[0] + w / 2), round_to_20(pt[1] + h / 2)
        positions.add((x,y))
    # light background
    template = cv.imread(str(  pathlib.Path(__file__).parent / 'chess pieces' / str(color+'_pieces') /
                               str(color+"_"+piece+"_2.png")  ), 0)
    w, h = template.shape[::-1]
    res = cv.matchTemplate(img_gray, template, cv.TM_CCOEFF_NORMED)
    loc = np.where(res >= threshold)
    for pt in zip(*loc[::-1]):
        x, y = round_to_20(pt[0] + w / 2), round_to_20(pt[1] + h / 2)
        positions.add((x,y))
        #cv.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0, 255, 0), 1)
    for pt in positions:
        # print(pt)

        cv.rectangle(img_rgb, (pt[0] - 10, pt[1] - 10), (pt[0] + 10, pt[1] + 10), (0, 255, 0), 1)

    clusters = clusterize(list(positions), piece)
    for pos in clusters:
        # print(pt)
        if pos:

            cv.rectangle(img_rgb, (pos[0] - 10, pos[1] - 10), (pos[0] + 10, pos[1] + 10), (255, 0, 0), 1)

    return clusters

def get_board(screenshot):
    start = time.time()
    positions = set()
    #dark background
    img_gray = cv.cvtColor(screenshot, cv.COLOR_BGR2GRAY)
    template = cv.imread(str(  pathlib.Path(__file__).parent / 'chess pieces' / 'board.png' ), 0)
    w, h = template.shape[::-1]
    res = cv.matchTemplate(img_gray, template, cv.TM_CCOEFF_NORMED)
    threshold = 0.5
    loc = np.where(res >= threshold)

    for pt in zip(*loc[::-1]):
        x, y = round_to_20(pt[0] + w / 2), round_to_20(pt[1] + h / 2)
        positions.add((x,y))
    #for pt in positions:
        # print(pt)

        #cv.rectangle(img_rgb, (pt[0] - 10, pt[1] - 10), (pt[0] + 10, pt[1] + 10), (255, 0, 0), 1)
    if len(positions):
        avgpos = (int(sum([k[0] for k in positions]) / len(positions)) , int(sum(k[1] for k in positions) / len(positions)))
        p1, p2 = (avgpos[0] - w//2, avgpos[1] - w//2), (avgpos[0] + w//2, avgpos[1] + w//2)
        cv.rectangle(img_rgb, p1, p2, (255, 0, 255), 1)
        return img_rgb[p1[1]:p2[1], p1[0]:p2[0]],avgpos, w, h
    else:
        return False, False, False, False

image = pyautogui.screenshot()
image = cv.cvtColor(np.array(image), cv.COLOR_RGB2BGR)
start = time.time()
cv.imwrite("in_memory_to_disk.png", image)
# this time take a screenshot directly to disk
pyautogui.screenshot("straight_to_disk.png")
# we can then load our screenshot from disk in OpenCV format
img_rgb = cv.imread("straight_to_disk.png")
imz, a, b, c = get_board(img_rgb)
currentboard = (a,b,c)
img_rgb = imz
rooks = (get_matches(img_rgb, "white", "rook"), get_matches(img_rgb, "black", "rook"))
knights = (get_matches(img_rgb, "white", "knight"), get_matches(img_rgb, "black", "knight"))
pawns = (get_matches(img_rgb, "white", "pawn"), get_matches(img_rgb, "black", "pawn"))
bishops = (get_matches(img_rgb, "white", "bishop"), get_matches(img_rgb, "black", "bishop"))
kings = (get_matches(img_rgb, "white", "king"), get_matches(img_rgb, "black", "king"))
queens = (get_matches(img_rgb, "white", "queen"), get_matches(img_rgb, "black", "queen"))

print(time.time()-start)
print(list(len(x) for x in [rooks, knights, pawns, bishops, kings, queens]))
print(get_board(img_rgb))
cv.imwrite('res.png',img_rgb)

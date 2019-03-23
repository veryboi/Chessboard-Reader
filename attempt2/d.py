import numpy as np
import pyautogui
import cv2 as cv
import pathlib
import time
import itertools
time.sleep(2)
white = [210,238,238] # BGR
black = "[86 150 118]" # BGR
start = time.time()
img = pyautogui.screenshot()
img = cv.cvtColor(np.array(img), cv.COLOR_RGB2BGR)
gray = cv.cvtColor(img,cv.COLOR_BGR2GRAY)
ret,gray = cv.threshold(gray,100,255,0)
gray2 = gray.copy()

contours, hier = cv.findContours(gray,cv.RETR_LIST,cv.CHAIN_APPROX_SIMPLE)
gray2 = cv.cvtColor(gray2, cv.COLOR_GRAY2BGR)
gray = cv.cvtColor(gray, cv.COLOR_GRAY2BGR)
c = max(contours, key=cv.contourArea)

(x,y,w,h) = cv.boundingRect(c)
unit = abs(w)/8
#cv.rectangle(img,(x,y),(x+w,y+h),(0,255,0),3)

bottoml = (x,y)
topr = (x+w, y+h)
images = []

for x_i in range(8):
    for y_i in range(8):

        my_image = gray2[  int(bottoml[1] + y_i * unit) : int(bottoml[1] + unit * (y_i+ 1)+2), int(bottoml[0] + x_i * unit) : int(bottoml[0] + unit * (x_i + 1)+2)  ]
        my_image = cv.cvtColor(my_image, cv.COLOR_BGR2GRAY)
        cv.imwrite( str(pathlib.Path(__file__).parent / 'test_images' / ('piece_' + str(x_i*8 + y_i) +'.png') ), my_image)
        images.append((  my_image, (x_i, y_i), (len(my_image) , len(my_image[0]))  ))

        #image, (x,y), coordinate,
names = list("pnbrqk")
board = [[1] * 8 for i in range(8) ]

for my_im in images:
    threshold = 0.8

    right_piece = "1"
    done = False
    for piece in names:
        template = cv.imread( (str(  pathlib.Path(__file__).parent / 'pieces' / 'black' /str(piece + ".png") )), 0)
        res = cv.matchTemplate(my_im[0], template, cv.TM_CCOEFF_NORMED)
        loc = np.where(res >= threshold)
        if len(list(zip(*loc[::-1]))) > 0:
            right_piece = piece
            board[my_im[1][1]][my_im[1][0]] = right_piece
            done = True
            break
    if not done:
        for piece in names:
            template = cv.imread((str(pathlib.Path(__file__).parent / 'pieces' / 'white' / str(piece + ".png"))), 0)
            res = cv.matchTemplate(my_im[0], template, cv.TM_CCOEFF_NORMED)
            loc = np.where(res >= threshold)
            if len(list(zip(*loc[::-1]))) > 0:
                # print(list(loc))
                right_piece = piece.upper()
                # print(my_im[1][0], my_im[1][1])
                board[my_im[1][1]][my_im[1][0]] = right_piece #fixed
                done = True
                break
    if not done:
        board[my_im[1][1]][my_im[1][0]] = "1"
for i in range(9):
    cv.line(gray2, (int(x + unit*i), y), (int(x + unit*i), y+h), (255,0,0), 1)
for i in range(9):
    cv.line(gray2, (x, int(y+unit*i)), (x+w, int(y+unit*i)),(255,0,0), 1)
cv.rectangle(gray2,(x,y),(x+w,y+h),(0,255,0),3)
#process the rows
fen = [0] * 8
for i in range(8):
    fen[i] = [sum(int(n) for n in v) if k == "1" else ''.join(v) for k, v in itertools.groupby(board[i])]
    for z in range(len(fen[i])):
        fen[i][z] = str(fen[i][z])
    fen[i] = ''.join(fen[i])
print('/'.join(fen) + ' w - - 0 1')
cv.imwrite('res.png',gray2)
cv.imwrite('original.png',img)
print(time.time() - start)
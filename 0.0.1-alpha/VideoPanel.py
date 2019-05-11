import sys
import math

import numpy as np
import cv2 as cv

SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
WINDOW_NAME = "VideoPanel"

# defining our paths
pathList = [
     "rtsp://login:password@IP:PORT/path_to_a_stream",  # this line depends on your device
     "path_to_some_video_file_1",                       # this path is either full path or relative to script path
     "path_to_some_video_file_2",
     "path_to_some_video_file_3",
     "path_to_some_video_file_4"]

if len(pathList) == 0:
    sys.exit()

# Creating array to hold video objects
caps = []

# Creating video objects using paths from pathList
for path in pathList:
    cap = cv.VideoCapture(path)
    if not cap.isOpened():
        print("Error opening ",path)
    else:
        caps.append(cap)
        #print(cap.get(cv.CAP_PROP_FPS))

if len(caps) == 0:
    sys.exit()

# checking number of the video sources for panel splitting
panelSize = math.ceil(math.sqrt(len(caps)))    # panel is a square, so this constant is a panel side

frameWidth = int(SCREEN_WIDTH/panelSize)
frameHeight = int(SCREEN_HEIGHT/panelSize)

emptycellImg = cv.imread('emptycell.png', cv.IMREAD_COLOR)
emptycellImg = cv.resize(emptycellImg,(frameWidth,frameHeight),cv.INTER_AREA)
framecaptureerrorImg = cv.imread('framecaptureerror.png', cv.IMREAD_COLOR)
framecaptureerrorImg = cv.resize(framecaptureerrorImg,(frameWidth,frameHeight),cv.INTER_AREA)

frameList = []
cv.namedWindow(WINDOW_NAME,cv.WINDOW_NORMAL)
cv.setWindowProperty(WINDOW_NAME, cv.WND_PROP_FULLSCREEN, cv.WINDOW_FULLSCREEN)
while True:
    frameList.clear()
    for capidx in range(len(caps)):
        ret, frame = caps[capidx].read()
        #frame = cv.UMat(frame)
        if ret:
            frame = cv.resize(frame,(frameWidth,frameHeight),cv.INTER_AREA)
            frameList.append(frame)
        else:
            frameList.append(framecaptureerrorImg)
            if caps[capidx].isOpened():
                caps[capidx].release()
                caps[capidx] = cv.VideoCapture(pathList[capidx])
            else:
                caps[capidx] = cv.VideoCapture(pathList[capidx])

    firstTimeInRow = True
    for row in range(panelSize):
        firstTimeInCol = True
        for col in range(panelSize):
            idx = row*panelSize+col
            if idx < len(caps):
                if firstTimeInCol:
                    panelCol = frameList[idx]
                    firstTimeInCol = False
                else:
                    panelCol = np.concatenate((panelCol,frameList[idx]),1)
            else:
                if firstTimeInCol:
                    panelCol = emptycellImg
                    firstTimeInCol = False
                else:
                    panelCol = np.concatenate((panelCol,emptycellImg),1)
        if firstTimeInRow:
            panel = panelCol
            firstTimeInRow = False
        else:
            panel = np.concatenate((panel,panelCol),0)

    cv.imshow(WINDOW_NAME, panel)
    if cv.waitKey(1) & 0xFF == ord('q'):
        break

for cap in caps:
    cap.release()
cv.destroyAllWindows()



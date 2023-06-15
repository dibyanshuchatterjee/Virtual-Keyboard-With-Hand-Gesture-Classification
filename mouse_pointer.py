"""
* With hand signs, generic messages - make 2
* Make mapping for switching to keyboard
* Make a key mapping to switch to hand det
"""
import sys

import cv2
from cvzone.HandTrackingModule import HandDetector
import time
import numpy as np
import cvzone
from pynput.keyboard import Key, Controller
import mediapipe as mp
from tensorflow.keras.models import load_model

cap = cv2.VideoCapture(1)
cap.set(3, 1280)
cap.set(4, 720)

detector = HandDetector(detectionCon=1)
keys = [["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P"],
        ["A", "S", "D", "F", "G", "H", "J", "K", "L", ";"],
        ["Z", "X", "C", "V", "B", "N", "M", ",", ".", "/"],
        ["space", "del"]]
finalText = ""

keyboard = Controller()


def drawAll(img, buttonList):
    for button in buttonList:
        x, y = button.pos
        w, h = button.size
        cvzone.cornerRect(img, (button.pos[0], button.pos[1], button.size[0], button.size[1]),
                          20, rt=0)
        # Change the color of the keyboard to black
        cv2.rectangle(img, button.pos, (x + w, y + h), (0, 0, 0), cv2.FILLED)
        # Change the color of the letters to white
        cv2.putText(img, button.text, (x + 20, y + 65),
                    cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4)
    return img


class Button():
    def __init__(self, pos, text, size=[85, 85]):
        self.pos = pos
        self.size = size
        self.text = text


buttonList = []
for i in range(len(keys)):
    for j, key in enumerate(keys[i]):
        buttonList.append(Button([100 * j + 50, 100 * i + 50], key))

# Add space and backspace buttons
# buttonList.append(Button([100 * 3 + 50, 100 * 3 + 50], "space"))


# buttonList.append(Button([100 * 3 + 50, 100 * 4 + 50], "space", [220, 85]))
# buttonList.append(Button([100 * 6 + 50, 100 * 4 + 50], "del", [120, 85]))
# buttonList.append(Button([100 * 0 + 50, 100 * 5 + 50], "switch to gestures", [1150, 85]))

# Add space, backspace, and switch buttons
buttonList.append(Button([100 * 0 + 50, 100 * 4 + 50], "space", [220, 85]))
buttonList.append(Button([100 * 9 + 50, 100 * 4 + 50], "del", [120, 85]))
buttonList.append(Button([100 * 0 + 50, 100 * 5 + 50], "switch to gestures", [1000, 85]))


while True:

    # Virtual keyboard code
    success, img = cap.read()
    img = detector.findHands(img)
    lmList, bboxInfo = detector.findPosition(img)
    img = drawAll(img, buttonList)

    # todo: keyborad:

    success, img = cap.read()
    img = detector.findHands(img)
    lmList, bboxInfo = detector.findPosition(img)
    img = drawAll(img, buttonList)

    if lmList:
        for button in buttonList:
            x, y = button.pos
            w, h = button.size

            if x < lmList[8][0] < x + w and y < lmList[8][1] < y + h:
                cv2.rectangle(img, (x - 5, y - 5), (x + w + 5, y + h + 5), (175, 0, 175), cv2.FILLED)
                cv2.putText(img, button.text, (x + 20, y + 65),
                            cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4)
                l, _, _ = detector.findDistance(8, 12, img, draw=False)
                print(l)

                # when clicked
                if l < 30:
                    if button.text != 'del' and button.text != 'space' and button.text != 'switch to gestures':

                        keyboard.press(button.text)
                        cv2.rectangle(img, button.pos, (x + w, y + h), (0, 255, 0), cv2.FILLED)
                        cv2.putText(img, button.text, (x + 20, y + 65),
                                    cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4)
                        finalText += button.text
                        time.sleep(0.15)
                    else:
                        if button.text == 'del':
                            print(f'dekho {button.text}')
                            keyboard.press(Key.backspace)
                            time.sleep(0.15)
                            keyboard.release(Key.backspace)
                        if button.text == 'space':
                            keyboard.press(Key.space)
                            keyboard.release(Key.space)
                        if button.text == 'switch to gestures':
                            sys.exit()

    cv2.rectangle(img, (50, 350), (700, 450), (175, 0, 175), cv2.FILLED)
    cv2.putText(img, finalText, (60, 430),
                cv2.FONT_HERSHEY_PLAIN, 5, (255, 255, 255), 5)

    cv2.imshow("Image", img)
    cv2.waitKey(1)

    if cv2.waitKey(1) == ord('q'):
        break

# release the webcam and destroy all active windows
cap.release()

cv2.destroyAllWindows()

import sys
import time
import cv2
import numpy as np
import cvzone
from pynput.keyboard import Key, Controller
import mediapipe as mp
from tensorflow.keras.models import load_model

cap = cv2.VideoCapture(1)
cap.set(3, 1280)
cap.set(4, 720)

# initialize mediapipe
mpHands = mp.solutions.hands
hands = mpHands.Hands(max_num_hands=1, min_detection_confidence=0.8)
mpDraw = mp.solutions.drawing_utils

# Load the gesture recognizer model
model = load_model('mp_hand_gesture')

# Load class names
f = open('gesture.names', 'r')
classNames = f.read().split('\n')
f.close()
print(classNames)

# Create an instance of the keyboard controller
keyboard = Controller()


def hand_sign_detection():
    # Read each frame from the webcam
    _, frame = cap.read()

    x, y, c = frame.shape

    # Flip the frame vertically
    frame = cv2.flip(frame, 1)
    framergb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Get hand landmark prediction
    result = hands.process(framergb)

    # print(result)

    className = ''

    # post process the result
    if result.multi_hand_landmarks:
        landmarks = []
        for handslms in result.multi_hand_landmarks:
            for lm in handslms.landmark:
                # print(id, lm)
                lmx = int(lm.x * x)
                lmy = int(lm.y * y)

                landmarks.append([lmx, lmy])

            # Drawing landmarks on frames
            mpDraw.draw_landmarks(frame, handslms, mpHands.HAND_CONNECTIONS)

            # Predict gesture
            prediction = model.predict([landmarks])
            # print(prediction)
            classID = np.argmax(prediction)
            className = classNames[classID]

    # show the prediction on the frame
    cv2.putText(frame, className, (10, 50), cv2.FONT_HERSHEY_SIMPLEX,
                1, (0, 0, 255), 2, cv2.LINE_AA)

    # Show the final output
    cv2.imshow("Output", frame)
    if className == 'Switch to Keyboard':
        cv2.putText(frame, "Switching to Virtual Keyboard....", (10, 50), cv2.FONT_HERSHEY_SIMPLEX,
                    1, (0, 0, 255), 2, cv2.LINE_AA)

        time.sleep(0.5)
        sys.exit()

    if className == 'okay':
        # Press and release the Enter key
        keyboard.press(Key.enter)
        keyboard.release(Key.enter)

    return className


def main():
    counter = 0
    delay = 30  # number of frames to wait before printing a new prediction
    prev_prediction = None
    while True:
        className = hand_sign_detection()

        if className != prev_prediction and counter >= delay:
            prev_prediction = className
            counter = 0
            # Iterate over each character in the string and type it
            for char in str(className):
                if className != 'okay':
                    keyboard.press(char)
                    keyboard.release(char)

        else:
            counter += 1

        if cv2.waitKey(1) == ord('q'):
            break
    # release the webcam and destroy all active windows
    cap.release()

    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()

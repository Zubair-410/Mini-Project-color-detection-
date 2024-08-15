import cv2
import pandas as pd

# Use 0 for the default webcam
cap = cv2.VideoCapture(0)

clicked = False
r = g = b = x_pos = y_pos = 0

index = ["color", "color_name", "hex", "R", "G", "B"]
csv = pd.read_csv('colors.csv', names=index, header=None)

def get_color_name(R, G, B):
    minimum = 10000
    for i in range(len(csv)):
        d = abs(R - int(csv.loc[i, "R"])) + abs(G - int(csv.loc[i, "G"])) + abs(B - int(csv.loc[i, "B"]))
        if d <= minimum:
            minimum = d
            cname = csv.loc[i, "color_name"]
    return cname

def draw_function(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDBLCLK:
        global b, g, r, x_pos, y_pos, clicked
        clicked = True
        x_pos = x
        y_pos = y
        b, g, r = frame[y, x]
        b = int(b)
        g = int(g)
        r = int(r)

cv2.namedWindow('video')
cv2.setMouseCallback('video', draw_function)

color_text = ""
color_rect = (0, 0, 0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    if clicked:
        color_rect = (b, g, r)
        color_text = get_color_name(r, g, b) + ' R=' + str(r) + ' G=' + str(g) + ' B=' + str(b)
        clicked = False

    cv2.rectangle(frame, (20, 20), (750, 60), color_rect, -1)
    cv2.putText(frame, color_text, (50, 50), 2, 0.8, (255, 255, 255), 2, cv2.LINE_AA)

    if sum(color_rect) >= 600:
        cv2.putText(frame, color_text, (50, 50), 2, 0.8, (0, 0, 0), 2, cv2.LINE_AA)

    cv2.imshow('video', frame)
    if cv2.waitKey(20) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()

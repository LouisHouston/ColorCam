import cv2
import numpy as np

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("camera error opening")
    exit()

while True:
    ret, frame = cap.read()

    if not ret:
        print("couldnt get image err")
        break
    
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    lower_color = np.array([100, 150, 50]) 
    upper_color = np.array([255, 255, 255]) 
    mask = cv2.inRange(hsv, lower_color, upper_color)

    result = cv2.bitwise_and(frame, frame, mask=mask)

    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if contours:
        largest_contour = max(contours, key=cv2.contourArea)

        x, y, w, h = cv2.boundingRect(largest_contour)

        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        shirt_roi = frame[y:y + h, x:x + w]

        avg_color_per_row = np.average(shirt_roi, axis=0)
        avg_color = np.average(avg_color_per_row, axis=0)

        avg_color_bgr = np.uint8([[avg_color]])
        avg_color_rgb = cv2.cvtColor(avg_color_bgr, cv2.COLOR_BGR2RGB)[0][0]
        
        cv2.putText(frame, f"Avg Color: {avg_color_rgb}", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

        print(f"Dominant color: {avg_color_rgb}")

    cv2.imshow('Shirt Color Detection', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break 


cap.release()
cv2.destroyAllWindows()
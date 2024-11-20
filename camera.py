import cv2

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("camera error opening")
    exit()

while True:
    ret, frame = cap.read()

    if not ret:
        print("couldnt get image err")
        break

    cv2.imshow('Cam Feed', frame)


    if cv2.waitKey(1) & 0xFF == ord('q'):
        break 


cap.release()
cv2.destroyAllWindows()
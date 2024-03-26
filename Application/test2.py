cap = cv2.VideoCapture(0)
while cap.isOpened():
    ret, frame =cap.read()
    cv2.imshow('Model: ', frame)

    if cv2.waitKey(10) and 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()

mp_drawing = mp.solutions.drawing_utils
mp_holistic = mp.solutions.holistic
cap = cv2.VideoCapture(0)

#initialize landmark model

cap = cv2.VideoCapture(0)

#CH
with mp_holistic.Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.5) as holistic:
    while cap.isOpened():
        ret, frame =cap.read()

        #recolor feed
        image = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)
        #DETECTIONS
        results = holistic.process(image)
        #print(results.face_landmarks)


        #recolor to bgr for rendering
        #image = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

        mp_drawing.draw_landmarks(image, results.face_landmarks, mp_holistic.FACEMESH_TESSELATION)


        cv2.imshow('Webcam feed: ', image)

        if cv2.waitKey(10) and 0xFF == ord('q'):
            break
cap.release()
cv2.destroyAllWindows()

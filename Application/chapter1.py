import cv2

#CV2 Opening Images, Videos, WEbcams
#reads an image
img = cv2.imread("Resources/hah.jpg")

#reads a video / webcam (cv2.VideoCapture(0) <== Put 0 - number of webcams you have)
cap = cv2.VideoCapture(0)

cap.set(3, 640)
cap.set(4, 480)
#shows an image
#cv2.imshow("Smug Tao", img)


#shows a video
while True:
    #A video is just multiple images, therefore we can loop through the video and show it
    success, img = cap.read()
    imgCanny = cv2.Canny(img, 55, 55)
    cv2.imshow("Vocoded", imgCanny)

    #Will close if the ord(key) is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
         break


#delays the showing of the image
#cv2.waitKey(3000)


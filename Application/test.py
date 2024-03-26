import cv2
from PySide6 import QtCore, QtWidgets, QtGui

#CV2 Opening Images, Videos, WEbcams
#reads a video / webcam (cv2.VideoCapture(0) <== Put 0 - number of webcams you have)
cap = cv2.VideoCapture(0)

cap.set(3, 640)
cap.set(4, 480)
#shows an image

#shows a video
while True:
    #A video is just multiple images, therefore we can loop through the video and show it
    success, img = cap.read()
    cv2.imshow("Cam", img)

    #Will close if the ord(key) is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
         break


#delays the showing of the image
#cv2.waitKey(3000)

class MyWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.hello = ["Hallo Welt", "Hei maailma", "Hola Mundo", "Привет мир"]

        self.button = QtWidgets.QPushButton("Click me!")
        self.text = QtWidgets.QLabel("Hello World",
                                     alignment=QtCore.Qt.AlignCenter)

        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.text)
        self.layout.addWidget(self.button)

        self.button.clicked.connect(self.magic)

    @QtCore.Slot()
    def magic(self):
        self.text.setText(random.choice(self.hello))

if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    widget = MyWidget()
    widget.resize(800, 600)
    widget.show()

    sys.exit(app.exec())
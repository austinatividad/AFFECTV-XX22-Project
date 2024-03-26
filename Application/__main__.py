import sys
import os
from PySide6.QtWidgets import QPushButton, QApplication, QVBoxLayout, QHBoxLayout, QLabel, QWidget, QFileDialog
from PySide6.QtGui import QPixmap, QImage
from PySide6.QtCore import QSize, Qt, QThread, Signal
import cv2
import face_detection
import emotion_detection
from time import time
print(os.getcwd())
class MainMenu(QWidget):

    def __init__(self):
        super().__init__()
        #  Image for  Main Menu
        self.bgImage = QPixmap(os.getcwd() + "/Application/reservations.png")
        self.bgImage = self.bgImage.scaled(QSize(640, 400))
        self.bgLabel = QLabel(self)
        self.bgLabel.setPixmap(self.bgImage)

        # Buttons for main menu
        self.startButton = QPushButton("Start")
        self.aboutButton = QPushButton("About")
        self.quitButton = QPushButton("Quit")

        btnLayout  = QHBoxLayout()
        btnLayout.addWidget(self.startButton)
        btnLayout.addWidget(self.aboutButton)
        btnLayout.addWidget(self.quitButton)

        # Create layout and add widgets
        layout = QVBoxLayout()
        layout.addWidget(self.bgLabel)
        layout.addLayout(btnLayout)
        # Set dialog layout
        self.setLayout(layout)
        
        # Add button signal to greetings slot
        self.startButton.clicked.connect(self.start)
        self.aboutButton.clicked.connect(self.about)
        self.quitButton.clicked.connect(self.quit)

        self.resize(640, 480)

    # Greets the user
    def start(self):
        print("Show App Tab Here")

    def about(self):
        print("Show About Tab Here")

    def quit(self):
        sys.exit()

class StartMenu(QWidget):

    def __init__(self):
        super().__init__()
        #  Image for  Main Menu
        self.screenLabel = QLabel(self)
        self.screenLabel.setStyleSheet("background-color: rgb(0,0,0)")

        self.angryLabel = QLabel(self)
        self.angryLabel.setText("Angry: 00.00%")
        self.happyLabel = QLabel(self)
        self.happyLabel.setText("Happy: 00.00%")
        self.neutralLabel = QLabel(self)
        self.neutralLabel.setText("Neutral: 00.00%")
        self.sadLabel = QLabel(self)
        self.sadLabel.setText("Sad: 00.00%")

        # Buttons for main menu
        self.startAppButton = QPushButton("Start")
        self.imgButton = QPushButton("I")
        self.vidButton = QPushButton("V")
        self.exitAppButton = QPushButton("Quit")

        btnLayout  = QHBoxLayout()
        btnLayout.addWidget(self.startAppButton)
        btnLayout.addWidget(self.imgButton)
        btnLayout.addWidget(self.vidButton)
        btnLayout.addWidget(self.exitAppButton)

        labelsLayout = QVBoxLayout()
        labelsLayout.addWidget(self.angryLabel)
        labelsLayout.addWidget(self.happyLabel)
        labelsLayout.addWidget(self.neutralLabel)
        labelsLayout.addWidget(self.sadLabel)
        # Create layout and add widgets
        appLayout = QVBoxLayout()
        appLayout.addWidget(self.screenLabel, alignment=Qt.AlignCenter)
        appLayout.addLayout(btnLayout)


        layout = QHBoxLayout()
        layout.addLayout(appLayout, stretch=4)
        layout.addLayout(labelsLayout, stretch=1)
        # Set dialog layout
        self.setLayout(layout)
        
        #Webcam connection
        self.webcamWorker = Webcam()
        self.webcamWorker.ImageUpdate.connect(self.updateVideo)
        
        # Add button signal to greetings slot
        self.startAppButton.clicked.connect(self.start)
        self.imgButton.clicked.connect(self.imgMode)
        self.vidButton.clicked.connect(self.vidMode)
        self.exitAppButton.clicked.connect(self.exit)

        self.resize(640, 480)

    def updateVideo(self, image, confidence_levels):
        self.screenLabel.setPixmap(QPixmap.fromImage(image).scaledToWidth(520).scaledToHeight(400))
        self.angryLabel.setText(confidence_levels["Angry"])
        self.happyLabel.setText(confidence_levels["Happy"])
        self.neutralLabel.setText(confidence_levels["Neutral"])
        self.sadLabel.setText(confidence_levels["Sad"])
    
    # Greets the user
    def start(self):
        print("Toggling Detection System Now")

    def imgMode(self):
        self.webcamWorker.stop()

        fname = QFileDialog.getOpenFileName(self, 'Open file', 'c:\\',"Image files (*.jpg *.png)")
        imageDirectory = fname[0]

        faceDetectionModel = face_detection.init_model('Application/face_landmarker_v2_with_blendshapes.task')
        emotionDetectionModel = emotion_detection.init_model('Application/emotion_model4.keras')

        image = cv2.imread(imageDirectory)
        DetectionResult, image = face_detection.detect_faces(faceDetectionModel, image)
        if len(DetectionResult.face_landmarks) > 0:
            print(DetectionResult.face_landmarks[1])
            confidence_levels = emotion_detection.detect_emotions(emotionDetectionModel, DetectionResult.face_landmarks[0])
        
        ConvertToQtFormat = QImage(image.data, image.shape[1], image.shape[0], QImage.Format_RGB888)
        pic = ConvertToQtFormat.scaled(640, 480, Qt.KeepAspectRatio)
        
        self.screenLabel.setPixmap(QPixmap.fromImage(pic).scaledToWidth(520).scaledToHeight(400))
        self.angryLabel.setText(confidence_levels["Angry"])
        self.happyLabel.setText(confidence_levels["Happy"])
        self.neutralLabel.setText(confidence_levels["Neutral"])
        self.sadLabel.setText(confidence_levels["Sad"])
    
    def vidMode(self):
        self.webcamWorker.start()
        print("Vid Mode On!")

    def exit(self):
        self.webcamWorker.stop()
        print("Bye Bye!")


class Webcam(QThread):
    ImageUpdate = Signal(QImage, dict)
    faceDetectionModel = face_detection.init_model('Application/face_landmarker_v2_with_blendshapes.task')
    emotionDetectionModel = emotion_detection.init_model('Application/emotion_model.keras')
    detectFaces = True
    DetectionResult = None

    def run(self):
        self.ThreadActive = True
        Capture = cv2.VideoCapture(0)

        previous = time()
        delta = 0

        confidence_levels = {
            "Angry" : "00.00%",
            "Happy" : "00.00%",
            "Neutral" : "00.00%",
            "Sad" : "00.00%"
        }
        
        while self.ThreadActive:
            ret, frame = Capture.read()
            if ret:
                # Get the current time, increase delta and update the previous variable
                current = time()
                delta += current - previous
                previous = current
                
                
                Image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                '''
                Uncomment This if you want to resize the image to what it used in the dataset (about 96x96)
                height, width = Image.shape[:2]
                scaling_factor = 96 / float(height)
                new_height = 96
                new_width = width * scaling_factor
                Image = cv2.resize(Image, (round(new_width), round(new_height))) 
                '''
                

                FlippedImage = cv2.flip(Image, 1)
                if self.detectFaces:
                    DetectionResult, FlippedImage = face_detection.detect_faces(self.faceDetectionModel, FlippedImage)

                    if delta > 1 and len(DetectionResult.face_landmarks) > 0:
                        confidence_levels = emotion_detection.detect_emotions(self.emotionDetectionModel, DetectionResult.face_landmarks[0])
                        print("Predicted Emotion:", confidence_levels)

                        delta = 0

                ConvertToQtFormat = QImage(FlippedImage.data, FlippedImage.shape[1], FlippedImage.shape[0], QImage.Format_RGB888)
                pic = ConvertToQtFormat.scaled(640, 480, Qt.KeepAspectRatio)
                self.ImageUpdate.emit(pic, confidence_levels)
    def stop(self):
        self.ThreadActive = False
        self.quit()

class AboutMenu(QWidget):

    def __init__(self):
        super().__init__()
        #  Image for  Main Menu
        self.bgLabel = QLabel(self)
        self.bgLabel.setText("About Page")
        # Buttons for main menu
        self.quitButton = QPushButton("Quit")
        # Create layout and add widgets
        layout = QVBoxLayout()
        layout.addWidget(self.bgLabel)
        layout.addWidget(self.quitButton)
        # Set dialog layout
        self.setLayout(layout)
        
        # Add button signal to greetings slot
        self.quitButton.clicked.connect(self.quit)

        self.resize(640, 480)

    def quit(self):
        print("Bye Bye!")


def showAbout(mainMenu, startMenu, aboutMenu):
    mainMenu.hide()
    startMenu.hide()
    aboutMenu.show()

def showStart(mainMenu, startMenu, aboutMenu):
    mainMenu.hide()
    startMenu.show()
    aboutMenu.hide()

def showMain(mainMenu, startMenu, aboutMenu):
    mainMenu.show()
    startMenu.hide()
    aboutMenu.hide()

if __name__ == '__main__':
    # Create the Qt Application
    app = QApplication(sys.argv)
    # Create and show the form
    mainMenu = MainMenu()
    aboutMenu = AboutMenu()
    startMenu = StartMenu()

    mainMenu.startButton.clicked.connect(lambda: showStart(mainMenu, startMenu, aboutMenu))
    mainMenu.aboutButton.clicked.connect(lambda: showAbout(mainMenu, startMenu, aboutMenu))

    startMenu.exitAppButton.clicked.connect(lambda: showMain(mainMenu, startMenu, aboutMenu))
    aboutMenu.quitButton.clicked.connect(lambda: showMain(mainMenu, startMenu, aboutMenu))

    mainMenu.show()

    # Run the main Qt loop
    sys.exit(app.exec())


import sys
import os
from PySide6.QtWidgets import QPushButton, QApplication, QVBoxLayout, QHBoxLayout, QLabel, QWidget, QFileDialog
from PySide6.QtGui import QPixmap, QImage
from PySide6.QtCore import QSize, Qt, QThread, Signal
import cv2
import face_detection
import emotion_detection
from time import time
dir_path = os.path.dirname(os.path.realpath(__file__))

face_detection_wd = dir_path + '/face_landmarker_v2_with_blendshapes.task'
emotion_detection_wd = dir_path + '/emotion_modelshrinkinglayers.keras'
class MainMenu(QWidget):

    def __init__(self):
        super().__init__()
        #  Image for  Main Menu
        self.bgImage = QPixmap(dir_path + "/reservations.png")
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
        self.toggleMaskButton = QPushButton("Toggle Mask: On")
        self.imgButton = QPushButton("Test Image")
        self.vidButton = QPushButton("Test Video")
        self.exitAppButton = QPushButton("Quit")

        self.useMask = True

        btnLayout  = QHBoxLayout()
        btnLayout.addWidget(self.toggleMaskButton)
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
        self.toggleMaskButton.clicked.connect(self.toggleMask)
        self.imgButton.clicked.connect(self.imgMode)
        self.vidButton.clicked.connect(self.vidMode)
        self.exitAppButton.clicked.connect(self.exit)

        self.resize(640, 480)

    def updateVideo(self, image, annotated_image, confidence_levels):
        imageToShow = image

        if self.useMask:
            imageToShow = annotated_image

        self.screenLabel.setPixmap(QPixmap.fromImage(imageToShow).scaledToWidth(400).scaledToHeight(400))
        self.angryLabel.setText(confidence_levels["Angry"])
        self.happyLabel.setText(confidence_levels["Happy"])
        self.neutralLabel.setText(confidence_levels["Neutral"])
        self.sadLabel.setText(confidence_levels["Sad"])
    
    # Greets the user
    def toggleMask(self):
        if self.useMask:
            self.useMask = False
            self.toggleMaskButton.setText("Toggle Mask: Off")
        else:
            self.useMask = True
            self.toggleMaskButton.setText("Toggle Mask: On")

    def imgMode(self):
        self.webcamWorker.stop()

        fname = QFileDialog.getOpenFileName(self, 'Open file', 'c:\\',"Image files (*.jpg *.png)")
        imageDirectory = fname[0]

        faceDetectionModel = face_detection.init_model(face_detection_wd)
        emotionDetectionModel = emotion_detection.init_model(emotion_detection_wd)

        image = cv2.imread(imageDirectory)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        height, width = image.shape[0:2]

        diff = abs(width - height) // 2

        if width < height: #Pad the sides
            image = cv2.copyMakeBorder(image, 0, 0, diff, diff, cv2.BORDER_CONSTANT, None, value=1)
        elif width > height: #Pad up andd down
            image = cv2.copyMakeBorder(image, diff, diff, 0, 0, cv2.BORDER_CONSTANT, None, value=1)
        else:
            image = cv2.copyMakeBorder(image, 2, 2, 2, 2, cv2.BORDER_CONSTANT, None, value=1)
        
        #Check if width is odd
        if width % 2 == 1:
            #Add 1 pixel to left
            image = cv2.copyMakeBorder(image, 0, 0, 0, 1, cv2.BORDER_CONSTANT, None, value=1)


        DetectionResult, annotated_image = face_detection.detect_faces(faceDetectionModel, image)

        if self.useMask:
            image = annotated_image

        if len(DetectionResult.face_landmarks) > 0:
            confidence_levels = emotion_detection.detect_emotions(emotionDetectionModel, DetectionResult.face_landmarks[0])
        else:
            confidence_levels = {
                "Angry" : "Angry: 00.00%",
                "Happy" : "Happy: 00.00%",
                "Neutral" : "Neutral: 00.00%",
                "Sad" : "Sad: 00.00%"
            }
        
        print("Before Conversion")
        
        bytesPerLine = image.shape[1] * 3
        ConvertToQtFormat = QImage(image.data, image.shape[1], image.shape[0], bytesPerLine, QImage.Format_RGB888)
        pic = ConvertToQtFormat.scaled(520, 400, Qt.KeepAspectRatio)
        
        print("Conversion!")
        self.screenLabel.setPixmap(QPixmap.fromImage(pic))
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
    ImageUpdate = Signal(QImage, QImage, dict)
    faceDetectionModel = face_detection.init_model(face_detection_wd)
    emotionDetectionModel = emotion_detection.init_model(emotion_detection_wd)
    detectFaces = True
    DetectionResult = None

    def run(self):
        self.ThreadActive = True
        Capture = cv2.VideoCapture(0)


        height = int(Capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
        width = int(Capture.get(cv2.CAP_PROP_FRAME_WIDTH))

        offset = width - height
        center_coord = (int(height * 0.45), int(height // 2))
        axes_length = (int(height * 0.35), int(height * 0.45))


        print(center_coord)

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
                
                Image = Image[0:height, int(offset // 2):int(offset // 2)+height]

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
                    DetectionResult, FlippedAnnotatedImage = face_detection.detect_faces(self.faceDetectionModel, FlippedImage)
                    
                    FlippedAnnotatedImage = cv2.circle(FlippedAnnotatedImage, center=center_coord, radius=2, color=(0, 255, 0), thickness=1)
                    FlippedAnnotatedImage = cv2.ellipse(FlippedAnnotatedImage, center=center_coord, axes=axes_length, angle=0, startAngle=0, endAngle=360, color=(0, 255, 0), thickness=1)

                    if delta > 1 and len(DetectionResult.face_landmarks) > 0:
                        confidence_levels = emotion_detection.detect_emotions(self.emotionDetectionModel, DetectionResult.face_landmarks[0])
                        print("Predicted Emotion:", confidence_levels)

                        delta = 0


                FlippedImage = cv2.circle(FlippedImage, center=center_coord, radius=2, color=(0, 255, 0), thickness=1)
                FlippedImage = cv2.ellipse(FlippedImage, center=center_coord, axes=axes_length, angle=0, startAngle=0, endAngle=360, color=(0, 255, 0), thickness=1)

                ConvertToQtFormatAnnotated = QImage(FlippedAnnotatedImage.data, FlippedAnnotatedImage.shape[1], FlippedAnnotatedImage.shape[0], QImage.Format_RGB888)
                picAnnotated = ConvertToQtFormatAnnotated.scaled(640, 480, Qt.KeepAspectRatio)

                ConvertToQtFormatAnnotated = QImage(FlippedImage.data, FlippedImage.shape[1], FlippedImage.shape[0], QImage.Format_RGB888)
                pic = ConvertToQtFormatAnnotated.scaled(640, 480, Qt.KeepAspectRatio)


                self.ImageUpdate.emit(pic, picAnnotated, confidence_levels)
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


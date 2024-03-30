from sys import exit
from PySide6.QtWidgets import QPushButton, QApplication, QVBoxLayout, QHBoxLayout, QLabel, QWidget, QFileDialog
from PySide6.QtGui import QPixmap, QImage, QIcon
from PySide6.QtCore import QSize, Qt, QThread, Signal
import cv2
import face_detection
import emotion_detection
from pandas import read_csv
from time import time
from numpy import ndarray
dir_path = "./assets/"
face_detection_wd = dir_path + 'face_landmarker_v2_with_blendshapes.task'
emotion_detection_wd = dir_path + 'emotion_model.keras'
emotion_detection_wd_simplified = dir_path + 'emotion_model_simplified.keras'

stat_df_simplified = read_csv(dir_path + 'stat_train_features_simplified.csv')
stat_df = read_csv(dir_path + 'stat_train_features.csv')

colors = {
    "blue": (88, 102, 195),
    "light_blue": (92, 107, 204),
    "dark1_blue": (73, 85, 162),
    "dark2_blue": (57, 67, 128),
    "dark3_blue": (42, 49, 94),
    "dark4_blue": (27, 31, 60)
}



class MainMenu(QWidget):

    def __init__(self):
        super().__init__()
        #  Image for  Main Menu
        self.bgImage = QPixmap(dir_path + "Face.png")
        self.bgImage = self.bgImage.scaled(QSize(640, 400))
        self.bgLabel = QLabel(self)
        self.bgLabel.setPixmap(self.bgImage)

        # Buttons for main menu
        self.startButton = QPushButton("Start")
        self.aboutButton = QPushButton("About")
        self.quitButton = QPushButton("Quit")

        self.startButton.setStyleSheet("background-color: rgb" + str(colors["dark1_blue"]) + "; color: rgb(255,255,255); font-size: 22px; font-weight: bold; padding: 3px;")
        self.aboutButton.setStyleSheet("background-color: rgb" + str(colors["dark1_blue"]) + "; color: rgb(255,255,255); font-size: 22px; font-weight: bold; padding: 3px;")
        self.quitButton.setStyleSheet("background-color: rgb" + str(colors["dark1_blue"]) + "; color: rgb(255,255,255); font-size: 22px; font-weight: bold; padding: 3px;")

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

        self.setWindowFlags(Qt.WindowCloseButtonHint | Qt.WindowMinimizeButtonHint)
        self.setStyleSheet("background-color: rgb" + str(colors["dark2_blue"]) + ";")
        self.resize(720, 480)
        self.setWindowTitle("AFFECT: Faces of Emotion")
        self.setWindowIcon(QIcon(dir_path + "Icon.png"))

    # Greets the user
    def start(self):
        print("Show App Tab Here")

    def about(self):
        print("Show About Tab Here")

    def quit(self):
        exit()

class AboutMenu(QWidget):

    def __init__(self):
        super().__init__()

        #  Image for  Main Menu
        self.bgLabel = QLabel(self)
        self.bgLabel.setText("<h1>About Page</h1><br><p>This application detects the emotion that a face projects using facial landmarks provided by <a href='https://developers.google.com/mediapipe/solutions/vision/face_landmarker'>Mediapipe</a>,</p><p>fed into a Convolutional Neural Network.</p><p>In Video Mode, make sure your face fills the outline!</p><br><a href='https://github.com/austinatividad/AFFECTV-XX22-Project'>Github Link</a>")
        self.bgLabel.setStyleSheet("background-color: rgb" + str(colors["dark4_blue"]) + "; color: rgb(255,255,255); font-size: 16px; font-weight: bold; padding: 3px;")
        # Buttons for main menu
        self.quitButton = QPushButton("Quit")
        self.quitButton.setStyleSheet("background-color: rgb" + str(colors["dark1_blue"]) + "; color: rgb(255,255,255); font-size: 22px; font-weight: bold; padding: 3px;")
        # Create layout and add widgets
        layout = QVBoxLayout()
        layout.addWidget(self.bgLabel)
        layout.addWidget(self.quitButton)
        # Set dialog layout
        self.setLayout(layout)
        
        # Add button signal to greetings slot
        self.quitButton.clicked.connect(self.quit)

        self.setWindowFlags(Qt.WindowCloseButtonHint | Qt.WindowMinimizeButtonHint)
        self.setStyleSheet("background-color: rgb" + str(colors["dark2_blue"]) + ";")
        self.resize(720, 480)
        self.setWindowTitle("AFFECT: Faces of Emotion")
        self.setWindowIcon(QIcon(dir_path + "/Icon.png"))

    def quit(self):
        print("Bye Bye!")

class StartMenu(QWidget):

    def __init__(self):
        super().__init__()

        self.faceDetectionModel = face_detection.init_model(face_detection_wd)
        self.emotionDetectionModelSimplified = emotion_detection.init_model(emotion_detection_wd_simplified)
        self.emotionDetectionModel = emotion_detection.init_model(emotion_detection_wd)

        #  Image for  Main Menu
        self.screenLabel = QLabel(self)
        self.screenLabel.setStyleSheet("background-color: rgb" + str(colors["dark2_blue"]) + ";")

        self.angryLabel = QLabel(self)
        self.angryLabel.setText("Angry: 00.00%")
        self.happyLabel = QLabel(self)
        self.happyLabel.setText("Happy: 00.00%")
        self.neutralLabel = QLabel(self)
        self.neutralLabel.setText("Neutral: 00.00%")
        self.sadLabel = QLabel(self)
        self.sadLabel.setText("Sad: 00.00%")

        self.angryLabel.setStyleSheet("background-color: rgb" + str(colors["dark4_blue"]) + "; color: rgb(255,255,255); font-size: 22px; font-weight: bold; padding: 3px;")
        self.happyLabel.setStyleSheet("background-color: rgb" + str(colors["dark4_blue"]) + "; color: rgb(255,255,255); font-size: 22px; font-weight: bold; padding: 3px;")
        self.neutralLabel.setStyleSheet("background-color: rgb" + str(colors["dark4_blue"]) + "; color: rgb(255,255,255); font-size: 22px; font-weight: bold; padding: 3px;")
        self.sadLabel.setStyleSheet("background-color: rgb" + str(colors["dark4_blue"]) + "; color: rgb(255,255,255); font-size: 22px; font-weight: bold; padding: 3px;")


        # Buttons for main menu
        self.toggleMaskButton = QPushButton("Show Mask: On")
        self.changeMaskModeButton = QPushButton("Mask Mode: Full")
        self.imgButton = QPushButton("Test Image")
        self.vidButton = QPushButton("Test Video")
        self.exitAppButton = QPushButton("Quit")

        self.toggleMaskButton.setStyleSheet("background-color: rgb" + str(colors["dark1_blue"]) + "; color: rgb(255,255,255); font-size: 22px; font-weight: bold; padding: 3px;")
        self.changeMaskModeButton.setStyleSheet("background-color: rgb" + str(colors["dark1_blue"]) + "; color: rgb(255,255,255); font-size: 22px; font-weight: bold; padding: 3px;")
        self.imgButton.setStyleSheet("background-color: rgb" + str(colors["dark1_blue"]) + "; color: rgb(255,255,255); font-size: 22px; font-weight: bold; padding: 3px;")
        self.vidButton.setStyleSheet("background-color: rgb" + str(colors["dark1_blue"]) + "; color: rgb(255,255,255); font-size: 22px; font-weight: bold; padding: 3px;")
        self.exitAppButton.setStyleSheet("background-color: rgb" + str(colors["dark1_blue"]) + "; color: rgb(255,255,255); font-size: 22px; font-weight: bold; padding: 3px;")


        self.useMask = True
        self.fullMask = True
        self.delta = 0

        btnLayout  = QHBoxLayout()
        btnLayout.addWidget(self.toggleMaskButton)
        btnLayout.addWidget(self.changeMaskModeButton)
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
        self.changeMaskModeButton.clicked.connect(self.toggleMaskMode)
        self.imgButton.clicked.connect(self.imgMode)
        self.vidButton.clicked.connect(self.vidMode)
        self.exitAppButton.clicked.connect(self.exit)

        self.setWindowFlags(Qt.WindowCloseButtonHint | Qt.WindowMinimizeButtonHint)
        self.setStyleSheet("background-color: rgb" + str(colors["dark2_blue"]) + ";") 
        self.resize(720, 480)
        self.setWindowTitle("AFFECT: Faces of Emotion")
        self.setWindowIcon(QIcon(dir_path + "/Icon.png"))

    def updateVideo(self, raw_image, timeElapsed, center_coord, ellipse_coord, axes_length):
        self.delta += timeElapsed
        DetectionResult, FlippedAnnotatedImage = face_detection.detect_faces(self.faceDetectionModel, raw_image, self.fullMask)

        if self.delta > 1 and len(DetectionResult.face_landmarks) > 0:
            model_to_use = self.emotionDetectionModelSimplified

            if self.fullMask:
                model_to_use = self.emotionDetectionModel

            confidence_levels = emotion_detection.detect_emotions(model_to_use, DetectionResult.face_landmarks[0], stat_full=stat_df, stat_simp=stat_df_simplified, fullMask=self.fullMask)
            print("Predicted Emotion:", confidence_levels)
            self.delta = 0
            self.setEmotionLabels(confidence_levels)
        
        imageToShow = raw_image
        if self.useMask:
            imageToShow = FlippedAnnotatedImage
            
        imageToShow = cv2.circle(imageToShow, center=center_coord, radius=2, color=colors["light_blue"], thickness=1)
        imageToShow = cv2.ellipse(imageToShow, center=ellipse_coord, axes=axes_length, angle=0, startAngle=0, endAngle=360, color=colors["light_blue"], thickness=1)

        ConvertToQtFormat = QImage(imageToShow.data, imageToShow.shape[1], imageToShow.shape[0], QImage.Format_RGB888)
        pic = ConvertToQtFormat.scaled(640, 480, Qt.KeepAspectRatio)

        self.screenLabel.setPixmap(QPixmap.fromImage(pic).scaledToWidth(400).scaledToHeight(400))
    
    def toggleMaskMode(self):
        if self.fullMask:
            self.fullMask = False
            self.changeMaskModeButton.setText("Mask Mode: Lite")
        else:
            self.fullMask = True
            self.changeMaskModeButton.setText("Mask Mode: Full")


    def toggleMask(self):
        if self.useMask:
            self.useMask = False
            self.toggleMaskButton.setText("Show Mask: Off")
        else:
            self.useMask = True
            self.toggleMaskButton.setText("Show Mask: On")

    def imgMode(self):
        self.webcamWorker.stop()

        fname = QFileDialog.getOpenFileName(self, 'Open file', 'c:\\',"Image files (*.jpg *.png)")
        imageDirectory = fname[0]

        image = cv2.imread(imageDirectory)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        height, width = image.shape[0:2]

        diff = abs(width - height) // 2

        if width < height: #Pad the sides
            image = cv2.copyMakeBorder(image, 0, 0, diff, diff, cv2.BORDER_CONSTANT, None, value=colors["blue"])
        elif width > height: #Pad up andd down
            image = cv2.copyMakeBorder(image, diff, diff, 0, 0, cv2.BORDER_CONSTANT, None, value=colors["blue"])
        else:
            image = cv2.copyMakeBorder(image, 2, 2, 2, 2, cv2.BORDER_CONSTANT, None, value=colors["blue"])
        
        #Check if width is odd
        if width % 2 == 1:
            #Add 1 pixel to left
            image = cv2.copyMakeBorder(image, 0, 0, 0, 1, cv2.BORDER_CONSTANT, None, value=colors["blue"])


        DetectionResult, annotated_image = face_detection.detect_faces(self.faceDetectionModel, image, self.fullMask)

        if self.useMask:
            image = annotated_image

        if len(DetectionResult.face_landmarks) > 0:
            model_to_use = self.emotionDetectionModelSimplified

            if self.fullMask:
                model_to_use = self.emotionDetectionModel

            confidence_levels = emotion_detection.detect_emotions(model_to_use, DetectionResult.face_landmarks[0], stat_full=stat_df, stat_simp=stat_df_simplified, fullMask=self.fullMask)
        else:
            confidence_levels = {
                "Angry" : 00.00,
                "Happy" : 00.00,
                "Neutral" : 00.00,
                "Sad" : 00.00
            }
        
        print("Before Conversion")
        
        bytesPerLine = image.shape[1] * 3
        ConvertToQtFormat = QImage(image.data, image.shape[1], image.shape[0], bytesPerLine, QImage.Format_RGB888)
        pic = ConvertToQtFormat.scaled(520, 400, Qt.KeepAspectRatio)
        
        print("Conversion!")
        self.screenLabel.setPixmap(QPixmap.fromImage(pic))
        self.setEmotionLabels(confidence_levels)

    def setEmotionLabels(self, confidence_levels):
        self.angryLabel.setText("Angry: " + str(confidence_levels["Angry"]) + "%")
        self.happyLabel.setText("Happy: " + str(confidence_levels["Happy"]) + "%")
        self.neutralLabel.setText("Neutral: " + str(confidence_levels["Neutral"]) + "%")
        self.sadLabel.setText("Sad: " + str(confidence_levels["Sad"]) + "%")
        
        self.angryLabel.setStyleSheet("background-color: rgb" + str(colors["dark4_blue"]) + "; color: rgb(255,255,255); font-size: 22px; font-weight: bold; padding: 3px;")
        self.happyLabel.setStyleSheet("background-color: rgb" + str(colors["dark4_blue"]) + "; color: rgb(255,255,255); font-size: 22px; font-weight: bold; padding: 3px;")
        self.neutralLabel.setStyleSheet("background-color: rgb" + str(colors["dark4_blue"]) + "; color: rgb(255,255,255); font-size: 22px; font-weight: bold; padding: 3px;")
        self.sadLabel.setStyleSheet("background-color: rgb" + str(colors["dark4_blue"]) + "; color: rgb(255,255,255); font-size: 22px; font-weight: bold; padding: 3px;")

        pred_emotion = max(confidence_levels, key=confidence_levels.get)

        if pred_emotion == "Angry":
            self.angryLabel.setStyleSheet("background-color: rgb" + str(colors["light_blue"]) + "; color: rgb"+ str(colors["dark3_blue"]) + "; font-size: 22px; font-weight: bold; padding: 3px;")
        elif pred_emotion == "Happy":
            self.happyLabel.setStyleSheet("background-color: rgb" + str(colors["light_blue"]) + "; color: rgb"+ str(colors["dark3_blue"]) + "; font-size: 22px; font-weight: bold; padding: 3px;") 
        elif pred_emotion == "Neutral":
            self.neutralLabel.setStyleSheet("background-color: rgb" + str(colors["light_blue"]) + "; color: rgb"+ str(colors["dark3_blue"]) + "; font-size: 22px; font-weight: bold; padding: 3px;") 
        elif pred_emotion == "Sad":
            self.sadLabel.setStyleSheet("background-color: rgb" + str(colors["light_blue"]) + "; color: rgb"+ str(colors["dark3_blue"]) + "; font-size: 22px; font-weight: bold; padding: 3px;") 

    def vidMode(self):
        self.webcamWorker.start()
        print("Vid Mode On!")

    def exit(self):
        self.webcamWorker.stop()
        print("Bye Bye!")


class Webcam(QThread):
    ImageUpdate = Signal(ndarray, float, tuple, tuple, tuple)
    DetectionResult = None

    def run(self):
        self.ThreadActive = True
        Capture = cv2.VideoCapture(0)


        height = int(Capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
        width = int(Capture.get(cv2.CAP_PROP_FRAME_WIDTH))

        offset = width - height
        center_coord = (int(height // 2), int(height // 2))
        ellipse_coord = (int(height // 2), int(height * 0.45))
        axes_length = (int(height * 0.35), int(height * 0.42))


        print(center_coord)

        previous = time()
        while self.ThreadActive:
            ret, frame = Capture.read()
            if ret:
                # Get the current time, increase delta and update the previous variable
                current = time()
                timeElapsed = current - previous
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
                self.ImageUpdate.emit(FlippedImage, timeElapsed, center_coord, ellipse_coord, axes_length)
    def stop(self):
        self.ThreadActive = False
        self.quit()

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
    app = QApplication([])
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
    exit(app.exec())


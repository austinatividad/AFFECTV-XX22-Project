import sys
from PySide6.QtWidgets import QPushButton, QApplication, QVBoxLayout, QHBoxLayout, QLabel, QWidget
from PySide6.QtGui import QPixmap
from PySide6.QtCore import QSize

class MainMenu(QWidget):

    def __init__(self):
        super().__init__()
        #  Image for  Main Menu
        self.bgImage = QPixmap("reservations.png")
        self.bgImage = self.bgImage.scaled(QSize(480, 360))
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

        # Buttons for main menu
        self.startAppButton = QPushButton("Start")
        self.camButton = QPushButton("C")
        self.vidButton = QPushButton("V")
        self.exitAppButton = QPushButton("Quit")

        modeLayout = QHBoxLayout()
        modeLayout.addWidget(self.camButton)
        modeLayout.addWidget(self.vidButton)

        btnLayout  = QVBoxLayout()
        btnLayout.addWidget(self.startAppButton)
        btnLayout.addLayout(modeLayout)
        btnLayout.addWidget(self.exitAppButton)

        # Create layout and add widgets
        layout = QHBoxLayout()
        layout.addWidget(self.screenLabel)
        layout.addLayout(btnLayout)
        # Set dialog layout
        self.setLayout(layout)
        
        # Add button signal to greetings slot
        self.startAppButton.clicked.connect(self.start)
        self.camButton.clicked.connect(self.camMode)
        self.vidButton.clicked.connect(self.vidMode)
        self.exitAppButton.clicked.connect(self.exit)

    # Greets the user
    def start(self):
        print("App Starting Now")

    def camMode(self):
        print("Cam Mode On!")
    
    def vidMode(self):
        print("Vid Mode On!")

    def exit(self):
        print("Bye Bye!")

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


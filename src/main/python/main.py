from fbs_runtime.application_context.PyQt5 import ApplicationContext
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QImage
from functions import blurFunction

import sys

history = []
# QImage or None ->  QImage 
# modifies array of images based on action, returns highest index qimage (to be displayed)
def modifyHistory(image, action):
    if action == "add":
        history.append(image) 
    elif action == "undo":
        history.pop(len(history) - 1)
    elif action == "open":
        history.clear
        history.append(image)
    elif action == "reset":
        while len(history) > 1:
            history.pop(len(history) - 1)
    return curImage()

def curImage():
    if len(history) > 0:        
        latestImage = history[len(history) - 1]
        return latestImage
    else:
        return False

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setWindowTitle("Image Editor")

        self.createMenuBar()
        self.connectActions()
        self.createImageWindow()
        self.createTopGroup()
        #self.createBotGroup()
        
        widget = QWidget()
        mainLayout = QGridLayout()
        mainLayout.addWidget(self.ImageWindow, 0, 0)
        mainLayout.addWidget(self.TopGroup, 3, 0)

        widget.setLayout(mainLayout)
        self.setCentralWidget(widget)
    
    def createMenuBar(self):
        menuBar = self.menuBar()
        self.setMenuBar(menuBar)
        #create menu using QMenu
        fileMenu = QMenu("&File", self)

        self.openaction = QAction("open", self)
        self.openaction.setShortcut("Ctrl+O")
        self.undoaction = QAction("undo", self)
        self.undoaction.setShortcut("Ctrl+Z")
        ################################
        self.bluraction = QAction("blur", self)
        self.bluraction.setShortcut("Ctrl+B")
        #
        self.saveaction = QAction("save", self)
        self.saveaction.setShortcut("Ctrl+S")
        self.exitaction = QAction("exit", self)
        self.exitaction.setShortcut("Alt+F4")

        fileMenu.addAction(self.openaction)
        fileMenu.addAction(self.undoaction)
        fileMenu.addAction(self.saveaction)
        fileMenu.addAction(self.bluraction)
        fileMenu.addSeparator()
        fileMenu.addAction(self.exitaction)

        menuBar.addMenu(fileMenu)
        
    def undo(self):
        # call modify history, remove image in last index of history
        newImage = modifyHistory(None, "undo")
        self.imageHandler(self, newImage, "display")


        # pass this new image to imageHandler to be displayed
        

    def openFile(self):
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getOpenFileName(self,"Select an image", "","Image Files (*.png *.jpg *.bmp)", options=options)
        if fileName:
            imageData = QImage(fileName).convertToFormat(QImage.Format_RGB32)
            self.imageHandler(self, imageData, "open")
    
    @staticmethod
    ## handles modifications/undo, changes history, updates display image
    def imageHandler(self, img, arg_str):
        if img == False:
            return
        if arg_str == "open":
            newImage = modifyHistory(img, "open")
        elif arg_str == "b":
            newImage = blurFunction(img)
            newImage = modifyHistory(newImage, "add")
        elif arg_str == "undo":
            newImage = modifyHistory(img, "undo")
        else:
            newImage = img
        self.displayNewImage(self, newImage)
    
    # QImage -> QPixmap -> void ()
    @staticmethod
    def displayNewImage(self, qimg):
        pixmap = QPixmap.fromImage(qimg)
        self.ImageWindow.setPixmap(pixmap)

  
    def saveFile(self):
        options = QFileDialog.Options()
        #options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getSaveFileName(self,"Save as ...","","Image Files (*.png *.jpg *.bmp)", options=options)
        ## TODO do i need to write file saving logic?
        ## https://pythonprogramming.net/file-saving-pyqt-tutorial/

    def exitFile(self):
        exit_code = appctxt.app.exec()
        sys.exit(exit_code)

    def connectActions(self):
        self.undoaction.triggered.connect(self.undo)
        self.openaction.triggered.connect(self.openFile)
        self.saveaction.triggered.connect(self.saveFile)
        self.exitaction.triggered.connect(self.exitFile)
        # when forward image modification is triggered, call image handler with the 
        # appropriate argument string
        self.bluraction.triggered.connect(lambda:self.imageHandler(self, curImage(), "b"))

    def createImageWindow(self):
        self.ImageWindow = QLabel()
        background = QPixmap('background.png')
        self.ImageWindow.setPixmap(background)
        self.ImageWindow.setScaledContents(True)
        self.setCentralWidget(self.ImageWindow)
        self.resize(background.width(), background.height())
    
    def createTopGroup(self):
        self.TopGroup = QGroupBox("Top Group")
        button1 = QPushButton("Button1")
        button2 = QPushButton("Button2")
        layout = QHBoxLayout()
        layout.addWidget(button1)
        layout.addWidget(button2)
        self.TopGroup.setLayout(layout)

    def createBotGroup(self):
        self.BotGroup = QGroupBox("Bot Group")



if __name__ == '__main__':
    appctxt = ApplicationContext()       # 1. Instantiate ApplicationContext
    window = MainWindow()
    window.resize(800, 800)
    window.show()
    exit_code = appctxt.app.exec()      # 2. Invoke appctxt.app.exec()
    sys.exit(exit_code)


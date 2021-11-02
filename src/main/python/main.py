from fbs_runtime.application_context.PyQt5 import ApplicationContext
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QImage
from functions.py import *

import sys

history = []
# QImage -> void (modifies history state)
# modifies array of images based on action
def modifyHistory(image, action):
    if action == "add":
        history.append(image) 
    elif action == "remove":
        history.pop(len(history) - 1)
    elif action == "open":
        history.clear
        history.append(image)
    elif action == "reset":
        while len(history) > 1:
            history.pop(len(history) - 1)


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
        self.newaction = QAction("new", self)
        self.saveaction = QAction("save", self)
        self.saveaction.setShortcut("Ctrl+S")
        self.exitaction = QAction("exit", self)

        fileMenu.addAction(self.openaction)
        fileMenu.addAction(self.newaction)
        fileMenu.addAction(self.saveaction)
        fileMenu.addSeparator()
        fileMenu.addAction(self.exitaction)

        menuBar.addMenu(fileMenu)
        
    def newFile(self):
        self.centralWidget.setText("<b>File > New</b> clicked")

    def openFile(self):
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getOpenFileName(self,"Select an image", "","Image Files (*.png *.jpg *.bmp)", options=options)
        if fileName:
            pixmap1 = QPixmap(fileName)
            self.ImageWindow.setPixmap(pixmap1)
            
            ## TODO static/global function to store list of images (for undo/reset)
            ## TODO call QImage so that above functions can modify image
            imageData = QImage(fileName)
            self.change_imageData(imageData, "open")
    
    @staticmethod
    def change_imageData(img, arg_str):
        if arg_str == "open":
            modifyHistory(img, "open")
            
        elif arg_str == "b":
            modifyHistory(img, "add")
        print(arg_str)
  
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
        self.newaction.triggered.connect(self.newFile)
        self.openaction.triggered.connect(self.openFile)
        self.saveaction.triggered.connect(self.saveFile)
        self.exitaction.triggered.connect(self.exitFile)

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


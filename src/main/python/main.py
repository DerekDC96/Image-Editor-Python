from fbs_runtime.application_context.PyQt5 import ApplicationContext
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, QObject, QThread, pyqtSignal
from PyQt5.QtGui import QPixmap, QImage
from time import sleep
from functions import arrayToImage, imageToArray, blurFunction, grayscaleFunction

import sys


#https://realpython.com/python-pyqt-qthread/

history = []
# QImage or False ->  void
# modifies array of images based on action
def modifyHistory(image, action):
    if action == "add":
        history.append(image) 
    elif action == "undo":
        if len(history) <= 1:
            return
        else:
            history.pop(len(history) - 1)
    elif action == "open":
        history.clear() 
        history.append(image)
    elif action == "reset":
        while len(history) > 1:
            history.pop(len(history) - 1)
    print(history)
    return 

def curImage():
    if len(history) > 0:        
        latestImage = history[len(history) - 1]
        return latestImage
    else:
        return False

class Worker(QObject):
    finished = pyqtSignal()
    progress = pyqtSignal(int)

    def run(self, arg_str):
        if arg_str == "b":
            #img = arrayToImage(blurFunction(imageToArray(img)))
            #modifyHistory(img, "add")
            img = arrayToImage(grayscaleFunction(imageToArray(curImage())))
            modifyHistory(img, "add")
        elif arg_str == "gray":
            img = arrayToImage(grayscaleFunction(imageToArray(curImage())))
            modifyHistory(img, "add")
        elif arg_str == "undo":
            modifyHistory(False, "undo")  
        self.finished.emit()
        return


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
        modifyHistory(None, "undo")
        self.imageHandler(self, "display")
        
    def openFile(self):  
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getOpenFileName(self,"Select an image", "","Image Files (*.png *.jpg *.bmp)", options=options)
        if fileName:
            img = QImage(fileName).convertToFormat(QImage.Format_RGB32)
            modifyHistory(img, "open")
            self.displayNewImage()


    
    def runImageHandler(self, arg_str):
        #creates separate thread for running imagehandler
        self.thread = QThread()
        self.worker = Worker()
        self.worker.moveToThread(self.thread)
         # Step 5: Connect signals and slots
        self.thread.started.connect(lambda:self.worker.run(arg_str))
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        #self.worker.progress.connect(self.reportProgress)
        # Step 6: Start the thread

        self.thread.start()
        # disable all buttons
        self.button1.setEnabled(False)
        self.button2.setEnabled(False)
        ## enable all buttons and update image
        self.thread.finished.connect(
            lambda:self.displayNewImage()
        )
        self.thread.finished.connect(
            lambda: self.button1.setEnabled(True)
        )
        self.thread.finished.connect(
            lambda: self.button2.setEnabled(True)
        )
        

    def displayNewImage(self):
        if len(history) > 0:
            pixmap = QPixmap.fromImage(curImage())
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
        self.bluraction.triggered.connect(lambda:self.imageHandler(self, "b"))

    def createImageWindow(self):
        self.ImageWindow = QLabel()
        background = QPixmap('background.png')
        self.ImageWindow.setPixmap(background)
        self.ImageWindow.setScaledContents(True)
        self.setCentralWidget(self.ImageWindow)
        self.resize(background.width(), background.height())
    
    def createTopGroup(self):
        self.TopGroup = QGroupBox("Top Group")
        self.button1 = QPushButton("Button1")
        #
        self.button1.clicked.connect(lambda:self.runImageHandler("gray"))#####
        self.button2 = QPushButton("Button2")
        self.button2.clicked.connect(lambda:self.displayNewImage())

        layout = QHBoxLayout()
        layout.addWidget(self.button1)
        layout.addWidget(self.button2)
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


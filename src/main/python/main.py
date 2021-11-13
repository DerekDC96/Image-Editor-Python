from fbs_runtime.application_context.PyQt5 import ApplicationContext
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, QObject, QThread, pyqtSignal
from PyQt5.QtGui import QPixmap, QImage
from time import sleep


import numpy as np
import sys



#https://realpython.com/python-pyqt-qthread/

history = []
# numpy array (RGBA) or False ->  void
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
    return 

## returns arra of RGBA
def curImage():
    if len(history) > 0:        
        latestImage = history[len(history) - 1]
        return latestImage
    else:
        return False

class Worker(QObject):
    from functions import arrayToImage, imageToArray, blurFunction, grayscaleFunction, redtintFunction, evilFunction, outlineFunction
    finished = pyqtSignal()
    progress = pyqtSignal(int)

    def run(self, arg_str):
        if arg_str == "blur":
            img = self.blurFunction(curImage())
            modifyHistory(img, "add")
        elif arg_str == "gray":
            img = self.grayscaleFunction(curImage())
            modifyHistory(img, "add")
        elif arg_str == "undo":
            modifyHistory(False, "undo")  
        elif arg_str == "reset":
            modifyHistory(False, "reset")
        elif arg_str == "redtint":
            img = self.redtintFunction(curImage())
            modifyHistory(img, "add")
        elif arg_str == "evil":
            img = self.evilFunction(curImage())
            modifyHistory(img, "add")
        elif arg_str == "outline":
            img = self.outlineFunction(curImage())
            modifyHistory(img, "add")
        self.finished.emit()
        return
    
    

class MainWindow(QMainWindow):
    from functions import arrayToImage, imageToArray
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)    
        self.setWindowTitle("Image Editor")

        self.createMenuBar()
        self.connectActions()
        self.createImageWindow()
        self.createTopGroup()

        self.pbar = QProgressBar(self)
        self.pbar.setGeometry(30, 40, 200, 25)

        #self.createBotGroup()
        
        widget = QWidget()
        mainLayout = QGridLayout()
        mainLayout.addWidget(self.ImageWindow, 0, 0)
        mainLayout.addWidget(self.TopGroup, 3, 0)
        mainLayout.addWidget(self.pbar, 4, 0)

        widget.setLayout(mainLayout)
        self.setCentralWidget(widget)
    
    def runImageHandler(self, arg_str):
        # separate thread for running imagehandler
        self.thread = QThread()
        self.worker = Worker()
        self.worker.moveToThread(self.thread)
         # Step 5: Connect signals and slots
        self.thread.started.connect(lambda:self.worker.run(arg_str))
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        self.worker.progress.connect(self.reportProgress)
        
        # Step 6: Start the thread
        self.thread.start()

        # disable all buttons
        self.button1.setEnabled(False)
        self.button2.setEnabled(False)
        self.button3.setEnabled(False)
        self.button4.setEnabled(False)
        self.button5.setEnabled(False)
        self.button6.setEnabled(False)
        self.button7.setEnabled(False)
        self.button8.setEnabled(False)
        self.button9.setEnabled(False)
        self.button10.setEnabled(False)

        # enable all buttons, update image, reset progress bar
        self.thread.finished.connect(lambda: self.displayNewImage())
        self.thread.finished.connect(lambda: self.reportProgress(0))

        if hasattr(curImage(), "__len__"):
            # handles edge cases for undo and reset
            self.thread.finished.connect(lambda: self.button1.setEnabled(True))
            self.thread.finished.connect(lambda: self.button2.setEnabled(True))
            self.thread.finished.connect(lambda: self.button3.setEnabled(True))
            self.thread.finished.connect(lambda: self.button4.setEnabled(True))
            self.thread.finished.connect(lambda: self.button5.setEnabled(True))
            self.thread.finished.connect(lambda: self.button6.setEnabled(True))
            self.thread.finished.connect(lambda: self.button7.setEnabled(True))
            self.thread.finished.connect(lambda: self.button8.setEnabled(True))
            self.thread.finished.connect(lambda: self.button9.setEnabled(True))
            self.thread.finished.connect(lambda: self.button10.setEnabled(True))
        
    def reportProgress(self, n):
        self.pbar.setValue(n)
        
    def displayNewImage(self):
        if len(history) > 0:
            pixmap = QPixmap.fromImage(self.arrayToImage(curImage()))
            self.ImageWindow.setPixmap(pixmap)
    
    def openFile(self):  
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getOpenFileName(self,"Select an image", "","Image Files (*.png *.jpg *.bmp)", options=options)
        if fileName:
            img = self.imageToArray(QImage(fileName).convertToFormat(QImage.Format_RGB32))
            modifyHistory(img, "open")
            self.displayNewImage()
            self.setWindowTitle("Image Editor                  " + fileName)
            self.button1.setEnabled(True)
            self.button2.setEnabled(True)
            self.button3.setEnabled(True)
            self.button4.setEnabled(True)
            self.button5.setEnabled(True)
            self.button6.setEnabled(True)
            self.button7.setEnabled(True)
            self.button8.setEnabled(True)
            self.button9.setEnabled(True)
            self.button10.setEnabled(True)

    def saveFile(self):
        img = self.arrayToImage(curImage())
        if not False == img:
            options = QFileDialog.Options()
            fileName, _ = QFileDialog.getSaveFileName(self,"Save as ...","","Image Files (*.png *.jpg *.bmp)", options=options)
            img.save(fileName)

    def exitFile(self):
        exit_code = appctxt.app.exec()
        sys.exit(exit_code)

    def connectActions(self):
        self.openaction.triggered.connect(self.openFile)
        self.saveaction.triggered.connect(self.saveFile)
        self.exitaction.triggered.connect(self.exitFile)
        self.undoaction.triggered.connect(lambda:self.runImageHandler("undo"))
        self.resetaction.triggered.connect(lambda:self.runImageHandler("reset"))

    def createMenuBar(self):
        menuBar = self.menuBar()
        self.setMenuBar(menuBar)
        #create menu using QMenu
        fileMenu = QMenu("&File", self)

        self.openaction = QAction("open", self)
        self.openaction.setShortcut("Ctrl+O")
        self.undoaction = QAction("undo", self)
        self.undoaction.setShortcut("Ctrl+Z")
        self.saveaction = QAction("save", self)
        self.saveaction.setShortcut("Ctrl+S")
        self.exitaction = QAction("exit", self)
        self.exitaction.setShortcut("Alt+F4")
        self.resetaction = QAction("reset", self)
        self.resetaction.setShortcut("Ctrl+R")

        fileMenu.addAction(self.openaction)
        fileMenu.addAction(self.undoaction)
        fileMenu.addAction(self.saveaction)
        fileMenu.addAction(self.resetaction)
        fileMenu.addSeparator()
        fileMenu.addAction(self.exitaction)

        menuBar.addMenu(fileMenu)

    def createImageWindow(self):
        self.ImageWindow = QLabel()
        background = QPixmap('background.png')
        self.ImageWindow.setPixmap(background)
        self.ImageWindow.setScaledContents(True)
        self.setCentralWidget(self.ImageWindow)
        self.resize(background.width(), background.height())
    
    

    def createTopGroup(self):
        self.TopGroup = QGroupBox("Top Group")
        self.button1 = QPushButton("Grayscale")
        self.button1.clicked.connect(lambda:self.runImageHandler("gray"))
        self.button2 = QPushButton("Blur")
        self.button2.clicked.connect(lambda:self.runImageHandler("blur"))
        self.button3 = QPushButton("Undo")
        self.button3.clicked.connect(lambda:self.runImageHandler("undo"))
        self.button4 = QPushButton("Red Tint")
        self.button4.clicked.connect(lambda:self.runImageHandler("redtint"))
        self.button5 = QPushButton("Invert Color")
        self.button5.clicked.connect(lambda:self.runImageHandler("evil"))
        self.button6 = QPushButton("Outline")
        self.button6.clicked.connect(lambda:self.runImageHandler("outline"))
        self.button7 = QPushButton("Evil")
        self.button7.clicked.connect(lambda:self.runImageHandler("evil"))
        self.button8 = QPushButton("Evil")
        self.button8.clicked.connect(lambda:self.runImageHandler("evil"))
        self.button9 = QPushButton("Evil")
        self.button9.clicked.connect(lambda:self.runImageHandler("evil"))
        self.button10 = QPushButton("Evil")
        self.button10.clicked.connect(lambda:self.runImageHandler("evil"))

        self.button1.setEnabled(False)
        self.button2.setEnabled(False)
        self.button3.setEnabled(False)
        self.button4.setEnabled(False)
        self.button5.setEnabled(False)
        self.button6.setEnabled(False)
        self.button7.setEnabled(False)
        self.button8.setEnabled(False)
        self.button9.setEnabled(False)
        self.button10.setEnabled(False)

        layout = QHBoxLayout()
        layout.addWidget(self.button1)
        layout.addWidget(self.button2)
        layout.addWidget(self.button3)
        layout.addWidget(self.button4)
        layout.addWidget(self.button5)
        layout.addWidget(self.button6)
        layout.addWidget(self.button7)
        layout.addWidget(self.button8)
        layout.addWidget(self.button9)
        layout.addWidget(self.button10)

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


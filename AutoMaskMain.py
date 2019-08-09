import sys
import os
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QFileDialog, QWidget, QMessageBox
from Ui_AutoMask import Ui_QWidget
from PyQt5.QtCore import pyqtSignal , Qt, QObject, QTimer, QThread
from PyQt5.QtGui import QTextCursor
from auto_mask_pattern import mask_process

class Stream(QObject):
    newText=pyqtSignal(str)
    
    def write(self, text):
        self.newText.emit(str(text))

class Worker(QThread):
    global faillogName
    global inputName
    global outputName
    def __init__(self, parent=None):
        super(Worker, self).__init__(parent)
    def __del__(self):
        self.wait()
    def run(self):
        mask_process(self.faillogName,self.inputName, self.outputName)

class MyUiProcess(QWidget,Ui_QWidget ):
    def __init__(self, parent=None):    
        super(MyUiProcess, self).__init__(parent)
        self.setupUi(self)
        self.faillogName=''
        self.inputName=''
        self.outputName=''
        self.progress=0
        self.working=False
        self.faillogButton.clicked.connect(self.getfaillogFile)
        self.inputButton.clicked.connect(self.getinputFile)
        self.outputButton.clicked.connect(self.getoutputFile)
        self.maskButton.clicked.connect(self.maskPattern)
        self.exitButton.clicked.connect(self.sysExit)
        self.aboutButton.clicked.connect(self.aboutInfor)
        sys.stdout = Stream(newText=self.onUpdateText)
        self.thread=Worker()
        self.timer=QTimer(self)
        self.timer.timeout.connect(self.refreshProgress)
        self.timer.start(100) #100ms
   
    def onUpdateText(self, text):
        cursor = self.outputBrowser.textCursor()
        cursor.movePosition(QTextCursor.End)
        cursor.insertText(text)
        self.outputBrowser.setTextCursor(cursor)
        self.outputBrowser.ensureCursorVisible()
        
    def getfaillogFile(self):
        self.faillogName, faillogType=QFileDialog.getOpenFileName(self, "Choose file", "./","All Files (*);;Text Files (*.txt)" )
        if self.faillogName is not None:
                self.faillogEdit.setText(self.faillogName)
                
    def getinputFile(self):
        self.inputName, inputType=QFileDialog.getOpenFileName(self, "Choose file", "./","All Files (*);;Text Files (*.txt)" )
        if self.inputName is not None:
                self.inputEdit.setText(self.inputName)   
    
    def getoutputFile(self):
        self.outputName, outputType=QFileDialog.getSaveFileName(self, "Choose file", "./","ATP Files (*.atp);;Text Files (*.txt)" )
        if self.outputName is not None:
                self.outputEdit.setText(self.outputName)
                outputFile=open(self.outputName, 'w')
                outputFile.close()
    
    def maskPattern(self):
        self.thread.faillogName=self.faillogName
        self.thread.inputName=self.inputName
        self.thread.outputName=self.outputName
        self.thread.start()
    
    def refreshProgress(self):
        if self.faillogName == '':
            self.statusLabel.setText('No fail log!')
        elif self.inputName == '':
            self.statusLabel.setText('No input ATP file!')
        elif self.outputName == '':
            self.statusLabel.setText('No output ATP file!')
        elif self.progress >= 100:
            self.statusLabel.setText('Mask successfully!')
        elif (self.progress >0) and (self.progress<100) :
            self.statusLabel.setText('Runing!')
        else:
            self.statusLabel.setText('Ready!')
        if (self.inputName !='') and (self.outputName !='') :
            iuputSize=os.path.getsize(self.inputName)
            outputSize=os.path.getsize(self.outputName)
            self.progress=round(outputSize/iuputSize*100, 2)
            self.progressBar.setValue(self.progress)
    
    def sysExit(self):
        sys.exit(0)
        
    def aboutInfor(self):
        QMessageBox.about(self,'Author','ethan.lv@teradyne.com')
        
    def __del__(self):
        sys.stdout = sys.__stdout__
if __name__ == "__main__":
    try:
        app = QtWidgets.QApplication(sys.argv)
        ui = MyUiProcess()
        ui.show()
        sys.exit(app.exec_())
    except Exception as e:
        print(e)

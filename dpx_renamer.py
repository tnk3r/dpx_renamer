#!/usr/bin/python
from PyQt4.QtGui import QMainWindow, QApplication, QFileDialog, QDialog, QPushButton, QLabel
from PyQt4.QtCore import QString
import os, sys
controller = QApplication(sys.argv)

class window(QMainWindow):
    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent=None)
        self.files = str(QFileDialog.getExistingDirectory(self, "Select Directory containing Resolve DPX stills"))
        self.Error = QString("")
        self.process_stills()
        sys.exit(0)

    def showdialog(self):
        d = QDialog(self)
        d.setFixedSize(300, 100)
        label = QLabel(self.Error, d)
        label.move(20, 20)
        b1 = QPushButton("Ok",d)
        b1.move(125,50)
        d.setWindowTitle("Error !")
        b1.clicked.connect(controller.quit)
        d.exec_()

    def process_stills(self):
        os.chdir(self.files)
        drx_files, stills, processed = [], [], []
        print self.files
        for x in os.listdir(self.files):
            if ".drx" in x:
                drx_files.append(x)
            else:
                stills.append(x)

        for drx in drx_files:
            for line in open(str(self.files)+"/"+drx).readlines():
                if "SrcTC" in line:
                    tc = line.replace(">", "<").split("<")[2].replace(":", "-")
            counter = 1
            for still in stills:
                if still.replace(".dpx", "") == drx.replace(".drx", ""):
                    with open(str(self.files)+"/"+still) as f:
                        head = f.read(4)
                        if "SDPX" in head:
                            f.seek(2900)
                            new = f.read(24).strip().split(".")
                            newName = str(new[0])+"_"+str(tc)
                            if newName+".dpx" in processed:
                                newName = newName+"_"+str(counter)
                                counter+=1
                                processed.append(newName+".dpx")
                            else:
                                processed.append(newName+".dpx")
                                counter = 1
                            try:
                                command = "mv "+str(still.replace("dpx", "drx"))+" "+newName+".drx"
                                print command
                                os.system(str(command))
                                command2 = "mv "+str(stills[stills.index(still)])+" "+newName+".dpx"
                                os.system(str(command2))
                            except StandardError as msg:
                                self.Error.swap("Something is wrong with the Selected Stills")
                                self.showdialog()

main = window()
main.show()
main.raise_()
sys.exit(controller.exec_())

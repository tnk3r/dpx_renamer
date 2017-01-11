#!/usr/bin/python
from PyQt4.QtGui import QMainWindow, QApplication, QFileDialog
import os, sys
controller = QApplication(sys.argv)

class window(QMainWindow):
    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent=None)
        self.files = str(QFileDialog.getExistingDirectory(self, "Select Directory containing Resolve DPX stills"))
        self.process_stills()
        sys.exit(0)

    def process_stills(self):
        os.chdir(self.files)
        drx_files, stills, processed = [], [], []
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
                                os.system("mv "+str(still.replace("dpx", "drx"))+" "+newName+".drx")
                                os.system("mv "+str(stills[stills.index(still)])+" "+newName+".dpx")
                            except StandardError as msg:
                                print "Error: "+str(msg)

main = window()
main.show()
main.raise_()
sys.exit(controller.exec_())

import os, sys, json, re
from PyQt6 import QtWidgets, uic
from PyQt6.QtWidgets import QMessageBox
from events2pdfMW import Ui_MainWindow
from events2pdf import *

CONFIG_FILE = "events2pdf_conf.json"
DEFAULT_CONFIG_FILE = "events2pdf_default_conf.json"

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):

    def showMessage(self, text):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Icon.Information)
       
        msg.setText(text)
        #msg.setInformativeText("This is additional information")
        msg.setWindowTitle("Events2PDF")
        #msg.setDetailedText("The details are as follows:")
        msg.setStandardButtons(QMessageBox.StandardButton.Ok)
        #msg.buttonClicked.connect(msgbtn)
        msg.exec()

    def load_gui(self):
        self.source_lineEdit.setText(self.conf["minput"])
        self.outputFileName_lineEdit.setText(self.conf["moutput"] ) 
        self.coverPage_lineEdit.setText(self.conf["mcover_page"] )
        self.orient_comboBox.setCurrentText(self.conf ["mpage_orientation"] )
        self.psize_comboBox.setCurrentText(self.conf ["mpage_size"])
        self.font_comboBox.setCurrentText(self.conf["mfont"] )
        self.fontSize_spinBox.setValue(self.conf["mfont_size"] )
        self.frame_count_spinBox.setValue(self.conf["mframe_count"] )
        self.pageMargin_doubleSpinBox.setValue(self.conf["mpage_margin"] )
        self.no_cols_spinBox.setValue(self.conf["mcols"] )
        self.col_widths_lineEdit.setText(f'{" ".join(str(x) for x in [x for x in self.conf[ "mcol_widths"]])}')
        
    def reset_conf(self):
        try:
            self.conf = json.load(open(DEFAULT_CONFIG_FILE))
        except Exception as err:
             self.showMessage(f"cannot load default config file {DEFAULT_CONFIG_FILE}: {err}")
            
        self.load_gui()
        
    def save_conf(self):
        self.conf["minput"] = self.source_lineEdit.text()
        self.conf["moutput"] = self.outputFileName_lineEdit.text()
        self.conf["mcover_page"] = self.coverPage_lineEdit.text()
        self.conf ["mpage_orientation"] = self.orient_comboBox.currentText()
        self.conf ["mpage_size"] = self.psize_comboBox.currentText()
        self.conf["mfont"] = self.font_comboBox.currentText()
        self.conf["mfont_size"] = self.fontSize_spinBox.value()
        self.conf["mframe_count"] = self.frame_count_spinBox.value()
        self.conf["mpage_margin"] = self.pageMargin_doubleSpinBox.value()
        self.conf["mcols"] = self.no_cols_spinBox.value()
        self.conf[ "mcol_widths"] = [int(x) for x in self.col_widths_lineEdit.text().split(' ') ]
        
        try:
            json.dump(self.conf, open(CONFIG_FILE, "w"), indent=4)
        except Exception as err:
             self.showMessage(f"cannot save config file {CONFIG_FILE}: {err}")
            
    def create_pdf(self):
        self.conf["minput"] = self.source_lineEdit.text()
        self.conf["moutput"] = self.outputFileName_lineEdit.text()
        self.conf["mcover_page"] = self.coverPage_lineEdit.text()
        self.conf ["mpage_orientation"] = self.orient_comboBox.currentText()
        self.conf ["mpage_size"] = self.psize_comboBox.currentText()
        self.conf["mfont"] = self.font_comboBox.currentText()
        self.conf["mfont_size"] = self.fontSize_spinBox.value()
        self.conf["mframe_count"] = self.frame_count_spinBox.value()
        self.conf["mpage_margin"] = self.pageMargin_doubleSpinBox.value()
        self.conf["mcols"] = self.no_cols_spinBox.value()
        self.conf[ "mcol_widths"] = [int(x) for x in self.col_widths_lineEdit.text().split(' ') ]
        events2pdf_sub(self.conf)
        self.showMessage(f'{self.conf["moutput"]} created')

        
    def __init__(self, *args, obj=None, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        
        try:                 
            self.conf = json.load(open(CONFIG_FILE))
        except Exception as err:
             self.showMessage(f"get_config: error loading config file {CONFIG_FILE}: {err}")
            
        self.setupUi(self)
        for x in self.conf["mfonts"]:
            self.font_comboBox.addItem(x)
        self.load_gui()        
        self.save_pushButton.pressed.connect(self.save_conf)
        self.create_pushButton.pressed.connect(self.create_pdf)
        self.reset_pushButton.pressed.connect(self.reset_conf)

app = QtWidgets.QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()
from PyQt5.QtWidgets import QWidget, QPushButton, QLineEdit, QComboBox, QTextEdit
from PyQt5.QtCore import pyqtSlot

from lib.traitement import filter_edt

class App(QWidget):

    def __init__(self, df_param_salle,df_param_pr,df_data):
        super().__init__()
        self.title = 'Emploi du temps'
        self.left = 100
        self.top = 100
        self.width = 1280
        self.height = 960
        
        #Propriétés de paramétrage
        self.df_param_salle=df_param_salle
        self.df_param_pr=df_param_pr
        self.df_data=df_data

        self.initUI()
        
    def initUI(self):
        #Fenetre
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        
		#Combobox prof/salle
        self.cb_filtre = QComboBox(self)
        self.cb_filtre.addItems(["Professeur", "Salle"])
        self.cb_filtre.move(20, 20)
        self.cb_filtre.resize(150,30)
        self.cb_filtre.currentIndexChanged.connect(self.selectionchange)
		
		#Combobox pr/salle
        self.cb_pr_salle = QComboBox(self)
        self.cb_pr_salle.move(20, 80)
        self.cb_pr_salle.resize(280,40)
        self.cb_pr_salle.addItems(self.df_param_pr) 
		
		#Textbox période validité
        self.box_dt_deb = QLineEdit(self)
        self.box_dt_deb.move(320, 80)
        self.box_dt_deb.resize(280,40)
        self.box_dt_deb.setPlaceholderText("Début période validité - ex : 2020-01-01")
        self.box_dt_fin = QLineEdit(self)
        self.box_dt_fin.move(620, 80)
        self.box_dt_fin.resize(280,40)
        self.box_dt_fin.setPlaceholderText("Fin période validité - ex : 2020-01-07")
        
        self.result = QTextEdit(self)
        self.result.move(20, 200)
        self.result.resize(960,680)
        
		#Boutton validation
        button = QPushButton("Filtrer", self)
        button.move(400,150)
        button.clicked.connect(self.on_click)
		
        self.show()
		
    @pyqtSlot()
    def on_click(self):
        df = filter_edt(self.df_data,self.cb_filtre.currentText(),self.cb_pr_salle.currentText(),self.box_dt_deb.text(),self.box_dt_fin.text())
        self.result.setText(df.to_string())
		
    def selectionchange(self,i):
        self.cb_pr_salle.clear()
        if self.cb_filtre.itemText(i)=="Salle": self.cb_pr_salle.addItems(self.df_param_salle)
        if self.cb_filtre.itemText(i)=="Professeur": self.cb_pr_salle.addItems(self.df_param_pr)
import pandas as pd

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLineEdit, QComboBox, QTextEdit
from PyQt5.QtCore import pyqtSlot

class App(QWidget):

    def __init__(self):
        super().__init__()
        self.title = 'Emploi du temps'
        self.left = 100
        self.top = 100
        self.width = 1280
        self.height = 960
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
        self.cb_pr_salle.addItems(df_param_pr) 
		
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
        df = filter_edt(df_union,self.cb_filtre.currentText(),self.cb_pr_salle.currentText(),self.box_dt_deb.text(),self.box_dt_fin.text())
        self.result.setText(df.to_string())
		
    def selectionchange(self,i):
        self.cb_pr_salle.clear()
        if self.cb_filtre.itemText(i)=="Salle":
            self.cb_pr_salle.addItems(df_param_salle)
        if self.cb_filtre.itemText(i)=="Professeur":
            self.cb_pr_salle.addItems(df_param_pr)

def filter_edt(df,col,pf_name,deb_valid,fin_valid):
	if (deb_valid=="" or deb_valid==""): 
		df_final = df[(df[col] == pf_name) & (df.Debut_validite.isnull() | df.Fin_validite.isnull())].sort_values(by=["Jour","Heure debut"])
	else :
		df_final = df[(df[col] == pf_name) & (df.Debut_validite.isnull() | df.Fin_validite.isnull() | ((df['Debut_validite'] <= fin_valid) & (df['Fin_validite'] >= deb_valid)))].sort_values(by=["Jour","Heure debut"])		
	return df_final



if __name__ == '__main__':
	#Ouvrir les données
	df_cours = pd.read_excel("data/data-edt.xlsx",sheet_name="CoursHebdo", header=0)
	df_reservation = pd.read_excel("data/data-edt.xlsx",sheet_name="Reservations", header=0).rename(columns = {"Nom réservation":"Cours"})
	df_union = df_cours.append(df_reservation)
	
	#Ouvrir le paramétrage de sélection
	df_param_pr = pd.read_excel("data/data-edt.xlsx",sheet_name="ListeProfesseurs", header=0).sort_values(by=["Professeur"]).Professeur.tolist()
	df_param_salle = pd.read_excel("data/data-edt.xlsx",sheet_name="ListeSalles", header=0).sort_values(by=["Salle"]).Salle.tolist()
	
	#GUI
	app = QApplication(sys.argv)
	ex = App()
	sys.exit(app.exec_())


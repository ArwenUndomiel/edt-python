import pandas as pd

from PyQt5.QtWidgets import QApplication
from lib.gui import App

import sys

if __name__ == '__main__':
	#Ouvrir les données
    df_cours = pd.read_excel("data/data-edt.xlsx",sheet_name="CoursHebdo", header=0)
    df_reservation = pd.read_excel("data/data-edt.xlsx",sheet_name="Reservations", header=0).rename(columns = {"Nom réservation":"Cours"})
    df_union = df_cours.append(df_reservation)

    #Ouvrir le paramétrage de sélection
    df_param_pr = pd.read_excel("data/data-edt.xlsx", sheet_name="ListeProfesseurs", header=0).sort_values(by=["Professeur"]).Professeur
    df_param_salle = pd.read_excel("data/data-edt.xlsx", sheet_name="ListeSalles", header=0).sort_values(by=["Salle"]).Salle
    df_param_jour = pd.read_excel("data/data-edt.xlsx", sheet_name="ListeJours", header=0).sort_values(by=["Jour"]).Jour
	
	#GUI
    app = QApplication(sys.argv)
    ex = App(df_param_salle, df_param_pr, df_param_jour, df_union)
    sys.exit(app.exec_())


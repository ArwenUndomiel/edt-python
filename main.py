""" Ce programme propose d'afficher
1) Les salles disponibles en fonction du créneau demander et la fréquence demandée
2) L'emploi du temps par professeur ou par salle
@param : chemin contenant les données
"""

import sys
import argparse
import pandas as pd

from PyQt5.QtWidgets import QApplication
from lib.gui import App

if __name__ == '__main__':
    #Initialisation du fichier de données
    parser = argparse.ArgumentParser(description='Description des arguments')
    parser.add_argument('path', type=str, help='Chemin vers les données')
    args = parser.parse_args()
    data_file = args.path

    #Ouvrir les données
    df_cours = pd.read_excel(data_file,sheet_name="CoursHebdo", header=0)
    df_reservation = pd.read_excel(data_file,sheet_name="Reservations", header=0)\
                        .rename(columns = {"Nom réservation":"Cours"})
    df_union = df_cours.append(df_reservation)

    #Ouvrir le paramétrage de sélection
    df_param_pr = pd.read_excel(data_file, sheet_name="ListeProfesseurs", header=0)\
                        .sort_values(by=["Professeur"]).Professeur
    df_param_salle = pd.read_excel(data_file, sheet_name="ListeSalles", header=0)\
                        .sort_values(by=["Salle"]).Salle
    df_param_jour = pd.read_excel(data_file, sheet_name="ListeJours", header=0)\
                        .sort_values(by=["Jour"]).Jour

	#GUI
    app = QApplication(sys.argv)
    ex = App(df_param_salle, df_param_pr, df_param_jour, df_union)
    sys.exit(app.exec_())

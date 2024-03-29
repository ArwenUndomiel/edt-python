"""
	Interface graphique de l'application
"""
from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QGridLayout, QWidget, QTabWidget, \
        QPushButton, QLineEdit, QComboBox, QTextEdit
from PyQt5.QtCore import pyqtSlot

from lib.traitement import filter_edt, dispo_salle

class App(QMainWindow):
    '''
        #Classe générale de l'application
    '''
    def __init__(self, df_param_salle, df_param_pr, df_jour, df_data):
        '''
            Constructeur de l'application
            @param : df_param_salle (df des salles existantes), df_param_pr (df des professeurs),
            df_jour (df des jours), df_data (df des données de l'emploi du temps)
        '''
        super().__init__()
        self.title = 'Emploi du temps'
        self.left = 100
        self.top = 100
        self.width = 1280
        self.height = 960
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.table_widget = MyTableWidget(self, df_param_salle, df_param_pr.tolist(),\
                            df_jour.tolist(), df_data)
        self.setCentralWidget(self.table_widget)

        self.show()

class MyTableWidget(QWidget):
    '''
    Classe onglet
        1) Définit le contenu graphique de chaque onglet de l'application
        2) Définit les actions lancées par l'utilisateur depuis l'ui
    '''

    def __init__(self, parent, df_param_salle, df_param_pr, df_jour, df_data):
        '''
            Constructeur des onglets
            @param : df_param_salle (df des salles existantes), df_param_pr (df des professeurs),
            df_jour (df des jours), df_data (df des données de l'emploi du temps)
        '''
        super(QWidget, self).__init__(parent)
        self.layout = QVBoxLayout(self)

		#Propriétés de paramétrage
        self.df_param_salle=df_param_salle
        self.df_param_pr=df_param_pr
        self.df_data=df_data
        self.df_jour=df_jour

        # Initialize tab screen
        self.tabs = QTabWidget()
        self.tab1 = QWidget()
        self.tab2 = QWidget()
        self.tabs.resize(300,200)

        # Add tabs
        self.tabs.addTab(self.tab1,"Affichage EDT")
        self.tabs.addTab(self.tab2,"Disponibilité Salle")

        # Design first tab
        self.init_t1_ui(self.tab1)
        self.init_t2_ui(self.tab2)

        # Add tabs to widget
        self.layout.addWidget(self.tabs)

    def init_t1_ui(self,tab):
        '''
            Initialise l'onglet 1
            @param : onglet 1
        '''
        self.tab = tab
        layout = QGridLayout(self)

		#Combobox prof/salle
        self.cb_filtre = QComboBox(self)
        self.cb_filtre.addItems(["Professeur", "Salle"])
        self.cb_filtre.currentIndexChanged.connect(self.selectionchange)
        layout.addWidget(self.cb_filtre, 1, 1, 1, 1)

        #Combobox pr/salle
        self.cb_pr_salle = QComboBox(self)
        self.cb_pr_salle.addItems(self.df_param_pr)
        layout.addWidget(self.cb_pr_salle, 2, 1, 1, 1)

        #Textbox période validité
        self.box_dt_deb = QLineEdit(self)
        self.box_dt_deb.setPlaceholderText("Début période validité - ex : 2020-01-01")
        layout.addWidget(self.box_dt_deb, 2, 2, 1, 1)
        self.box_dt_fin = QLineEdit(self)
        self.box_dt_fin.setPlaceholderText("Fin période validité - ex : 2020-01-07")
        layout.addWidget(self.box_dt_fin, 2, 3, 1, 1)

        #Résultat
        self.result = QTextEdit(self)
        layout.addWidget(self.result, 4, 1, 5, 3)

        #Boutton validation
        self.button = QPushButton("Filtrer", self)
        layout.addWidget(self.button, 3, 1, 1, 1)
        self.button.clicked.connect(self.on_click_t1)

        self.tab.setLayout(layout)
        self.show()

    def init_t2_ui(self,tab):
        '''
            Initialise l'onglet 2
            @param : onglet 2
        '''
        self.tab = tab
        layout = QGridLayout(self)

        #Combobox jour
        self.cb_jour = QComboBox(self)
        self.cb_jour.addItems(self.df_jour)
        layout.addWidget(self.cb_jour, 2, 1, 1, 1)

        #Textbox période validité
        self.box_dt_deb_t2 = QLineEdit(self)
        self.box_dt_deb_t2.setPlaceholderText("Début période validité - ex : 2020-01-01")
        layout.addWidget(self.box_dt_deb_t2, 2, 2, 1, 1)
        self.box_dt_fin_t2 = QLineEdit(self)
        self.box_dt_fin_t2.setPlaceholderText("Fin période validité - ex : 2020-01-07")
        layout.addWidget(self.box_dt_fin_t2, 2, 3, 1, 1)

        #Textbox créneau
        self.box_cren_deb = QLineEdit(self)
        self.box_cren_deb.setPlaceholderText("Début du créneau - ex : 20:00")
        layout.addWidget(self.box_cren_deb, 3, 2, 1, 1)
        self.box_cren_fin = QLineEdit(self)
        self.box_cren_fin.setPlaceholderText("Fin du créneau - ex : 21:00")
        layout.addWidget(self.box_cren_fin, 3, 3, 1, 1)

        #Affichage résultat
        self.result_t2 = QTextEdit(self)
        layout.addWidget(self.result_t2, 5, 1, 4, 3)

        #Boutton validation
        self.button = QPushButton("Filtrer", self)
        layout.addWidget(self.button, 4, 1, 1, 1)
        self.button.clicked.connect(self.on_click_t2)

        self.tab.setLayout(layout)
        self.show()

    @pyqtSlot()
    def on_click_t1(self):
        '''
            Réaction à un clic sur le bouton de l'onglet 1
        '''
        df_res = filter_edt(self.df_data,self.cb_filtre.currentText(),self.cb_pr_salle.currentText(),\
                        self.box_dt_deb.text(),self.box_dt_fin.text())
        if df_res.empty:
            self.result.setText("Pas de cours")
        else:
            self.result.setText(df_res.to_string(index=False))

    @pyqtSlot()
    def on_click_t2(self):
        '''
            Réaction à un clic sur le bouton de l'onglet 2
        '''
        df_res = dispo_salle(self.df_data, self.df_param_salle, self.cb_jour.currentText(),\
                        self.box_dt_deb_t2.text(), self.box_dt_fin_t2.text(),\
						self.box_cren_deb.text(), self.box_cren_fin.text())
        if df_res.empty:
            self.result_t2.setText("Pas de salle disponible")
        else:
            self.result_t2.setText(df_res.to_string(index=False))

    def selectionchange(self,i):
        '''
            Réaction à un clic sur la liste de choix pr/salle dans l'onglet 1
        '''
        self.cb_pr_salle.clear()
        if self.cb_filtre.itemText(i)=="Salle":
            self.cb_pr_salle.addItems(self.df_param_salle.tolist())
        if self.cb_filtre.itemText(i)=="Professeur":
            self.cb_pr_salle.addItems(self.df_param_pr)

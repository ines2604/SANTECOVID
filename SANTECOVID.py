import sys
import csv
import glob
import datetime
from pathlib import Path
import re
import os
from PyQt5.QtWidgets import QFrame,QSizePolicy,QSpacerItem,QTableWidget,QDialog,QDesktopWidget,QStyleFactory,QDialog,QDialogButtonBox,QApplication, QMainWindow, QAction, QMenu ,QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox, QComboBox
from PyQt5 import QtWidgets ,QtGui ,QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor,QPalette,QPixmap,QIcon,QFont
from PyQt5.QtWidgets import QTableWidgetItem
from PyQt5.QtWidgets import QHBoxLayout
def calculer_pourcentage_maladie(code_maladie):
    total_maladies = len(maladie_dict)
    occurrences_maladie = 0
    for cle, val in maladie_dict.items():
        if val['nom maladie'] == code_maladie:
            occurrences_maladie += 1
    # Calculate percentage
    if(occurrences_maladie ==0):
        return 0
    else:
        pourcentage = (occurrences_maladie / total_maladies) * 100
        return pourcentage
def chercher_personne_par_age(age,personne_dict):
    result = {}
    for k, v in personne_dict.items():
        if v.get('age') == age:
            result[k] = v
    return result
def chercher_personne_non_decedes(personne_dict):
    result = {}
    for k, v in personne_dict.items():
        if v.get('decédé') == "0":
            result[k] = v
    return result
def chercher_personne_decedes(personne_dict):
    result = {}
    for k, v in personne_dict.items():
        if v.get('decédé') == "1":
            result[k] = v
    return result
def chercher_personne_par_nationalite(nationalite,personne_dict):
    result = {}
    for k, v in personne_dict.items():
        if v.get('nationalité') == nationalite:
            result[k] = v
    return result
def chercher_personne_par_numero_telephone(numero_telephone, personne_dict):
    result = {}
    for k, v in personne_dict.items():
        if v.get('numéro_telephone') == numero_telephone:
            result[k] = v
    return result
def contenu_dictionnaire(dictionnaire):
    return dictionnaire.items()
def aff_dic(x):
    result = ""
    for cle, val in x:
        result += f"numéro de carte d'identité: {cle}, {val}\n"
    return result
def existe(d,x):
    for k in d.keys():
        if k==x:
            return True
    return False
personne_dict = {}
maladie_dict = {}
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        font = QFont()
        font.setFamily("arial")
        font.setPointSize(14)
        font.setBold(True)  # make the font bold
        # Appliquez la police personnalisée à l'application
        self.setFont(font)
        self.changeTheme()
        menubar = self.menuBar()
        personne_menu = menubar.addMenu('Gestion des personnes')
        personne_menu.setFont(font)
        maladies_menu = menubar.addMenu('Gestion des maladies')
        maladies_menu.setFont(font)
        calcul_menu = menubar.addMenu('Calcul et affichage')
        calcul_menu.setFont(font)
        enregistrement_menu = menubar.addMenu('Enregistrement et recuperation des fichiers')
        enregistrement_menu.setFont(font)
        mise_menu = QMenu('Mise à jour des personnes', self)
        mise_menu.setFont(font)
        mise_action1 = QAction(QIcon('ajouter.png'),'Ajouter personne', self)
        mise_action1.triggered.connect(self.show_window1)
        mise_menu.addAction(mise_action1)
        mise_menu1 = QMenu('Supprimer personne', self)
        mise_menu1.setFont(font)
        mise_menu.addMenu(mise_menu1)
        mise_action2= QAction(QIcon('supprimer.png'),'Suppression personne donné',self)
        mise_action2.triggered.connect(self.show_window8)
        mise_menu1.addAction(mise_action2)
        mise_action3= QAction(QIcon('supprimer.png'),'Suppression des personnes d\'une nationnalité donnée',self)
        mise_action3.triggered.connect(self.show_window9)
        mise_menu1.addAction(mise_action3)
        mise_action4= QAction(QIcon('supprimer.png'),'Suppression des personnes d\'un indicatif donné',self)
        mise_action4.triggered.connect(self.show_window10)
        mise_menu1.addAction(mise_action4)
        mise_menu2 = QMenu('Modifier personne', self)
        mise_menu2.setFont(font)
        mise_menu.addMenu(mise_menu2)
        mise_action5= QAction(QIcon('telephone.png'),'Télèphone',self)
        mise_action5.triggered.connect(self.show_window11)
        mise_menu2.addAction(mise_action5)
        mise_action6= QAction(QIcon('adresse.png'),'Adresse',self)
        mise_action6.triggered.connect(self.show_window12)
        mise_menu2.addAction(mise_action6)
        personne_menu.addMenu(mise_menu)
        recherche_menu=QMenu('recherche , Affichage',self)
        recherche_menu.setFont(font)
        recherche_action1 = QAction(QIcon('afficher.png'),'Cotenu du dictionnaire personne',self)
        recherche_action1.triggered.connect(self.show_window6)
        recherche_menu.addAction(recherche_action1)
        recherche_action2 = QAction(QIcon('images.png'),'Recherche par numéro téléphone',self)
        recherche_action2.triggered.connect(self.show_window7)
        recherche_menu.addAction(recherche_action2)
        recherche_action3= QAction(QIcon('images.png'),'Recherche par indicatif',self)
        recherche_action3.triggered.connect(self.show_window2)
        recherche_menu.addAction(recherche_action3)
        recherche_action4= QAction(QIcon('images.png'),'Recherche par nationalité',self)
        recherche_action4.triggered.connect(self.show_window5)
        recherche_menu.addAction(recherche_action4)
        recherche_action5= QAction(QIcon('images.png'),'Recherche des personnes décédés',self)
        recherche_action5.triggered.connect(self.show_window4)
        recherche_menu.addAction(recherche_action5)
        recherche_action6= QAction(QIcon('images.png'),'Recherche des personnes non décédés',self)
        recherche_action6.triggered.connect(self.show_window3)
        recherche_menu.addAction(recherche_action6)
        personne_menu.addMenu(recherche_menu)
        Mise_menu = QMenu('mise à jour',self)
        Mise_menu.setFont(font)
        Mise_action1 = QAction(QIcon('maladie.png'),'Ajouter un nouvelle maladie',self)
        Mise_action1.triggered.connect(self.show_window13)
        Mise_menu.addAction(Mise_action1)
        Mise_action2 = QAction(QIcon('supprimer.png'),'Supprimer une maladie',self)
        Mise_action2.triggered.connect(self.show_window16)
        Mise_menu.addAction(Mise_action2)
        Mise_menu1 = QMenu("Modifier les données d'une maladie",self)
        Mise_menu1.setFont(font)
        Mise_menu.addMenu(Mise_menu1)
        Mise_action3 = QAction(QIcon('modifier.png'),'nombre d\'années',self)
        Mise_action3.triggered.connect(self.show_window14)
        Mise_menu1.addAction(Mise_action3)
        Mise_action4 = QAction(QIcon('modifier.png'),'modifier décés',self)
        Mise_action4.triggered.connect(self.show_window15)
        Mise_menu1.addAction(Mise_action4)
        maladies_menu.addMenu(Mise_menu)
        Recherche_menu=QMenu('Recherche et Afficher',self)
        Recherche_menu.setFont(font)
        Recherche_action1 = QAction(QIcon('afficher.png'),'Contenu du dictionnaires maladies',self)
        Recherche_action1.triggered.connect(self.show_window17)
        Recherche_menu.addAction(Recherche_action1)
        Recherche_action2 = QAction(QIcon('images.png'),'Recherche par une maladie',self)
        Recherche_action2.triggered.connect(self.show_window18)
        Recherche_menu.addAction(Recherche_action2)
        Recherche_action3 = QAction(QIcon('images.png'),'Recherche maladies d\'une personnes',self)
        Recherche_action3.triggered.connect(self.show_window19)
        Recherche_menu.addAction(Recherche_action3)
        Recherche_action4 = QAction(QIcon('images.png'),'Recherche le pourcentage de chaque maladie',self)
        Recherche_action4.triggered.connect(self.show_window20)
        Recherche_menu.addAction(Recherche_action4)
        Recherche_action5 = QAction(QIcon('images.png'),'Recherche maladies de chaque personnes',self)
        Recherche_action5.triggered.connect(self.show_window21)
        Recherche_menu.addAction(Recherche_action5)
        maladies_menu.addMenu(Recherche_menu)
        afficher_action = QAction(QIcon('afficher.png'),'Afficher par nationnalité', self)
        afficher_action.triggered.connect(self.show_window26)
        calcul_menu.addAction(afficher_action)
        quarantaine_action = QAction(QIcon('images.png'),'Personnes en quarantaine', self)
        quarantaine_action.triggered.connect(self.show_window28)
        calcul_menu.addAction(quarantaine_action)
        decedes_action = QAction(QIcon('images.png'),'Personnes décédés', self)
        decedes_action.triggered.connect(self.show_window27)
        calcul_menu.addAction(decedes_action)
        risque_action = QAction(QIcon('images.png'),'Personnes à risque', self)
        risque_action.triggered.connect(self.show_window29)
        calcul_menu.addAction(risque_action)
        enregistrement1_action = QAction(QIcon('enregistrer.png'),'Enregistrement fichier Personnes', self)
        enregistrement1_action.triggered.connect(self.show_window22)
        enregistrement_menu.addAction(enregistrement1_action)
        recuperation1_action = QAction(QIcon('recuperer.png'),'Recupération fichier Personnes', self)
        recuperation1_action.triggered.connect(self.show_window24)
        enregistrement_menu.addAction(recuperation1_action)
        enregistrement2_action = QAction(QIcon('enregistrer.png'),'Enregistrement fichier Maladies', self)
        enregistrement2_action.triggered.connect(self.show_window23)
        enregistrement_menu.addAction(enregistrement2_action)
        recuperation2_action = QAction(QIcon('recuperer.png'),'Recupération fichier Maladies', self)
        recuperation2_action.triggered.connect(self.show_window25)
        enregistrement_menu.addAction(recuperation2_action)
        #self.setGeometry(300, 200, 1000,800)
        #self.show()
        desktop = QDesktopWidget().screenGeometry()
        width, height = desktop.width(), desktop.height()
        # Set the size of the application window to match the desktop screen
        self.setGeometry(0, 0, width, height)
        self.setWindowTitle('mini projet CORONA')
        self.show()
    def show_window4(self):
        layout = QVBoxLayout()
        result = chercher_personne_decedes(personne_dict)
        resultat=contenu_dictionnaire(result)
        count=len(result)
        if count!=0:
            # Créer le QLabel pour afficher le pourcentage
            pourcentage_label = QLabel(f"Il y a  {count} personnes décédés")
            pourcentage_label.setAlignment(Qt.AlignCenter)
            font = QFont("Arial", 16)
            font.setBold(True)
            pourcentage_label.setFont(font)
            
            self.setWindowTitle("Personnes décédé")
            self.setGeometry(200, 200, 800, 600)
            self.table = QTableWidget(self)
            self.table.setColumnCount(9)
            self.table.setHorizontalHeaderLabels(["Numéro de carte d'identité", "Nom", "Prénom", "Âge", "Adresse", "Nationalité", "Numéro de téléphone", "Date d'infection", "Décédé"])
            self.table.setRowCount(len(resultat))
            
            # Définir le style des cellules contenant les mots "Nom", "Prénom" et "Risque"
            bold_font = QtGui.QFont()
            bold_font.setBold(True)
            blue_background = QtGui.QBrush(QtGui.QColor(230,230,230)) # couleur de fond bleue
            
            item_nom = QtWidgets.QTableWidgetItem("nom")
            item_nom.setFont(bold_font)
            item_nom.setBackground(blue_background)
            self.table.setItem(0, 0, item_nom)

            item_prenom = QtWidgets.QTableWidgetItem("prenom")
            item_prenom.setFont(bold_font)
            item_prenom.setBackground(blue_background)
            self.table.setItem(0, 1, item_prenom)

            item_age = QtWidgets.QTableWidgetItem("age")
            item_age.setFont(bold_font)
            item_age.setBackground(blue_background)
            self.table.setItem(0, 2, item_age)
            
            item_adresse = QtWidgets.QTableWidgetItem("adresse")
            item_adresse.setFont(bold_font)
            item_adresse.setBackground(blue_background)
            self.table.setItem(0, 3, item_adresse)
            
            item_nationalité = QtWidgets.QTableWidgetItem("nationalité")
            item_nationalité.setFont(bold_font)
            item_nationalité.setBackground(blue_background)
            self.table.setItem(0, 4, item_nationalité)
            
            item_numéro_telephone = QtWidgets.QTableWidgetItem("numéro_telephone")
            item_numéro_telephone.setFont(bold_font)
            item_numéro_telephone.setBackground(blue_background)
            self.table.setItem(0, 5, item_numéro_telephone)
            
            item_date_infectation = QtWidgets.QTableWidgetItem("date d'infectation")
            item_date_infectation.setFont(bold_font)
            item_date_infectation.setBackground(blue_background)
            self.table.setItem(0,6, item_date_infectation)
            
            item_décédé = QtWidgets.QTableWidgetItem("décédé")
            item_décédé.setFont(bold_font)
            item_décédé.setBackground(blue_background)
            self.table.setItem(0,7, item_décédé)
            
            # Définir le style du tableau
            self.table.setStyleSheet("""
                QTableWidget { background-color: white; color: black; font-size: 12pt; font-weight: bold; }
                QHeaderView::section { background-color: #007acc; color: white; font-size: 12pt; font-weight: bold; }
            """)
            
            self.table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
            for i, (cle, personne) in enumerate(result.items()):
                # Assigner la clé de la personne à la première colonne de la ligne i
                self.table.setItem(i, 0, QTableWidgetItem(str(cle)))
                
                # Assigner les autres attributs de la personne aux colonnes suivantes
                for j, item in enumerate(personne.values()):
                    self.table.setItem(i, j+1, QTableWidgetItem(str(item)))
                    self.table.item(i, j+1).setTextAlignment(QtCore.Qt.AlignCenter)
            font = QtGui.QFont()
            font.setBold(True)
            self.table.setFont(font)
            
            layout = QtWidgets.QVBoxLayout()
            layout.addWidget(pourcentage_label)
            # Redimensionner la largeur des colonnes pour s'adapter au contenu
            self.table.resizeColumnsToContents()
            layout.addWidget(self.table)
            self.table_dialog = QtWidgets.QDialog(self) # initialisez ici
            button_box = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Close)
            button_box.rejected.connect(self.table_dialog.reject)
            layout.addWidget(button_box)
            button_box.setStyleSheet("background-color: #007acc;")
            self.table_dialog.setLayout(layout)
            self.table_dialog.setWindowTitle("Personnes décédé")
            self.table_dialog.resize(2000,1000)
            self.table_dialog.show() 
        else:
            message_box = QtWidgets.QMessageBox(self)
            message_box = QtWidgets.QMessageBox(self)
            message_box.setWindowTitle('personnes décédé')
            message_box.setText("Il n' ya pas des personnes décédés.")
            message_box.setIcon(QtWidgets.QMessageBox.Information)
            ok_button = message_box.addButton(QtWidgets.QMessageBox.Ok)
            message_box.setStyleSheet("font-size: 14pt; font-weight: bold; color: #333; background-color: #fff;")
            ok_button.setStyleSheet("background-color: #007acc; color: white; font-size: 16px; padding: 10px 20px; border-radius: 50px;")
            message_box.exec_()
    def show_window1(self):
        def validate_line_edit1():
            data = line_edit1.text()
            if not data.isnumeric()or len(data)!=8:
                line_edit1.clear()
                line_edit1.setPlaceholderText('Invalid input')
        def validate_line_edit2():
            data = line_edit2.text()
            if  not data.isalpha():
                line_edit2.clear()
                line_edit2.setPlaceholderText('Invalid input')
        def validate_line_edit3():
            data = line_edit3.text()
            if  not data.isalpha():
                line_edit3.clear()
                line_edit3.setPlaceholderText('Invalid input')
        def validate_line_edit4():
            data = line_edit4.text()
            if  not data.isnumeric() or len(data)>3 :
                line_edit4.clear()
                line_edit4.setPlaceholderText('Invalid input')
        def validate_line_edit7():
            data = line_edit7.text()
            if not data.isnumeric() or len(data)!=8:
                line_edit7.clear()
                line_edit7.setPlaceholderText('Invalid input')
        def validate_line_edit9():
            data = line_edit9.text()
            if  not (data.isnumeric() and (data == "0" or data == "1")):
                line_edit9.clear()
                line_edit9.setPlaceholderText('Invalid input')
        def validate_line_edit8():
            data = line_edit8.text()
            # Vérifier que la chaîne de caractères est au bon format (jj/mm/aaaa)
            if not re.match(r'^\d{2}/\d{2}/\d{4}$', data):
                # Effacer le contenu de la ligne d'édition et afficher un message d'erreur
                line_edit8.clear()
                line_edit8.setPlaceholderText('Format de date invalide (jj/mm/aaaa)')
            else:
                # Convertir la chaîne de caractères en objet datetime
                try:
                    date_obj = datetime.datetime.strptime(data, '%d/%m/%Y')
                    # Formater la date au format "jj/mm/aaaa" et mettre à jour le contenu de la ligne d'édition
                    formatted_date = date_obj.strftime('%d/%m/%Y')
                    line_edit8.setText(formatted_date)
                except ValueError:
                    # Effacer le contenu de la ligne d'édition et afficher un message d'erreur
                    line_edit8.clear()
                    line_edit8.setPlaceholderText('Format de date invalide (jj/mm/aaaa)')
        def fermer_fenetre():
            self.mise_action1.close()
        def tous_les_champs_remplis():
            champs = [line_edit1, line_edit2, line_edit3, line_edit4, line_edit5, line_edit7, line_edit8, line_edit9]
            for champ in champs:
                if champ.text() == "":
                    return False
            return True
        self.mise_action1 = QWidget()
        self.mise_action1.setGeometry(0,0,1000,1000)
        self.mise_action1.setStyleSheet("background-color: white")
        self.mise_action1.setWindowTitle('ajouter personne')
        layout = QVBoxLayout(self.mise_action1)
        # Create QLabel instances and add them to the layout
        label1 = QLabel('Numéro de carte d\'identité  :', self.mise_action1)
        label1.setStyleSheet("font-weight: bold; font-size: 18pt;")
        line_edit1 = QLineEdit(self.mise_action1)
        line_edit1.setFont(QFont('Arial',20))
        line_edit1.setFixedWidth(400)
        line_edit1.returnPressed.connect(validate_line_edit1)
        line_edit1.returnPressed.connect(lambda: line_edit2.setFocus())
        layout.addWidget(label1)
        layout.addWidget(line_edit1)
        
        label2 = QLabel('Nom :', self.mise_action1)
        label2.setStyleSheet("font-weight: bold; font-size: 20pt;")
        line_edit2 = QLineEdit(self.mise_action1)
        line_edit2.setFont(QFont('Arial', 20))
        line_edit2.setFixedWidth(400)
        line_edit2.returnPressed.connect(validate_line_edit2)
        line_edit2.returnPressed.connect(lambda: line_edit3.setFocus())
        layout.addWidget(label2)
        layout.addWidget(line_edit2)
        
        label3 = QLabel('Prénom :', self.mise_action1)
        label3.setStyleSheet("font-weight: bold; font-size: 20pt;")
        line_edit3 = QLineEdit(self.mise_action1)
        line_edit3.setFont(QFont('Arial', 20))
        line_edit3.setFixedWidth(400)
        line_edit3.returnPressed.connect(validate_line_edit3)
        line_edit3.returnPressed.connect(lambda: line_edit4.setFocus())
        layout.addWidget(label3)
        layout.addWidget(line_edit3)
        
        label4 = QLabel('Age :', self.mise_action1)
        label4.setStyleSheet("font-weight: bold; font-size: 20pt;")
        line_edit4 = QLineEdit(self.mise_action1)
        line_edit4.setFont(QFont('Arial', 20))
        line_edit4.setFixedWidth(400)
        line_edit4.returnPressed.connect(validate_line_edit4)
        line_edit4.returnPressed.connect(lambda: line_edit5.setFocus())
        layout.addWidget(label4)
        layout.addWidget(line_edit4)
        
        label5 = QLabel('Adresse :', self.mise_action1)
        label5.setStyleSheet("font-weight: bold; font-size: 20pt;")
        line_edit5 = QLineEdit(self.mise_action1)
        line_edit5.setFont(QFont('Arial', 20))
        line_edit5.setFixedWidth(400)
        line_edit5.returnPressed.connect(lambda: line_edit7.setFocus())
        layout.addWidget(label5)
        layout.addWidget(line_edit5)
        
        label6 = QLabel('Nationalité : ', self.mise_action1)
        label6.setStyleSheet("font-weight: bold; font-size: 20pt;")
        # Liste des nationalités possibles
        nationalites = ['Afghan','Albanais','Algérien','Allemand','Américain','Angolais','Argentin','Arménien','Arubais','Australien','Autrichien','Azerbaïdjanais','Bahaméen','Bangladais','Belge','Benin','Biélorusse','Birmain','Bolivien','Bosniaque','Botswanais','Bouthan','Brésilien','Britannique','Bulgare','Burkinabè','Burundais','Caïmanien','Cambodgien','Camerounais','Canadien','Chilien','Chinois','Chypriote','Colombien','Congolais','Costaricain','Croate','Cubain','Danois','Dominicain','Egyptien','Emirati','Equatorien','Espagnol','Estonien','Ethiopien','Européen','Finlandais','Français','Gabonais','Georgien','Ghanéen','Grec','Guatemala','Guinéen','Haïtien','Hollandais','Hondurien','Hong-Kong','Hongrois','Indien','Indonésien','Irakien','Iranien','Irlandais','Islandais','Israélien','Italien','Ivoirien','Jamaïcain','Japonais','Jordanien','Kazakh','Kenyan','Kirghiz','Kosovar','Koweïtien','Kurde','Laotien','Lésothien','Letton','Libanais','Libyen','Liechtenstein','Lituanien','Luxembourgeois','Macédonien','Madagascar','Malaisien','Malien','Maltais','Marocain','Mauritanien','Mauritien','Mexicain','Monégasque','Mongol','Monténégrin','Mozambique','Namibien','Néo-Zélandais','Népalais','Nicaraguayen','Nigérien','Nord Coréen','Norvégien','Ougandais','Pakistanais','Palestinien','Panaméen','Paraguayen','Péruvien','Philippiens','Polonais','Portoricain','Portugais','Qatar','Roumain','Russe','Rwandais','Saoudien','Sénégalais','Serbe','Singapour','Slovaque','Somalien','Soudanais','Soviétique','Sri-Lankais','Sud-Africain','Sud-Coréen','Suédois','Suédois','Suisse','Syrien','Tadjik','Taïwanais','Tanzanien','Tchadien','Tchèque','Tchétchène','Thaïlandais','Trinité-Et-Tobago','Tunisien','Turc','Ukranien','Uruguayen','Vénézuélien','Vietnamien','Yéménite','Yougoslave','Zimbabwéen']
        # Création de la combobox
        combobox_nationalite = QComboBox(self.mise_action1)
        combobox_nationalite.setFont(QFont('Arial', 20))
        combobox_nationalite.setFixedWidth(400)
        combobox_nationalite.addItems(nationalites)
        #Ajout de la combobox au layout
        layout.addWidget(label6)
        layout.addWidget(combobox_nationalite)
        
        label7 = QLabel('Téléphone :', self.mise_action1)
        label7.setStyleSheet("font-weight: bold; font-size: 20pt;")
        line_edit7 = QLineEdit(self.mise_action1)
        line_edit7.setFont(QFont('Arial', 20))
        line_edit7.setFixedWidth(400)
        line_edit7.returnPressed.connect(validate_line_edit7)
        line_edit7.returnPressed.connect(lambda: line_edit8.setFocus())
        layout.addWidget(label7)
        layout.addWidget(line_edit7)
        
        label8 = QLabel('Date d\'infection :', self.mise_action1)
        label8.setStyleSheet("font-weight: bold; font-size: 20pt;")
        line_edit8 = QLineEdit(self.mise_action1)
        line_edit8.setFont(QFont('Arial', 20))
        line_edit8.setFixedWidth(400)
        line_edit8.returnPressed.connect(validate_line_edit8)
        line_edit8.returnPressed.connect(lambda: line_edit9.setFocus())
        layout.addWidget(label8)
        layout.addWidget(line_edit8)
        
        label9 = QLabel('Décédé :', self.mise_action1)
        label9.setStyleSheet("font-weight: bold; font-size: 20pt;")
        line_edit9 = QLineEdit(self.mise_action1)
        line_edit9.setFont(QFont('Arial', 20))
        line_edit9.setFixedWidth(400)
        line_edit9.returnPressed.connect(validate_line_edit9)
        layout.addWidget(label9)
        layout.addWidget(line_edit9)
        # Ajouter un bouton pour enregistrer les informations de la personne
        button_enregistrer = QPushButton('Enregistrer', self.mise_action1)
        button_enregistrer.setFixedWidth(400)
        button_enregistrer.setStyleSheet("background-color: #007acc; color: white; font-size: 16px; padding: 10px 20px; border-radius: 50px;")
        layout.addWidget(button_enregistrer)
        #Ajouter un bouton pour fermer la fenêtre
        button_fermer = QPushButton('Fermer', self.mise_action1)
        button_fermer.setFixedWidth(400)
        button_fermer.setStyleSheet("background-color: #007acc; color: white; font-size: 16px; padding: 10px 20px; border-radius: 50px;")
        layout.addWidget(button_fermer)
        layout.setAlignment(Qt.AlignCenter)
        def enregistrer_personne(self):
            # Vérifier si tous les champs sont remplis
            if not tous_les_champs_remplis() :
                error_message = QtWidgets.QMessageBox()
                error_message.setIcon(QtWidgets.QMessageBox.Warning)
                error_message.setWindowTitle("Erreur")
                error_message.setText("Veuillez remplir tous les champs avant d'enregistrer un personne.")

                # Personnaliser le texte en gras et de taille plus grande
                error_message.setStyleSheet("QMessageBox QLabel{ font-weight: bold; font-size: 25px; }")

                # Personnaliser le bouton OK en bleu, en gras et de taille plus grande
                error_message.setStyleSheet("QMessageBox QPushButton{ background-color: #007acc; color: white; font-weight: bold; font-size: 16px; }")

                error_message.exec_()
                return
            # Ajouter les informations de la personne au dictionnaire
            numero_carte_identite = line_edit1.text()
            nom = line_edit2.text()
            prenom = line_edit3.text()
            age = line_edit4.text()
            adresse = line_edit5.text()
            nationalite =combobox_nationalite.currentText()
            date_de_naissance = line_edit8.text()
            numero_telephone = line_edit7.text()
            decédé = line_edit9.text()
            if (existe(personne_dict,numero_carte_identite)==True):
                error_message = QtWidgets.QMessageBox()
                error_message.setIcon(QtWidgets.QMessageBox.Warning)
                error_message.setWindowTitle("Erreur")
                error_message.setText("Ce numéro de carte d'identité déja existe.")

                # Personnaliser le texte en gras et de taille plus grande
                error_message.setStyleSheet("QMessageBox QLabel{ font-weight: bold; font-size: 25px; }")

                # Personnaliser le bouton OK en bleu, en gras et de taille plus grande
                error_message.setStyleSheet("QMessageBox QPushButton{ background-color: #007acc; color: white; font-weight: bold; font-size: 16px; }")

                error_message.exec_()
                return
            else:
                message_box = QtWidgets.QMessageBox()
                message_box.setWindowTitle("Confirmation d'enregistrement")
                message_box.setText("Êtes-vous sûr de vouloir enregistrer ce personne?")
                message_box.setIcon(QtWidgets.QMessageBox.Warning)
                message_box.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
                message_box.setStyleSheet("font-size: 14pt; font-weight: bold; color: #333; background-color: #fff;")
                response = message_box.exec_()
                if response == QtWidgets.QMessageBox.Yes:
                    list={"nom":nom,"prenom":prenom,"age":age,"adresse":adresse,"nationalité":nationalite,"numéro_telephone":numero_telephone,"date d'infection":date_de_naissance,"decédé":decédé}
                    personne_dict[numero_carte_identite]=list
                    # Vider les champs de texte après avoir enregistré la personne
                    line_edit1.setText("")
                    line_edit2.setText("")
                    line_edit3.setText("")
                    line_edit4.setText("")
                    line_edit5.setText("")
                    line_edit7.setText("")
                    line_edit8.setText("")
                    line_edit9.setText("")
                    message_box = QtWidgets.QMessageBox()
                    message_box.setWindowTitle("enregistrement personne")
                    message_box.setText("Ce personne est bien enregistré")
                    message_box.setIcon(QtWidgets.QMessageBox.Information)
                    ok_button = message_box.addButton(QtWidgets.QMessageBox.Ok)
                    message_box.setStyleSheet("font-size: 14pt; font-weight: bold; color: #333; background-color: #fff;")
                    ok_button.setStyleSheet("background-color: #007acc; color: white; font-size: 16px; padding: 10px 20px; border-radius: 50px;")
                    message_box.exec_()
        button_enregistrer.clicked.connect(enregistrer_personne)
        button_fermer.clicked.connect(fermer_fenetre)
        self.mise_action1.show()
    def show_window6(self):
        layout = QVBoxLayout()
        result=contenu_dictionnaire(personne_dict)
        count = len(result)
        personnes_dict = []
        for numero_carte_identite, infos in personne_dict.items():
            nom = infos['nom']
            prenom = infos['prenom']
            age =infos['age']
            adresse=infos['adresse']
            nationalité=infos['nationalité']
            numéro_telephone=infos['numéro_telephone']
            décédé=infos['decédé']
            date_infection = infos['date d\'infection']
            personnes_dict.append((numero_carte_identite,nom, prenom, age, adresse, nationalité, numéro_telephone,date_infection, décédé ))  # Ajouter le numéro de carte d'identité et les informations de la personne à la liste des personnes en quarantaine
       
        if personnes_dict:
            self.setWindowTitle("contenu de dictionnaire personnes")
            self.table = QTableWidget(self)
            self.table.setColumnCount(9)
            self.table.setHorizontalHeaderLabels(["Numéro de carte d'identité", "Nom", "Prénom", "Âge", "Adresse", "Nationalité", "Numéro de téléphone", "Date d'infection", "Décédé"])
            self.table.setRowCount(len(personnes_dict))
            
            # Définir le style des cellules contenant les mots "Nom", "Prénom" et "Risque"
            bold_font = QtGui.QFont()
            bold_font.setBold(True)
            blue_background = QtGui.QBrush(QtGui.QColor(230,230,230)) # couleur de fond bleue
            
            item_nom = QtWidgets.QTableWidgetItem("nom")
            item_nom.setFont(bold_font)
            item_nom.setBackground(blue_background)
            self.table.setItem(0, 0, item_nom)

            item_prenom = QtWidgets.QTableWidgetItem("prenom")
            item_prenom.setFont(bold_font)
            item_prenom.setBackground(blue_background)
            self.table.setItem(0, 1, item_prenom)

            item_age = QtWidgets.QTableWidgetItem("age")
            item_age.setFont(bold_font)
            item_age.setBackground(blue_background)
            self.table.setItem(0, 2, item_age)
            
            item_adresse = QtWidgets.QTableWidgetItem("adresse")
            item_adresse.setFont(bold_font)
            item_adresse.setBackground(blue_background)
            self.table.setItem(0, 3, item_adresse)
            
            item_nationalité = QtWidgets.QTableWidgetItem("nationalité")
            item_nationalité.setFont(bold_font)
            item_nationalité.setBackground(blue_background)
            self.table.setItem(0, 4, item_nationalité)
            
            item_numéro_telephone = QtWidgets.QTableWidgetItem("numéro_telephone")
            item_numéro_telephone.setFont(bold_font)
            item_numéro_telephone.setBackground(blue_background)
            self.table.setItem(0, 5, item_numéro_telephone)
            
            item_date_infectation = QtWidgets.QTableWidgetItem("date d'infectation")
            item_date_infectation.setFont(bold_font)
            item_date_infectation.setBackground(blue_background)
            self.table.setItem(0,6, item_date_infectation)
            
            item_décédé = QtWidgets.QTableWidgetItem("décédé")
            item_décédé.setFont(bold_font)
            item_décédé.setBackground(blue_background)
            self.table.setItem(0,7, item_décédé)
            
            # Définir le style du tableau
            self.table.setStyleSheet("""
                QTableWidget { background-color: white; color: black; font-size: 12pt; font-weight: bold; }
                QHeaderView::section { background-color: #007acc; color: white; font-size: 12pt; font-weight: bold; }
            """)
            
            self.table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
            for i, personne in enumerate(personnes_dict):
                for j in range(len(personne)):
                    item = QTableWidgetItem(str(personne[j]))
                    item.setTextAlignment(QtCore.Qt.AlignCenter)
                    self.table.setItem(i, j, item)
            font = QtGui.QFont()
            font.setBold(True)
            self.table.setFont(font)
            
            layout = QtWidgets.QVBoxLayout()
            # Redimensionner la largeur des colonnes pour s'adapter au contenu
            self.table.resizeColumnsToContents()
            layout.addWidget(self.table)
            self.table_dialog = QtWidgets.QDialog(self) # initialisez ici
            button_box = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Close)
            button_box.rejected.connect(self.table_dialog.reject)
            layout.addWidget(button_box)
            button_box.setStyleSheet("background-color: #007acc;")
            self.table_dialog.setLayout(layout)
            self.table_dialog.setWindowTitle("Pcontenu de dictionnaire personnes")
            self.table_dialog.resize(2000,1000)
            self.table_dialog.show() 
            
        else:
            message_box = QtWidgets.QMessageBox(self)
            message_box = QtWidgets.QMessageBox(self)
            message_box.setWindowTitle('contenu de dictionnaire personnes')
            message_box.setText("Le dictionnaire est vide")
            message_box.setIcon(QtWidgets.QMessageBox.Information)
            ok_button = message_box.addButton(QtWidgets.QMessageBox.Ok)
            message_box.setStyleSheet("font-size: 14pt; font-weight: bold; color: #333; background-color: #fff;")
            ok_button.setStyleSheet("background-color: #007acc; color: white; font-size: 16px; padding: 10px 20px; border-radius: 50px;")
            message_box.exec_()
        
    def show_window7(self):
        def validate_line_edit1():
            data = age_edit.text()
            if not data.isnumeric() or len(data)!=8:
                age_edit.clear()
                age_edit.setPlaceholderText('Invalid input')
        def tous_les_champs_remplis():
            champs = [age_edit]
            for champ in champs:
                if champ.text() == "":
                    return False
            return True
        self.recherche_action2 = QWidget()
        self.recherche_action2.setGeometry(500,500,200,200)
        self.recherche_action2.setStyleSheet("background-color: white")
        self.recherche_action2.setWindowTitle('Recherche par numéro de téléphone')
        layout = QVBoxLayout(self.recherche_action2)
        
        label1 = QLabel("Numéro de téléphone:", self.recherche_action2)
        label1.setStyleSheet("font-weight: bold; font-size: 18pt;")
        age_edit = QLineEdit()
        age_edit.setFont(QFont('Arial',20))
        age_edit.setFixedWidth(400)
        age_edit.returnPressed.connect(validate_line_edit1)
        layout.addWidget(label1)
        layout.addWidget(age_edit)
        recherche_button = QPushButton("calculer")
        recherche_button.setFixedWidth(400)
        recherche_button.setStyleSheet("background-color: #007acc; color: black; font-size: 16px; padding: 10px 20px; border-radius: 50px;")
        layout.addWidget(recherche_button)
        # Ajouter un QPushButton pour fermer la fenêtre
        close_button = QPushButton("Fermer la fenêtre")
        close_button.setFixedWidth(400)
        close_button.setStyleSheet("background-color: white; color: black; font-size: 16px; padding: 10px 20px; border-radius: 50px;")
        layout.addWidget(close_button)
        layout.setAlignment(Qt.AlignCenter)
        # Définir la fonction qui sera appelée lorsqu'on clique sur le bouton de recherche
        def search_phone_number():
            numero_telephone = age_edit.text()
            result = chercher_personne_par_numero_telephone(numero_telephone,personne_dict)
            resultat=contenu_dictionnaire(result)
            count=len(result)
            font = QtGui.QFont("Arial", 12)
            if not tous_les_champs_remplis() :
                error_message = QtWidgets.QMessageBox()
                error_message.setIcon(QtWidgets.QMessageBox.Warning)
                error_message.setWindowTitle("Erreur")
                error_message.setText("Veuillez remplir le champ du numéro de téléphone avant de chercher.")

                # Personnaliser le texte en gras et de taille plus grande
                error_message.setStyleSheet("QMessageBox QLabel{ font-weight: bold; font-size: 25px; }")

                # Personnaliser le bouton OK en bleu, en gras et de taille plus grande
                error_message.setStyleSheet("QMessageBox QPushButton{ background-color: #007acc; color: white; font-weight: bold; font-size: 16px; }")

                error_message.exec_()
                return
            elif resultat:
                layout = QVBoxLayout()
                # Créer le QLabel pour afficher le pourcentage
                pourcentage_label = QLabel(f"Nombres des personnes ayant cette age: {count}")
                pourcentage_label.setAlignment(Qt.AlignCenter)
                font = QFont("Arial", 16)
                font.setBold(True)
                pourcentage_label.setFont(font)
                
                self.table = QTableWidget(self)
                self.table.setColumnCount(9)
                self.table.setHorizontalHeaderLabels(["Numéro de carte d'identité", "Nom", "Prénom", "Âge", "Adresse", "Nationalité", "Numéro de téléphone", "Date d'infection", "Décédé"])
                self.table.setRowCount(len(result))
                
                # Définir le style des cellules contenant les mots "Nom", "Prénom" et "Risque"
                bold_font = QtGui.QFont()
                bold_font.setBold(True)
                blue_background = QtGui.QBrush(QtGui.QColor(230,230,230)) # couleur de fond bleue
                
                item_nom = QtWidgets.QTableWidgetItem("nom")
                item_nom.setFont(bold_font)
                item_nom.setBackground(blue_background)
                self.table.setItem(0, 0, item_nom)

                item_prenom = QtWidgets.QTableWidgetItem("prenom")
                item_prenom.setFont(bold_font)
                item_prenom.setBackground(blue_background)
                self.table.setItem(0, 1, item_prenom)

                item_age = QtWidgets.QTableWidgetItem("age")
                item_age.setFont(bold_font)
                item_age.setBackground(blue_background)
                self.table.setItem(0, 2, item_age)
                
                item_adresse = QtWidgets.QTableWidgetItem("adresse")
                item_adresse.setFont(bold_font)
                item_adresse.setBackground(blue_background)
                self.table.setItem(0, 3, item_adresse)
                
                item_nationalité = QtWidgets.QTableWidgetItem("nationalité")
                item_nationalité.setFont(bold_font)
                item_nationalité.setBackground(blue_background)
                self.table.setItem(0, 4, item_nationalité)
                
                item_numéro_telephone = QtWidgets.QTableWidgetItem("numéro_telephone")
                item_numéro_telephone.setFont(bold_font)
                item_numéro_telephone.setBackground(blue_background)
                self.table.setItem(0, 5, item_numéro_telephone)
                
                item_date_infectation = QtWidgets.QTableWidgetItem("date d'infectation")
                item_date_infectation.setFont(bold_font)
                item_date_infectation.setBackground(blue_background)
                self.table.setItem(0,6, item_date_infectation)
                
                item_décédé = QtWidgets.QTableWidgetItem("décédé")
                item_décédé.setFont(bold_font)
                item_décédé.setBackground(blue_background)
                self.table.setItem(0,7, item_décédé)
                
                # Définir le style du tableau
                self.table.setStyleSheet("""
                    QTableWidget { background-color: white; color: black; font-size: 12pt; font-weight: bold; }
                    QHeaderView::section { background-color: #007acc; color: white; font-size: 12pt; font-weight: bold; }
                """)
                
                self.table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
                for i, (cle, personne) in enumerate(result.items()):
                    # Assigner la clé de la personne à la première colonne de la ligne i
                    self.table.setItem(i, 0, QTableWidgetItem(str(cle)))
                    
                    # Assigner les autres attributs de la personne aux colonnes suivantes
                    for j, item in enumerate(personne.values()):
                        self.table.setItem(i, j+1, QTableWidgetItem(str(item)))
                        self.table.item(i, j+1).setTextAlignment(QtCore.Qt.AlignCenter)
                font = QtGui.QFont()
                font.setBold(True)
                self.table.setFont(font)
                
                layout.addWidget(pourcentage_label)
                # Redimensionner la largeur des colonnes pour s'adapter au contenu
                self.table.resizeColumnsToContents()
                layout.addWidget(self.table)
                self.table_dialog = QtWidgets.QDialog(self) # initialisez ici
                button_box = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Close)
                button_box.rejected.connect(self.table_dialog.reject)
                layout.addWidget(button_box)
                button_box.setStyleSheet("background-color: #007acc;")
                self.table_dialog.setLayout(layout)
                self.table_dialog.setWindowTitle("recherche personne par numéro de téléphone")
                self.table_dialog.resize(2000,1000)
                self.table_dialog.show()
            else:
                message_box = QtWidgets.QMessageBox()
                message_box.setWindowTitle("Recherche par numéro de téléphone")
                message_box.setText("il n'y a pas des personnes ayant ce numérp de téléphone.")
                message_box.setIcon(QtWidgets.QMessageBox.Information)
                ok_button = message_box.addButton(QtWidgets.QMessageBox.Ok)
                message_box.setStyleSheet("font-size: 14pt; font-weight: bold; color: #333; background-color: #fff;")
                ok_button.setStyleSheet("background-color: #007acc; color: white; font-size: 16px; padding: 10px 20px; border-radius: 50px;")
                message_box.exec_()
        #Définir la fonction qui sera appelée lorsqu'on clique sur le bouton de fermeture
        def close_window():
            self.recherche_action2.close()
        # Connecter la fonction de fermeture au bouton de fermeture
        close_button.clicked.connect(close_window)
        recherche_button.clicked.connect(search_phone_number)
        self.recherche_action2.show()
    def show_window5(self):
        self.recherche_action3 = QWidget()
        self.recherche_action3.setGeometry(500,200,500,500)
        self.recherche_action3.setStyleSheet("background-color: white")
        self.recherche_action3 .setWindowTitle('Afficher par nationalité')
        layout = QVBoxLayout(self.recherche_action3)
        
        
        label1 = QLabel("Nationalité: ", self.recherche_action3)
        label1.setStyleSheet("font-weight: bold; font-size: 18pt;")
        # Liste des nationalités possibles
        nationalites = ['Afghan','Albanais','Algérien','Allemand','Américain','Angolais','Argentin','Arménien','Arubais','Australien','Autrichien','Azerbaïdjanais','Bahaméen','Bangladais','Belge','Benin','Biélorusse','Birmain','Bolivien','Bosniaque','Botswanais','Bouthan','Brésilien','Britannique','Bulgare','Burkinabè','Burundais','Caïmanien','Cambodgien','Camerounais','Canadien','Chilien','Chinois','Chypriote','Colombien','Congolais','Costaricain','Croate','Cubain','Danois','Dominicain','Egyptien','Emirati','Equatorien','Espagnol','Estonien','Ethiopien','Européen','Finlandais','Français','Gabonais','Georgien','Ghanéen','Grec','Guatemala','Guinéen','Haïtien','Hollandais','Hondurien','Hong-Kong','Hongrois','Indien','Indonésien','Irakien','Iranien','Irlandais','Islandais','Israélien','Italien','Ivoirien','Jamaïcain','Japonais','Jordanien','Kazakh','Kenyan','Kirghiz','Kosovar','Koweïtien','Kurde','Laotien','Lésothien','Letton','Libanais','Libyen','Liechtenstein','Lituanien','Luxembourgeois','Macédonien','Madagascar','Malaisien','Malien','Maltais','Marocain','Mauritanien','Mauritien','Mexicain','Monégasque','Mongol','Monténégrin','Mozambique','Namibien','Néo-Zélandais','Népalais','Nicaraguayen','Nigérien','Nord Coréen','Norvégien','Ougandais','Pakistanais','Palestinien','Panaméen','Paraguayen','Péruvien','Philippiens','Polonais','Portoricain','Portugais','Qatar','Roumain','Russe','Rwandais','Saoudien','Sénégalais','Serbe','Singapour','Slovaque','Somalien','Soudanais','Soviétique','Sri-Lankais','Sud-Africain','Sud-Coréen','Suédois','Suédois','Suisse','Syrien','Tadjik','Taïwanais','Tanzanien','Tchadien','Tchèque','Tchétchène','Thaïlandais','Trinité-Et-Tobago','Tunisien','Turc','Ukranien','Uruguayen','Vénézuélien','Vietnamien','Yéménite','Yougoslave','Zimbabwéen']
        
        # Création de la combobox
        combobox_nationalite = QComboBox(self.recherche_action3)
        combobox_nationalite.setFont(QFont('Arial', 20))
        combobox_nationalite.setFixedWidth(400)
        combobox_nationalite.addItems(nationalites)


        # Ajouter les widgets au layout
        layout.addWidget(label1)
        layout.addWidget(combobox_nationalite)
        
        # Ajouter un QPushButton pour effectuer la recherche
        recherche_button = QPushButton("calculer")
        recherche_button.setFixedWidth(400)
        recherche_button.setStyleSheet("background-color: #007acc; color: black; font-size: 24px; padding: 10px 20px; border-radius: 50px;")
        layout.addWidget(recherche_button)
        # Ajouter un QPushButton pour fermer la fenêtre
        close_button = QPushButton("Fermer la fenêtre")
        close_button.setFixedWidth(400)
        close_button.setStyleSheet("background-color: white; color: black; font-size: 24px; padding: 10px 20px; border-radius: 50px;")
        layout.addWidget(close_button)
        layout.setAlignment(Qt.AlignCenter)

        # Définir la fonction qui sera appelée lorsqu'on clique sur le bouton de recherche
        def search_nationalite():
            nationalite =combobox_nationalite.currentText()
            result = chercher_personne_par_nationalite(nationalite,personne_dict)
            count=len(result)
            if result:
                layout = QVBoxLayout()
                # Créer le QLabel pour afficher le pourcentage
                pourcentage_label = QLabel(f"Nombres des personnes ayant cette nationalité: {count}")
                pourcentage_label.setAlignment(Qt.AlignCenter)
                font = QFont("Arial", 16)
                font.setBold(True)
                pourcentage_label.setFont(font)
                
                self.table = QTableWidget(self)
                self.table.setColumnCount(9)
                self.table.setHorizontalHeaderLabels(["Numéro de carte d'identité", "Nom", "Prénom", "Âge", "Adresse", "Nationalité", "Numéro de téléphone", "Date d'infection", "Décédé"])
                self.table.setRowCount(len(result))
                
                # Définir le style des cellules contenant les mots "Nom", "Prénom" et "Risque"
                bold_font = QtGui.QFont()
                bold_font.setBold(True)
                blue_background = QtGui.QBrush(QtGui.QColor(230,230,230)) # couleur de fond bleue
                
                item_nom = QtWidgets.QTableWidgetItem("nom")
                item_nom.setFont(bold_font)
                item_nom.setBackground(blue_background)
                self.table.setItem(0, 0, item_nom)

                item_prenom = QtWidgets.QTableWidgetItem("prenom")
                item_prenom.setFont(bold_font)
                item_prenom.setBackground(blue_background)
                self.table.setItem(0, 1, item_prenom)

                item_age = QtWidgets.QTableWidgetItem("age")
                item_age.setFont(bold_font)
                item_age.setBackground(blue_background)
                self.table.setItem(0, 2, item_age)
                
                item_adresse = QtWidgets.QTableWidgetItem("adresse")
                item_adresse.setFont(bold_font)
                item_adresse.setBackground(blue_background)
                self.table.setItem(0, 3, item_adresse)
                
                item_nationalité = QtWidgets.QTableWidgetItem("nationalité")
                item_nationalité.setFont(bold_font)
                item_nationalité.setBackground(blue_background)
                self.table.setItem(0, 4, item_nationalité)
                
                item_numéro_telephone = QtWidgets.QTableWidgetItem("numéro_telephone")
                item_numéro_telephone.setFont(bold_font)
                item_numéro_telephone.setBackground(blue_background)
                self.table.setItem(0, 5, item_numéro_telephone)
                
                item_date_infectation = QtWidgets.QTableWidgetItem("date d'infectation")
                item_date_infectation.setFont(bold_font)
                item_date_infectation.setBackground(blue_background)
                self.table.setItem(0,6, item_date_infectation)
                
                item_décédé = QtWidgets.QTableWidgetItem("décédé")
                item_décédé.setFont(bold_font)
                item_décédé.setBackground(blue_background)
                self.table.setItem(0,7, item_décédé)
                
                # Définir le style du tableau
                self.table.setStyleSheet("""
                    QTableWidget { background-color: white; color: black; font-size: 12pt; font-weight: bold; }
                    QHeaderView::section { background-color: #007acc; color: white; font-size: 12pt; font-weight: bold; }
                """)
                
                self.table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
                for i, (cle, personne) in enumerate(result.items()):
                    # Assigner la clé de la personne à la première colonne de la ligne i
                    self.table.setItem(i, 0, QTableWidgetItem(str(cle)))
                    
                    # Assigner les autres attributs de la personne aux colonnes suivantes
                    for j, item in enumerate(personne.values()):
                        self.table.setItem(i, j+1, QTableWidgetItem(str(item)))
                        self.table.item(i, j+1).setTextAlignment(QtCore.Qt.AlignCenter)
                font = QtGui.QFont()
                font.setBold(True)
                self.table.setFont(font)
                
                layout.addWidget(pourcentage_label)
                # Redimensionner la largeur des colonnes pour s'adapter au contenu
                self.table.resizeColumnsToContents()
                layout.addWidget(self.table)
                self.table_dialog = QtWidgets.QDialog(self) # initialisez ici
                button_box = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Close)
                button_box.rejected.connect(self.table_dialog.reject)
                layout.addWidget(button_box)
                button_box.setStyleSheet("background-color: #007acc;")
                self.table_dialog.setLayout(layout)
                self.table_dialog.setWindowTitle("Personnes à risque")
                self.table_dialog.resize(2000,1000)
                self.table_dialog.show()
            else:
                message_box = QtWidgets.QMessageBox()
                message_box.setWindowTitle("afficher par nationalité.")
                message_box.setText("Aucun personne ayant cette nationalité")
                message_box.setIcon(QtWidgets.QMessageBox.Information)
                ok_button = message_box.addButton(QtWidgets.QMessageBox.Ok)
                message_box.setStyleSheet("font-size: 14pt; font-weight: bold; color: #333; background-color: #fff;")
                ok_button.setStyleSheet("background-color: #007acc; color: white; font-size: 16px; padding: 10px 20px; border-radius: 50px;")
                message_box.exec_()
        def close_window():
            self.recherche_action3.close()
        # Connecter la fonction de fermeture au bouton de fermeture
        close_button.clicked.connect(close_window)
        recherche_button.clicked.connect(search_nationalite)
        self.recherche_action3.show()
    def show_window3(self):
        layout = QVBoxLayout()
        result = chercher_personne_non_decedes(personne_dict)
        count=len(result)
        if count!=0:
            # Créer le QLabel pour afficher le pourcentage
            pourcentage_label = QLabel(f"Il y a  {count} personnes non décédés")
            pourcentage_label.setAlignment(Qt.AlignCenter)
            font = QFont("Arial", 16)
            font.setBold(True)
            pourcentage_label.setFont(font)
            
            self.setWindowTitle("Personnes décédé")
            self.setGeometry(200, 200, 800, 600)
            self.table = QTableWidget(self)
            self.table.setColumnCount(9)
            self.table.setHorizontalHeaderLabels(["Numéro de carte d'identité", "Nom", "Prénom", "Âge", "Adresse", "Nationalité", "Numéro de téléphone", "Date d'infection", "Décédé"])
            self.table.setRowCount(len(result))
            
            # Définir le style des cellules contenant les mots "Nom", "Prénom" et "Risque"
            bold_font = QtGui.QFont()
            bold_font.setBold(True)
            blue_background = QtGui.QBrush(QtGui.QColor(230,230,230)) # couleur de fond bleue
            
            item_nom = QtWidgets.QTableWidgetItem("nom")
            item_nom.setFont(bold_font)
            item_nom.setBackground(blue_background)
            self.table.setItem(0, 0, item_nom)

            item_prenom = QtWidgets.QTableWidgetItem("prenom")
            item_prenom.setFont(bold_font)
            item_prenom.setBackground(blue_background)
            self.table.setItem(0, 1, item_prenom)

            item_age = QtWidgets.QTableWidgetItem("age")
            item_age.setFont(bold_font)
            item_age.setBackground(blue_background)
            self.table.setItem(0, 2, item_age)
            
            item_adresse = QtWidgets.QTableWidgetItem("adresse")
            item_adresse.setFont(bold_font)
            item_adresse.setBackground(blue_background)
            self.table.setItem(0, 3, item_adresse)
            
            item_nationalité = QtWidgets.QTableWidgetItem("nationalité")
            item_nationalité.setFont(bold_font)
            item_nationalité.setBackground(blue_background)
            self.table.setItem(0, 4, item_nationalité)
            
            item_numéro_telephone = QtWidgets.QTableWidgetItem("numéro_telephone")
            item_numéro_telephone.setFont(bold_font)
            item_numéro_telephone.setBackground(blue_background)
            self.table.setItem(0, 5, item_numéro_telephone)
            
            item_date_infectation = QtWidgets.QTableWidgetItem("date d'infectation")
            item_date_infectation.setFont(bold_font)
            item_date_infectation.setBackground(blue_background)
            self.table.setItem(0,6, item_date_infectation)
            
            item_décédé = QtWidgets.QTableWidgetItem("décédé")
            item_décédé.setFont(bold_font)
            item_décédé.setBackground(blue_background)
            self.table.setItem(0,7, item_décédé)
            
            # Définir le style du tableau
            self.table.setStyleSheet("""
                QTableWidget { background-color: white; color: black; font-size: 12pt; font-weight: bold; }
                QHeaderView::section { background-color: #007acc; color: white; font-size: 12pt; font-weight: bold; }
            """)
            
            self.table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
            for i, (cle, personne) in enumerate(result.items()):
                # Assigner la clé de la personne à la première colonne de la ligne i
                self.table.setItem(i, 0, QTableWidgetItem(str(cle)))
                
                # Assigner les autres attributs de la personne aux colonnes suivantes
                for j, item in enumerate(personne.values()):
                    self.table.setItem(i, j+1, QTableWidgetItem(str(item)))
                    self.table.item(i, j+1).setTextAlignment(QtCore.Qt.AlignCenter)
            font = QtGui.QFont()
            font.setBold(True)
            self.table.setFont(font)
            
            layout = QtWidgets.QVBoxLayout()
            layout.addWidget(pourcentage_label)
            # Redimensionner la largeur des colonnes pour s'adapter au contenu
            self.table.resizeColumnsToContents()
            layout.addWidget(self.table)
            self.table_dialog = QtWidgets.QDialog(self) # initialisez ici
            button_box = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Close)
            button_box.rejected.connect(self.table_dialog.reject)
            layout.addWidget(button_box)
            button_box.setStyleSheet("background-color: #007acc;")
            self.table_dialog.setLayout(layout)
            self.table_dialog.setWindowTitle("Personnes non décédé")
            self.table_dialog.resize(2000,1000)
            self.table_dialog.show() 
        else:
            message_box = QtWidgets.QMessageBox(self)
            message_box = QtWidgets.QMessageBox(self)
            message_box.setWindowTitle('personnes non décédé')
            message_box.setText("le dictionnaire est vide.")
            message_box.setIcon(QtWidgets.QMessageBox.Information)
            ok_button = message_box.addButton(QtWidgets.QMessageBox.Ok)
            message_box.setStyleSheet("font-size: 14pt; font-weight: bold; color: #333; background-color: #fff;")
            ok_button.setStyleSheet("background-color: #007acc; color: white; font-size: 16px; padding: 10px 20px; border-radius: 50px;")
            message_box.exec_()
    def show_window2(self):
        def validate_line_edit1():
            data = age_edit.text()
            if not data.isnumeric() or len(data)>3:
                age_edit.clear()
                age_edit.setPlaceholderText('Invalid input')
        def tous_les_champs_remplis():
            champs = [age_edit]
            for champ in champs:
                if champ.text() == "":
                    return False
            return True
        self.recherche_action3 = QWidget()
        self.recherche_action3.setGeometry(500,500,200,200)
        self.recherche_action3.setStyleSheet("background-color: white")
        self.recherche_action3.setWindowTitle('Recherche par indicatif')
        layout = QVBoxLayout(self.recherche_action3)
        # Ajouter un QLineEdit pour entrer le numéro de téléphone
        label1 = QLabel("Age:", self.recherche_action3)
        label1.setStyleSheet("font-weight: bold; font-size: 18pt;")
        age_edit = QLineEdit()
        age_edit.setFont(QFont('Arial',20))
        age_edit.setFixedWidth(400)
        age_edit.returnPressed.connect(validate_line_edit1)
        layout.addWidget(label1)
        layout.addWidget(age_edit)
        recherche_button = QPushButton("calculer")
        recherche_button.setFixedWidth(400)
        recherche_button.setStyleSheet("background-color: #007acc; color: black; font-size: 16px; padding: 10px 20px; border-radius: 50px;")
        layout.addWidget(recherche_button)
        # Ajouter un QPushButton pour fermer la fenêtre
        close_button = QPushButton("Fermer la fenêtre")
        close_button.setFixedWidth(400)
        close_button.setStyleSheet("background-color: white; color: black; font-size: 16px; padding: 10px 20px; border-radius: 50px;")
        layout.addWidget(close_button)
        layout.setAlignment(Qt.AlignCenter)
        # Définir la fonction qui sera appelée lorsqu'on clique sur le bouton de recherche
        def search_age():
            age = age_edit.text()
            result = chercher_personne_par_age(age,personne_dict)
            resultat=contenu_dictionnaire(result)
            count=len(result)
            if not tous_les_champs_remplis() :
                error_message = QtWidgets.QMessageBox()
                error_message.setIcon(QtWidgets.QMessageBox.Warning)
                error_message.setWindowTitle("Erreur")
                error_message.setText("Veuillez remplir le champ d'age avant de chercher.")

                # Personnaliser le texte en gras et de taille plus grande
                error_message.setStyleSheet("QMessageBox QLabel{ font-weight: bold; font-size: 25px; }")

                # Personnaliser le bouton OK en bleu, en gras et de taille plus grande
                error_message.setStyleSheet("QMessageBox QPushButton{ background-color: #007acc; color: white; font-weight: bold; font-size: 16px; }")

                error_message.exec_()
                return
            elif result:
                layout = QVBoxLayout()
                # Créer le QLabel pour afficher le pourcentage
                pourcentage_label = QLabel(f"Nombres des personnes ayant cette age: {count}")
                pourcentage_label.setAlignment(Qt.AlignCenter)
                font = QFont("Arial", 16)
                font.setBold(True)
                pourcentage_label.setFont(font)
                
                self.table = QTableWidget(self)
                self.table.setColumnCount(9)
                self.table.setHorizontalHeaderLabels(["Numéro de carte d'identité", "Nom", "Prénom", "Âge", "Adresse", "Nationalité", "Numéro de téléphone", "Date d'infection", "Décédé"])
                self.table.setRowCount(len(result))
                
                # Définir le style des cellules contenant les mots "Nom", "Prénom" et "Risque"
                bold_font = QtGui.QFont()
                bold_font.setBold(True)
                blue_background = QtGui.QBrush(QtGui.QColor(230,230,230)) # couleur de fond bleue
                
                item_nom = QtWidgets.QTableWidgetItem("nom")
                item_nom.setFont(bold_font)
                item_nom.setBackground(blue_background)
                self.table.setItem(0, 0, item_nom)

                item_prenom = QtWidgets.QTableWidgetItem("prenom")
                item_prenom.setFont(bold_font)
                item_prenom.setBackground(blue_background)
                self.table.setItem(0, 1, item_prenom)

                item_age = QtWidgets.QTableWidgetItem("age")
                item_age.setFont(bold_font)
                item_age.setBackground(blue_background)
                self.table.setItem(0, 2, item_age)
                
                item_adresse = QtWidgets.QTableWidgetItem("adresse")
                item_adresse.setFont(bold_font)
                item_adresse.setBackground(blue_background)
                self.table.setItem(0, 3, item_adresse)
                
                item_nationalité = QtWidgets.QTableWidgetItem("nationalité")
                item_nationalité.setFont(bold_font)
                item_nationalité.setBackground(blue_background)
                self.table.setItem(0, 4, item_nationalité)
                
                item_numéro_telephone = QtWidgets.QTableWidgetItem("numéro_telephone")
                item_numéro_telephone.setFont(bold_font)
                item_numéro_telephone.setBackground(blue_background)
                self.table.setItem(0, 5, item_numéro_telephone)
                
                item_date_infectation = QtWidgets.QTableWidgetItem("date d'infectation")
                item_date_infectation.setFont(bold_font)
                item_date_infectation.setBackground(blue_background)
                self.table.setItem(0,6, item_date_infectation)
                
                item_décédé = QtWidgets.QTableWidgetItem("décédé")
                item_décédé.setFont(bold_font)
                item_décédé.setBackground(blue_background)
                self.table.setItem(0,7, item_décédé)
                
                # Définir le style du tableau
                self.table.setStyleSheet("""
                    QTableWidget { background-color: white; color: black; font-size: 12pt; font-weight: bold; }
                    QHeaderView::section { background-color: #007acc; color: white; font-size: 12pt; font-weight: bold; }
                """)
                
                self.table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
                for i, (cle, personne) in enumerate(result.items()):
                    # Assigner la clé de la personne à la première colonne de la ligne i
                    self.table.setItem(i, 0, QTableWidgetItem(str(cle)))
                    
                    # Assigner les autres attributs de la personne aux colonnes suivantes
                    for j, item in enumerate(personne.values()):
                        self.table.setItem(i, j+1, QTableWidgetItem(str(item)))
                        self.table.item(i, j+1).setTextAlignment(QtCore.Qt.AlignCenter)
                font = QtGui.QFont()
                font.setBold(True)
                self.table.setFont(font)
                
                layout.addWidget(pourcentage_label)
                # Redimensionner la largeur des colonnes pour s'adapter au contenu
                self.table.resizeColumnsToContents()
                layout.addWidget(self.table)
                self.table_dialog = QtWidgets.QDialog(self) # initialisez ici
                button_box = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Close)
                button_box.rejected.connect(self.table_dialog.reject)
                layout.addWidget(button_box)
                button_box.setStyleSheet("background-color: #007acc;")
                self.table_dialog.setLayout(layout)
                self.table_dialog.setWindowTitle("recherche personne par age")
                self.table_dialog.resize(2000,1000)
                self.table_dialog.show()
            else:
                message_box = QtWidgets.QMessageBox()
                message_box.setWindowTitle("Recherche par age")
                message_box.setText("il n'y a pas des personnes ayant cette age")
                message_box.setIcon(QtWidgets.QMessageBox.Information)
                ok_button = message_box.addButton(QtWidgets.QMessageBox.Ok)
                message_box.setStyleSheet("font-size: 14pt; font-weight: bold; color: #333; background-color: #fff;")
                ok_button.setStyleSheet("background-color: #007acc; color: white; font-size: 16px; padding: 10px 20px; border-radius: 50px;")
                message_box.exec_()
        #Définir la fonction qui sera appelée lorsqu'on clique sur le bouton de fermeture
        def close_window():
            self.recherche_action3.close()
        # Connecter la fonction de fermeture au bouton de fermeture
        close_button.clicked.connect(close_window)
        recherche_button.clicked.connect(search_age)
        self.recherche_action3.show()
    def show_window8(self):
        def tous_les_champs_remplis():
            champs = [cin_edit]
            for champ in champs:
                if champ.text() == "":
                    return False
            return True
        def validate_line_edit1():
            data = cin_edit.text()
            if not data.isnumeric() or len(data)!=8:
                cin_edit.clear()
                cin_edit.setPlaceholderText('Invalid input')
        self.mise_action2 = QWidget()
        self.mise_action2.setGeometry(200,200,500,500)
        self.mise_action2.setStyleSheet("background-color: #f2f2f2")
        self.mise_action2.setWindowTitle('Suppression personne donné')
        layout = QVBoxLayout(self.mise_action2)
        # Ajouter un QLineEdit pour entrer le numéro de téléphone
        cin_edit = QLineEdit()
        cin_edit.setFont(QFont('Arial', 30))
        cin_edit.returnPressed.connect(validate_line_edit1)
        num_label = QLabel("Numéro de carte d'identité:")
        num_label.setStyleSheet("font-weight: bold; font-size: 20pt;")
        layout.addWidget(num_label)
        cin_edit.setFixedWidth(400)

        # mettre le texte en gras
        cin_edit.setStyleSheet("font-weight: bold")
        layout.addWidget(cin_edit)
        # Ajouter un QPushButton pour effectuer la recherche
        suppression_button = QPushButton("Supprimer")
        suppression_button.setFixedWidth(400)
        suppression_button.setStyleSheet("background-color: #007acc; color: white; font-size: 16px; padding: 10px 20px; border-radius: 50px;")
        layout.addWidget(suppression_button)
        # Ajouter un QPushButton pour fermer la fenêtre
        close_button = QPushButton("Fermer")
        close_button.setFixedWidth(400)
        close_button.setStyleSheet("background-color: #007acc; color: white; font-size: 16px; padding: 10px 20px; border-radius: 50px;")
        layout.addWidget(close_button)
        layout.setAlignment(Qt.AlignCenter)
        def suppression_personne_cin():
            cin=cin_edit.text()
            if not tous_les_champs_remplis() :
                error_message = QtWidgets.QMessageBox()
                error_message.setIcon(QtWidgets.QMessageBox.Warning)
                error_message.setWindowTitle("Erreur")
                error_message.setText("Veuillez remplir le champ de numéro de téléphone avant de supprimer.")

                # Personnaliser le texte en gras et de taille plus grande
                error_message.setStyleSheet("QMessageBox QLabel{ font-weight: bold; font-size: 25px; }")

                # Personnaliser le bouton OK en bleu, en gras et de taille plus grande
                error_message.setStyleSheet("QMessageBox QPushButton{ background-color: #007acc; color: white; font-weight: bold; font-size: 16px; }")

                error_message.exec_()
                return
            elif existe(personne_dict,cin)==True:
                message_box = QtWidgets.QMessageBox(self)
                message_box.setWindowTitle("Confirmation de suppression")
                message_box.setText("Êtes-vous sûr de vouloir supprimer les personnes ayant cette numéro d'identité?")
                message_box.setIcon(QtWidgets.QMessageBox.Warning)
                message_box.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
                message_box.setStyleSheet("font-size: 14pt; font-weight: bold; color: #333; background-color: #fff;")
                response = message_box.exec_()
                if response == QtWidgets.QMessageBox.Yes:
                    del personne_dict[cin]
                    message_box = QtWidgets.QMessageBox(self)
                    message_box.setWindowTitle("Suppression personne donné")
                    message_box.setText("le personne est bien supprimé")
                    message_box.setIcon(QtWidgets.QMessageBox.Information)
                    ok_button = message_box.addButton(QtWidgets.QMessageBox.Ok)
                    message_box.setStyleSheet("font-size: 14pt; font-weight: bold; color: #333; background-color: #fff;")
                    ok_button.setStyleSheet("background-color: #007acc; color: white; font-size: 16px; padding: 10px 20px; border-radius: 50px;")
                    message_box.exec_()
            else:
                message_box = QtWidgets.QMessageBox(self)
                message_box.setWindowTitle("'Supression personne donné")
                message_box.setText("il n'y a personne ayant ce numéro de carte d'identité")
                message_box.setIcon(QtWidgets.QMessageBox.Information)
                ok_button = message_box.addButton(QtWidgets.QMessageBox.Ok)
                message_box.setStyleSheet("font-size: 14pt; font-weight: bold; color: #333; background-color: #fff;")
                ok_button.setStyleSheet("background-color: #007acc; color: white; font-size: 16px; padding: 10px 20px; border-radius: 50px;")
                message_box.exec_()
        #Définir la fonction qui sera appelée lorsqu'on clique sur le bouton de fermeture
        def close_window():
            self.mise_action2.close()
        # Connecter la fonction de fermeture au bouton de fermeture
        close_button.clicked.connect(close_window)
        suppression_button.clicked.connect(suppression_personne_cin)
        self.mise_action2.show()
    def show_window9(self):
        self.mise_action3 = QWidget()
        self.mise_action3.setGeometry(500,200,500,500)
        self.mise_action3.setStyleSheet("background-color: white")
        self.mise_action3 .setWindowTitle('Supprimer par nationalité')
        layout = QVBoxLayout(self.mise_action3)
        
        
        label1 = QLabel("Nationalité: ", self.mise_action3)
        label1.setStyleSheet("font-weight: bold; font-size: 18pt;")
        # Liste des nationalités possibles
        nationalites = ['Afghan','Albanais','Algérien','Allemand','Américain','Angolais','Argentin','Arménien','Arubais','Australien','Autrichien','Azerbaïdjanais','Bahaméen','Bangladais','Belge','Benin','Biélorusse','Birmain','Bolivien','Bosniaque','Botswanais','Bouthan','Brésilien','Britannique','Bulgare','Burkinabè','Burundais','Caïmanien','Cambodgien','Camerounais','Canadien','Chilien','Chinois','Chypriote','Colombien','Congolais','Costaricain','Croate','Cubain','Danois','Dominicain','Egyptien','Emirati','Equatorien','Espagnol','Estonien','Ethiopien','Européen','Finlandais','Français','Gabonais','Georgien','Ghanéen','Grec','Guatemala','Guinéen','Haïtien','Hollandais','Hondurien','Hong-Kong','Hongrois','Indien','Indonésien','Irakien','Iranien','Irlandais','Islandais','Israélien','Italien','Ivoirien','Jamaïcain','Japonais','Jordanien','Kazakh','Kenyan','Kirghiz','Kosovar','Koweïtien','Kurde','Laotien','Lésothien','Letton','Libanais','Libyen','Liechtenstein','Lituanien','Luxembourgeois','Macédonien','Madagascar','Malaisien','Malien','Maltais','Marocain','Mauritanien','Mauritien','Mexicain','Monégasque','Mongol','Monténégrin','Mozambique','Namibien','Néo-Zélandais','Népalais','Nicaraguayen','Nigérien','Nord Coréen','Norvégien','Ougandais','Pakistanais','Palestinien','Panaméen','Paraguayen','Péruvien','Philippiens','Polonais','Portoricain','Portugais','Qatar','Roumain','Russe','Rwandais','Saoudien','Sénégalais','Serbe','Singapour','Slovaque','Somalien','Soudanais','Soviétique','Sri-Lankais','Sud-Africain','Sud-Coréen','Suédois','Suédois','Suisse','Syrien','Tadjik','Taïwanais','Tanzanien','Tchadien','Tchèque','Tchétchène','Thaïlandais','Trinité-Et-Tobago','Tunisien','Turc','Ukranien','Uruguayen','Vénézuélien','Vietnamien','Yéménite','Yougoslave','Zimbabwéen']
        
        # Création de la combobox
        combobox_nationalite = QComboBox(self.mise_action3)
        combobox_nationalite.setFont(QFont('Arial', 20))
        combobox_nationalite.setFixedWidth(400)
        combobox_nationalite.addItems(nationalites)


        # Ajouter les widgets au layout
        layout.addWidget(label1)
        layout.addWidget(combobox_nationalite)
        # Ajouter un QPushButton pour effectuer la recherche
        recherche_button = QPushButton("Supprimer")
        recherche_button.setFixedWidth(400)
        recherche_button.setStyleSheet("background-color: #007acc; color: black; font-size: 24px; padding: 10px 20px; border-radius: 50px;")
    
        layout.addWidget(recherche_button)
        close_button = QPushButton("Fermer la fenêtre")
        close_button.setFixedWidth(400)
        close_button.setStyleSheet("background-color: white; color: black; font-size: 24px; padding: 10px 20px; border-radius: 50px;")
        layout.addWidget(close_button)
        layout.setAlignment(Qt.AlignCenter)
        # Définir la fonction qui sera appelée lorsqu'on clique sur le bouton de recherche
        def search_nationalite():
            nationalite =combobox_nationalite.currentText()
            result = chercher_personne_par_nationalite(nationalite,personne_dict)
            resultat=contenu_dictionnaire(result)
            if resultat:
                message_box = QtWidgets.QMessageBox()
                message_box.setWindowTitle("Confirmation de suppression")
                message_box.setText("Êtes-vous sûr de vouloir supprimer cette nationalité?")
                message_box.setIcon(QtWidgets.QMessageBox.Warning)
                message_box.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
                message_box.setStyleSheet("font-size: 14pt; font-weight: bold; color: #333; background-color: #fff;")
                response = message_box.exec_()
                if response == QtWidgets.QMessageBox.Yes:
                    for cle,val in resultat:
                        del personne_dict[cle]
                    message_box = QtWidgets.QMessageBox()
                    message_box.setWindowTitle("Recherche par nationalité")
                    message_box.setText("les personnes ayant cette nationalité sont bien supprimés")
                    message_box.setIcon(QtWidgets.QMessageBox.Information)
                    ok_button = message_box.addButton(QtWidgets.QMessageBox.Ok)
                    message_box.setStyleSheet("font-size: 14pt; font-weight: bold; color: #333; background-color: #fff;")
                    ok_button.setStyleSheet("background-color: #007acc; color: white; font-size: 16px; padding: 10px 20px; border-radius: 50px;")
                    message_box.exec_()
            else:
                message_box = QtWidgets.QMessageBox()
                message_box.setWindowTitle("Recherche par nationalité")
                message_box.setText("Il n' y a pas des personnes ayant cette nationalité.")
                message_box.setIcon(QtWidgets.QMessageBox.Information)
                ok_button = message_box.addButton(QtWidgets.QMessageBox.Ok)
                message_box.setStyleSheet("font-size: 14pt; font-weight: bold; color: #333; background-color: #fff;")
                ok_button.setStyleSheet("background-color: #007acc; color: white; font-size: 16px; padding: 10px 20px; border-radius: 50px;")
                message_box.exec_()

        #Définir la fonction qui sera appelée lorsqu'on clique sur le bouton de fermeture
        def close_window():
            self.mise_action3.close()
        # Connecter la fonction de fermeture au bouton de fermeture
        close_button.clicked.connect(close_window)
        recherche_button.clicked.connect(search_nationalite)
        self.mise_action3.show()
    def show_window10(self):
        def validate_line_edit1():
            data = phone_edit.text()
            if not data.isnumeric() or len(data)!=8:
                phone_edit.clear()
                phone_edit.setPlaceholderText('Invalid input')
        def tous_les_champs_remplis():
            champs = [phone_edit]
            for champ in champs:
                if champ.text() == "":
                    return False
            return True
        self.mise_action4 = QWidget()
        self.mise_action4.setGeometry(200,200,500,500)
        self.mise_action4.setStyleSheet("background-color: #f2f2f2")
        self.mise_action4.setWindowTitle("Suppression des personnes d'un indicatif donné (téléphone)")
        layout = QVBoxLayout(self.mise_action4)

        # Ajouter un QLineEdit pour entrer le numéro de téléphone
        phone_edit = QLineEdit()
        phone_edit.setFont(QFont('Arial', 30))
        phone_edit.returnPressed.connect(validate_line_edit1)
        num_label = QLabel("Numéro de téléphone:")
        num_label.setStyleSheet("font-weight: bold; font-size: 20pt;")
        layout.addWidget(num_label)
        phone_edit.setFixedWidth(400)

        # mettre le texte en gras
        phone_edit.setStyleSheet("font-weight: bold")
        layout.addWidget(phone_edit)

        # Ajouter un QPushButton pour effectuer la recherche
        search_button = QPushButton("Supprimer")
        search_button.setFixedWidth(400)
        search_button.setStyleSheet("background-color: #007acc; color: white; font-size: 16px; padding: 10px 20px; border-radius: 50px;")
        layout.addWidget(search_button)

        # Ajouter un QPushButton pour fermer la fenêtre
        close_button = QPushButton("Fermer")
        close_button.setFixedWidth(400)
        close_button.setStyleSheet("background-color: #007acc; color: white; font-size: 16px; padding: 10px 20px; border-radius: 50px;")
        layout.addWidget(close_button)
        layout.setAlignment(Qt.AlignCenter)
        # Définir la fonction qui sera appelée lorsqu'on clique sur le bouton de recherche
        def search_phone_number():
            numero_telephone = phone_edit.text()
            result = chercher_personne_par_numero_telephone(numero_telephone,personne_dict)
            resultat=contenu_dictionnaire(result)
            if not tous_les_champs_remplis() :
                error_message = QtWidgets.QMessageBox()
                error_message.setIcon(QtWidgets.QMessageBox.Warning)
                error_message.setWindowTitle("Erreur")
                error_message.setText("Veuillez remplir le champ de numéro de téléphone avant de supprimer.")

                # Personnaliser le texte en gras et de taille plus grande
                error_message.setStyleSheet("QMessageBox QLabel{ font-weight: bold; font-size: 25px; }")

                # Personnaliser le bouton OK en bleu, en gras et de taille plus grande
                error_message.setStyleSheet("QMessageBox QPushButton{ background-color: #007acc; color: white; font-weight: bold; font-size: 16px; }")

                error_message.exec_()
                return
            elif resultat:
                message_box = QtWidgets.QMessageBox(self)
                message_box.setWindowTitle("Confirmation de suppression")
                message_box.setText("Êtes-vous sûr de vouloir supprimer les personnes ayant ce numéro de téléphone ?")
                message_box.setIcon(QtWidgets.QMessageBox.Warning)
                message_box.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
                message_box.setStyleSheet("font-size: 14pt; font-weight: bold; color: #333; background-color: #fff;")
                response = message_box.exec_()
                if response == QtWidgets.QMessageBox.Yes:
                    for cle, val in resultat:
                        del personne_dict[cle]
                    message_box = QtWidgets.QMessageBox(self)
                    message_box.setWindowTitle("Suppression des personnes d'un indicatif donné")
                    message_box.setText("les personnes ayant ce numéro de téléphone sont bien supprimés.")
                    message_box.setIcon(QtWidgets.QMessageBox.Information)
                    ok_button = message_box.addButton(QtWidgets.QMessageBox.Ok)
                    message_box.setStyleSheet("font-size: 14pt; font-weight: bold; color: #333; background-color: #fff;")
                    ok_button.setStyleSheet("background-color: #007acc; color: white; font-size: 16px; padding: 10px 20px; border-radius: 50px;")
                    message_box.exec_()
            else:
                message_box = QtWidgets.QMessageBox(self)
                message_box.setWindowTitle("Suppression des personnes d'un indicatif donné")
                message_box.setText("il n'y a pas des personnes qui ont ce numéro de téléphone.")
                message_box.setIcon(QtWidgets.QMessageBox.Information)
                ok_button = message_box.addButton(QtWidgets.QMessageBox.Ok)
                message_box.setStyleSheet("font-size: 14pt; font-weight: bold; color: #333; background-color: #fff;")
                ok_button.setStyleSheet("background-color: #007acc; color: white; font-size: 16px; padding: 10px 20px; border-radius: 50px;")
                message_box.exec_()
        #Définir la fonction qui sera appelée lorsqu'on clique sur le bouton de fermeture
        def close_window():
            self.mise_action4.close()

        # Connecter la fonction de fermeture au bouton de fermeture
        close_button.clicked.connect(close_window)
        search_button.clicked.connect(search_phone_number)
        self.mise_action4.show()
    def show_window11(self):
        def tous_les_champs_remplis():
            champs = [cin_edit,phone_edit]
            for champ in champs:
                if champ.text() == "":
                    return False
            return True
        def validate_line_edit1():
            data = cin_edit.text()
            if not data.isnumeric() or len(data)!=8:
                cin_edit.clear()
                cin_edit.setPlaceholderText('Invalid input')
        def validate_line_edit2():
            data = phone_edit.text()
            if not data.isnumeric() or len(data)!=8:
                phone_edit.clear()
                phone_edit.setPlaceholderText('Invalid input')
        self.mise_action5 = QWidget()
        self.mise_action5.setGeometry(500,500,200,200)
        self.mise_action5.setStyleSheet("background-color: white")
        self.mise_action5.setWindowTitle('modifier le numéro du téléphone.')
        layout = QVBoxLayout(self.mise_action5)
        # Ajouter un QLineEdit pour entrer le numéro de carte d'identité
        label1 = QLabel("Numéro de cin:", self.mise_action5)
        label1.setStyleSheet("font-weight: bold; font-size: 18pt;")
        cin_edit = QLineEdit()
        cin_edit.setFont(QFont('Arial',20))
        cin_edit.setFixedWidth(400)
        cin_edit.returnPressed.connect(validate_line_edit1)
        layout.addWidget(label1)
        layout.addWidget(cin_edit)
        # Ajouter un QLineEdit pour entrer le numéro de téléphone
        label2 = QLabel("Numéro de téléphone:", self.mise_action5)
        label2.setStyleSheet("font-weight: bold; font-size: 18pt;")
        phone_edit = QLineEdit()
        phone_edit.setFont(QFont('Arial',20))
        phone_edit.setFixedWidth(400)
        phone_edit.returnPressed.connect(validate_line_edit2)
        layout.addWidget(label2)
        layout.addWidget(phone_edit)
        # Ajouter un QPushButton pour effectuer la recherche
        modifier_button = QPushButton("modifier")
        modifier_button.setFixedWidth(400)
        modifier_button.setStyleSheet("background-color: #007acc; color: black; font-size: 16px; padding: 10px 20px; border-radius: 50px;")
        layout.addWidget(modifier_button)
        # Ajouter un QPushButton pour fermer la fenêtre
        close_button = QPushButton("Fermer la fenêtre")
        close_button.setFixedWidth(400)
        close_button.setStyleSheet("background-color: white; color: black; font-size: 16px; padding: 10px 20px; border-radius: 50px;")
        layout.addWidget(close_button)
        layout.setAlignment(Qt.AlignCenter)
        def modifier_téléphone():
            cin=cin_edit.text()
            phone=phone_edit.text()
            if not tous_les_champs_remplis() :
                error_message = QtWidgets.QMessageBox()
                error_message.setIcon(QtWidgets.QMessageBox.Warning)
                error_message.setWindowTitle("Erreur")
                error_message.setText("Veuillez remplir tous les champs avnt de modifier.")

                # Personnaliser le texte en gras et de taille plus grande
                error_message.setStyleSheet("QMessageBox QLabel{ font-weight: bold; font-size: 25px; }")

                # Personnaliser le bouton OK en bleu, en gras et de taille plus grande
                error_message.setStyleSheet("QMessageBox QPushButton{ background-color: #007acc; color: white; font-weight: bold; font-size: 16px; }")

                error_message.exec_()
                return
            elif existe(personne_dict,cin)==True:
                message_box = QtWidgets.QMessageBox()
                message_box.setWindowTitle("Confirmation d'enregistrement")
                message_box.setText("Êtes-vous sûr de vouloir enregistrer cette maladie pour ce personne?")
                message_box.setIcon(QtWidgets.QMessageBox.Warning)
                message_box.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
                message_box.setStyleSheet("font-size: 14pt; font-weight: bold; color: #333; background-color: #fff;")
                response = message_box.exec_()
                if response == QtWidgets.QMessageBox.Yes:
                    liste_personne = personne_dict[cin]
                    liste_personne["numéro_telephone"] = phone
                    message_box = QtWidgets.QMessageBox()
                    message_box.setWindowTitle("modifier téléphone")
                    message_box.setText("le numéro de téléphone de ce personne est bien modifiée.")
                    message_box.setIcon(QtWidgets.QMessageBox.Information)
                    ok_button = message_box.addButton(QtWidgets.QMessageBox.Ok)
                    message_box.setStyleSheet("font-size: 14pt; font-weight: bold; color: #333; background-color: #fff;")
                    ok_button.setStyleSheet("background-color: #007acc; color: white; font-size: 16px; padding: 10px 20px; border-radius: 50px;")
                    message_box.exec_()
            else:
                message_box = QtWidgets.QMessageBox()
                message_box.setWindowTitle("modifier téléphone")
                message_box.setText("il n'y a personne ayant ce numéro de carte d'identité.")
                message_box.setIcon(QtWidgets.QMessageBox.Information)
                ok_button = message_box.addButton(QtWidgets.QMessageBox.Ok)
                message_box.setStyleSheet("font-size: 14pt; font-weight: bold; color: #333; background-color: #fff;")
                ok_button.setStyleSheet("background-color: #007acc; color: white; font-size: 16px; padding: 10px 20px; border-radius: 50px;")
                message_box.exec_()
        #Définir la fonction qui sera appelée lorsqu'on clique sur le bouton de fermeture
        def close_window():
            self.mise_action5.close()
        # Connecter la fonction de fermeture au bouton de fermeture
        close_button.clicked.connect(close_window)
        modifier_button.clicked.connect(modifier_téléphone)
        self.mise_action5.show()
    def show_window12(self):
        def tous_les_champs_remplis():
            champs = [cin_edit,adresse_edit]
            for champ in champs:
                if champ.text() == "":
                    return False
            return True
        def validate_line_edit1():
            data = cin_edit.text()
            if not data.isnumeric() or len(data)!=8:
                cin_edit.clear()
                cin_edit.setPlaceholderText('Invalid input')
        def validate_line_edit2():
            data = adresse_edit.text()
            if not data.alpha():
                adresse_edit.clear()
                adresse_edit.setPlaceholderText('Invalid input')
        self.mise_action6 = QWidget()
        self.mise_action6.setGeometry(500,500,200,200)
        self.mise_action6.setStyleSheet("background-color: white")
        self.mise_action6.setWindowTitle("modifier l'adresse.")
        layout = QVBoxLayout(self.mise_action6)
        # Ajouter un QLineEdit pour entrer le numéro de carte d'identité
        label1 = QLabel("Numéro de cin:", self.mise_action6)
        label1.setStyleSheet("font-weight: bold; font-size: 18pt;")
        cin_edit = QLineEdit()
        cin_edit.setFont(QFont('Arial',20))
        cin_edit.setFixedWidth(400)
        cin_edit.returnPressed.connect(validate_line_edit1)
        layout.addWidget(label1)
        layout.addWidget(cin_edit)
        # Ajouter un QLineEdit pour entrer le numéro de téléphone
        label2 = QLabel("Adresse:", self.mise_action6)
        label2.setStyleSheet("font-weight: bold; font-size: 18pt;")
        adresse_edit = QLineEdit()
        adresse_edit.setFont(QFont('Arial',20))
        adresse_edit.setFixedWidth(400)
        adresse_edit.returnPressed.connect(validate_line_edit2)
        layout.addWidget(label2)
        layout.addWidget(adresse_edit)
        # Ajouter un QPushButton pour effectuer la recherche
        modifier_button = QPushButton("modifier")
        modifier_button.setFixedWidth(400)
        modifier_button.setStyleSheet("background-color: #007acc; color: black; font-size: 16px; padding: 10px 20px; border-radius: 50px;")
        layout.addWidget(modifier_button)
        # Ajouter un QPushButton pour fermer la fenêtre
        close_button = QPushButton("Fermer la fenêtre")
        close_button.setFixedWidth(400)
        close_button.setStyleSheet("background-color: white; color: black; font-size: 16px; padding: 10px 20px; border-radius: 50px;")
        layout.addWidget(close_button)
        layout.setAlignment(Qt.AlignCenter)
        def modifier_adresse():
            cin=cin_edit.text()
            adresse=adresse_edit.text()
            if not tous_les_champs_remplis() :
                error_message = QtWidgets.QMessageBox()
                error_message.setIcon(QtWidgets.QMessageBox.Warning)
                error_message.setWindowTitle("Erreur")
                error_message.setText("Veuillez remplir tous les champs avnt de modifier.")

                # Personnaliser le texte en gras et de taille plus grande
                error_message.setStyleSheet("QMessageBox QLabel{ font-weight: bold; font-size: 25px; }")

                # Personnaliser le bouton OK en bleu, en gras et de taille plus grande
                error_message.setStyleSheet("QMessageBox QPushButton{ background-color: #007acc; color: white; font-weight: bold; font-size: 16px; }")

                error_message.exec_()
                return
            elif existe(personne_dict,cin)==True:
                message_box = QtWidgets.QMessageBox()
                message_box.setWindowTitle("Confirmation d'enregistrement")
                message_box.setText("Êtes-vous sûr de vouloir enregistrer cette maladie pour ce personne?")
                message_box.setIcon(QtWidgets.QMessageBox.Warning)
                message_box.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
                message_box.setStyleSheet("font-size: 14pt; font-weight: bold; color: #333; background-color: #fff;")
                response = message_box.exec_()
                if response == QtWidgets.QMessageBox.Yes:
                    liste_personne = personne_dict[cin]
                    liste_personne["adresse"] = adresse
                    message_box = QtWidgets.QMessageBox()
                    message_box.setWindowTitle("modifier adresse")
                    message_box.setText("l'adresse de ce personne est bien modifiée.")
                    message_box.setIcon(QtWidgets.QMessageBox.Information)
                    ok_button = message_box.addButton(QtWidgets.QMessageBox.Ok)
                    message_box.setStyleSheet("font-size: 14pt; font-weight: bold; color: #333; background-color: #fff;")
                    ok_button.setStyleSheet("background-color: #007acc; color: white; font-size: 16px; padding: 10px 20px; border-radius: 50px;")
                    message_box.exec_()
            else:
                message_box = QtWidgets.QMessageBox()
                message_box.setWindowTitle("modifier l'adresse")
                message_box.setText("il n'y a personne ayant ce numéro de carte d'identité.")
                message_box.setIcon(QtWidgets.QMessageBox.Information)
                ok_button = message_box.addButton(QtWidgets.QMessageBox.Ok)
                message_box.setStyleSheet("font-size: 14pt; font-weight: bold; color: #333; background-color: #fff;")
                ok_button.setStyleSheet("background-color: #007acc; color: white; font-size: 16px; padding: 10px 20px; border-radius: 50px;")
                message_box.exec_()
        #Définir la fonction qui sera appelée lorsqu'on clique sur le bouton de fermeture
        def close_window():
            self.mise_action6.close()
        # Connecter la fonction de fermeture au bouton de fermeture
        close_button.clicked.connect(close_window)
        modifier_button.clicked.connect(modifier_adresse)
        self.mise_action6.show()
    def show_window13(self):
        def verifier_personne(code):
            for cle, info in maladie_dict.items():
                if cle== code :
                    return True
            return False
        def validate_line_edit1():
            data = line_edit1.text()
            if not data.isdigit() or len(data)<=1:
                line_edit1.clear()
                line_edit1.setPlaceholderText('Invalid input')
        def validate_line_edit2():
            data = line_edit2.text()
            if  not data.isdigit() or len(data)!=8:
                line_edit2.clear()
                line_edit2.setPlaceholderText('Invalid input')
        def validate_line_edit3():
            data = line_edit3.text()
            if  not data.isalpha():
                line_edit3.clear()
                line_edit3.setPlaceholderText('Invalid input')
        def validate_line_edit4():
            data = line_edit4.text()
            if  not data.isnumeric() or len(data)>2 or len(data)<1:
                line_edit4.clear()
                line_edit4.setPlaceholderText('Invalid input')
        def fermer_fenetre():
            self.Mise_action1.close()
        def tous_les_champs_remplis():
            champs = [line_edit1, line_edit2, line_edit3, line_edit4]
            for champ in champs:
                if champ.text() == "":
                    return False
            return True
        self.Mise_action1 = QWidget()
        self.Mise_action1.setGeometry(0, 0,500,500)
        self.Mise_action1.setStyleSheet("background-color: white")
        self.Mise_action1.setWindowTitle('ajouter une nouvelle maladie')
        layout = QVBoxLayout(self.Mise_action1)
        # Create QLabel instances and add them to the layout
        label1 = QLabel('Code :', self.Mise_action1)
        label1.setStyleSheet("font-weight: bold; font-size: 18pt;")
        line_edit1 = QLineEdit(self.Mise_action1)
        line_edit1.setFont(QFont('Arial',20))
        line_edit1.setFixedWidth(400)
        line_edit1.returnPressed.connect(validate_line_edit1)
        line_edit1.returnPressed.connect(lambda: line_edit2.setFocus())
        layout.addWidget(label1)
        layout.addWidget(line_edit1)
        
        label2 = QLabel('CIN :', self.Mise_action1)
        label2.setStyleSheet("font-weight: bold; font-size: 18pt;")
        line_edit2 = QLineEdit(self.Mise_action1)
        line_edit2.setFont(QFont('Arial',20))
        line_edit2.setFixedWidth(400)
        line_edit2.returnPressed.connect(validate_line_edit2)
        line_edit2.returnPressed.connect(lambda: line_edit3.setFocus())
        layout.addWidget(label2)
        layout.addWidget(line_edit2)
        
        label3 = QLabel('Nom maladie :', self.Mise_action1)
        label3.setStyleSheet("font-weight: bold; font-size: 18pt;")
        line_edit3 = QLineEdit(self.Mise_action1)
        line_edit3.setFont(QFont('Arial',20))
        line_edit3.setFixedWidth(400)
        line_edit3.returnPressed.connect(validate_line_edit3)
        line_edit3.returnPressed.connect(lambda: line_edit4.setFocus())
        layout.addWidget(label3)
        layout.addWidget(line_edit3)
        
        label4 = QLabel('Nombre d\'années :', self.Mise_action1)
        label4.setStyleSheet("font-weight: bold; font-size: 18pt;")
        line_edit4 = QLineEdit(self.Mise_action1)
        line_edit4.setFont(QFont('Arial',20))
        line_edit4.setFixedWidth(400)
        line_edit4.returnPressed.connect(validate_line_edit4)
        layout.addWidget(label4)
        layout.addWidget(line_edit4)
        # Ajouter un bouton pour enregistrer les informations de la personne
        button_enregistrer = QPushButton('Enregistrer', self.Mise_action1)
        button_enregistrer.setFixedWidth(400)
        button_enregistrer.setStyleSheet("background-color: #007acc; color: white; font-size: 16px; padding: 10px 20px; border-radius: 50px;")
        layout.addWidget(button_enregistrer)
        #Ajouter un bouton pour fermer la fenêtre
        button_fermer = QPushButton('Fermer', self.Mise_action1)
        button_fermer.setFixedWidth(400)
        button_fermer.setStyleSheet("background-color: #007acc; color: white; font-size: 16px; padding: 10px 20px; border-radius: 50px;")
        layout.addWidget(button_fermer)
        layout.setAlignment(Qt.AlignCenter)
        def enregistrer_maladie(self):
            # Vérifier si tous les champs sont remplis
            if not tous_les_champs_remplis() :
                error_message = QtWidgets.QMessageBox()
                error_message.setIcon(QtWidgets.QMessageBox.Warning)
                error_message.setWindowTitle("Erreur")
                error_message.setText("Veuillez remplir tous les champs avant d'enregistrer une maladie.")

                # Personnaliser le texte en gras et de taille plus grande
                error_message.setStyleSheet("QMessageBox QLabel{ font-weight: bold; font-size: 25px; }")

                # Personnaliser le bouton OK en bleu, en gras et de taille plus grande
                error_message.setStyleSheet("QMessageBox QPushButton{ background-color: #007acc; color: white; font-weight: bold; font-size: 16px; }")

                error_message.exec_()
                return
            # Ajouter les informations de la personne au dictionnaire
            code = line_edit1.text()
            cin = line_edit2.text()
            nom = line_edit3.text()
            nb_année = line_edit4.text()
            if(verifier_personne(code)==True):
                error_message = QtWidgets.QMessageBox()
                error_message.setIcon(QtWidgets.QMessageBox.Warning)
                error_message.setWindowTitle("Erreur")
                error_message.setText("Ce code séquentiel est déja utilisé.Il faut le modifier.")

                # Personnaliser le texte en gras et de taille plus grande
                error_message.setStyleSheet("QMessageBox QLabel{ font-weight: bold; font-size: 25px; }")

                # Personnaliser le bouton OK en bleu, en gras et de taille plus grande
                error_message.setStyleSheet("QMessageBox QPushButton{ background-color: #007acc; color: white; font-weight: bold; font-size: 16px; }")

                error_message.exec_()
                line_edit1.setText("")
                return
                
            if(existe(personne_dict,cin)==False):
                error_message = QtWidgets.QMessageBox()
                error_message.setIcon(QtWidgets.QMessageBox.Warning)
                error_message.setWindowTitle("Erreur")
                error_message.setText("Ce CIN n'existe pas.Il faut enregistrer ce personne d'abord.")

                # Personnaliser le texte en gras et de taille plus grande
                error_message.setStyleSheet("QMessageBox QLabel{ font-weight: bold; font-size: 25px; }")

                # Personnaliser le bouton OK en bleu, en gras et de taille plus grande
                error_message.setStyleSheet("QMessageBox QPushButton{ background-color: #007acc; color: white; font-weight: bold; font-size: 16px; }")

                error_message.exec_()
                return
            else:
                message_box = QtWidgets.QMessageBox()
                message_box.setWindowTitle("Confirmation d'enregistrement")
                message_box.setText("Êtes-vous sûr de vouloir enregistrer cette maladie pour ce personne?")
                message_box.setIcon(QtWidgets.QMessageBox.Warning)
                message_box.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
                message_box.setStyleSheet("font-size: 14pt; font-weight: bold; color: #333; background-color: #fff;")
                response = message_box.exec_()
                if response == QtWidgets.QMessageBox.Yes:
                    list={'CIN':cin,'nom maladie':nom,"nombre d'années":nb_année}
                    maladie_dict[code]=list
                    # Vider les champs de texte après avoir enregistré la personne
                    line_edit1.setText("")
                    line_edit2.setText("")
                    line_edit3.setText("")
                    line_edit4.setText("")
                    message_box = QtWidgets.QMessageBox()
                    message_box.setWindowTitle("enregistrement personne")
                    message_box.setText("Cette maladie est bien enregistré pour ce personne.")
                    message_box.setIcon(QtWidgets.QMessageBox.Information)
                    ok_button = message_box.addButton(QtWidgets.QMessageBox.Ok)
                    message_box.setStyleSheet("font-size: 14pt; font-weight: bold; color: #333; background-color: #fff;")
                    ok_button.setStyleSheet("background-color: #007acc; color: white; font-size: 16px; padding: 10px 20px; border-radius: 50px;")
                    message_box.exec_()
        button_enregistrer.clicked.connect(enregistrer_maladie)
        button_fermer.clicked.connect(fermer_fenetre)
        self.Mise_action1.show()
    def show_window14(self):
        def verifier_personne(cin, nom):
            for code, info in maladie_dict.items():
                if info['CIN'] == cin and info['nom maladie'] == nom:
                    return True
            return False
        def tous_les_champs_remplis():
            champs = [cin_edit,nom_edit,nb_années_edit]
            for champ in champs:
                if champ.text() == "":
                    return False
            return True
        def validate_line_edit1():
            data = cin_edit.text()
            if not data.isnumeric() or len(data)!=8:
                cin_edit.clear()
                cin_edit.setPlaceholderText('Invalid input')
        def validate_line_edit3():
            data = nb_années_edit.text()
            if not data.isnumeric():
                nb_années_edit.clear()
                nb_années_edit.setPlaceholderText('Invalid input')
        def validate_line_edit2():
            data = nom_edit.text()
            if not data.isalpha():
                nom_edit.clear()
                nom_edit.setPlaceholderText('Invalid input')
        self.Mise_action3 = QWidget()
        self.Mise_action3.setGeometry(0, 0,500,500)
        self.Mise_action3.setStyleSheet("background-color: white")
        self.Mise_action3.setWindowTitle('modifier le nombres d\'années.')
        layout = QVBoxLayout(self.Mise_action3)
        # Ajouter un QLineEdit pour entrer le numéro de carte d'identité
        label1 = QLabel("Numéro de carte d'identité:", self.Mise_action3)
        label1.setStyleSheet("font-weight: bold; font-size: 18pt;")
        cin_edit = QLineEdit()
        cin_edit.setFont(QFont('Arial',20))
        cin_edit.setFixedWidth(400)
        cin_edit.returnPressed.connect(validate_line_edit1)
        cin_edit.returnPressed.connect(lambda: nom_edit.setFocus())
        layout.addWidget(label1)
        layout.addWidget(cin_edit)
        # Ajouter un QLineEdit pour entrer le numéro de téléphone
        label2 = QLabel("Nom de maladie", self.Mise_action3)
        label2.setStyleSheet("font-weight: bold; font-size: 18pt;")
        nom_edit = QLineEdit()
        nom_edit.setFont(QFont('Arial',20))
        nom_edit.setFixedWidth(400)
        nom_edit.returnPressed.connect(validate_line_edit2)
        nom_edit.returnPressed.connect(lambda: nb_années_edit.setFocus())
        layout.addWidget(label2)
        layout.addWidget(nom_edit)
        
        label3 = QLabel("Nom de maladie", self.Mise_action3)
        label3.setStyleSheet("font-weight: bold; font-size: 18pt;")
        nb_années_edit = QLineEdit()
        nb_années_edit.setFont(QFont('Arial',20))
        nb_années_edit.setFixedWidth(400)
        nb_années_edit.returnPressed.connect(validate_line_edit3)
        layout.addWidget(label3)
        layout.addWidget(nb_années_edit)
        # Ajouter un QPushButton pour effectuer la recherche
        button_enregistrer = QPushButton('Modifier', self.Mise_action3)
        button_enregistrer.setFixedWidth(400)
        button_enregistrer.setStyleSheet("background-color: #007acc; color: white; font-size: 16px; padding: 10px 20px; border-radius: 50px;")
        layout.addWidget(button_enregistrer)
        #Ajouter un bouton pour fermer la fenêtre
        button_fermer = QPushButton('Fermer', self.Mise_action3)
        button_fermer.setFixedWidth(400)
        button_fermer.setStyleSheet("background-color: #007acc; color: white; font-size: 16px; padding: 10px 20px; border-radius: 50px;")
        layout.addWidget(button_fermer)
        layout.setAlignment(Qt.AlignCenter)
        def modifier_nb_années():
            cin=cin_edit.text()
            nom=nom_edit.text()
            nb_annees=nb_années_edit.text()
            if not tous_les_champs_remplis() :
                error_message = QtWidgets.QMessageBox()
                error_message.setIcon(QtWidgets.QMessageBox.Warning)
                error_message.setWindowTitle("Erreur")
                error_message.setText("Veuillez remplir tous les champs .")

                # Personnaliser le texte en gras et de taille plus grande
                error_message.setStyleSheet("QMessageBox QLabel{ font-weight: bold; font-size: 25px; }")

                # Personnaliser le bouton OK en bleu, en gras et de taille plus grande
                error_message.setStyleSheet("QMessageBox QPushButton{ background-color: #007acc; color: white; font-weight: bold; font-size: 16px; }")

                error_message.exec_()
                return
            # Vérifier si la personne existe dans le dictionnaire
            elif not verifier_personne(cin, nom):
                error_message = QtWidgets.QMessageBox()
                error_message.setIcon(QtWidgets.QMessageBox.Warning)
                error_message.setWindowTitle("Erreur")
                error_message.setText("La personne avec le numéro de CIN et le nom de maladie donnés n'existe pas.")

                # Personnaliser le texte en gras et de taille plus grande
                error_message.setStyleSheet("QMessageBox QLabel{ font-weight: bold; font-size: 25px; }")

                # Personnaliser le bouton OK en bleu, en gras et de taille plus grande
                error_message.setStyleSheet("QMessageBox QPushButton{ background-color: #007acc; color: white; font-weight: bold; font-size: 16px; }")

                error_message.exec_()
                cin_edit.setText("")
                nom_edit.setText("")
                nb_années_edit.setText("")
                return
            # Modifier le nombre d'années de la maladie
            else:
                message_box = QtWidgets.QMessageBox()
                message_box.setWindowTitle("Confirmation d'enregistrement")
                message_box.setText("Êtes-vous sûr de vouloir enregistrer cette maladie pour ce personne?")
                message_box.setIcon(QtWidgets.QMessageBox.Warning)
                message_box.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
                message_box.setStyleSheet("font-size: 14pt; font-weight: bold; color: #333; background-color: #fff;")
                response = message_box.exec_()
                if response == QtWidgets.QMessageBox.Yes:
                    for code, info in maladie_dict.items():
                        if info['CIN'] == cin and info['nom maladie'] == nom:
                            info["nombre d'années"] = nb_annees
                    # Vider les champs de texte après avoir modifié le nombre d'années
                    cin_edit.setText("")
                    nom_edit.setText("")
                    nb_années_edit.setText("")
                    message_box = QtWidgets.QMessageBox()
                    message_box.setWindowTitle("enregistrement personne")
                    message_box.setText("le nombre d'années est bien modifier.")
                    message_box.setIcon(QtWidgets.QMessageBox.Information)
                    ok_button = message_box.addButton(QtWidgets.QMessageBox.Ok)
                    message_box.setStyleSheet("font-size: 14pt; font-weight: bold; color: #333; background-color: #fff;")
                    ok_button.setStyleSheet("background-color: #007acc; color: white; font-size: 16px; padding: 10px 20px; border-radius: 50px;")
                    message_box.exec_()
        #Définir la fonction qui sera appelée lorsqu'on clique sur le bouton de fermeture
        def close_window():
            self.Mise_action3.close()
        # Connecter la fonction de fermeture au bouton de fermeture
        button_fermer.clicked.connect(close_window)
        button_enregistrer.clicked.connect(modifier_nb_années)
        self.Mise_action3.show()
    def show_window15(self):
        def verifier_personne(cin):
            for code, info in personne_dict.items():
                if code == cin :
                    return True
            return False
        def tous_les_champs_remplis():
            champs = [cin_edit]
            for champ in champs:
                if champ.text() == "":
                    return False
            return True
        def validate_line_edit1():
            data = cin_edit.text()
            if not data.isnumeric() or len(data)!=8:
                cin_edit.clear()
                cin_edit.setPlaceholderText('Invalid input')
        self.Mise_action4 = QWidget()
        self.Mise_action4.setGeometry(0, 0,200,200)
        self.Mise_action4.setStyleSheet("background-color: white")
        self.Mise_action4.setWindowTitle('modifier décés')
        layout = QVBoxLayout(self.Mise_action4)
        # Ajouter un QLineEdit pour entrer le numéro de carte d'identité
        label1 = QLabel("Numéro de carte d'identité:", self.Mise_action4)
        label1.setStyleSheet("font-weight: bold; font-size: 18pt;")
        cin_edit = QLineEdit()
        cin_edit.setFont(QFont('Arial',20))
        cin_edit.setFixedWidth(400)
        cin_edit.returnPressed.connect(validate_line_edit1)
        cin_edit.returnPressed.connect(lambda: cin_edit.setFocus())
        layout.addWidget(label1)
        layout.addWidget(cin_edit)
        # Ajouter un QPushButton pour effectuer la recherche
        button_enregistrer = QPushButton('Modifier', self.Mise_action4)
        button_enregistrer.setFixedWidth(400)
        button_enregistrer.setStyleSheet("background-color: #007acc; color: white; font-size: 16px; padding: 10px 20px; border-radius: 50px;")
        layout.addWidget(button_enregistrer)
        #Ajouter un bouton pour fermer la fenêtre
        button_fermer = QPushButton('Fermer', self.Mise_action4)
        button_fermer.setFixedWidth(400)
        button_fermer.setStyleSheet("background-color: #007acc; color: white; font-size: 16px; padding: 10px 20px; border-radius: 50px;")
        layout.addWidget(button_fermer)
        layout.setAlignment(Qt.AlignCenter)
        def modifier_décés():
            cin=cin_edit.text()
            if not tous_les_champs_remplis() :
                error_message = QtWidgets.QMessageBox()
                error_message.setIcon(QtWidgets.QMessageBox.Warning)
                error_message.setWindowTitle("Erreur")
                error_message.setText("Veuillez remplir le champ du numéro de carte d'identité")

                # Personnaliser le texte en gras et de taille plus grande
                error_message.setStyleSheet("QMessageBox QLabel{ font-weight: bold; font-size: 25px; }")

                # Personnaliser le bouton OK en bleu, en gras et de taille plus grande
                error_message.setStyleSheet("QMessageBox QPushButton{ background-color: #007acc; color: white; font-weight: bold; font-size: 16px; }")

                error_message.exec_()
                return
            # Vérifier si la personne existe dans le dictionnaire
            elif not verifier_personne(cin) :
                error_message = QtWidgets.QMessageBox()
                error_message.setIcon(QtWidgets.QMessageBox.Warning)
                error_message.setWindowTitle("Erreur")
                error_message.setText("La personne avec le numéro de CIN n'existe pas.")

                # Personnaliser le texte en gras et de taille plus grande
                error_message.setStyleSheet("QMessageBox QLabel{ font-weight: bold; font-size: 25px; }")

                # Personnaliser le bouton OK en bleu, en gras et de taille plus grande
                error_message.setStyleSheet("QMessageBox QPushButton{ background-color: #007acc; color: white; font-weight: bold; font-size: 16px; }")

                error_message.exec_()
                cin_edit.setText("")
                return
            # Modifier décés
            else:
                message_box = QtWidgets.QMessageBox()
                message_box.setWindowTitle("Confirmation d'enregistrement")
                message_box.setText("Êtes-vous sûr de vouloir enregistrer cette personne comme décédé?")
                message_box.setIcon(QtWidgets.QMessageBox.Warning)
                message_box.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
                message_box.setStyleSheet("font-size: 14pt; font-weight: bold; color: #333; background-color: #fff;")
                response = message_box.exec_()
                if response == QtWidgets.QMessageBox.Yes:
                    liste_personne = personne_dict[cin]
                    liste_personne["decédé"] = "1"
                    # Vider les champs de texte après avoir modifié le nombre d'années
                    cin_edit.setText("")
                    message_box = QtWidgets.QMessageBox()
                    message_box.setWindowTitle("modifier décédé")
                    message_box.setText("la modification est bien réalisée.")
                    message_box.setIcon(QtWidgets.QMessageBox.Information)
                    ok_button = message_box.addButton(QtWidgets.QMessageBox.Ok)
                    message_box.setStyleSheet("font-size: 14pt; font-weight: bold; color: #333; background-color: #fff;")
                    ok_button.setStyleSheet("background-color: #007acc; color: white; font-size: 16px; padding: 10px 20px; border-radius: 50px;")
                    message_box.exec_()
        #Définir la fonction qui sera appelée lorsqu'on clique sur le bouton de fermeture
        def close_window():
            self.Mise_action4.close()
        # Connecter la fonction de fermeture au bouton de fermeture
        button_fermer.clicked.connect(close_window)
        button_enregistrer.clicked.connect(modifier_décés)
        self.Mise_action4.show()
    def show_window16(self):
        def tous_les_champs_remplis():
            champs = [maladie_edit]
            for champ in champs:
                if champ.text() == "":
                    return False
            return True
        def validate_line_edit1():
            data = maladie_edit.text()
            if not data.isalpha():
                maladie_edit.clear()
                maladie_edit.setPlaceholderText('Invalid input')
        self.Mise_action2 = QWidget()
        self.Mise_action2.setGeometry(200,200,500,500)
        self.Mise_action2.setStyleSheet("background-color: #f2f2f2")
        self.Mise_action2.setWindowTitle('supprimer maladie')
        layout = QVBoxLayout(self.Mise_action2)
        # Ajouter un QLineEdit pour entrer le numéro de carte d'identité
        maladie_edit = QLineEdit()
        maladie_edit.setFont(QFont('Arial', 30))
        maladie_edit.returnPressed.connect(validate_line_edit1)
        num_label = QLabel("Non du maladie:")
        num_label.setStyleSheet("font-weight: bold; font-size: 20pt;")
        layout.addWidget(num_label)
        maladie_edit.setFixedWidth(400)

        # mettre le texte en gras
        maladie_edit.setStyleSheet("font-weight: bold")
        layout.addWidget(maladie_edit)
        suppression_button = QPushButton("Supprimer")
        suppression_button.setFixedWidth(400)
        suppression_button.setStyleSheet("background-color: #007acc; color: white; font-size: 16px; padding: 10px 20px; border-radius: 50px;")
        layout.addWidget(suppression_button)
        # Ajouter un QPushButton pour fermer la fenêtre
        close_button = QPushButton("Fermer")
        close_button.setFixedWidth(400)
        close_button.setStyleSheet("background-color: #007acc; color: white; font-size: 16px; padding: 10px 20px; border-radius: 50px;")
        layout.addWidget(close_button)
        layout.setAlignment(Qt.AlignCenter)
        
        def supprimer_maladie():
            nom=maladie_edit.text()
            if not tous_les_champs_remplis() :
                error_message = QtWidgets.QMessageBox()
                error_message.setIcon(QtWidgets.QMessageBox.Warning)
                error_message.setWindowTitle("Erreur")
                error_message.setText("Veuillez remplir le champ du numéro de carte d'identité avant de supprimer.")

                # Personnaliser le texte en gras et de taille plus grande
                error_message.setStyleSheet("QMessageBox QLabel{ font-weight: bold; font-size: 25px; }")

                # Personnaliser le bouton OK en bleu, en gras et de taille plus grande
                error_message.setStyleSheet("QMessageBox QPushButton{ background-color: #007acc; color: white; font-weight: bold; font-size: 16px; }")

                error_message.exec_()
                return
            else:
                message_box = QtWidgets.QMessageBox(self)
                message_box.setWindowTitle("Confirmation de suppression")
                message_box.setText("Êtes-vous sûr de vouloir supprimer les personnes ayant cette numéro d'identité?")
                message_box.setIcon(QtWidgets.QMessageBox.Warning)
                message_box.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
                message_box.setStyleSheet("font-size: 14pt; font-weight: bold; color: #333; background-color: #fff;")
                response = message_box.exec_()
                if response == QtWidgets.QMessageBox.Yes:
                    keys_to_remove = []
                    for code, info in maladie_dict.items():
                        if info['nom maladie'] == nom:
                            keys_to_remove.append(code)

                    for code in keys_to_remove:
                        del maladie_dict[code]
                    message_box = QtWidgets.QMessageBox(self)
                    message_box.setWindowTitle("Suppression une maladie")
                    message_box.setText("Cette maladie est bien supprimé")
                    message_box.setIcon(QtWidgets.QMessageBox.Information)
                    ok_button = message_box.addButton(QtWidgets.QMessageBox.Ok)
                    message_box.setStyleSheet("font-size: 14pt; font-weight: bold; color: #333; background-color: #fff;")
                    ok_button.setStyleSheet("background-color: #007acc; color: white; font-size: 16px; padding: 10px 20px; border-radius: 50px;")
                    message_box.exec_()
            # Vider les champs de texte après avoir modifié le nombre d'années
            maladie_edit.setText("")
            
        #Définir la fonction qui sera appelée lorsqu'on clique sur le bouton de fermeture
        def close_window():
            self.Mise_action2.close()
        # Connecter la fonction de fermeture au bouton de fermeture
        close_button.clicked.connect(close_window)
        suppression_button.clicked.connect(supprimer_maladie)
        self.Mise_action2.show()
    def show_window17(self):
        layout = QVBoxLayout()
        result=contenu_dictionnaire(maladie_dict)
        count = len(result)
        personnes_dicte = []
        for cle, infos in maladie_dict.items():
            prenom = infos['CIN']
            age =infos['nom maladie']
            adresse=infos['nombre d\'années']
            personnes_dicte.append((cle, prenom, age, adresse)) # Ajouter le numéro de carte d'identité et les informations de la personne à la liste des personnes en quarantaine
       
        if maladie_dict:
            # Set window title
            self.setWindowTitle("Contenu du dictionnaire maladies")
            
            # Create table widget
            self.table = QTableWidget(self)
            self.table.setColumnCount(4)
            self.table.setHorizontalHeaderLabels(['Code', "Numéro de carte d'identité", "Nom maladie", "Nombre d'années"])
            self.table.setRowCount(count)
            
            # Define cell style for headers
            bold_font = QtGui.QFont()
            bold_font.setBold(True)
            blue_background = QtGui.QBrush(QtGui.QColor(230, 230, 230)) # Blue background color
            item_code = QtWidgets.QTableWidgetItem("Code")
            item_code.setFont(bold_font)
            item_code.setBackground(blue_background)
            self.table.setItem(0, 0, item_code)
            item_identite = QtWidgets.QTableWidgetItem("Numéro de carte d'identité")
            item_identite.setFont(bold_font)
            item_identite.setBackground(blue_background)
            self.table.setItem(0, 1, item_identite)
            item_nom = QtWidgets.QTableWidgetItem("Nom maladie")
            item_nom.setFont(bold_font)
            item_nom.setBackground(blue_background)
            self.table.setItem(0, 2, item_nom)
            item_annees = QtWidgets.QTableWidgetItem("Nombre d'années")
            item_annees.setFont(bold_font)
            item_annees.setBackground(blue_background)
            self.table.setItem(0, 3, item_annees)
            
            # Define style of the table
            self.table.setStyleSheet("""
                QTableWidget { background-color: white; color: black; font-size: 12pt; font-weight: bold; }
                QHeaderView::section { background-color: #007acc; color: white; font-size: 12pt; font-weight: bold; }
            """)
            
            # Populate table with data from dictionary
            self.table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
            for i, maladie in enumerate(personnes_dicte):
                for j in range(len(maladie)):
                    item = QTableWidgetItem(str(maladie[j]))
                    item.setTextAlignment(QtCore.Qt.AlignCenter)
                    self.table.setItem(i, j, item)
            font = QtGui.QFont()
            font.setBold(True)
            self.table.setFont(font)
            
            # Add table widget to layout
            layout = QtWidgets.QVBoxLayout()
            self.table.resizeColumnsToContents()
            layout.addWidget(self.table)
            
            
            # Create and show table dialog window
            self.table_dialog = QtWidgets.QDialog(self)
            self.table_dialog.setLayout(layout)
            # Add close button
            button_box = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Close)
            button_box.rejected.connect(self.table_dialog.reject)
            layout.addWidget(button_box)
            button_box.setStyleSheet("background-color: #007acc;")
            self.table_dialog.setWindowTitle("Contenu du dictionnaire maladies")
            self.table_dialog.resize(2000, 1000)
            self.table_dialog.show()  
            
        else:
            message_box = QtWidgets.QMessageBox(self)
            message_box = QtWidgets.QMessageBox(self)
            message_box.setWindowTitle('contenu de dictionnaire maladies')
            message_box.setText("Le dictionnaire est vide")
            message_box.setIcon(QtWidgets.QMessageBox.Information)
            ok_button = message_box.addButton(QtWidgets.QMessageBox.Ok)
            message_box.setStyleSheet("font-size: 14pt; font-weight: bold; color: #333; background-color: #fff;") 
            ok_button.setStyleSheet("background-color: #007acc; color: white; font-size: 16px; padding: 10px 20px; border-radius: 50px;")
            message_box.exec()
    def show_window18(self):
        def tous_les_champs_remplis():
            champs = [nom_edit]
            for champ in champs:
                if champ.text() == "":
                    return False
            return True
        def validate_line_edit1():
            data = nom_edit.text()
            if not data.isalpha():
                nom_edit.clear()
                nom_edit.setPlaceholderText('Invalid input')
        self.Recherche_action2 = QWidget()
        self.Recherche_action2.setGeometry(500,500,200,200)
        self.Recherche_action2.setStyleSheet("background-color: white")
        self.Recherche_action2.setWindowTitle('Recherche par une maladie')
        layout = QVBoxLayout(self.Recherche_action2)
        # Ajouter un QLineEdit pour entrer le numéro de carte d'identité
        label1 = QLabel("Nom maladie:", self.Recherche_action2)
        label1.setStyleSheet("font-weight: bold; font-size: 18pt;")
        nom_edit = QLineEdit()
        nom_edit.setFont(QFont('Arial',20))
        nom_edit.setFixedWidth(400)
        nom_edit.returnPressed.connect(validate_line_edit1)
        layout.addWidget(label1)
        layout.addWidget(nom_edit)
        # Ajouter un QPushButton pour effectuer la recherche
        recherche_button = QPushButton("rechercher")
        recherche_button.setFixedWidth(400)
        recherche_button.setStyleSheet("background-color: #007acc; color: black; font-size: 16px; padding: 10px 20px; border-radius: 50px;")
        layout.addWidget(recherche_button)
        # Ajouter un QPushButton pour fermer la fenêtre
        close_button = QPushButton("Fermer la fenêtre")
        close_button.setFixedWidth(400)
        close_button.setStyleSheet("background-color: white; color: black; font-size: 16px; padding: 10px 20px; border-radius: 50px;")
        layout.addWidget(close_button)
        layout.setAlignment(Qt.AlignCenter)
        def afficher_maladie():
            nom=nom_edit.text()
            if not tous_les_champs_remplis() :
                error_message = QtWidgets.QMessageBox()
                error_message.setIcon(QtWidgets.QMessageBox.Warning)
                error_message.setWindowTitle("Erreur")
                error_message.setText("Veuillez remplir le champ du nom du maladie avant de chercher.")

                # Personnaliser le texte en gras et de taille plus grande
                error_message.setStyleSheet("QMessageBox QLabel{ font-weight: bold; font-size: 25px; }")

                # Personnaliser le bouton OK en bleu, en gras et de taille plus grande
                error_message.setStyleSheet("QMessageBox QPushButton{ background-color: #007acc; color: white; font-weight: bold; font-size: 16px; }")

                error_message.exec_()
                return
            else:
                result = [] # Liste pour stocker les résultats de toutes les personnes ayant la maladie recherchée
                for code, info in maladie_dict.items():
                    if info['nom maladie'] == nom: 
                        cin = info['CIN']
                        dictionnaire_dict = {cin: personne_dict[cin]}
                        result.extend(contenu_dictionnaire(dictionnaire_dict))
                count=len(result)
                if result:
                    layout = QVBoxLayout()
                    # Créer le QLabel pour afficher le pourcentage
                    pourcentage_label = QLabel(f"Nombres des personnes ayant cette maladie: {count}")
                    pourcentage_label.setAlignment(Qt.AlignCenter)
                    font = QFont("Arial", 16)
                    font.setBold(True)
                    pourcentage_label.setFont(font)
                    
                    self.table = QTableWidget(self)
                    self.table.setColumnCount(9)
                    self.table.setHorizontalHeaderLabels(["Numéro de carte d'identité", "Nom", "Prénom", "Âge", "Adresse", "Nationalité", "Numéro de téléphone", "Date d'infection", "Décédé"])
                    self.table.setRowCount(len(result))
                    
                    # Définir le style des cellules contenant les mots "Nom", "Prénom" et "Risque"
                    bold_font = QtGui.QFont()
                    bold_font.setBold(True)
                    blue_background = QtGui.QBrush(QtGui.QColor(230,230,230)) # couleur de fond bleue
                    
                    item_nom = QtWidgets.QTableWidgetItem("nom")
                    item_nom.setFont(bold_font)
                    item_nom.setBackground(blue_background)
                    self.table.setItem(0, 0, item_nom)

                    item_prenom = QtWidgets.QTableWidgetItem("prenom")
                    item_prenom.setFont(bold_font)
                    item_prenom.setBackground(blue_background)
                    self.table.setItem(0, 1, item_prenom)

                    item_age = QtWidgets.QTableWidgetItem("age")
                    item_age.setFont(bold_font)
                    item_age.setBackground(blue_background)
                    self.table.setItem(0, 2, item_age)
                    
                    item_adresse = QtWidgets.QTableWidgetItem("adresse")
                    item_adresse.setFont(bold_font)
                    item_adresse.setBackground(blue_background)
                    self.table.setItem(0, 3, item_adresse)
                    
                    item_nationalité = QtWidgets.QTableWidgetItem("nationalité")
                    item_nationalité.setFont(bold_font)
                    item_nationalité.setBackground(blue_background)
                    self.table.setItem(0, 4, item_nationalité)
                    
                    item_numéro_telephone = QtWidgets.QTableWidgetItem("numéro_telephone")
                    item_numéro_telephone.setFont(bold_font)
                    item_numéro_telephone.setBackground(blue_background)
                    self.table.setItem(0, 5, item_numéro_telephone)
                    
                    item_date_infectation = QtWidgets.QTableWidgetItem("date d'infectation")
                    item_date_infectation.setFont(bold_font)
                    item_date_infectation.setBackground(blue_background)
                    self.table.setItem(0,6, item_date_infectation)
                    
                    item_décédé = QtWidgets.QTableWidgetItem("décédé")
                    item_décédé.setFont(bold_font)
                    item_décédé.setBackground(blue_background)
                    self.table.setItem(0,7, item_décédé)
                    
                    # Définir le style du tableau
                    self.table.setStyleSheet("""
                        QTableWidget { background-color: white; color: black; font-size: 12pt; font-weight: bold; }
                        QHeaderView::section { background-color: #007acc; color: white; font-size: 12pt; font-weight: bold; }
                    """)
                    
                    self.table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
                    for i, (cle, personne) in enumerate(result):
                        # Assigner la clé de la personne à la première colonne de la ligne i
                        self.table.setItem(i, 0, QTableWidgetItem(str(cle)))
                        
                        # Assigner les autres attributs de la personne aux colonnes suivantes
                        for j, item in enumerate(personne.values()):
                            self.table.setItem(i, j+1, QTableWidgetItem(str(item)))
                            self.table.item(i, j+1).setTextAlignment(QtCore.Qt.AlignCenter)
                    font = QtGui.QFont()
                    font.setBold(True)
                    self.table.setFont(font)
                    
                    layout.addWidget(pourcentage_label)
                    # Redimensionner la largeur des colonnes pour s'adapter au contenu
                    self.table.resizeColumnsToContents()
                    layout.addWidget(self.table)
                    self.table_dialog = QtWidgets.QDialog(self) # initialisez ici
                    button_box = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Close)
                    button_box.rejected.connect(self.table_dialog.reject)
                    layout.addWidget(button_box)
                    button_box.setStyleSheet("background-color: #007acc;")
                    self.table_dialog.setLayout(layout)
                    self.table_dialog.setWindowTitle("recherche personne par numéro de téléphone")
                    self.table_dialog.resize(2000,1000)
                    self.table_dialog.show()
                else:
                    message_box = QtWidgets.QMessageBox()
                    message_box.setWindowTitle("Recherche par maladie")
                    message_box.setText("il n'y a pas des personnes ayant cette maladie.")
                    message_box.setIcon(QtWidgets.QMessageBox.Information)
                    ok_button = message_box.addButton(QtWidgets.QMessageBox.Ok)
                    message_box.setStyleSheet("font-size: 14pt; font-weight: bold; color: #333; background-color: #fff;")
                    ok_button.setStyleSheet("background-color: #007acc; color: white; font-size: 16px; padding: 10px 20px; border-radius: 50px;")
                    message_box.exec_()  
            # Vider les champs de texte après avoir modifié le nombre d'années
            nom_edit.setText("")
        #Définir la fonction qui sera appelée lorsqu'on clique sur le bouton de fermeture
        def close_window():
            self.Recherche_action2.close()
        # Connecter la fonction de fermeture au bouton de fermeture
        close_button.clicked.connect(close_window)
        recherche_button.clicked.connect(afficher_maladie)
        self.Recherche_action2.show()
    def show_window19(self):
        def tous_les_champs_remplis():
            champs = [cin_edit]
            for champ in champs:
                if champ.text() == "":
                    return False
            return True
        def validate_line_edit1():
            data = cin_edit.text()
            if not data.isnumeric() or len(data)!=8:
                cin_edit.clear()
                cin_edit.setPlaceholderText('Invalid input')
        self.Recherche_action3 = QWidget()
        self.Recherche_action3.setGeometry(500,500,200,200)
        self.Recherche_action3.setStyleSheet("background-color: white")
        self.Recherche_action3.setWindowTitle('recherche maladie d\'une personne')
        layout = QVBoxLayout(self.Recherche_action3)
        # Ajouter un QLineEdit pour entrer le numéro de carte d'identité
        label1 = QLabel("Numéro de carte d'identité:", self.Recherche_action3)
        label1.setStyleSheet("font-weight: bold; font-size: 18pt;")
        cin_edit = QLineEdit()
        cin_edit.setFont(QFont('Arial',20))
        cin_edit.setFixedWidth(400)
        cin_edit.returnPressed.connect(validate_line_edit1)
        layout.addWidget(label1)
        layout.addWidget(cin_edit)
        # Ajouter un QPushButton pour effectuer la recherche
        recherche_button = QPushButton("rechercher")
        recherche_button.setFixedWidth(400)
        recherche_button.setStyleSheet("background-color: #007acc; color: black; font-size: 16px; padding: 10px 20px; border-radius: 50px;")
        layout.addWidget(recherche_button)
        # Ajouter un QPushButton pour fermer la fenêtre
        close_button = QPushButton("Fermer la fenêtre")
        close_button.setFixedWidth(400)
        close_button.setStyleSheet("background-color: white; color: black; font-size: 16px; padding: 10px 20px; border-radius: 50px;")
        layout.addWidget(close_button)
        layout.setAlignment(Qt.AlignCenter)
        def recherche_maladies():
            cin=cin_edit.text()
            if not tous_les_champs_remplis() :
                error_message = QtWidgets.QMessageBox()
                error_message.setIcon(QtWidgets.QMessageBox.Warning)
                error_message.setWindowTitle("Erreur")
                error_message.setText("Veuillez remplir le champ du carte d'identité avant de chercher.")

                # Personnaliser le texte en gras et de taille plus grande
                error_message.setStyleSheet("QMessageBox QLabel{ font-weight: bold; font-size: 25px; }")

                # Personnaliser le bouton OK en bleu, en gras et de taille plus grande
                error_message.setStyleSheet("QMessageBox QPushButton{ background-color: #007acc; color: white; font-weight: bold; font-size: 16px; }")

                error_message.exec_()
                return
            elif(existe(personne_dict,cin)==True):
                result=[]
                for code, info in maladie_dict.items():
                    if  info['CIN'] == cin:
                        dictionnaire_dict = {code: maladie_dict[code]}
                        result.extend(contenu_dictionnaire(dictionnaire_dict))
                count=len(result)
                if result:
                    self.setWindowTitle("Recherche maladie d'une personne.")
                    # Create table widget
                    self.table = QTableWidget(self)
                    self.table.setColumnCount(4)
                    self.table.setHorizontalHeaderLabels(['Code', "Numéro de carte d'identité", "Nom maladie", "Nombre d'années"])
                    self.table.setRowCount(count)
                    # Define cell style for headers
                    bold_font = QtGui.QFont()
                    bold_font.setBold(True)
                    blue_background = QtGui.QBrush(QtGui.QColor(230, 230, 230)) # Blue background color
                    item_code = QtWidgets.QTableWidgetItem("Code")
                    item_code.setFont(bold_font)
                    item_code.setBackground(blue_background)
                    self.table.setItem(0, 0, item_code)
                    item_identite = QtWidgets.QTableWidgetItem("Numéro de carte d'identité")
                    item_identite.setFont(bold_font)
                    item_identite.setBackground(blue_background)
                    self.table.setItem(0, 1, item_identite)
                    item_nom = QtWidgets.QTableWidgetItem("Nom maladie")
                    item_nom.setFont(bold_font)
                    item_nom.setBackground(blue_background)
                    self.table.setItem(0, 2, item_nom)
                    item_annees = QtWidgets.QTableWidgetItem("Nombre d'années")
                    item_annees.setFont(bold_font)
                    item_annees.setBackground(blue_background)
                    self.table.setItem(0, 3, item_annees)
                    
                    # Define style of the table
                    self.table.setStyleSheet("""
                        QTableWidget { background-color: white; color: black; font-size: 12pt; font-weight: bold; }
                        QHeaderView::section { background-color: #007acc; color: white; font-size: 12pt; font-weight: bold; }
                    """)
                    
                    # Populate table with data from dictionary
                    self.table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
                    for i, (cle, personne) in enumerate(result):
                        # Assigner la clé de la personne à la première colonne de la ligne i
                        self.table.setItem(i, 0, QTableWidgetItem(str(cle)))
                        
                        # Assigner les autres attributs de la personne aux colonnes suivantes
                        for j, item in enumerate(personne.values()):
                            self.table.setItem(i, j+1, QTableWidgetItem(str(item)))
                            self.table.item(i, j+1).setTextAlignment(QtCore.Qt.AlignCenter)
                    font = QtGui.QFont()
                    font.setBold(True)
                    self.table.setFont(font)
                    
                    # Add table widget to layout
                    layout = QtWidgets.QVBoxLayout()
                    self.table.resizeColumnsToContents()
                    layout.addWidget(self.table)
                    
                    
                    # Create and show table dialog window
                    self.table_dialog = QtWidgets.QDialog(self)
                    self.table_dialog.setLayout(layout)
                    # Add close button
                    button_box = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Close)
                    button_box.rejected.connect(self.table_dialog.reject)
                    layout.addWidget(button_box)
                    button_box.setStyleSheet("background-color: #007acc;")
                    self.table_dialog.setWindowTitle("recherche maladies d'une personnes")
                    self.table_dialog.resize(2000, 1000)
                    self.table_dialog.show()  
                else:
                    message_box = QtWidgets.QMessageBox(self)
                    message_box = QtWidgets.QMessageBox(self)
                    message_box.setWindowTitle('afficher maladies du cette personne')
                    message_box.setText("Aucun problème de santé n'a été détecté chez cette personne.")
                    message_box.setIcon(QtWidgets.QMessageBox.Information)
                    ok_button = message_box.addButton(QtWidgets.QMessageBox.Ok)
                    message_box.setStyleSheet("font-size: 14pt; font-weight: bold; color: #333; background-color: #fff;") 
                    ok_button.setStyleSheet("background-color: #007acc; color: white; font-size: 16px; padding: 10px 20px; border-radius: 50px;")
                    message_box.exec()    
            # Vider les champs de texte après avoir modifié le nombre d'années
            cin_edit.setText("")
        #Définir la fonction qui sera appelée lorsqu'on clique sur le bouton de fermeture
        def close_window():
            self.Recherche_action3.close()
        # Connecter la fonction de fermeture au bouton de fermeture
        close_button.clicked.connect(close_window)
        recherche_button.clicked.connect(recherche_maladies)
        self.Recherche_action3.show()
    def show_window20(self):
        def tous_les_champs_remplis():
            champs = [nom_edit]
            for champ in champs:
                if champ.text() == "":
                    return False
            return True
        def validate_line_edit1():
            data = nom_edit.text()
            if not data.isalpha():
                nom_edit.clear()
                nom_edit.setPlaceholderText('Invalid input')
        self.Recherche_action4 = QWidget()
        self.Recherche_action4.setGeometry(500,500,500,500)
        self.Recherche_action4.setStyleSheet("background-color: white")
        self.Recherche_action4.setWindowTitle('recherche le pourcentage de chaque maladie')
        layout = QVBoxLayout(self.Recherche_action4)
        # Ajouter un QLineEdit pour entrer le numéro de carte d'identité
        label1 = QLabel("Nom du maladie:", self.Recherche_action4)
        label1.setStyleSheet("font-weight: bold; font-size: 18pt;")
        nom_edit = QLineEdit()
        nom_edit.setFont(QFont('Arial',20))
        nom_edit.setFixedWidth(400)
        nom_edit.returnPressed.connect(validate_line_edit1)
        layout.addWidget(label1)
        layout.addWidget(nom_edit)
        # Ajouter un QPushButton pour effectuer la recherche
        recherche_button = QPushButton("calculer")
        recherche_button.setFixedWidth(400)
        recherche_button.setStyleSheet("background-color: #007acc; color: black; font-size: 16px; padding: 10px 20px; border-radius: 50px;")
        layout.addWidget(recherche_button)
        # Ajouter un QPushButton pour fermer la fenêtre
        close_button = QPushButton("Fermer la fenêtre")
        close_button.setFixedWidth(400)
        close_button.setStyleSheet("background-color: white; color: black; font-size: 16px; padding: 10px 20px; border-radius: 50px;")
        layout.addWidget(close_button)
        layout.setAlignment(Qt.AlignCenter)
        def calculer_maladie():
            nom=nom_edit.text()
            if not tous_les_champs_remplis() :
                error_message = QtWidgets.QMessageBox()
                error_message.setIcon(QtWidgets.QMessageBox.Warning)
                error_message.setWindowTitle("Erreur")
                error_message.setText("Veuillez remplir le champ du nom du maladie.")

                # Personnaliser le texte en gras et de taille plus grande
                error_message.setStyleSheet("QMessageBox QLabel{ font-weight: bold; font-size: 25px; }")

                # Personnaliser le bouton OK en bleu, en gras et de taille plus grande
                error_message.setStyleSheet("QMessageBox QPushButton{ background-color: #007acc; color: white; font-weight: bold; font-size: 16px; }")

                error_message.exec_()
                return
            else:
                x=calculer_pourcentage_maladie(nom)
                if x!=0:
                    message_box = QtWidgets.QMessageBox()
                    message_box.setWindowTitle("recherche le pourcentage de chaque maladie")
                    message = nom + " " + str(x) + "%"
                    message_box.setText(message)
                    message_box.setIcon(QtWidgets.QMessageBox.Information)
                    ok_button = message_box.addButton(QtWidgets.QMessageBox.Ok)
                    message_box.setStyleSheet("font-size: 14pt; font-weight: bold; color: #333; background-color: #fff;")
                    ok_button.setStyleSheet("background-color: #007acc; color: white; font-size: 16px; padding: 10px 20px; border-radius: 50px;")
                    message_box.exec_()
                else:
                    message_box = QtWidgets.QMessageBox()
                    message_box.setWindowTitle("recherche le pourcentage de chaque maladie")
                    message_box.setText("Aucun personne ayant cette maladie")
                    message_box.setIcon(QtWidgets.QMessageBox.Information)
                    ok_button = message_box.addButton(QtWidgets.QMessageBox.Ok)
                    message_box.setStyleSheet("font-size: 14pt; font-weight: bold; color: #333; background-color: #fff;")
                    ok_button.setStyleSheet("background-color: #007acc; color: white; font-size: 16px; padding: 10px 20px; border-radius: 50px;")
                    message_box.exec_()
                   # Vider les champs de texte après avoir modifié le nombre d'années
            nom_edit.setText("")
        #Définir la fonction qui sera appelée lorsqu'on clique sur le bouton de fermeture
        def close_window():
            self.Recherche_action4.close()
        # Connecter la fonction de fermeture au bouton de fermeture
        close_button.clicked.connect(close_window)
        recherche_button.clicked.connect(calculer_maladie)
        self.Recherche_action4.show()
    def show_window21(self):
        def tous_les_champs_remplis():
            champs = [cin_edit]
            for champ in champs:
                if champ.text() == "":
                    return False
            return True
        def validate_line_edit1():
            data = cin_edit.text()
            if not data.isnumeric() or len(data)!=8:
                cin_edit.clear()
                cin_edit.setPlaceholderText('Invalid input')
        self.Recherche_action5 = QWidget()
        self.Recherche_action5.setGeometry(500,500,500,500)
        self.Recherche_action5.setStyleSheet("background-color: white")
        self.Recherche_action5.setWindowTitle('recherche maladie d\'une personne')
        layout = QVBoxLayout(self.Recherche_action5)
        # Ajouter un QLineEdit pour entrer le numéro de carte d'identité
        label1 = QLabel("Numéro de carte d'identité:", self.Recherche_action5)
        label1.setStyleSheet("font-weight: bold; font-size: 18pt;")
        cin_edit = QLineEdit()
        cin_edit.setFont(QFont('Arial',20))
        cin_edit.setFixedWidth(400)
        cin_edit.returnPressed.connect(validate_line_edit1)
        layout.addWidget(label1)
        layout.addWidget(cin_edit)
        # Ajouter un QPushButton pour effectuer la recherche
        recherche_button = QPushButton("rechercher")
        recherche_button.setFixedWidth(400)
        recherche_button.setStyleSheet("background-color: #007acc; color: black; font-size: 16px; padding: 10px 20px; border-radius: 50px;")
        layout.addWidget(recherche_button)
        # Ajouter un QPushButton pour fermer la fenêtre
        close_button = QPushButton("Fermer la fenêtre")
        close_button.setFixedWidth(400)
        close_button.setStyleSheet("background-color: white; color: black; font-size: 16px; padding: 10px 20px; border-radius: 50px;")
        layout.addWidget(close_button)
        layout.setAlignment(Qt.AlignCenter)
        def recherche_maladie_personne():
            cin=cin_edit.text()
            if not tous_les_champs_remplis() :
                error_message = QtWidgets.QMessageBox()
                error_message.setIcon(QtWidgets.QMessageBox.Warning)
                error_message.setWindowTitle("Erreur")
                error_message.setText("Veuillez remplir le champ du carte d'identité avant de chercher.")

                # Personnaliser le texte en gras et de taille plus grande
                error_message.setStyleSheet("QMessageBox QLabel{ font-weight: bold; font-size: 25px; }")

                # Personnaliser le bouton OK en bleu, en gras et de taille plus grande
                error_message.setStyleSheet("QMessageBox QPushButton{ background-color: #007acc; color: white; font-weight: bold; font-size: 16px; }")

                error_message.exec_()
                return
            elif(existe(personne_dict,cin)==False):
                error_message = QtWidgets.QMessageBox()
                error_message.setIcon(QtWidgets.QMessageBox.Warning)
                error_message.setWindowTitle("Erreur")
                error_message.setText("Ce personne n'existe pas .")
                
                # Personnaliser le texte en gras et de taille plus grande
                error_message.setStyleSheet("QMessageBox QLabel{ font-weight: bold; font-size: 25px; }")

                # Personnaliser le bouton OK en bleu, en gras et de taille plus grande
                error_message.setStyleSheet("QMessageBox QPushButton{ background-color: #007acc; color: white; font-weight: bold; font-size: 16px; }")
                error_message.exec_()
                return
            else:
                result=[]
                for code, info in maladie_dict.items():
                    if  info['CIN'] == cin:
                        dictionnaire_dict = {code: maladie_dict[code]}
                        result.extend(contenu_dictionnaire(dictionnaire_dict))
                count=len(result)
                if result:
                    self.setWindowTitle("Recherche maladie d'une personne.")
                    message=''
                    # Créer le QLabel pour afficher le pourcentage
                    for cle,val in personne_dict.items():
                        if cle==cin:
                            #message+="\n*  numéro de carte d'identité: "+cin+"\n*nom : "+val["nom"]+"\*prénom :"+val["prenom"]+"\n*age: "+val["age"]+"\n*adresse: "+val["adresse"]+"\n*nationalité: "+val["nationalité"]+"\n*numéro de téléphone: "+val["numéro_telephone"]+"\n*date d'infection: "+val["date d'infection"]+"\n*décédé: "+val["decédé"] 
                            message += "\n* numéro de carte d'identité: " + cin + "\n* nom: " + val["nom"] + "\n* prénom: " + val["prenom"] + "\n* age: " + val["age"] + "\n* adresse: " + val["adresse"] + "\n* nationalité: " + val["nationalité"] + "\n* numéro de téléphone: " + val["numéro_telephone"] + "\n* date d'infection: " + val["date d'infection"] + "\n* décédé: " + val["decédé"] 
                    pourcentage_label = QLabel(f"les coordonnées de ce personne :  {message}")
                    pourcentage_label.setAlignment(Qt.AlignCenter)
                    font = QFont("Arial", 16)
                    font.setBold(True)
                    pourcentage_label.setFont(font)
                    # Create table widget
                    self.table = QTableWidget(self)
                    self.table.setColumnCount(4)
                    self.table.setHorizontalHeaderLabels(['Code', "Numéro de carte d'identité", "Nom maladie", "Nombre d'années"])
                    self.table.setRowCount(count)
                    # Define cell style for headers
                    bold_font = QtGui.QFont()
                    bold_font.setBold(True)
                    blue_background = QtGui.QBrush(QtGui.QColor(230, 230, 230)) # Blue background color
                    item_code = QtWidgets.QTableWidgetItem("Code")
                    item_code.setFont(bold_font)
                    item_code.setBackground(blue_background)
                    self.table.setItem(0, 0, item_code)
                    item_identite = QtWidgets.QTableWidgetItem("Numéro de carte d'identité")
                    item_identite.setFont(bold_font)
                    item_identite.setBackground(blue_background)
                    self.table.setItem(0, 1, item_identite)
                    item_nom = QtWidgets.QTableWidgetItem("Nom maladie")
                    item_nom.setFont(bold_font)
                    item_nom.setBackground(blue_background)
                    self.table.setItem(0, 2, item_nom)
                    item_annees = QtWidgets.QTableWidgetItem("Nombre d'années")
                    item_annees.setFont(bold_font)
                    item_annees.setBackground(blue_background)
                    self.table.setItem(0, 3, item_annees)
                    
                    # Define style of the table
                    self.table.setStyleSheet("""
                        QTableWidget { background-color: white; color: black; font-size: 12pt; font-weight: bold; }
                        QHeaderView::section { background-color: #007acc; color: white; font-size: 12pt; font-weight: bold; }
                    """)
                    
                    # Populate table with data from dictionary
                    self.table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
                    for i, (cle, personne) in enumerate(result):
                        # Assigner la clé de la personne à la première colonne de la ligne i
                        self.table.setItem(i, 0, QTableWidgetItem(str(cle)))
                        
                        # Assigner les autres attributs de la personne aux colonnes suivantes
                        for j, item in enumerate(personne.values()):
                            self.table.setItem(i, j+1, QTableWidgetItem(str(item)))
                            self.table.item(i, j+1).setTextAlignment(QtCore.Qt.AlignCenter)
                    font = QtGui.QFont()
                    font.setBold(True)
                    self.table.setFont(font)
                    
                    # Add table widget to layout
                    layout = QtWidgets.QVBoxLayout()
                    layout.addWidget(pourcentage_label)
                    self.table.resizeColumnsToContents()
                    layout.addWidget(self.table)
                    
                    
                    # Create and show table dialog window
                    self.table_dialog = QtWidgets.QDialog(self)
                    self.table_dialog.setLayout(layout)
                    # Add close button
                    button_box = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Close)
                    button_box.rejected.connect(self.table_dialog.reject)
                    layout.addWidget(button_box)
                    button_box.setStyleSheet("background-color: #007acc;")
                    self.table_dialog.setWindowTitle("recherche maladies d'une personnes")
                    self.table_dialog.resize(2000, 1000)
                    self.table_dialog.show() 
               
            # Vider les champs de texte après avoir modifié le nombre d'années
            cin_edit.setText("")
        #Définir la fonction qui sera appelée lorsqu'on clique sur le bouton de fermeture
        def close_window():
            self.Recherche_action5.close()
        # Connecter la fonction de fermeture au bouton de fermeture
        close_button.clicked.connect(close_window)
        recherche_button.clicked.connect(recherche_maladie_personne)
        self.Recherche_action5.show()
    def show_window22(self):
        with open('personnes.csv', 'w', newline='') as f:
            fieldnames = ["Cle", "Nom", "Prenom", "age", "adresse", "nationalité", "date d'infection", "numéro_telephone", "decédé"]  # Définir les noms de colonnes
            writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter=';')
            writer.writeheader()  # Écrire les en-têtes des colonnes dans la première ligne du fichier
            # Parcourir les clés et les sous-dictionnaires, puis écrire les valeurs dans les colonnes
            for cle, subdict in personne_dict.items():
                row = {"Cle": cle, "Nom": subdict.get("nom", ""), "Prenom": subdict.get("prenom", ""), "age": subdict.get("age", ""), "adresse": subdict.get("adresse", ""), "nationalité": subdict.get("nationalité", ""), "numéro_telephone": subdict.get("numéro_telephone", ""), "date d'infection": subdict.get("date d'infection", ""),"decédé": subdict.get("decédé", "")}
                writer.writerow(row)
            # Définir la couleur de fond de la fenêtre
            self.setStyleSheet("background-color: #f5f5f5;")

            # Définir un style de police personnalisé pour le message box
            message_box = QtWidgets.QMessageBox(self)
            message_box.setWindowTitle('Enregistrement fichier personne')
            message_box.setText("Le dictionnaire des personnes est bien enregistré")
            message_box.setIcon(QtWidgets.QMessageBox.Information)
            ok_button = message_box.addButton(QtWidgets.QMessageBox.Ok)
            message_box.setStyleSheet("font-size: 14pt; font-weight: bold; color: #333; background-color: #fff;")
            ok_button.setStyleSheet("background-color: #007acc; color: white; font-size: 16px; padding: 10px 20px; border-radius: 50px;")
            message_box.exec_()
    def show_window23(self):
        with open('maladies.csv', 'w', newline='') as f:
            fieldnames = ["Code", "CIN", "nom maladie", "nombre d'années"]  # Définir les noms de colonnes
            writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter=';')
            writer.writeheader()  # Écrire les en-têtes des colonnes dans la première ligne du fichier
            # Parcourir les clés et les sous-dictionnaires, puis écrire les valeurs dans les colonnes
            for cle, subdict in maladie_dict.items():
                row = {"Code": cle, "CIN": subdict.get("CIN", ""), "nom maladie": subdict.get("nom maladie", ""), "nombre d'années": subdict.get("nombre d'années", "")}
                writer.writerow(row)
            message_box = QtWidgets.QMessageBox(self)
            message_box.setWindowTitle('Enregistrement fichier personne')
            message_box.setText("Le dictionnaire des maladies est bien enregistré")
            message_box.setIcon(QtWidgets.QMessageBox.Information)
            ok_button = message_box.addButton(QtWidgets.QMessageBox.Ok)
            message_box.setStyleSheet("font-size: 14pt; font-weight: bold; color: #333; background-color: #fff;")
            ok_button.setStyleSheet("background-color: #007acc; color: white; font-size: 16px; padding: 10px 20px; border-radius: 50px;")
            message_box.exec_()
    def show_window24(self):
        global personne_dict  # Declare that you are referring to the global variable personne_dict
        def load_dict_from_csv(file_path):
            # Access personne_dict here and update it with the information from the CSV file
            with open(file_path, 'r', newline='') as f:
                reader = csv.DictReader(f, delimiter=';')
                for row in reader:
                    numero_carte_identite = row.get("Cle")
                    nom = row.get("Nom")
                    prenom = row.get("Prenom")
                    age = row.get("age")
                    adresse = row.get("adresse")
                    nationalite = row.get("nationalité")
                    date_de_naissance = row.get("date d'infection")
                    numero_telephone = row.get("numéro_telephone")
                    decede = row.get("decédé")

                    # Update the global personne_dict with the information from the CSV file
                    info_personne = {"nom": nom, "prenom": prenom, "age": age, "adresse": adresse,
                                     "nationalité": nationalite,
                                     "numéro_telephone": numero_telephone,"date d'infection": date_de_naissance, "decédé": decede}
                    personne_dict[numero_carte_identite] = info_personne

        # Call the nested function to populate personne_dict
        load_dict_from_csv('C:/Users/pc/Desktop/projet final/personnes.csv')
        message_box = QtWidgets.QMessageBox(self)
        message_box.setWindowTitle('Récupération fichier personnes')
        message_box.setText("le contenu de dictionnaire est bien récupéré.")
        message_box.setIcon(QtWidgets.QMessageBox.Information)
        ok_button = message_box.addButton(QtWidgets.QMessageBox.Ok)
        message_box.setStyleSheet("font-size: 14pt; font-weight: bold; color: #333; background-color: #fff;")
        ok_button.setStyleSheet("background-color: #007acc; color: white; font-size: 16px; padding: 10px 20px; border-radius: 50px;")
        message_box.exec_()
    def show_window25(self):
        global maladie_dict  
        def load_dict_from_csv(file_path):
            with open(file_path, 'r', newline='') as f:
                reader = csv.DictReader(f, delimiter=';')
                for row in reader:
                    code = row.get("Code")
                    cin = row.get("CIN")
                    nom = row.get("nom maladie")
                    nombre = row.get("nombre d'années")
                    info_maladie = { "CIN": cin, "nom maladie": nom, "nombre d'années": nombre}
                    maladie_dict[code] = info_maladie

        # Call the nested function to populate personne_dict
        load_dict_from_csv('C:/Users/pc/Desktop/projet final/maladies.csv')
        message_box = QtWidgets.QMessageBox(self)
        message_box.setWindowTitle('Récupération fichier personnes')
        message_box.setText("le contenu de fichier est bien récupéré.")
        message_box.setIcon(QtWidgets.QMessageBox.Information)
        ok_button = message_box.addButton(QtWidgets.QMessageBox.Ok)
        message_box.setStyleSheet("font-size: 14pt; font-weight: bold; color: #333; background-color: #fff;")
        ok_button.setStyleSheet("background-color: #007acc; color: white; font-size: 16px; padding: 10px 20px; border-radius: 50px;")
        message_box.exec_()
    def show_window26(self):
        
        self.afficher_action = QWidget()
        self.afficher_action.setGeometry(500,200,500,500)
        self.afficher_action.setStyleSheet("background-color: white")
        self.afficher_action .setWindowTitle('Afficher par nationalité')
        layout = QVBoxLayout(self.afficher_action)
        
        
        label1 = QLabel("Nationalité: ", self.afficher_action)
        label1.setStyleSheet("font-weight: bold; font-size: 18pt;")
        # Liste des nationalités possibles
        nationalites = ['Afghan','Albanais','Algérien','Allemand','Américain','Angolais','Argentin','Arménien','Arubais','Australien','Autrichien','Azerbaïdjanais','Bahaméen','Bangladais','Belge','Benin','Biélorusse','Birmain','Bolivien','Bosniaque','Botswanais','Bouthan','Brésilien','Britannique','Bulgare','Burkinabè','Burundais','Caïmanien','Cambodgien','Camerounais','Canadien','Chilien','Chinois','Chypriote','Colombien','Congolais','Costaricain','Croate','Cubain','Danois','Dominicain','Egyptien','Emirati','Equatorien','Espagnol','Estonien','Ethiopien','Européen','Finlandais','Français','Gabonais','Georgien','Ghanéen','Grec','Guatemala','Guinéen','Haïtien','Hollandais','Hondurien','Hong-Kong','Hongrois','Indien','Indonésien','Irakien','Iranien','Irlandais','Islandais','Israélien','Italien','Ivoirien','Jamaïcain','Japonais','Jordanien','Kazakh','Kenyan','Kirghiz','Kosovar','Koweïtien','Kurde','Laotien','Lésothien','Letton','Libanais','Libyen','Liechtenstein','Lituanien','Luxembourgeois','Macédonien','Madagascar','Malaisien','Malien','Maltais','Marocain','Mauritanien','Mauritien','Mexicain','Monégasque','Mongol','Monténégrin','Mozambique','Namibien','Néo-Zélandais','Népalais','Nicaraguayen','Nigérien','Nord Coréen','Norvégien','Ougandais','Pakistanais','Palestinien','Panaméen','Paraguayen','Péruvien','Philippiens','Polonais','Portoricain','Portugais','Qatar','Roumain','Russe','Rwandais','Saoudien','Sénégalais','Serbe','Singapour','Slovaque','Somalien','Soudanais','Soviétique','Sri-Lankais','Sud-Africain','Sud-Coréen','Suédois','Suédois','Suisse','Syrien','Tadjik','Taïwanais','Tanzanien','Tchadien','Tchèque','Tchétchène','Thaïlandais','Trinité-Et-Tobago','Tunisien','Turc','Ukranien','Uruguayen','Vénézuélien','Vietnamien','Yéménite','Yougoslave','Zimbabwéen']
        
        # Création de la combobox
        combobox_nationalite = QComboBox(self.afficher_action)
        combobox_nationalite.setFont(QFont('Arial', 20))
        combobox_nationalite.setFixedWidth(400)
        combobox_nationalite.addItems(nationalites)


        # Ajouter les widgets au layout
        layout.addWidget(label1)
        layout.addWidget(combobox_nationalite)
        
        # Ajouter un QPushButton pour effectuer la recherche
        recherche_button = QPushButton("calculer")
        recherche_button.setFixedWidth(400)
        recherche_button.setStyleSheet("background-color: #007acc; color: black; font-size: 24px; padding: 10px 20px; border-radius: 50px;")
        layout.addWidget(recherche_button)
        # Ajouter un QPushButton pour fermer la fenêtre
        close_button = QPushButton("Fermer la fenêtre")
        close_button.setFixedWidth(400)
        close_button.setStyleSheet("background-color: white; color: black; font-size: 24px; padding: 10px 20px; border-radius: 50px;")
        layout.addWidget(close_button)
        layout.setAlignment(Qt.AlignCenter)

        # Définir la fonction qui sera appelée lorsqu'on clique sur le bouton de recherche
        def search_nationalite():
            nationalite =combobox_nationalite.currentText()
            result = chercher_personne_par_nationalite(nationalite,personne_dict)
            count=len(result)
            if result:
                layout = QVBoxLayout()
                # Créer le QLabel pour afficher le pourcentage
                pourcentage_label = QLabel(f"Nombres des personnes ayant cette nationalité: {count}")
                pourcentage_label.setAlignment(Qt.AlignCenter)
                font = QFont("Arial", 16)
                font.setBold(True)
                pourcentage_label.setFont(font)
                
                self.table = QTableWidget(self)
                self.table.setColumnCount(9)
                self.table.setHorizontalHeaderLabels(["Numéro de carte d'identité", "Nom", "Prénom", "Âge", "Adresse", "Nationalité", "Numéro de téléphone", "Date d'infection", "Décédé"])
                self.table.setRowCount(len(result))
                
                # Définir le style des cellules contenant les mots "Nom", "Prénom" et "Risque"
                bold_font = QtGui.QFont()
                bold_font.setBold(True)
                blue_background = QtGui.QBrush(QtGui.QColor(230,230,230)) # couleur de fond bleue
                
                item_nom = QtWidgets.QTableWidgetItem("nom")
                item_nom.setFont(bold_font)
                item_nom.setBackground(blue_background)
                self.table.setItem(0, 0, item_nom)

                item_prenom = QtWidgets.QTableWidgetItem("prenom")
                item_prenom.setFont(bold_font)
                item_prenom.setBackground(blue_background)
                self.table.setItem(0, 1, item_prenom)

                item_age = QtWidgets.QTableWidgetItem("age")
                item_age.setFont(bold_font)
                item_age.setBackground(blue_background)
                self.table.setItem(0, 2, item_age)
                
                item_adresse = QtWidgets.QTableWidgetItem("adresse")
                item_adresse.setFont(bold_font)
                item_adresse.setBackground(blue_background)
                self.table.setItem(0, 3, item_adresse)
                
                item_nationalité = QtWidgets.QTableWidgetItem("nationalité")
                item_nationalité.setFont(bold_font)
                item_nationalité.setBackground(blue_background)
                self.table.setItem(0, 4, item_nationalité)
                
                item_numéro_telephone = QtWidgets.QTableWidgetItem("numéro_telephone")
                item_numéro_telephone.setFont(bold_font)
                item_numéro_telephone.setBackground(blue_background)
                self.table.setItem(0, 5, item_numéro_telephone)
                
                item_date_infectation = QtWidgets.QTableWidgetItem("date d'infectation")
                item_date_infectation.setFont(bold_font)
                item_date_infectation.setBackground(blue_background)
                self.table.setItem(0,6, item_date_infectation)
                
                item_décédé = QtWidgets.QTableWidgetItem("décédé")
                item_décédé.setFont(bold_font)
                item_décédé.setBackground(blue_background)
                self.table.setItem(0,7, item_décédé)
                
                # Définir le style du tableau
                self.table.setStyleSheet("""
                    QTableWidget { background-color: white; color: black; font-size: 12pt; font-weight: bold; }
                    QHeaderView::section { background-color: #007acc; color: white; font-size: 12pt; font-weight: bold; }
                """)
                
                self.table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
                for i, (cle, personne) in enumerate(result.items()):
                    # Assigner la clé de la personne à la première colonne de la ligne i
                    self.table.setItem(i, 0, QTableWidgetItem(str(cle)))
                    
                    # Assigner les autres attributs de la personne aux colonnes suivantes
                    for j, item in enumerate(personne.values()):
                        self.table.setItem(i, j+1, QTableWidgetItem(str(item)))
                        self.table.item(i, j+1).setTextAlignment(QtCore.Qt.AlignCenter)
                font = QtGui.QFont()
                font.setBold(True)
                self.table.setFont(font)
                
                layout.addWidget(pourcentage_label)
                # Redimensionner la largeur des colonnes pour s'adapter au contenu
                self.table.resizeColumnsToContents()
                layout.addWidget(self.table)
                self.table_dialog = QtWidgets.QDialog(self) # initialisez ici
                button_box = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Close)
                button_box.rejected.connect(self.table_dialog.reject)
                layout.addWidget(button_box)
                button_box.setStyleSheet("background-color: #007acc;")
                self.table_dialog.setLayout(layout)
                self.table_dialog.setWindowTitle("Personnes à risque")
                self.table_dialog.resize(2000,1000)
                self.table_dialog.show()
            else:
                message_box = QtWidgets.QMessageBox()
                message_box.setWindowTitle("afficher par nationalité.")
                message_box.setText("Aucun personne ayant cette nationalité")
                message_box.setIcon(QtWidgets.QMessageBox.Information)
                ok_button = message_box.addButton(QtWidgets.QMessageBox.Ok)
                message_box.setStyleSheet("font-size: 14pt; font-weight: bold; color: #333; background-color: #fff;")
                ok_button.setStyleSheet("background-color: #007acc; color: white; font-size: 16px; padding: 10px 20px; border-radius: 50px;")
                message_box.exec_()
        def close_window():
            self.afficher_action.close()
        # Connecter la fonction de fermeture au bouton de fermeture
        close_button.clicked.connect(close_window)
        recherche_button.clicked.connect(search_nationalite)
        self.afficher_action.show() 
    def show_window27(self):
        layout = QVBoxLayout()
        result = chercher_personne_decedes(personne_dict)
        resultat=contenu_dictionnaire(result)
        count=len(result)
        somme=len(personne_dict)
        if somme!=0:
            pourcentage=(count/somme)*100
            # Créer le QLabel pour afficher le pourcentage
            pourcentage_label = QLabel(f"Pourcentage de décédés : {pourcentage:.2f}%")
            pourcentage_label.setAlignment(Qt.AlignCenter)
            font = QFont("Arial", 16)
            font.setBold(True)
            pourcentage_label.setFont(font)
            
            self.setWindowTitle("Personnes décédé")
            self.setGeometry(200, 200, 800, 600)
            self.table = QTableWidget(self)
            self.table.setColumnCount(9)
            self.table.setHorizontalHeaderLabels(["Numéro de carte d'identité", "Nom", "Prénom", "Âge", "Adresse", "Nationalité", "Numéro de téléphone", "Date d'infection", "Décédé"])
            self.table.setRowCount(len(resultat))
            
            # Définir le style des cellules contenant les mots "Nom", "Prénom" et "Risque"
            bold_font = QtGui.QFont()
            bold_font.setBold(True)
            blue_background = QtGui.QBrush(QtGui.QColor(230,230,230)) # couleur de fond bleue
            
            item_nom = QtWidgets.QTableWidgetItem("nom")
            item_nom.setFont(bold_font)
            item_nom.setBackground(blue_background)
            self.table.setItem(0, 0, item_nom)

            item_prenom = QtWidgets.QTableWidgetItem("prenom")
            item_prenom.setFont(bold_font)
            item_prenom.setBackground(blue_background)
            self.table.setItem(0, 1, item_prenom)

            item_age = QtWidgets.QTableWidgetItem("age")
            item_age.setFont(bold_font)
            item_age.setBackground(blue_background)
            self.table.setItem(0, 2, item_age)
            
            item_adresse = QtWidgets.QTableWidgetItem("adresse")
            item_adresse.setFont(bold_font)
            item_adresse.setBackground(blue_background)
            self.table.setItem(0, 3, item_adresse)
            
            item_nationalité = QtWidgets.QTableWidgetItem("nationalité")
            item_nationalité.setFont(bold_font)
            item_nationalité.setBackground(blue_background)
            self.table.setItem(0, 4, item_nationalité)
            
            item_numéro_telephone = QtWidgets.QTableWidgetItem("numéro_telephone")
            item_numéro_telephone.setFont(bold_font)
            item_numéro_telephone.setBackground(blue_background)
            self.table.setItem(0, 5, item_numéro_telephone)
            
            item_date_infectation = QtWidgets.QTableWidgetItem("date d'infectation")
            item_date_infectation.setFont(bold_font)
            item_date_infectation.setBackground(blue_background)
            self.table.setItem(0,6, item_date_infectation)
            
            item_décédé = QtWidgets.QTableWidgetItem("décédé")
            item_décédé.setFont(bold_font)
            item_décédé.setBackground(blue_background)
            self.table.setItem(0,7, item_décédé)
            
            # Définir le style du tableau
            self.table.setStyleSheet("""
                QTableWidget { background-color: white; color: black; font-size: 12pt; font-weight: bold; }
                QHeaderView::section { background-color: #007acc; color: white; font-size: 12pt; font-weight: bold; }
            """)
            
            self.table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
            for i, (cle, personne) in enumerate(result.items()):
                # Assigner la clé de la personne à la première colonne de la ligne i
                self.table.setItem(i, 0, QTableWidgetItem(str(cle)))
                
                # Assigner les autres attributs de la personne aux colonnes suivantes
                for j, item in enumerate(personne.values()):
                    self.table.setItem(i, j+1, QTableWidgetItem(str(item)))
                    self.table.item(i, j+1).setTextAlignment(QtCore.Qt.AlignCenter)
            font = QtGui.QFont()
            font.setBold(True)
            self.table.setFont(font)
            
            layout = QtWidgets.QVBoxLayout()
            layout.addWidget(pourcentage_label)
            # Redimensionner la largeur des colonnes pour s'adapter au contenu
            self.table.resizeColumnsToContents()
            layout.addWidget(self.table)
            self.table_dialog = QtWidgets.QDialog(self) # initialisez ici
            button_box = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Close)
            button_box.rejected.connect(self.table_dialog.reject)
            layout.addWidget(button_box)
            button_box.setStyleSheet("background-color: #007acc;")
            self.table_dialog.setLayout(layout)
            self.table_dialog.setWindowTitle("Personnes à risque")
            self.table_dialog.resize(2000,1000)
            self.table_dialog.show() 
        else:
            message_box = QtWidgets.QMessageBox(self)
            message_box = QtWidgets.QMessageBox(self)
            message_box.setWindowTitle('personnes décédé')
            message_box.setText("Le dictionnaire est vide")
            message_box.setIcon(QtWidgets.QMessageBox.Information)
            ok_button = message_box.addButton(QtWidgets.QMessageBox.Ok)
            message_box.setStyleSheet("font-size: 14pt; font-weight: bold; color: #333; background-color: #fff;")
            ok_button.setStyleSheet("background-color: #007acc; color: white; font-size: 16px; padding: 10px 20px; border-radius: 50px;")
            message_box.exec_()
    def show_window28(self):
        date_format = "%d/%m/%Y"  # Format de date
        date_en_cours = datetime.date.today()
        personnes_en_quarantaine = []
        for numero_carte_identite, infos in personne_dict.items():
            nom = infos['nom']
            prenom = infos['prenom']
            age =infos['age']
            adresse=infos['adresse']
            nationalité=infos['nationalité']
            numéro_telephone=infos['numéro_telephone']
            décédé=infos['decédé']
            date_infection = datetime.datetime.strptime(infos['date d\'infection'], date_format).date()  # Convertir la date d'infection en objet date
            jours_quarantaine = (date_en_cours - date_infection).days  # Calculer le nombre de jours depuis l'infection
            if jours_quarantaine <= 14 and décédé=="0":  # Vérifier si le nombre de jours en quarantaine est inférieur ou égal à 14
                personnes_en_quarantaine.append((numero_carte_identite,nom, prenom, age, adresse, nationalité, numéro_telephone,date_infection, décédé ))  # Ajouter le numéro de carte d'identité et les informations de la personne à la liste des personnes en quarantaine
        if personnes_en_quarantaine:
            self.setWindowTitle("Personnes en quarantaine")
            self.setGeometry(200, 200, 800, 600)
            self.table = QTableWidget(self)
            self.table.setColumnCount(9)
            self.table.setHorizontalHeaderLabels(["Numéro de carte d'identité", "Nom", "Prénom", "Âge", "Adresse", "Nationalité", "Numéro de téléphone", "Date d'infection", "Décédé"])
            self.table.setRowCount(len(personnes_en_quarantaine))
            
            # Définir le style des cellules contenant les mots "Nom", "Prénom" et "Risque"
            bold_font = QtGui.QFont()
            bold_font.setBold(True)
            blue_background = QtGui.QBrush(QtGui.QColor(230,230,230)) # couleur de fond bleue
            
            item_nom = QtWidgets.QTableWidgetItem("nom")
            item_nom.setFont(bold_font)
            item_nom.setBackground(blue_background)
            self.table.setItem(0, 0, item_nom)

            item_prenom = QtWidgets.QTableWidgetItem("prenom")
            item_prenom.setFont(bold_font)
            item_prenom.setBackground(blue_background)
            self.table.setItem(0, 1, item_prenom)

            item_age = QtWidgets.QTableWidgetItem("age")
            item_age.setFont(bold_font)
            item_age.setBackground(blue_background)
            self.table.setItem(0, 2, item_age)
            
            item_adresse = QtWidgets.QTableWidgetItem("adresse")
            item_adresse.setFont(bold_font)
            item_adresse.setBackground(blue_background)
            self.table.setItem(0, 3, item_adresse)
            
            item_nationalité = QtWidgets.QTableWidgetItem("nationalité")
            item_nationalité.setFont(bold_font)
            item_nationalité.setBackground(blue_background)
            self.table.setItem(0, 4, item_nationalité)
            
            item_numéro_telephone = QtWidgets.QTableWidgetItem("numéro_telephone")
            item_numéro_telephone.setFont(bold_font)
            item_numéro_telephone.setBackground(blue_background)
            self.table.setItem(0, 5, item_numéro_telephone)
            
            item_date_infectation = QtWidgets.QTableWidgetItem("date d'infectation")
            item_date_infectation.setFont(bold_font)
            item_date_infectation.setBackground(blue_background)
            self.table.setItem(0,6, item_date_infectation)
            
            item_décédé = QtWidgets.QTableWidgetItem("décédé")
            item_décédé.setFont(bold_font)
            item_décédé.setBackground(blue_background)
            self.table.setItem(0,7, item_décédé)
            
            # Définir le style du tableau
            self.table.setStyleSheet("""
                QTableWidget { background-color: white; color: black; font-size: 12pt; font-weight: bold; }
                QHeaderView::section { background-color: #007acc; color: white; font-size: 12pt; font-weight: bold; }
            """)
            
            self.table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
            for i, personne in enumerate(personnes_en_quarantaine):
                for j in range(len(personne)):
                    item = QTableWidgetItem(str(personne[j]))
                    item.setTextAlignment(QtCore.Qt.AlignCenter)
                    self.table.setItem(i, j, item)
            font = QtGui.QFont()
            font.setBold(True)
            self.table.setFont(font)
            
            layout = QtWidgets.QVBoxLayout()
            # Redimensionner la largeur des colonnes pour s'adapter au contenu
            self.table.resizeColumnsToContents()
            layout.addWidget(self.table)
            self.table_dialog = QtWidgets.QDialog(self) # initialisez ici
            button_box = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Close)
            button_box.rejected.connect(self.table_dialog.reject)
            layout.addWidget(button_box)
            button_box.setStyleSheet("background-color: #007acc;")
            self.table_dialog.setLayout(layout)
            self.table_dialog.setWindowTitle("Personnes à risque")
            self.table_dialog.resize(2000,1000)
            self.table_dialog.show() 
            
        else:
            message_box = QtWidgets.QMessageBox(self)
            message_box = QtWidgets.QMessageBox(self)
            message_box.setWindowTitle('personnes en quarantaine')
            message_box.setText("Il n'y a pas des personnes en quarantaine.")
            message_box.setIcon(QtWidgets.QMessageBox.Information)
            ok_button = message_box.addButton(QtWidgets.QMessageBox.Ok)
            message_box.setStyleSheet("font-size: 14pt; font-weight: bold; color: #333; background-color: #fff;")
            ok_button.setStyleSheet("background-color: #007acc; color: white; font-size: 16px; padding: 10px 20px; border-radius: 50px;")
            message_box.exec_()
    def show_window29(self):
        personnes_risque = []
        for cle,personne in personne_dict.items():
            cin=cle
            nom = personne['nom']
            prenom = personne['prenom']
            age = int(personne['age'])
            decede=int(personne['decédé'])
            risque = 0
            result=[]
            for code, info in maladie_dict.items():
                if  info['CIN'] == cin:
                    result.extend(info["nom maladie"].split(','))
            # Vérifier l'âge et augmenter le risque en conséquence
            if age > 70:
                risque += 20
            elif 50 <= age <= 70:
                risque += 10
            # Vérifier les conditions médicales et augmenter le risque en conséquence
            if "diabete" in result:
                risque += 15
            if "hypertension" in result:
                risque += 20
            if "asthme" in result:
                risque += 20

            # Ajouter la personne à la liste des personnes à risque
            if decede==0:
                personnes_risque.append((nom, prenom, risque))
        personnes_risque.sort(key=lambda x: x[2], reverse=True)
        self.tableau = QtWidgets.QTableWidget()
        self.tableau.setStyleSheet("QTableWidget { background-color: white; color: black; font-size: 12pt; font-weight: bold; }")
        self.tableau.setColumnCount(3)
        self.tableau.setRowCount(len(personnes_risque))
        # Définir le style des cellules contenant les mots "Nom", "Prénom" et "Risque"
        bold_font = QtGui.QFont()
        bold_font.setBold(True)
        blue_background = QtGui.QBrush(QtGui.QColor(230,230,230)) # couleur de fond bleue

        # Définir le style du tableau
        self.tableau.setStyleSheet("""
            QTableWidget { background-color: white; color: black; font-size: 12pt; font-weight: bold; }
            QHeaderView::section { background-color: #007acc; color: white; font-size: 12pt; font-weight: bold; }
        """)

        self.tableau.setHorizontalHeaderLabels(['Nom', 'Prénom', 'Risque'])
        # Appliquer le style aux cellules contenant les mots "Nom", "Prénom" et "Risque"
        item_nom = QtWidgets.QTableWidgetItem("Nom")
        item_nom.setFont(bold_font)
        item_nom.setBackground(blue_background)
        self.tableau.setItem(0, 0, item_nom)

        item_prenom = QtWidgets.QTableWidgetItem("Prénom")
        item_prenom.setFont(bold_font)
        item_prenom.setBackground(blue_background)
        self.tableau.setItem(0, 1, item_prenom)

        item_risque = QtWidgets.QTableWidgetItem("Risque")
        item_risque.setFont(bold_font)
        item_risque.setBackground(blue_background)
        self.tableau.setItem(0, 2, item_risque)
        self.tableau.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        for i, (nom, prenom, risque) in enumerate(personnes_risque):
            item_nom = QtWidgets.QTableWidgetItem(nom)
            item_nom.setTextAlignment(Qt.AlignCenter)
            self.tableau.setItem(i, 0, item_nom)
            
            item_prenom = QtWidgets.QTableWidgetItem(prenom)
            item_prenom.setTextAlignment(Qt.AlignCenter)
            self.tableau.setItem(i, 1, item_prenom)
            
            item_risque = QtWidgets.QTableWidgetItem(str(risque)+"%")
            item_risque.setTextAlignment(Qt.AlignCenter)
            self.tableau.setItem(i, 2, item_risque)
        layout = QtWidgets.QVBoxLayout()
        # Redimensionner la largeur des colonnes pour s'adapter au contenu
        self.tableau.resizeColumnsToContents()
        layout.addWidget(self.tableau)
        self.tableau_dialog = QtWidgets.QDialog(self) # initialisez ici
        button_box = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Close)
        button_box.rejected.connect(self.tableau_dialog.reject)
        layout.addWidget(button_box)
        button_box.setStyleSheet("background-color: #007acc;")
        self.tableau_dialog.setLayout(layout)
        self.tableau_dialog.setWindowTitle("Personnes à risque")
        self.tableau_dialog.resize(2000,1000)
        self.tableau_dialog.show()

        
    def changeTheme(self):
        # Appliquer le style "Fusion"
        QApplication.setStyle('Windows10')
        # Définir une nouvelle palette de couleurs pour l'application
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(230,230,230))  # Couleur de fond
        palette.setColor(QPalette.WindowText, Qt.black)  # Couleur du texte
        palette.setColor(QPalette.Base, QColor(0,0,0))  # Couleur des champs de texte
        self.setPalette(palette)

        # Appliquer la nouvelle palette de couleurs
        QApplication.instance().setPalette(palette)

        # Charger l'image depuis un fichier
        pixmap = QPixmap("corona.jpg")

        # Créer un QLabel pour afficher l'image
        self.image_label = QLabel()

        # Redimensionner l'image pour qu'elle remplisse toute la fenêtre
        scaled_pixmap = pixmap.scaled(pixmap.width() * 1.5, pixmap.height() * 1.5)

        # Afficher l'image dans le QLabel
        self.image_label.setPixmap(scaled_pixmap)

        # Centrer le QLabel dans la fenêtre
        self.setCentralWidget(self.image_label)
                    
app = QApplication(sys.argv)
window = MainWindow()
app.exec_()

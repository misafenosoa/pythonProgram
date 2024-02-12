from PIL import Image, ImageTk
import os
from tkinter import Tk, Canvas, Entry, Label, Button , messagebox
import numpy as np

# Variable pour suivre l'état du jeu (commencé ou non)
jeu_commence = False

# Compteur de coups
nombre_coups = 0

matrice = None

original_matrice =None

morceaux = None

# Fonction pour commencer le jeu
def commencer_jeu():
    global jeu_commence
    global nombre_coups

    # Réinitialiser le nombre de coups
    nombre_coups = 0

    # Mélanger les morceaux au début du jeu
    # melanger_et_actualiser()

    # Mettre à jour l'état du jeu
    jeu_commence = True

def redimensionner_image(image_path, nouvelle_largeur, nouvelle_hauteur):
    # Charger l'image
    image = Image.open(image_path)

    # Redimensionner l'image
    image_redimensionnee = image.resize((nouvelle_largeur, nouvelle_hauteur))

    return image_redimensionnee

def decouper_image(image_path, morceau_longueur, morceau_largeur, output_path):
    # Vérifier si le répertoire de sortie existe, sinon le créer
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    else:
        # Nettoyer le dossier de sortie en supprimant les fichiers existants
        for fichier in os.listdir(output_path):
            fichier_path = os.path.join(output_path, fichier)
            if os.path.isfile(fichier_path):
                os.remove(fichier_path)

    # Charger l'image
    image = Image.open(image_path)

    # Redimensionner l'image
    nouvelle_largeur = morceau_largeur * 100
    nouvelle_hauteur = morceau_longueur * 100
    image_redimensionnee = image.resize((nouvelle_largeur, nouvelle_hauteur))

    # Obtenir la taille de l'image redimensionnée
    largeur, hauteur = image_redimensionnee.size

    # Calculer la largeur et la hauteur de chaque morceau
    largeur_morceau = largeur // morceau_largeur
    hauteur_morceau = hauteur // morceau_longueur

    # Découper l'image en morceaux et les sauvegarder
    for i in range(morceau_longueur):
        for j in range(morceau_largeur):
            # Coordonnées du coin supérieur gauche du morceau
            x1 = j * largeur_morceau
            y1 = i * hauteur_morceau

            # Coordonnées du coin inférieur droit du morceau
            x2 = (j + 1) * largeur_morceau
            y2 = (i + 1) * hauteur_morceau

            # Découper le morceau
            morceau = image_redimensionnee.crop((x1, y1, x2, y2))

            # Construire le chemin de sauvegarde pour le morceau
            morceau_path = os.path.join(output_path, f'morceau_{i}_{j}.png')

            # Sauvegarder le morceau
            morceau.save(morceau_path)

def melanger_morceaux(morceaux):
    # Mélanger l'ordre des morceaux
    import random
    
    random.shuffle(morceaux)


def comparer_matrices(matrice1, matrice2):
    # Convertir les listes en tableaux NumPy
    np_matrice1 = np.array(matrice1)
    np_matrice2 = np.array(matrice2)
    
    # Comparer les tableaux NumPy
    if np.array_equal(np_matrice1, np_matrice2):
        return True
    else:
        return False
def afficher_morceaux(output_path, nb_colonnes, nb_lignes, espacement_entre_images=10):
    # Créer une fenêtre Tkinter
    fenetre = Tk()
    fenetre.title("Affichage des morceaux")

    # Parcourir tous les fichiers dans le répertoire de sortie
    global morceaux
    morceaux = []

    for filename in sorted(os.listdir(output_path)):  # Utiliser sorted pour garantir un ordre approprié
        if filename.endswith(".png"):
            # Construire le chemin complet du morceau
            morceau_path = os.path.join(output_path, filename)

            # Ouvrir le morceau avec PIL
            morceau_pil = Image.open(morceau_path)

            # Convertir le morceau en format compatible avec Tkinter
            morceau_tk = ImageTk.PhotoImage(morceau_pil)

            # Ajouter le morceau à la liste
            morceaux.append(morceau_tk)

    # Créer un canevas pour afficher les morceaux
    canvas = Canvas(fenetre, width=morceaux[0].width() * nb_colonnes + (nb_colonnes - 1) * espacement_entre_images,
                    height=morceaux[0].height() * nb_lignes + (nb_lignes - 1) * espacement_entre_images)
    canvas.pack()
    
    # Créer une matrice avec des valeurs de 1 à nb_colonnes * nb_lignes
    global matrice
    temp = np.arange(1, nb_colonnes * nb_lignes + 1).reshape((nb_lignes, nb_colonnes))
    matrice = temp
    global original_matrice
    original_matrice = temp
    # Afficher la matrice
    print("Matrice :")
    print(matrice)
    
    

    

    # Fonction pour afficher les morceaux en grille avec espacement
    def afficher_morceaux_en_grille():
        global morceaux
        x, y = 0, 0

        for i in range(nb_lignes):
            for j in range(nb_colonnes):
                morceau = morceaux[i * nb_colonnes + j]
                canvas.create_image(x, y, anchor='nw', image=morceau)
                x += morceau.width() + espacement_entre_images

            # Passer à la ligne suivante
            x = 0
            y += morceaux[0].height() + espacement_entre_images

        fenetre.update_idletasks()

    # Fonction pour mélanger les morceaux et actualiser l'affichage
    def melanger_et_actualiser():
        global morceaux
        melanger_morceaux(morceaux)
        canvas.delete("all")
        afficher_morceaux_en_grille()
        


        
    def interchanger_cases(morceaux, index1, index2):
        # Vérifier que les indices sont valides
        global matrice
        global original_matrice
        global jeu_commence
        if 0 <= index1 < len(morceaux) and 0 <= index2 < len(morceaux):
            # Interchanger les morceaux aux indices spécifiés
            morceaux[index1], morceaux[index2] = morceaux[index2], morceaux[index1]
            
            # Interchanger les valeurs dans la matrice
            temp = matrice[index1 // len(matrice[0])][index1 % len(matrice[0])]
            matrice[index1 // len(matrice[0])][index1 % len(matrice[0])] = matrice[index2 // len(matrice[0])][index2 % len(matrice[0])]
            matrice[index2 // len(matrice[0])][index2 % len(matrice[0])] = temp
            
            print("-------\n")
            print(matrice)
            # Comparer les matrices
            if comparer_matrices(matrice, original_matrice) and jeu_commence:
                messagebox.showinfo("Félicitations!", "Le jeu est fini. Les matrices sont identiques.")
        else:
            print("Indices non valides.")


    # Déclaration de la fonction on_interchanger_clic
    def on_interchanger_clic():
        global nombre_coups

        if jeu_commence:
            nombre_coups += 1

        # Récupérer les indices saisis par l'utilisateur
        indice1 = int(entry_indice1.get())
        indice2 = int(entry_indice2.get())
        global morceaux
        # Appeler la fonction d'interchangement
        interchanger_cases(morceaux, indice1, indice2)

        if jeu_commence:
            mettre_a_jour_label_coups()
        # Actualiser l'affichage après l'interchangement
        canvas.delete("all")
        afficher_morceaux_en_grille()
        

    # Ajouter des widgets d'entrée et un bouton pour l'interchangement
    label_indice1 = Label(fenetre, text="Indice 1:")
    label_indice1.pack()

    entry_indice1 = Entry(fenetre)
    entry_indice1.pack()

    label_indice2 = Label(fenetre, text="Indice 2:")
    label_indice2.pack()

    entry_indice2 = Entry(fenetre)
    entry_indice2.pack()

    bouton_interchanger = Button(fenetre, text="Interchanger", command=on_interchanger_clic)
    bouton_interchanger.pack()

    bouton_commencer = Button(fenetre, text="Commencer", command=commencer_jeu)
    bouton_commencer.pack()

    label_nombre_coups = Label(fenetre, text="Nombre de coups: 0")
    label_nombre_coups.pack()
    # Ajouter un bouton "Mélanger"
    bouton_melanger = Button(fenetre, text="Mélanger", command=melanger_et_actualiser)
    bouton_melanger.pack()

    # Ajouter un bouton "Tourner 90°"
    bouton_tourner_90 = Button(fenetre, text="Tourner 90°", command=tourner_90)
    bouton_tourner_90.pack()

    def mettre_a_jour_label_coups():
        label_nombre_coups.config(text=f"Nombre de coups: {nombre_coups}")

    # Appeler la fonction pour afficher les morceaux
    afficher_morceaux_en_grille()


    # Lancer la boucle principale Tkinter
    fenetre.mainloop()

# Fonction pour tourner la matrice de 90 degrés
def tourner_90():
    # Cette fonction ne fait rien pour l'instant
    pass

# Exemple d'utilisation
decouper_image('C:/Users/ratia/Pictures/Screenshots/x.png', 3, 3, 'workspaceIMG')
afficher_morceaux('workspaceIMG', 3, 3)

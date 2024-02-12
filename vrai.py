from PIL import Image, ImageTk
import os
from tkinter import Tk, Canvas, Entry, Label, Button
import numpy as np
import tkinter.messagebox


# Variable pour suivre l'état du jeu (commencé ou non)
jeu_commence = False

# Compteur de coups
nombre_coups = 0

morceaux = None

original_matrice =None
col =3 
lg =4

nombrefoismelanger = 0

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

def melanger_morceaux(morceaux_matrice):
    # Convertir la matrice en un tableau numpy
    morceaux_array = np.array(morceaux_matrice)
    
    # Mélanger les lignes de la matrice
    np.random.shuffle(morceaux_array)
    
    return morceaux_array.tolist()  # Reconvertir en liste de listes

def comparer_matrices():
    global original_matrice
    global morceaux    
    # Comparer les tableaux NumPy
    return np.array_equal(morceaux, original_matrice)

def afficher_morceaux(output_path, nb_colonnes, nb_lignes, espacement_entre_images=10):
    # Créer une fenêtre Tkinter
    fenetre = Tk()
    fenetre.title("Affichage des morceaux")

    # Parcourir tous les fichiers dans le répertoire de sortie
    global morceaux
    
    global original_matrice

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

    # Convertir la liste de morceaux en une matrice de nb_colonnes par nb_lignes
    morceaux_matrice = [morceaux[i:i+nb_colonnes] for i in range(0, len(morceaux), nb_colonnes)]

    # Créer un canevas pour afficher les morceaux
    canvas = Canvas(fenetre, width=morceaux_matrice[0][0].width() * nb_colonnes + (nb_colonnes - 1) * espacement_entre_images,
                    height=morceaux_matrice[0][0].height() * nb_lignes + (nb_lignes - 1) * espacement_entre_images)
    canvas.pack()
    
    morceaux = morceaux_matrice

    original_matrice = morceaux_matrice.copy()
    

    # Fonction pour afficher les morceaux en grille avec espacement
    def afficher_morceaux_en_grille():
        x, y = 0, 0
        global morceaux
        for i in range(nb_lignes):
            for j in range(nb_colonnes):
                morceau = morceaux[i][j]
                canvas.create_image(x, y, anchor='nw', image=morceau)
                x += morceau.width() + espacement_entre_images

            # Passer à la ligne suivante
            x = 0
            y += morceaux[0][0].height() + espacement_entre_images

        # Forcer la mise à jour de l'affichage
        fenetre.update_idletasks()


    # Fonction pour mélanger les morceaux et actualiser l'affichage
    def melanger_et_actualiser():
        global morceaux
        morceaux= melanger_morceaux(morceaux)
        
        global nombrefoismelanger
        nombrefoismelanger = nombrefoismelanger +1
        
        global nombre_coups
        global jeu_commence
        canvas.delete("all")
        afficher_morceaux_en_grille()

        # if jeu_commence:

        #     if nombrefoismelanger >3 :
        #         # tkinter.messagebox.showinfo("Information", "Les morceaux sont en ordre.")
        #         nombre_coups +=1
        #         nombrefoismelanger =0
                
                            
        #         mettre_a_jour_label_coups()
        


        
    def interchanger_cases( index1, index2):
        global morceaux
        # Convertir la matrice de morceaux en une liste
        morceaux_liste = np.array(morceaux).flatten().tolist()
        # Vérifier que les indices sont valides
        if 0 <= index1 < len(morceaux_liste) and 0 <= index2 < len(morceaux_liste):
            # Interchanger les morceaux dans la liste aux indices spécifiés
            morceaux_liste[index1], morceaux_liste[index2] = morceaux_liste[index2], morceaux_liste[index1]
            
            # Reconvertir la liste de morceaux en une matrice
            morceaux = np.array(morceaux_liste).reshape(np.array(morceaux).shape)
            
                       
            afficher_morceaux_en_grille()

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
        # Appeler la fonction d'interchangement
        interchanger_cases( indice1, indice2)

        if jeu_commence:
            mettre_a_jour_label_coups()
            # en ordre ve?
            if comparer_matrices() :
                tkinter.messagebox.showinfo("Information", "Les morceaux sont en ordre.")
            # elif nombre_coups>8 :
            #     tkinter.messagebox.showinfo("Information", "Vou avez perdu.")
                
        # Actualiser l'affichage après l'interchangement
        canvas.delete("all")
        afficher_morceaux_en_grille()
        
        
    def tourner_90():
        global morceaux
        # Transposer la matrice pour effectuer une rotation de 90 degrés
        morceaux = np.array(morceaux).T.reshape(lg,col).tolist()
        # Inverser l'ordre de chaque ligne pour conserver l'ordre visuel des morceaux
        morceaux = [ligne[::-1] for ligne in morceaux]
        
        # global nombre_coups

        # Actualiser l'affichage
        if jeu_commence:
            
            if comparer_matrices() :
                tkinter.messagebox.showinfo("Information", "Les morceaux sont en ordre.")
        canvas.delete("all")
        afficher_morceaux_en_grille()

    def tourner_moins_90():
        global morceaux
        # Transposer la matrice pour effectuer une rotation de -90 degrés
        morceaux = np.array(morceaux).T.reshape(lg,col).tolist()
        # Inverser l'ordre des colonnes pour effectuer une rotation antihoraire
        morceaux = morceaux[::-1]
        # Actualiser l'affichage
        if jeu_commence:
            if comparer_matrices() :
                tkinter.messagebox.showinfo("Information", "Les morceaux sont en ordre.")
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
    
    bouton_tourner_90 = Button(fenetre, text="Tourner 90", command=tourner_90)
    bouton_tourner_90.pack()
    
    # Ajouter un bouton "Tourner -90"
    bouton_tourner_moins_90 = Button(fenetre, text="Tourner -90", command=tourner_moins_90)
    bouton_tourner_moins_90.pack()

    def mettre_a_jour_label_coups():
        label_nombre_coups.config(text=f"Nombre de coups: {nombre_coups}")

    # Appeler la fonction pour afficher les morceaux

    afficher_morceaux_en_grille()


    # Lancer la boucle principale Tkinter
    fenetre.mainloop()

# Exemple d'utilisation
decouper_image('C:/Users/ratia/Desktop/workspace/S5/MrTahina/Puzzle/test/OIP.jpeg', col,lg, 'workspaceIMG')
afficher_morceaux('workspaceIMG', col, lg)
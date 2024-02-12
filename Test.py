import numpy as np

# Matrice après rotation de 90 degrés
morceaux = np.array([[2, 4, 6],
                     [1, 3, 5]])

# Redimensionner la matrice pour qu'elle conserve ses dimensions d'origine (3x2)
morceaux_redimensionne = morceaux.reshape((3, 2))

print(morceaux_redimensionne)

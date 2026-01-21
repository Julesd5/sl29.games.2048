"""Module providing the logic of the 2048 game"""

import random
from typing import List, Tuple

TAILLE:int = 4


# ==========================================================
# 🎯 FONCTION PUBLIQUE (API POUR L’INTERFACE)
# ==========================================================

def nouvelle_partie() -> Tuple[List[List[int]], int]:
    """
    Crée une nouvelle partie du jeu 2048.

    :return: Une grille TAILLExTAILLE initialisée avec deux tuiles, ainsi que le score à 0.
    :rtype: Tuple[List[List[int]], int]
    """
    plateau = _creer_plateau_vide()
    plateau = _ajouter_tuile(plateau)
    plateau = _ajouter_tuile(plateau)
    return plateau, 0

def jouer_coup(plateau: List[List[int]], direction: str) -> tuple[List[List[int]], int, bool]:
    """
    Effectuer un mouvement sur le plateau.

    :param plateau: Une grille TAILLExTAILLE du jeu.
    :type plateau: List[List[int]]
    :param direction: La direction du déplacement : 'g' (gauche), 'd' (droite), 'h' (haut), 'b' (bas).
    :type direction: str
    :return: Retourne un tuple (nouveau_plateau, points, est_fini).
    :rtype: tuple[List[List[int]], int, bool]
    """

    # En fonction de la direction choisie on effectue les déplacement du plateau
    if direction == "g":
        nouveau, points_du_coup = _deplacer_gauche(plateau)
    elif direction == "d":
        nouveau, points_du_coup = _deplacer_droite(plateau)
    elif direction == "h":
        nouveau, points_du_coup = _deplacer_haut(plateau)
    elif direction == 'b':
        nouveau, points_du_coup = _deplacer_bas(plateau)
    else:
        return plateau, 0, False

    if nouveau != plateau:
        nouveau = _ajouter_tuile(nouveau)

    # Vérification si partie terminée ou non
    fini: bool = _partie_terminee(nouveau)

    return nouveau, points_du_coup, fini

# ==========================================================
# 🔒 FONCTIONS PRIVÉES (LOGIQUE INTERNE)
# ==========================================================

def _creer_plateau_vide() -> List[List[int]]:
    """
    Crée une grille TAILLExTAILLE remplie de zéros.
    :return: Une grille vide.
    :rtype: List[List[int]]
    """
    plateau: List[List[int]] = []
    for _ in range(TAILLE):
        ligne: List[int] = []
        for _ in range(TAILLE):
            ligne.append(0)
        plateau.append(ligne)
    return plateau

def _get_cases_vides(plateau: List[List[int]]) -> List[Tuple[int, int]]:
    """
    Retourne les coordonnées des cases vides sous forme d'une liste de coordonnées

    :param plateau: La grille actuelle.
    :type plateau: List[List[int]]
    :return: Une liste de coordonnées
    :rtype: List[Tuple[int, int]]
    """
    cases_vides: List[Tuple[int, int]] = []
    for i in range(TAILLE):
        for j in range(TAILLE):
            if plateau[i][j] == 0:
                cases_vides.append((i, j))
    return cases_vides

def _ajouter_tuile(plateau: List[List[int]]) -> List[List[int]]:
    """
    Ajoute une tuile de valeur 2 sur une case vide.

    :param plateau: La grille actuelle.
    :type plateau: List[List[int]]
    :return: Une nouvelle grille avec une tuile ajoutée.
    :rtype: List[List[int]]
    """
    nouveau: List[List[int]] = []
    for ligne in plateau:
        nouvelle_ligne: List[int] = []
        for valeur in ligne:
            nouvelle_ligne.append(valeur)
        nouveau.append(nouvelle_ligne)

    cases_vides = _get_cases_vides(nouveau)
    if cases_vides:
        i, j = random.choice(cases_vides)
        nouveau[i][j] = 2

    return nouveau

def _supprimer_zeros(ligne: List[int]) -> List[int]:
    """
    Supprime les zéros d'une ligne.

    :param ligne: Une ligne de la grille.
    :type ligne: List[int]
    :return: La ligne sans zéros.
    :rtype: List[int]
    """
    resultat: List[int] = []
    for valeur in ligne:
        if valeur != 0:
            resultat.append(valeur)
    return resultat

def _fusionner(ligne: List[int]) -> Tuple[List[int], int]:
    """
    Fusionne les valeurs identiques consécutives d'une ligne.

    :param ligne: Une ligne sans zéros.
    :type ligne: List[int]
    :return: La ligne après fusion, les points gagnés
    :rtype: Tuple[List[int], int]
    """
    points = 0
    fusion: List[int] = []
    i = 0
    while i < len(ligne):
        # pour fusionner il faut que la case courante ne soit pas la derniere et qu'elle soit égale à la case suivante
        if i+1 < len(ligne) and ligne[i] == ligne[i+1]:
            points += ligne[i]+ligne[i+1]
            fusion.append(ligne[i]+ligne[i+1])
            i+=2
        else:
            fusion.append(ligne[i])
            i+=1
    return fusion, points

def _completer_zeros(ligne: List[int])-> List[int]:
    """
    Ajoute les 0 manquants à la fin de notre ligne

    :param ligne: Une ligne sans zéros.
    :type ligne: List[int]
    :return: une ligne avec les zéros ajoutés
    :rtype: List[int]
    """
    nouvelle_ligne: List[int] = []
    # Je crée une liste remplie de 0
    for _ in range(TAILLE):
        nouvelle_ligne.append(0)
    # J'écrase les premières cases avec le contenu des cases de ligne
    for i in range(len(ligne)):
        nouvelle_ligne[i] = ligne[i]
    return nouvelle_ligne

def _deplacer_gauche(plateau: List[List[int]]) -> Tuple[List[List[int]], int]:
    """
    Déplace les tuiles vers la gauche en fusionnant les valeurs identiques.

    :param plateau: La grille actuelle du jeu.
    :type plateau: List[List[int]]
    :return: Un tuple contenant la nouvelle grille après déplacement et les points gagnés.
    :rtype: Tuple[List[List[int]], int]
    """
    nouveaux_points = 0
    nouveau_plateau: List[List[int]] = []

    for ligne in plateau:
        ligne_sans_zeros = _supprimer_zeros(ligne)
        ligne_fusionnee, points = _fusionner(ligne_sans_zeros)# <--- Bien récupérer les points ici
        nouveaux_points += points # <--- Et les cumuler
        ligne_finale = _completer_zeros(ligne_fusionnee)
        nouveau_plateau.append(ligne_finale)
    return nouveau_plateau, nouveaux_points

def _inverser_lignes(plateau: List[List[int]]) -> List[List[int]]:
    """
    Inverse l'ordre des éléments de chaque ligne.

    :param plateau: La grille actuelle.
    :type plateau: List[List[int]]
    :return: La grille modifiée.
    :rtype: List[List[int]]
    """
    lignes_inversees: List[List[int]] = []
    for ligne in plateau:
        nouvelle_ligne: List[int] = []
        i = len(ligne) - 1
        while i >= 0:
            nouvelle_ligne.append(ligne[i])
            i -= 1
        lignes_inversees.append(nouvelle_ligne)

    return lignes_inversees

def _deplacer_droite(plateau: List[List[int]]) -> Tuple[List[List[int]], int]:
    """
    Déplace les tuiles vers la droite en fusionnant les valeurs identiques.

    :param plateau: La grille actuelle du jeu.
    :type plateau: List[List[int]]
    :return: Un tuple contenant la nouvelle grille après déplacement et les points gagnés.
    :rtype: Tuple[List[List[int]], int]
    """
    plateau_inverse = _inverser_lignes(plateau)
    plateau_deplace, nouveaux_points = _deplacer_gauche(plateau_inverse)
    plateau_final = _inverser_lignes(plateau_deplace)
    return plateau_final, nouveaux_points

def _transposer(plateau: List[List[int]]) -> List[List[int]]:
    """
    Transpose la grille (lignes ↔ colonnes).

    :param plateau: La grille à transposer.
    :return: La grille transposée.
    """
    nouveau_plateau: List[List[int]] = []

    for i in range(TAILLE):
        ligne: List[int] = []
        for j in range(TAILLE):
            ligne.append(plateau[j][i])
        nouveau_plateau.append(ligne)

    return nouveau_plateau

def _deplacer_haut(plateau: List[List[int]]) -> Tuple[List[List[int]], int]:
    """
    Déplace les tuiles vers le haut en fusionnant les valeurs identiques.

    :param plateau: La grille actuelle du jeu.
    :return: Un tuple contenant la nouvelle grille après déplacement et les points gagnés.
    """
    plateau_transpose = _transposer(plateau)
    plateau_deplace, nouveaux_points  = _deplacer_gauche(plateau_transpose)
    plateau_final = _transposer(plateau_deplace)
    return plateau_final, nouveaux_points


def _deplacer_bas(plateau: List[List[int]]) -> Tuple[List[List[int]], int]:
    """
    Déplace les tuiles vers le bas en fusionnant les valeurs identiques.

    :param plateau: La grille actuelle du jeu.
    :return: Un tuple contenant la nouvelle grille après déplacement et les points gagnés.
    """
    plateau_transpose = _transposer(plateau)
    plateau_deplace, nouveaux_points = _deplacer_droite(plateau_transpose)
    plateau_final = _transposer(plateau_deplace)
    return plateau_final, nouveaux_points

def _partie_terminee(plateau: List[List[int]]) -> bool:
    """
    Indique si aucun déplacement n'est possible.

    :param plateau: La grille actuelle.
    :return: True si la partie est terminée, False sinon.
    """
    # Partie non terminee si il y a des cases vides
    # Partie non terminee si il y a des fusions possibles (horizontale ou verticale)
    # Sinon c'est vrai
    # raise NotImplementedError("Fonction partie_terminee non encore implémentée.")
    # 1. S'il reste une case vide, ce n'est pas fini
    if _get_cases_vides(plateau):
        return False

    # 2. Vérifier les fusions possibles (horizontalement et verticalement)
    for i in range(TAILLE):
        for j in range(TAILLE):
            # Fusion horizontale possible ?
            if j + 1 < TAILLE and plateau[i][j] == plateau[i][j+1]:
                return False
            # Fusion verticale possible ?
            if i + 1 < TAILLE and plateau[i][j] == plateau[i+1][j]:
                return False

    return True

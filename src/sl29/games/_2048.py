"""Module providing the logic of the 2048 game"""

import random
import copy
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
    plateau2 =_ajouter_tuile(plateau)
    plateau3 = _ajouter_tuile(plateau2)
    return plateau3, 0

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
    return [[0 for _ in range(TAILLE)] for _ in range(TAILLE)]

def _get_cases_vides(plateau: List[List[int]]) -> List[Tuple[int, int]]:
    """
    Retourne les coordonnées des cases vides sous forme d'une liste de coordonnées

    :param plateau: La grille actuelle.
    :type plateau: List[List[int]]
    :return: Une liste de coordonnées
    :rtype: List[Tuple[int, int]]
    """
    liste = []
    for i in range(len((plateau))):
        for j in range(len((plateau))):
            if plateau[i][j] == 0:
                liste.append((i,j))
    return liste

def _ajouter_tuile(plateau: List[List[int]]) -> List[List[int]]:
    """
    Ajoute une tuile de valeur 2 sur une case vide.

    :param plateau: La grille actuelle.
    :type plateau: List[List[int]]
    :return: Une nouvelle grille avec une tuile ajoutée.
    :rtype: List[List[int]]
    """
    liste = _get_cases_vides(plateau)
    (i,j) = random.choice(liste)
    n_plateau = copy.deepcopy(plateau)
    n_plateau[i][j]= 2
    return n_plateau


def _supprimer_zeros(ligne: List[int]) -> List[int]:
    """
    Supprime les zéros d'une ligne.

    :param ligne: Une ligne de la grille.
    :type ligne: List[int]
    :return: La ligne sans zéros.
    :rtype: List[int]
    """
    result = []
    for value in ligne:
        if value != 0:
            result.append(value)
    return result


def _fusionner(ligne: List[int]) -> Tuple[List[int], int]:
    """
    Fusionne les valeurs identiques consécutives d'une ligne.

    :param ligne: Une ligne sans zéros.
    :type ligne: List[int]
    :return: La ligne après fusion, les points gagnés
    :rtype: Tuple[List[int], int]
    """
    liste_fusionnee = []
    i = 0
    points = 0
    
    while i < len(ligne):
        if (i+1)< len(ligne) and ligne[i]==ligne[i+1]:
            fusion = ligne[i] + ligne[i+1]
            points += fusion
            liste_fusionnee.append(fusion)
            i += 2
        else:
            liste_fusionnee.append(ligne[i])
            i += 1
    return liste_fusionnee, points


def _completer_zeros(ligne: List[int]) -> List[int]:
    """
    :param ligne: Une ligne sans zeros
    :type ligne: List[int]
    :return: La ligne avec des zeros apres fusion
    :rtype: Tuple[List[int], int]
    """
    liste = ligne
    while len(liste) < TAILLE:
        liste.append(0)
    return liste


def _deplacer_gauche(plateau: List[List[int]]) -> Tuple[List[List[int]], int]:
    """
    Déplace les tuiles vers la gauche en fusionnant les valeurs identiques.
    
    :param plateau: La grille actuelle du jeu.
    :type plateau: List[List[int]]
    :return: Un tuple contenant la nouvelle grille après déplacement et les points gagnés.
    :rtype: Tuple[List[List[int]], int]
    """
    nv_plateau = []
    nv_points = 0
    for i in range(len(plateau)):
        ligne_sans_zeros = _supprimer_zeros(plateau[i])
        ligne_fusionee, points = _fusionner(ligne_sans_zeros)
        nv_points += points
        ligne_finale = _completer_zeros(ligne_fusionee)
        nv_plateau.append(ligne_finale)
    return nv_plateau, nv_points


def _inverser_lignes(plateau: List[List[int]]) -> List[List[int]]:
    """
    Inverse l'ordre des lignes du plateau (première ligne devient dernière, etc.).
    
    :param plateau: La grille actuelle du jeu.
    :type plateau: List[List[int]]
    :return: Le plateau avec les lignes inversées.
    :rtype: List[List[int]]
    """
    return plateau[::-1]


def _deplacer_droite(plateau: List[List[int]]) -> Tuple[List[List[int]], int]:
    """
    Déplace les tuiles vers la droite en fusionnant les valeurs identiques.

    :param plateau: La grille actuelle du jeu.
    :type plateau: List[List[int]]
    :return: Un tuple contenant la nouvelle grille après déplacement et les points gagnés.
    :rtype: Tuple[List[List[int]], int]
    """
    nv_plateau = []
    nv_points = 0
    for i in range(len(plateau)):
        ligne_inversee = plateau[i][::-1]
        ligne_sans_zeros = _supprimer_zeros(ligne_inversee)
        ligne_fusionee, points = _fusionner(ligne_sans_zeros)
        nv_points += points
        ligne_finale = _completer_zeros(ligne_fusionee)
        ligne_finale = ligne_finale[::-1]
        nv_plateau.append(ligne_finale)
    return nv_plateau, nv_points


def _transposer(plateau: List[List[int]]) -> List[List[int]]:
    """
    Transpose la matrice (échange lignes et colonnes).
    
    :param plateau: La grille actuelle du jeu.
    :type plateau: List[List[int]]
    :return: La grille transposée.
    :rtype: List[List[int]]
    """
    return [[plateau[i][j] for i in range(len(plateau))] for j in range(len(plateau[0]))]


def _deplacer_haut(plateau: List[List[int]]) -> Tuple[List[List[int]], int]:
    """
    Déplace les tuiles vers le haut.

    :param plateau: La grille actuelle du jeu.
    :return: Un tuple contenant la nouvelle grille après déplacement et les points gagnés.
    """
    plateau_transpose = _transposer(plateau)
    plateau_deplace, points = _deplacer_gauche(plateau_transpose)
    return _transposer(plateau_deplace), points


def _deplacer_bas(plateau: List[List[int]]) -> Tuple[List[List[int]], int]:
    """
    Déplace les tuiles vers le bas.

    :param plateau: La grille actuelle du jeu.
    :return: Un tuple contenant la nouvelle grille après déplacement et les points gagnés.
    """
    plateau_transpose = _transposer(plateau)
    plateau_deplace, points = _deplacer_droite(plateau_transpose)
    return _transposer(plateau_deplace), points

def _partie_terminee(plateau: List[List[int]]) -> bool:
    """
    Vérifie si la partie est terminée.
    """
    return False

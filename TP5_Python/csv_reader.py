
import csv
import os


# Exception principale
class CsvException(Exception):
    def __init__(self, message):
        super().__init__(message)


# Exceptions spécialisées
class FichierIntrouvableException(CsvException):
    pass


class LigneInvalideException(CsvException):
    pass


class PrixNegatifException(CsvException):
    pass


def charger_csv(chemin):
    articles = []

    if not os.path.exists(chemin):
        raise FichierIntrouvableException(
            "Le fichier CSV est introuvable."
        )

    with open(chemin, "r", encoding="utf-8", newline="") as fichier:
        lecteur = csv.reader(fichier, delimiter=";")

        for numero, ligne in enumerate(lecteur, start=1):

            # Ignorer les lignes vides
            if not ligne or all(colonne.strip() == "" for colonne in ligne):
                continue

            # Vérifier le nombre de colonnes
            if len(ligne) != 3:
                raise LigneInvalideException(
                    f"Ligne {numero} : exactement 3 colonnes sont attendues."
                )

            identifiant, nom, prix = [colonne.strip() for colonne in ligne]

            # Vérifier les champs obligatoires
            if not identifiant or not nom or not prix:
                raise LigneInvalideException(
                    f"Ligne {numero} : une colonne est vide."
                )

            # Vérifier que le prix est numérique
            try:
                prix = float(prix)
            except ValueError:
                raise LigneInvalideException(
                    f"Ligne {numero} : le prix doit être numérique."
                )

            # Vérifier que le prix est strictement positif
            if prix <= 0:
                raise PrixNegatifException(
                    f"Ligne {numero} : le prix doit être supérieur à zéro."
                )

            articles.append({
                "id": identifiant,
                "nom": nom,
                "prix": prix
            })

    return articles

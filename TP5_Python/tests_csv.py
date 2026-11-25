
import unittest
import os

from csv_reader import (
    charger_csv,
    FichierIntrouvableException,
    LigneInvalideException,
    PrixNegatifException
)


class TestCSV(unittest.TestCase):

    def setUp(self):
        self.fichier = "test_articles.csv"

    def tearDown(self):
        if os.path.exists(self.fichier):
            os.remove(self.fichier)

    def creer_fichier(self, contenu):
        with open(self.fichier, "w", encoding="utf-8") as f:
            f.write(contenu)

    def test_csv_valide(self):
        self.creer_fichier("1;Clavier;150\n2;Souris;80\n")
        articles = charger_csv(self.fichier)
        self.assertEqual(len(articles), 2)

    def test_fichier_absent(self):
        with self.assertRaises(FichierIntrouvableException):
            charger_csv("inexistant.csv")

    def test_prix_texte(self):
        self.creer_fichier("1;Clavier;abc\n")
        with self.assertRaises(LigneInvalideException):
            charger_csv(self.fichier)

    def test_prix_negatif(self):
        self.creer_fichier("1;Clavier;-50\n")
        with self.assertRaises(PrixNegatifException):
            charger_csv(self.fichier)

    def test_colonnes_incorrectes(self):
        self.creer_fichier("1;Clavier\n")
        with self.assertRaises(LigneInvalideException):
            charger_csv(self.fichier)


if __name__ == "__main__":
    unittest.main()

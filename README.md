# Scraping books.toscrape.com

Application permettant d'extraire les informations de tous les produits du site books.toscrape.com.

## Installation et Exécution

Si vous avez déjà installé Python, assurez-vous que sa version est à jour.
Sinon, téléchargez et installez Python. [Site Web](https://www.python.org/downloads/)

Commencez par télécharger le repository en cliquant sur le menu "Code", puis "Download ZIP".

Extrayez le dossier. Dans celui-ci, créez et activez un environnement virtuel. Pour cela :
- Ouvrez votre terminal et placez-vous dans le dossier extrait,
- Exécutez la commande : `python -m venv env`,
- Exécutez ensuite la commande : `source env/bin/activate` (Sous Windows, l'activation se fera avec le fichier env/Scripts/activate.bat).

Installez les dépendances en exécutant la commande : `pip install -r requirements.txt`

Tout est prêt ! Lancez l'application avec la commande : `python book_scrap.py`

Dans le dossier "csv", vous trouverez les informations des produits selon leur catégorie.

Dans le dossier "img", vous trouverez les images de tous les produits.

Les fichiers csv doivent être ouverts en utf-8 dans le logiciel utilisé (exemple : Excel).

## Utilisations alternatives

- Afficher les informations d'un produit : `python product.py (nom du produit)`,
- Afficher la liste des produits d'une catégorie : `python category.py (nom de la catégorie)`,
- Récupérer un nombre limité de catégories : `python book_scrap.py (nombre de catégories)`.
    
Le nom du produit ou de la catégorie doit être écrit comme sur le site. S'il y a des espaces, entourez le nom avec des guillemets.
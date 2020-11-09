"""Script récupérant les informations de tous les produits du site web."""
import os
import sys

import requests
from bs4 import BeautifulSoup

from category import get_category_products


def main(number):
    """Fonction principale exécutant le script."""
    # Création des dossiers csv et img.
    if not os.path.exists("csv"):
        os.mkdir("csv")
    if not os.path.exists("img"):
        os.mkdir("img")

    r = requests.get("http://books.toscrape.com/index.html")
    r.encoding = "utf-8"
    if r.ok:
        index_page = BeautifulSoup(r.text, "lxml")
        # Récupération du nom et de l'url de chaque catégorie.
        category_links = index_page.select_one(".nav-list ul").select("li a")
        if number is None:
            for category in category_links:
                category_name = category.get_text().strip()
                category_url = "http://books.toscrape.com/" + category.get("href")
                get_category_products(category_name, category_url)
        else:
            if number.isdigit():
                number = int(number)
                i = 0
                for category in category_links:
                    category_name = category.get_text().strip()
                    category_url = "http://books.toscrape.com/" + category.get("href")
                    get_category_products(category_name, category_url)
                    i += 1
                    if i >= number:
                        break
            else:
                print("Spécifiez un nombre de catégories correct.")


if __name__ == '__main__':
    try:
        number = sys.argv[1]
    except IndexError:
        number = None

    main(number)

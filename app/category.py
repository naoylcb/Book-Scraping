"""Script récupérant les informations des produits d'une catégorie."""
import sys
import csv
import datetime

import requests
from bs4 import BeautifulSoup

import product


def get_category_products(c_name, c_url):
    """Fonction récupérant les informations des produits d'une catégorie dans un fichier csv."""
    # Récupération de la date.
    date = str(datetime.date.today())

    # Écriture des en-têtes du fichier csv de la catégorie.
    with open(f"csv/{date}-{c_name}.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f, delimiter=";")
        writer.writerow(["product_page_url", "universal_product_code", "title", "price_including_tax",
                         "price_excluding_tax", "number_available", "product_description", "category",
                         "review_rating",
                         "image_url"])

    # Requête à l'url de la catégorie.
    r = requests.get(c_url)
    r.encoding = "utf-8"
    if r.ok:
        i = 1
        # Parcours des pages de la catégorie en ajoutant les informations de chaque produit dans le fichier csv.
        while r.status_code != 404:
            category_page = BeautifulSoup(r.text, "lxml")
            products_links = category_page.select(".col-xs-6")
            for p in products_links:
                product.get_product_infos(date, "http://books.toscrape.com/catalogue/" +
                                  p.select_one(".image_container a").get("href").replace("../../../", ""))
            i += 1
            r = requests.get(c_url.replace(f"index", f"page-{i}"))
            r.encoding = "utf-8"

    print(f"{c_name} / OK")


def print_category_products(c_name):
    """Fonction listant les produits d'une catégorie."""
    c_url = ""

    # Requête à l'url de la page d'accueil du site web.
    r = requests.get("http://books.toscrape.com/index.html")
    r.encoding = "utf-8"
    if r.ok:
        index_page = BeautifulSoup(r.text, "lxml")
        # Récupération de l'url de la catégorie choisie.
        category_links = index_page.select_one(".nav-list ul").select("li a")
        for category in category_links:
            if c_name == category.get_text().strip():
                c_url = "http://books.toscrape.com/" + category.get("href")
                break

    # Si la catégorie existe.
    if c_url != "":
        # Requête à l'url de la catégorie.
        r = requests.get(c_url)
        r.encoding = "utf-8"
        if r.ok:
            i = 1
            # Parcours des pages de la catégorie en listant les produits.
            while r.status_code != 404:
                category_page = BeautifulSoup(r.text, "lxml")
                products_links = category_page.select(".col-xs-6")
                for p in products_links:
                    print(p.select_one(".image_container img").get("alt"))
                i += 1
                r = requests.get(c_url.replace(f"index", f"page-{i}"))
                r.encoding = "utf-8"
    # Si la catégorie n'existe pas.
    else:
        print("Cette catégorie n'existe pas.")


if __name__ == '__main__':
    print_category_products(sys.argv[1])

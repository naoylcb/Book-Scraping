"""Script qui récupère les informations de tous les produits"""

import requests
import csv
from bs4 import BeautifulSoup
import os

img_number = 0


def get_infos_product(p_url):
    """Fonction qui récupère les informations d'un produit,
    les ajoutes dans le fichier csv de sa catégorie et télécharge l'image du produit"""

    r = requests.get(p_url)
    r.encoding = "utf-8"
    if r.ok:
        page = BeautifulSoup(r.text, "lxml")

        p_title = page.find("h1").get_text()
        p_category = page.find("ul", class_="breadcrumb").select_one("li:nth-of-type(3) a").get_text()

        p_image_attrs = page.find("img").attrs
        p_image_url = "http://books.toscrape.com/" + p_image_attrs["src"].replace("../../", "")

        p_stars_attrs = page.select_one(".star-rating").attrs
        p_review_rating = p_stars_attrs["class"][1]

        try:
            p_description = page.select_one("#product_description + p").get_text()
        except AttributeError:
            p_description = "pas de description"

        p_infos = page.find_all("td")
        p_upc = p_infos[0].get_text()
        p_exc_tax = p_infos[2].get_text().replace("£", "")
        p_inc_tax = p_infos[3].get_text().replace("£", "")
        p_availability = "".join(list(filter(str.isdigit, p_infos[5].get_text())))

        # Ajout des informations du produit dans le fichier csv de sa catégorie
        with open(f"csv/{p_category}.csv", "a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f, delimiter=";")
            writer.writerow([p_url, p_upc, p_title, p_inc_tax, p_exc_tax, p_availability, p_description, p_category,
                             p_review_rating, p_image_url])

        # Téléchargement de l'image du produit
        global img_number
        img_number += 1
        image_r = requests.get(p_image_url)
        with open(f"img/img_{img_number}.jpg", "wb") as f:
            f.write(image_r.content)


def get_products_category(c_name, c_url):
    """Fonction qui récupère les informations de tous les produits d'une catégorie
    dans un fichier csv"""

    # Écriture des en-têtes du fichier csv de la catégorie
    with open(f"csv/{c_name}.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f, delimiter=";")
        writer.writerow(["product_page_url", "universal_product_code", "title", "price_including_tax",
                         "price_excluding_tax", "number_available", "product_description", "category",
                         "review_rating",
                         "image_url"])

    r = requests.get(c_url)
    r.encoding = "utf-8"
    if r.ok:
        i = 1
        # Parcours des pages de la catégorie en ajoutant les informations de chaque produit dans le fichier csv
        while r.status_code != 404:
            category_page = BeautifulSoup(r.text, "lxml")
            p_links = category_page.select(".col-xs-6")
            for l in p_links:
                get_infos_product("http://books.toscrape.com/catalogue/" +
                                 l.select_one(".image_container a").get("href").replace("../../../", ""))
            i += 1
            r = requests.get(c_url.replace(f"index", f"page-{i}"))
            r.encoding = "utf-8"


def main():
    """Fonction principale exécutant le script"""

    # Création des dossiers csv et img
    try:
        os.mkdir("csv")
    except FileExistsError:
        pass

    try:
        os.mkdir("img")
    except FileExistsError:
        pass

    r = requests.get("http://books.toscrape.com/index.html")
    r.encoding = "utf-8"
    if r.ok:
        index_page = BeautifulSoup(r.text, "lxml")
        # Récupération du nom et de l'url de chaque catégorie afin de récupérer les produits de celle-ci
        category_links = index_page.select_one(".nav-list ul").select("li a")
        for category in category_links:
            category_name = category.get_text().strip().lower()
            category_url = "http://books.toscrape.com/" + category.get("href")
            get_products_category(category_name, category_url)


if __name__ == '__main__':
    main()

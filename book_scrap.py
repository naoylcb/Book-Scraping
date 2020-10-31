"""Script qui récupère les informations de tous les produits d'une catégorie choisie
(en mettant son nom en deuxième argument dans la commande)"""

import requests
import csv
from bs4 import BeautifulSoup
import sys

# Fonction qui récupère les informations d'une page produit
def get_info_product(p_url):
    r = requests.get(p_url)
    r.encoding = "utf-8"
    if r.ok:
        page = BeautifulSoup(r.text, "lxml")

        p_title = page.find("h1").get_text()
        p_description = page.select_one("#product_description + p").get_text()
        p_category = page.find("ul", class_="breadcrumb").select_one("li:nth-of-type(3) a").get_text()

        p_image_attrs = page.find("img").attrs
        p_image_url = "http://books.toscrape.com/" + p_image_attrs["src"].replace("../../", "")

        p_stars_attrs = page.select_one(".star-rating").attrs
        p_review_rating = p_stars_attrs["class"][1]

        p_infos = page.find_all("td")
        p_upc = p_infos[0].get_text()
        p_exc_tax = p_infos[2].get_text().replace("£", "")
        p_inc_tax = p_infos[3].get_text().replace("£", "")
        p_availability = p_infos[5].get_text().replace("In stock (", "").replace(" available)", "")

        with open("products.csv", "a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f, delimiter=";")
            writer.writerow([p_url, p_upc, p_title, p_inc_tax, p_exc_tax, p_availability, p_description, p_category,
                             p_review_rating, p_image_url])


categories = {}
category_url = ""
products_urls = []

r = requests.get("http://books.toscrape.com/index.html")
r.encoding = "utf-8"
if r.ok:
    index_page = BeautifulSoup(r.text, "lxml")

    # Récupération du nom et de l'url de chaque catégorie
    c_links = index_page.select_one(".nav-list ul").select("li a")
    for c in c_links:
        c_name = c.get_text().strip().lower()
        c_url = "http://books.toscrape.com/" + c.get("href")
        categories[c_name] = c_url

    # Écriture des en-têtes du fichier csv
    with open("products.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f, delimiter=";")
        writer.writerow(["product_page_url", "universal_product_code", "title", "price_including_tax",
                         "price_excluding_tax", "number_available", "product_description", "category",
                         "review_rating",
                         "image_url"])

    # Récupération de l'url de la catégorie passée en argument dans la commande
    for k,v in categories.items():
        if sys.argv[1] == k:
            category_url = v

    category_url = category_url.replace("index", "page-1")
    r = requests.get(category_url)
    r.encoding = "utf-8"
    # Si la catégorie a plusieurs pages
    if r.ok:
        i = 1
        # Parcours de toutes les pages en écrivant les informations de chaque produit dans le fichier csv
        while r.status_code != 404:
            category_page = BeautifulSoup(r.text, "lxml")
            p_links = category_page.select(".col-xs-6")
            for l in p_links:
                get_info_product("http://books.toscrape.com/catalogue/" +
                                     l.select_one(".image_container a").get("href").replace("../../../", ""))
            i += 1
            r = requests.get(category_url.replace(f"page-1", f"page-{i}"))
            r.encoding = "utf-8"
    # Si la catégorie a une seule page
    elif r.status_code == 404:
        r = requests.get(category_url.replace("page-1", "index"))
        r.encoding = "utf-8"
        if r.ok:
            category_page = BeautifulSoup(r.text, "lxml")
            p_links = category_page.select(".col-xs-6")
            for l in p_links:
                get_info_product("http://books.toscrape.com/catalogue/" +
                                 l.select_one(".image_container a").get("href").replace("../../../", ""))

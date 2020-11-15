"""Script récupérant les informations d'un produit."""
import sys
import csv

import requests
from bs4 import BeautifulSoup

img_number = 0


def get_product_infos(date, p_url):
    """Fonction qui télécharge l'image du produit et qui récupère les informations du produit dans un fichier csv."""
    # Requête à l'url de la page produit.
    r = requests.get(p_url)
    r.encoding = "utf-8"
    if r.ok:
        page = BeautifulSoup(r.text, "lxml")

        p_title = page.find("h1").get_text()

        p_category = page.select_one(".breadcrumb").select_one("li:nth-of-type(3) a").get_text()

        p_image_attrs = page.find("img").attrs
        p_image_url = "http://books.toscrape.com/" + p_image_attrs["src"].replace("../../", "")

        number_rating = {"One": "1", "Two": "2", "Three": "3", "Four": "4", "Five": "5"}
        p_stars_attrs = page.select_one(".star-rating").attrs
        text_number = p_stars_attrs["class"][1]
        p_review_rating = number_rating[text_number]

        # Texte par défaut si le produit n'a pas de description.
        try:
            p_description = page.select_one("#product_description + p").get_text()
        except AttributeError:
            p_description = "pas de description"

        p_infos = page.find_all("td")
        p_upc = p_infos[0].get_text()
        p_excl_tax = p_infos[2].get_text().replace("£", "")
        p_incl_tax = p_infos[3].get_text().replace("£", "")
        p_availability = "".join(list(filter(str.isdigit, p_infos[5].get_text())))

        # Téléchargement de l'image du produit.
        global img_number
        img_number += 1
        image_r = requests.get(p_image_url)
        p_image_url = f"img/img_{img_number}.jpg"
        with open(p_image_url, "wb") as f:
            f.write(image_r.content)

        # Écriture des informations du produit dans le fichier csv de sa catégorie.
        with open(f"csv/{date}-{p_category}.csv", "a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f, delimiter=";")
            writer.writerow([p_url, p_upc, p_title, p_incl_tax, p_excl_tax, p_availability, p_description, p_category,
                             p_review_rating, p_image_url])


def print_product_infos(p_name):
    """Fonction affichant les informations d'un produit."""
    p_url = ""

    # Requête à l'url de la page d'accueil du site web.
    url = "http://books.toscrape.com/catalogue/page-1.html"
    r = requests.get(url)
    r.encoding = "utf-8"
    if r.ok:
        i = 1
        # Parcours des pages du site web afin de récupérer l'url du produit.
        while r.status_code != 404 and p_url == "":
            web_page = BeautifulSoup(r.text, "lxml")
            p_links = web_page.select(".col-xs-6")
            for p in p_links:
                if p_name == p.select_one(".image_container img").get("alt"):
                    p_url = "http://books.toscrape.com/catalogue/" + p.select_one(".image_container a").get("href")
            i += 1
            r = requests.get(url.replace(f"page-1", f"page-{i}"))
            r.encoding = "utf-8"

    # Si le produit existe.
    if p_url != "":
        # Requête à l'url de la page produit.
        r = requests.get(p_url)
        r.encoding = "utf-8"
        if r.ok:
            # Dictionnaire qui contiendra les informations du produit.
            product_infos = {}
            page = BeautifulSoup(r.text, "lxml")

            product_infos["CATÉGORIE"] = page.select_one(".breadcrumb").select_one(
                "li:nth-of-type(3) a").get_text()

            p_image_attrs = page.find("img").attrs
            product_infos["URL IMAGE"] = "http://books.toscrape.com/" + p_image_attrs["src"].replace("../../", "")

            number_rating = {"One": "1", "Two": "2", "Three": "3", "Four": "4", "Five": "5"}
            p_stars_attrs = page.select_one(".star-rating").attrs
            text_number = p_stars_attrs["class"][1]
            product_infos["NOTE"] = number_rating[text_number]

            # Texte par défaut si le produit n'a pas de description.
            try:
                product_infos["DESCRIPTION"] = page.select_one("#product_description + p").get_text()
            except AttributeError:
                product_infos["DESCRIPTION"] = "pas de description"

            p_infos = page.find_all("td")
            product_infos["UPC"] = p_infos[0].get_text()
            product_infos["PRIX HT"] = p_infos[2].get_text().replace("£", "")
            product_infos["PRIX TTC"] = p_infos[3].get_text().replace("£", "")
            product_infos["EN STOCK"] = "".join(list(filter(str.isdigit, p_infos[5].get_text())))

            # Affichage des informations du produit.
            for name, info in product_infos.items():
                print(name, ":", info)
    # Si le produit n'existe pas.
    else:
        print("Ce produit n'existe pas.")


if __name__ == '__main__':
    print_product_infos(sys.argv[1])

import requests
import csv
from bs4 import BeautifulSoup

p_url = "http://books.toscrape.com/catalogue/the-black-maria_991/index.html"
response = requests.get(p_url)
response.encoding = "utf-8"

if response.ok:
    page = BeautifulSoup(response.text, "lxml")

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

    with open("file.csv", "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file, delimiter=";")
        writer.writerow(["product_page_url", "universal_product_code", "title", "price_including_tax",
                         "price_excluding_tax", "number_available", "product_description", "category", "review_rating",
                         "image_url"])
        writer.writerow([p_url, p_upc, p_title, p_inc_tax, p_exc_tax, p_availability, p_description, p_category,
                         p_review_rating, p_image_url])

*(Project realized during my training)*  
*(The goal being to learn scraping)*

# Scraping books.toscrape.com

Application to extract information from all products on the books.toscrape.com site.

## Installation and execution

If you already have Python installed, make sure its version is up to date.
If not, download and install Python. [Website](https://www.python.org/downloads/)

Start by downloading the repository by clicking on the "Code" menu, then "Download ZIP".

Extract the folder. In it, create and activate a virtual environment. To do this:
- Open your terminal and place yourself in the extracted folder,
- Run the command: `python -m venv env`,
- Then run the command: `source env/bin/activate` (On Windows, activation will be done with the file env/Scripts/activate.bat).

Install the dependencies by running the command: `pip install -r requirements.txt`.

Everything is ready! Run the application with the command: `python book_scrap.py`

In the "csv" folder, you will find the product information according to their category.

In the "img" folder, you will find the images of all products.

The csv files must be opened in utf-8 in the software used (example: Excel).

## Alternative uses

- Display the information of a product: `python product.py (product name)`,
- Display the list of products in a category: `python category.py (category name)`,
- Retrieve a limited number of categories: `python book_scrap.py (number of categories)`.
    
The name of the product or category must be written as it is on the site. If there are spaces, surround the name with quotes.
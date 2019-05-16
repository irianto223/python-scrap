from requests import get
from bs4 import BeautifulSoup

page        = get('http://www.nanokomputer.com/', {}, stream=True)
parsed_page = BeautifulSoup(page.content, 'html.parser')
side_bar    = parsed_page.find_all('li', class_=['daddy', 'cat_lev_0'])
cat_lev_1   = []

for parent in side_bar:
  child = parent.find_all(class_=['daddy', 'cat_lev_1'])
  cat_lev_1.append(child)

# def get_product_link(arr_of_product_elements):

print(cat_lev_1)
print(len(cat_lev_1))
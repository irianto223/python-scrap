import os
from requests import get
from bs4 import BeautifulSoup

BASE_URL = 'http://www.nanokomputer.com/' 



def get_homepage():
  print("Fetching homepage ...")
  
  if os.path.exists("./data/html/homepage.html"):
    print("homepage.html already exists.")
  else:
    homepage  = get(BASE_URL, {}, stream=True)
    parsed    = BeautifulSoup(homepage.content, 'html.parser')
    f = open("./data/html/homepage.html", "a")
    f.write(parsed.prettify())
    print("DONE.")  



def get_megamenu_link():
  f                             = open("./data/html/homepage.html", "r")
  homepage                      = BeautifulSoup(f.read(), 'html.parser')
  all_link_with_link_lev_class  = homepage.select('a[class^=link_lev_]')

  print("Fetching mega menu ...")

  if os.path.exists("./data/txt/megamenu-link.txt"):
    print("megamenu-link.txt already exists.")
  else:
    ff = open("./data/txt/megamenu-link.txt", "a")
    for i in all_link_with_link_lev_class:
      
      if 'daddy' in i['class']:
        continue
      else:
        if all_link_with_link_lev_class.index(i) < len(all_link_with_link_lev_class)-1:
          ff.write(i['href']+"\n")
        else:
          ff.write(i['href'])
    
    ff.close()
    print("DONE.")
  
  f.close()



def get_product_list_page():
  print("Fetching product list page ...")
  megamenu_total_line = sum(1 for line in open("./data/txt/megamenu-link.txt"))

  if os.path.exists("./data/html/product-list-" + str(megamenu_total_line) + ".html"):
    print("product-list.html already exists.")
  else:
    f     = open("./data/txt/megamenu-link.txt", "r")
    count = 1
    for data in f:
      product_list_page = get(data, {}, stream=True)
      parsed            = BeautifulSoup(product_list_page.content, 'html.parser')
      # ff = open("./data/html/product-list-" + str(i) + ".html", "a")
      ff = open("./data/html/product-list-" + str(count) + ".html", "a")
      ff.write(parsed.prettify())
      ff.close()
      count += 1
    print("DONE.")


def get_product_link():
  # harusnya bisa dapat dengan kata kunci "<a href="http://www.nanokomputer.com/product_info.php?"

get_homepage()
get_megamenu_link()
get_product_list_page()
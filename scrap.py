from requests import get
from bs4 import BeautifulSoup

import os


url = 'http://www.nanokomputer.com/'


def get_homepage(url):
  homepage  = get(url, {}, stream=True)
  parsed    = BeautifulSoup(homepage.content, 'html.parser')
  return parsed


def get_product_link(homepage):
  all_link_with_link_lev_class  = homepage.select('a[class^=link_lev_]')
  link                          = []
  
  for i in all_link_with_link_lev_class:
  
    if 'daddy' in i['class']:
      continue
    else:
      link.append(i['href'])
  
  return link


def write_megamenu_link_txt(list, filename):
  # os.remove(filename)
  f = open(filename, "a")
  
  for i in list:
    if list.index(i) < len(list)-1:
      f.write(i+"\n")
    else:
      f.write(i)

  f.close()


def get_product_list(txtfile):
  if os.path.exists(txtfile):
    print("EXISTS")
  else:
    result = get_product_link(get_homepage(url))
    write_megamenu_link_txt(result, txtfile)
    print("CREATED")



get_product_list("megamenu-link.txt")


# print(result)
# print(len(result))

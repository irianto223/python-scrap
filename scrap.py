from requests import get
from bs4 import BeautifulSoup

page                          = get('http://www.nanokomputer.com/', {}, stream=True)
parsed_page                   = BeautifulSoup(page.content, 'html.parser')
all_link_with_link_lev_class  = parsed_page.select('a[class^=link_lev_]')


def get_product_link(product_element_list):

  link  = []
  
  for i in product_element_list:
  
    if 'daddy' in i['class']:
      continue
    else:
      link.append(i['href'])
  
  return link
  

result = get_product_link(all_link_with_link_lev_class)

print(result)
print(len(result))

import os, sys, resource, csv, urllib.parse
from requests import get
from bs4 import BeautifulSoup

resource.setrlimit(resource.RLIMIT_STACK, (2**29,-1))
sys.setrecursionlimit(10**6)

BASE_URL = 'http://www.nanokomputer.com/' 



def get_homepage():
  print('Fetching homepage ...')
  
  if os.path.exists('./data/html/homepage.html'):
    print('homepage.html already exists.')
  else:
    homepage  = get(BASE_URL, {}, stream=True)
    parsed    = BeautifulSoup(homepage.content, 'html.parser')
    f = open('./data/html/homepage.html', 'a')
    f.write(parsed.prettify())
    f.close()
    print('DONE.')  



def get_megamenu_link():
  f                             = open('./data/html/homepage.html', 'r')
  homepage                      = BeautifulSoup(f.read(), 'html.parser')
  all_link_with_link_lev_class  = homepage.select('a[class^=link_lev_]')

  print('Fetching mega menu URL ...')

  if os.path.exists('./data/txt/megamenu-link.txt'):
    print('megamenu-link.txt already exists.')
  else:
    ff = open('./data/txt/megamenu-link.txt', 'a')
    for i in all_link_with_link_lev_class:
      
      if 'daddy' in i['class']:
        continue
      else:
        if all_link_with_link_lev_class.index(i) < len(all_link_with_link_lev_class)-1:
          ff.write(i['href']+'\n')
          print(i['href'])
        else:
          ff.write(i['href'])
    
    ff.close()
    print('DONE.')
  
  f.close()



def get_product_list_page():
  print('Fetching product list page ...')
  megamenu_total_line = sum(1 for line in open('./data/txt/megamenu-link.txt'))

  if os.path.exists('./data/html/product-list/product-list-' + str(megamenu_total_line) + '.html'):
    print('product list 1-' + str(megamenu_total_line) + ' already exists.')
  else:
    f     = open('./data/txt/megamenu-link.txt', 'r')
    count = 1
    for data in f:
      product_list_page = get(data, {}, stream=True)
      parsed            = BeautifulSoup(product_list_page.content, 'html.parser')
      ff = open('./data/html/product-list/product-list-' + str(count) + '.html', 'a')
      ff.write(parsed.prettify())
      ff.close()

      print('Creating product-list-' + str(count) + '.html < ' + data.strip())

      get_product_list_page_next(parsed, 'product-list-' + str(count), 1)

      count += 1
    print('DONE.')



def get_product_list_page_next(html, name_prefix, count):
  # fungsi rekursif untuk dapatkan next page dari setiap product list page
  page_results  = html.select('a[class^=pageResults]')

  for i in page_results:
    if i['title'] == ' Next Page ':
      product_list_page = get(i['href'], {}, stream=True)
      parsed            = BeautifulSoup(product_list_page.content, 'html.parser')


      f = open('./data/html/product-list/' + name_prefix + '#'+ str(count+1) +'.html', 'a')
      f.write(parsed.prettify())
      print('Creating ' + name_prefix + '#'+ str(count+1) +'.html < ' + i['href'].strip())
      f.close()
      
      get_product_list_page_next(parsed, name_prefix, count+1)
  
  return
  


def get_product_link():
  print('Fetching product detail URL ...')
  if os.path.exists('./data/txt/product-link.txt'):
      print('product-link.txt already exists.')
      return

  file_list       = os.listdir('./data/html/product-list/')

  for i in file_list:
    ff = open('./data/html/product-list/' + i)
    # ff.read()
    html = BeautifulSoup(ff, 'html.parser')

    tr              = html.select('tr[class^=productListing-odd]')
    tr_even         = html.select('tr[class^=productListing-even]')
    a               = []

    for i in tr_even:
      tr.append(i)
    
    for i in tr:
      x = i.contents
      # print(len(x))
      if len(x) > 3:
        a.append(x[3].contents[1]['href'])

    f = open('./data/txt/product-link.txt', 'a')
    for data in a:
      print(data)
      f.write(data + '\n')
    f.close()
    
  ff.close()
  print('DONE.')



def get_product_page():
  print('Fetching product detail page ...')

  product_link_total_line = sum(1 for line in open('./data/txt/product-link.txt'))
  url_list                = open('./data/txt/product-link.txt')

  product_dir = os.listdir('./data/html/product-detail/')

  if len(product_dir) >= product_link_total_line:
    print('product detail 1-'+ str(product_link_total_line) + ' already exists.')
    return

  count = 1
  for url in url_list:
    html      = get(url, {}, stream=True)
    parsed    = BeautifulSoup(html.content, 'html.parser')
    ff        = open('./data/html/product-detail/product-detail-' + str(count) + '.html', 'a')
    ff.write(parsed.prettify())
    print('Creating product-detail-' + str(count) + '.html < ' + url.strip())
    ff.close()
    count += 1
  
  url_list.close()
  print('DONE.')



def create_csv_file():
  f           = open('./data/html/product-detail/product-detail-2.html')
  html        = BeautifulSoup(f, 'html.parser')
  post_title  = html.select_one('td[class^=pageHeadingN]').contents[0].strip().split('\t')[0]

  content_table             = html.select('span[class^=smallText_SD]')[3].select('table')
  short_desc_table          = html.select('span[class^=smallText_SD]')[1].contents
  short_desc_list           = []
  header_nav                = html.select('td[class^=headerNavigation]')[0].select('a')
  price_heading             = html.select('td[class^=pageHeadingP]')[0].contents[0].strip()
  image                     = html.select('td[class^=main]')[2].contents[1].contents[1].contents[1].contents[3].contents[1].get('href')
  plain_content             = []
  categories_list           = []
  categories                = []
  categories_split_by_arrow = []
  price                     = 0

  for i, data in enumerate(short_desc_table):
    string = str(data)
    # if string.strip() != '<br/>':
    #   short_desc_list.append(string.replace('\n', '').strip())
    short_desc_list.append(string.replace('\n', '').strip())
  
  excerpt = ''.join(short_desc_list)

  # di sini validasi jika harga tidakkosong
  # maka update variabel harga di atas
  
  if price_heading != '':
    x = price_heading
    y = []
    for s in x:
      if s.isdigit():
        y.append(s)

    z = ''.join(y)
    price = int(z)

  for i in header_nav:
    cat = i.contents[0].strip()
    categories_list.append(cat)

  sku = categories_list[len(categories_list)-1]

  categories_list.remove('Home')
  categories_list.remove('Katalog')
  categories_list.remove(sku)

  for i, cat in enumerate(categories_list):
    arr = categories_list[0:(i+1)]
    categories.append(arr)
  
  for cat in categories:
    categories_split_by_arrow.append('>'.join(cat))

  categories_split_by_comma = ','.join(categories_split_by_arrow)
  published                = 0

  if price != 0:
    published = 1

  field_name_list = ['post_title', 'published', 'sku', 'type', 'categories', 'regular_price', 'post_excerpt', 'post_content', 'images']
  rows            = [post_title, published, sku, 'simple', categories_split_by_comma, price, excerpt, '', image]

  table_counter   = 0
  tr_counter      = 0

  for i, table in enumerate(content_table):
    table_counter += 1
    
    tbody = table.contents[1]
    
    for tr in tbody:

      if tr != '\n':
        tr_counter += 1
        # field_name_list.append('Attribute ' + str(tr_counter) + ' name')
        # field_name_list.append('Attribute ' + str(tr_counter) + ' value(s)')

        attribute_name  = tr.contents[1].contents[1].contents[0].strip().split('\n')[0]
        attribute_value = tr.contents[3].contents[1].contents[0].strip().split('\n')[0]

        if attribute_name == '':
          attribute_name = tr.contents[1].contents[1].contents[1].contents[0].strip().split('\n')[0]
        
        if attribute_value == '':
          attribute_value = tr.contents[3].contents[1].contents[1].contents[0].strip().split('\n')[0]

        rows.append(attribute_name)
        rows.append(attribute_value)

        plain_content.append(str(tr.contents[1].contents[1]).replace('      ', '').replace('     ', '').strip())
        plain_content.append(str(tr.contents[3].contents[1]).replace('      ', '').replace('     ', '').strip())

  rows[7] = ''.join(plain_content).replace('\n', '').replace(';', '').strip()

  i = 1
  while i <= 100:
    field_name_list.append('Attribute ' + str(i) + ' name')
    field_name_list.append('Attribute ' + str(i) + ' value(s)')
    i += 1

  f_to_read   = open('./data/csv/test.csv')
  f_to_write  = open('./data/csv/test.csv', 'a')
  csv_reader  = csv.reader(f_to_read.readlines(), delimiter=';', quotechar='|', quoting=csv.QUOTE_MINIMAL)
  csv_writer  = csv.writer(f_to_write, delimiter=';', quotechar='|', quoting=csv.QUOTE_MINIMAL)
  total_line  = sum(1 for line in csv_reader)

  if total_line == 0:
    csv_writer.writerow(field_name_list)
  csv_writer.writerow(rows)

  # print(csv_reader)

  # line_to_override = {1:field_name_list}

  # for i, row in enumerate(csv_reader):
  #   if i == 0:
  #     if len(field_name_list) > len(row):
  #       data = line_to_override.get(i, row)
  #       # csv_writer.writerow(data)
  #       print('TEST!')
  #       print(data)


  f_to_read.close()
  f_to_write.close()



get_homepage()
get_megamenu_link()
get_product_list_page()
get_product_link()
get_product_page()
create_csv_file()

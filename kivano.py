import csv
import requests
from bs4 import BeautifulSoup
import time
from datetime import datetime
from multiprocessing import Pool

while True:
    def get_html(url):
        response = requests.get(url)
        return response.text

    def get_soup(html):
        soup = BeautifulSoup(html, 'lxml')
        return soup

    def get_1page_links(soup):
        links = []
        container = soup.find('div', class_='list-view')
        items = container.find_all('div', class_='item product_listbox oh')
        for item in items:
            a = item.find('a').get('href')
            link = 'http://kivano.kg' + a
            links.append(link)
        return links

    def get_last_page(soup):
        pages = soup.find('ul', class_='pagination pagination-sm').find('li', class_='last').find('a')
        last_page = pages.text
        return int(last_page)

    def get_all_links():
        i=1
        res = []
        url = f'https://www.kivano.kg/mobilnye-telefony?page=1'
        html = get_html(url)
        soup = get_soup(html)
        last_page = get_last_page(soup)
        while True:
            url = f'https://www.kivano.kg/mobilnye-telefony?page={i}'
            html = get_html(url)
            soup = get_soup(html)
            page_links = get_1page_links(soup)
            res.extend(page_links)
            print(f'спарсили {i}/{last_page} страницу')
            if i == last_page:
                break
            i+=1
        return res

    def get_phone_data(link):
        html = get_html(link)
        soup = get_soup(html)
        name = soup.find('div', id='right_side').find('h1').text
        price = soup.find('div', class_='product_price2').find('span').text.strip()
        if 'сом' not in price:
            price = price + ' сом'
        img = 'http://kivano.kg' + soup.find('a', class_='fancybox').get('href')
        data = {'name':name,'price':price,'img':img}
        return data

    def prepare_csv():
        with open('kivano.csv', 'w') as file:
            writer = csv.writer(file)
            writer.writerow(['Name', 'Price','Image'])

    def write_to_csv(data):
        with open('kivano.csv', 'a') as file:
            writer = csv.writer(file)
            writer.writerow([data['name'],data['price'],data['img']])
            print(f'{data["name"]} - parsed')

    def make_all(link):
        data = get_phone_data(link)
        write_to_csv(data)

    def main():
        prepare_csv()
        links = get_all_links()
        with Pool(10) as pool:
            pool.map(make_all,links)

    if __name__ == '__main__':
        start = datetime.now()
        main()
        finish = datetime.now()
        print(f'Парсинг занял {finish - start}')
    time.sleep(3600)
    # html = get_html('https://www.kivano.kg/mobilnye-telefony?page=1')
    # soup = get_soup(html)
    # print(get_last_page(soup))





























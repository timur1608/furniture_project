import requests
from bs4 import BeautifulSoup
import urllib
import pandas as pd
import lxml


def get_photo(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    quotes = soup.find_all('img', class_='range-revamp-aspect-ratio-image__image')
    if quotes:
        jpg = urllib.request.urlopen(quotes[0]['src']).read()
        return jpg
    else:
        return


if __name__ == '__main__':
    csv_file = pd.read_csv('db/IKEA_SA_Furniture_Web_Scrapings_sss.csv', index_col=0)
    array = csv_file[csv_file['category'] == 'Wardrobes']['link']
    for i, j in zip(range(len(array)), array):
        output_image = f'Wardrobes/output{array.index[i]}.png'
        file = open(output_image, 'wb')
        photo = get_photo(j)
        if photo:
            file.write(photo)
        file.close()

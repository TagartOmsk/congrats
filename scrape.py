import urllib.request
from bs4 import BeautifulSoup
from tqdm import tqdm
import json
from pprint import pprint


def main():
    # headers = {'Accept-Encoding': 'identity'}
    # resp = requests.get('http://pozdravok.ru/pozdravleniya/den-rozhdeniya/proza-250.htm', headers=headers)
    # url = 'http://pozdravok.ru/pozdravleniya/den-rozhdeniya/proza.htm'

    texts_list = []

    # soup = BeautifulSoup(urllib.request.urlopen(url).read(), features='lxml')
    # texts = soup.find_all('p', {'class': 'sfst'})
    # x = texts[0]
    for i in tqdm(range(2, 251)):
        url = f'http://pozdravok.ru/pozdravleniya/den-rozhdeniya/proza-{i}.htm'
        soup = BeautifulSoup(urllib.request.urlopen(url).read(), features='lxml')
        texts = soup.find_all('p', {'class': 'sfst'})
        for x in texts:
            try:
                texts_list.append(x.contents[0].replace('\xa0', " "))
            except Exception as e:
                print(e)
        # pprint(x.contents[0].replace('\xa0', " "))

    print(f'Scraped {len(texts_list)} texts')

    with open('/home/vyacheslav/Projects/congrats/scraped/congratulations.json', "w") as f:
        json.dump({'items': [{"text": x} for x in texts_list]}, f, indent=4)
    # print([x.index('>'), x.rindex('<')])
    # texts_ready = [x[x.index('>'):x.rindex('<')] for x in texts]
    # pprint.pprint(texts_ready)


if __name__ == '__main__':
    main()

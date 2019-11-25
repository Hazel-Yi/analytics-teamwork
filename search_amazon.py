# This webscraper retrieves prices from Amazon Australia or Amazon USA
# Will make a search request for the game and try to retrieve a price if found
# Note that after several requests it won't be able to make any more because amazon can detect web crawlers and ban/limit their requests

import requests
from bs4 import BeautifulSoup
from difflib import SequenceMatcher
from urllib.parse import quote_plus
from collections import defaultdict
import re

def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

### TESTING GAMES ###
#game = 'Betrayal at House on the Hill'.strip()
#game = 'Pandemic Legacy: Season 1'
#game = 'Catan'
#game = 'Coup'
#game = 'Alhambra'
#game = 'Azul'
#game = 'Sagrada'
game = '7 Wonders'
#game = 'Sheriff of Nottingham'
#game = 'Love Letter'
#game = 'Dead of Winter: The Long Night'
#game = 'Lords of Waterdeep'
#game = 'A Game of Thrones: The Board Game (Second Edition)'
#game = 'The Princes of Machu Picchu'
#game = 'Beyond Baker Street'
#game = 'Dragon Slayer'
#game = 'AuZtralia'
#game = 'Star Wars Miniatures'
#game = 'Merchants of Amsterdam'
#game = 'New Bedford'

amazon = 'https://www.amazon.com'

def search_amazon_price(game, loc, ext=False):
    if loc == 'us':
        url = amazon + '/s?k={}&i=toys&ref=nb_sb_noss'
    if loc == 'au':
        url = amazon + '.' + loc + '/s?k={}&i=toys&ref=nb_sb_noss'
    search_param = quote_plus(game)
    search_result = requests.get(url.format(search_param))
    if search_result.ok:
        src = search_result.content
        soup = BeautifulSoup(src, 'html.parser')
        similar_games = defaultdict(list)

        delimiters = "-", ":", "_", ",", ";", "(", ")", ".", " "
        regexPattern = '|'.join(map(re.escape, delimiters))
        results = soup.find_all('span', {'cel_widget_id' : 'SEARCH_RESULTS-SEARCH_RESULTS'})
        match_ratio = 0.0
        best_match = [0.0]
        
        for res in results:
            r = res.find_all('a', {'class' : 'a-link-normal a-text-normal'})
            for t in r:
                link = amazon + t.attrs['href']
                title = t.span.text
                title_split = re.split(regexPattern, title)
                ratio = similar(game, title)
                if ratio == 1.0:
                    best_match = [ratio, title, link]
                    break

                if ratio > 0.4:
                    similar_games[title] = [ratio, title, link]
                    if ratio > match_ratio:
                        match_ratio = ratio

                else:
                    if game in title_split:
                        similar_games[title] = [ratio, title, link]
                
                for g in similar_games:
                    if ((similar_games[g][0] > best_match[0]) and (similar_games[g][0] > 0.5)):
                        best_match = similar_games[g]

        if not len(best_match) > 1:
            if similar_games:
                best_match = next(iter(similar_games.values()))              

        if best_match:
            price = retrieve_amazon_price(best_match[2])
            best_match = [best_match[1], best_match[2]]
            best_match.append(price)

            if len(best_match) > 1:
                return best_match
            else:
                return False
        else:
            return False


def retrieve_amazon_price(url):
    price_page = requests.get(url)
    if price_page.ok:
        print('OK')
        src = price_page.content
        soup = BeautifulSoup(src, 'html.parser')
        span = soup.find('span', {'id' : 'priceblock_ourprice'})
        price = span.text
        return price
        
def get_amazon_price(game, loc, ext=False):
    if loc == 'au':
        print('Trying Amazon Australia')
    else:
        print('Trying Amazon USA')
    price = search_amazon_price(game, loc, ext)
    if price:
        print('Amazon.com.au price for {} is {}'.format(price[0], price[2]))
        if ext == True:
            return price
        else:
            return price[2]
    else:
        return False

    
if __name__ == '__main__':
    price = get_amazon_price(game, 'us', True)
    print(price)



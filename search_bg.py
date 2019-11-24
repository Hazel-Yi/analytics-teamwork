# This webscraper retrieves prices from https://www.boardgamegateway.com/
# If no exact match found, will make a search request for the game and try to retrieve a price if found
# Can bypass all other irrelevant prices for the game (like old prices, or prices for other listed games on the same page and only returns the current discounted price)

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
game = 'Catan'
#game = 'Coup'
#game = 'Alhambra'
#game = 'Azul'
#game = 'Sagrada'
#game = '7 Wonders'
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


def search_bg_price(game):
    url = 'https://www.boardgamegateway.com/?s='
    search_param = quote_plus(game)
    #print('Searching BoardGameGateway.com')
    search_result = requests.get(url.format(search_param))
    if search_result.ok:
        src = search_result.content
        soup = BeautifulSoup(src, 'html.parser')
        similar_urls = []
        similar_titles = []

        results = soup.find_all('h1', {'class' : 'entry-title-archive'})

        for res in results:
            link = res.a.attrs['href']
            title = res.a.text.strip()
            if game == title:
                return [title, link]
            else:
                similar_urls.append(link)
                similar_titles.append(title)
                continue

        if similar_urls:
            match_ratio = 0.0
            similar_game_title = ''
            similar_game_url = ''
            for i in range(len(similar_titles)):
                ratio = similar(game, similar_titles[i])
                #print('Matching: ' + similar_titles[i] + '\t' + str(ratio))
                if ratio > match_ratio:
                    match_ratio = ratio
                    similar_game_title = similar_titles[i]
                    similar_game_url = similar_urls[i]
            if (match_ratio > 0.7):
                #print('Match: ' + similar_game_title)
                return [similar_game_title, similar_game_url]
            else:
                return False
        else:
            return False


def retrieve_bg_price(url):
    price_page = requests.get(url)
    if price_page.ok:
        #print('There is a price page')
        src = price_page.content
        soup = BeautifulSoup(src, 'html.parser')
        prices = []
        dels = []
        flag = False
        div = soup.find('div', {'class' : 'product_infos'})
        span = div.find_all('span', {'class' : 'woocommerce-Price-amount amount'})
        dels_ = div.find_all('del')
        for d in dels_:
            dels.append(d)
        if dels:
            flag = True
        
        for price in span:
            prices.append(price.text)

        #for price in prices:
            #print(price)

        if flag:
            #print('THE PRICE IS ' + min(prices))
            return prices[1]
        else:
            #print('THE PRICE IS ' + prices[0])
            return prices[0]
    else:
        return False


def get_bg_price(game, ext=False):
    print('Trying BoardGameGateway.com')
    url = 'https://www.boardgamegateway.com/product/{}?ref=2'
    game_price_norm = game.replace(' ', '-')
    price = retrieve_bg_price(url.format(game.lower()))

    if price: 
        price = [game, url.format(game.lower()), price]

    else:
        price = retrieve_bg_price(url.format(game_price_norm.lower()))

        if price:
            price = [game, url.format(game_price_norm.lower()), price]

        else:
            similar_url = search_bg_price(game)
            if similar_url:
                price = retrieve_bg_price(similar_url[1])
                print('BoardGameGateway.com price for {} is {}'.format(price[0], price[2]))
                price = similar_url.append(price)
                if ext == True:
                    return price
                else:
                    return price[2]
            else:
                return False

    print('BoardGameGateway.com price for {} is {}'.format(price[0], price[2]))
    if ext == True:
        return price
    else:
        return price[2]
        

    

if __name__ == '__main__':
    price = get_bg_price(game, True)
    print(price)


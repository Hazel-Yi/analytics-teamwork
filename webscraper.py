# This webscraper retrieves prices from https://www.boardgamegateway.com/ (can be expanded to include more sites)
# If no exact match found, will make a search request for the game and try to retrieve a price if found
# Can bypass all other irrelevant prices for the game (like old prices, or prices for other listed games on the same page and only returns the current discounted price)

import requests
from bs4 import BeautifulSoup
from difflib import SequenceMatcher

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
#game = '7 Wonders'
#game = 'Sheriff of Nottingham'
#game = 'Love Letter'
#game = 'Dead of Winter: The Long Night'
#game = 'Lords of Waterdeep'
game = 'A Game of Thrones: The Board Game (Second Edition)'


def search_price(game):
    search_param = game.replace(':', '%3A').replace(' ', '+')
    print('Searching... search parameter: ' + search_param)
    search_result = requests.get('https://www.boardgamegateway.com/?s=' + game)
    if search_result.ok:
        print('Search Match Found')
        src = search_result.content
        soup = BeautifulSoup(src, 'html.parser')
        similar_urls = []
        similar_titles = []

        results = soup.find_all('h1', {'class' : 'entry-title-archive'})

        for res in results:
            link = res.a.attrs['href']
            title = res.a.text.strip()
            if game == title:
                return link
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
                print('Match: ' + similar_game_title)
                return similar_game_url
            else:
                return False
        else:
            return False


def retrieve_price(url):
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


def get_price(game):
    print('Retrieving prices for ' + game)
    url = 'https://www.boardgamegateway.com/product/{}?ref=2'
    game_price_norm = game.replace(' ', '-')
    price = retrieve_price(url.format(game.lower()))
    if not price:
        print('Trying ' + game_price_norm)
        price = retrieve_price(url.format(game_price_norm.lower()))

    if not price:
        similar_url = search_price(game)
        if similar_url:
            price = retrieve_price(similar_url)
            print('Price for {} is {}'.format(game, price))
            return price

        else:
            print('There is no price for {}'.format(game))
            return False

    if price: print('Price for {} is {}'.format(game, price))
    return price
        

    

if __name__ == '__main__':
    price = get_price(game)


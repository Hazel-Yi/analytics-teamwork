from search_amazon import get_amazon_price
from search_bg import get_bg_price

### TESTING GAMES ###
#game = 'Betrayal at House on the Hill'.strip()
#game = 'Pandemic Legacy: Season 1'
#game = 'Catan'
#game = 'Coup'
#game = 'Alhambra'
game = 'Azul'
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


def get_price(game, ext=False):
    price_bg = get_bg_price(game, ext)
    if price_bg:
        return price_bg
    
    price_amazon_au = get_amazon_price(game, 'au', ext)
    if price_amazon_au:
        return price_amazon_au
    
    price_amazon_us = get_amazon_price(game, 'us', ext)
    if price_amazon_us:
        return price_amazon_us

    else:
        return False

def get_all_prices(game, loc='au', ext=False):
    prices = []
    prices.append(get_bg_price(game, ext))
    prices.append(get_amazon_price(game, loc, ext))
    return prices

if __name__ == '__main__':
    price = get_price(game, True)
    print(price)

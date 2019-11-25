# This webscraper retrieves prices from Amazon Australia or Amazon USA
# Will make a search request for the game and try to retrieve a price if found
# Note that after several requests it won't be able to make any more because amazon can detect web crawlers and ban/limit their requests

import requests
from bs4 import BeautifulSoup
from difflib import SequenceMatcher
from urllib.parse import quote_plus
from collections import defaultdict
import re
import time
import random

user_agent_list = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
    'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)',
    'Mozilla/5.0 (compatible; Bingbot/2.0; +http://www.bing.com/bingbot.htm)',
    'Mozilla/5.0 (compatible; Yahoo! Slurp; http://help.yahoo.com/help/us/ysearch/slurp)',
    'DuckDuckBot/1.0; (+http://duckduckgo.com/duckduckbot.html)',
    'Mozilla/5.0 (compatible; Baiduspider/2.0; +http://www.baidu.com/search/spider.html)',
    'Mozilla/5.0 (compatible; YandexBot/3.0; +http://yandex.com/bots)',
    'Sogou Pic Spider/3.0( http://www.sogou.com/docs/help/webmasters.htm#07)',
    'Sogou head spider/3.0( http://www.sogou.com/docs/help/webmasters.htm#07)',
    'Sogou web spider/4.0(+http://www.sogou.com/docs/help/webmasters.htm#07)',
    'Sogou Orion spider/3.0( http://www.sogou.com/docs/help/webmasters.htm#07)',
    'Sogou-Test-Spider/4.0 (compatible; MSIE 5.5; Windows 98)',
    'Mozilla/5.0 (compatible; Konqueror/3.5; Linux) KHTML/3.5.5 (like Gecko) (Exabot-Thumbnails)',
    'Mozilla/5.0 (compatible; Exabot/3.0; +http://www.exabot.com/go/robot)',
    'facebot',
    'facebookexternalhit/1.0 (+http://www.facebook.com/externalhit_uatext.php)',
    'facebookexternalhit/1.1 (+http://www.facebook.com/externalhit_uatext.php)',
    'ia_archiver (+http://www.alexa.com/site/help/webmasters; crawler@alexa.com)',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
    'Mozilla/5.0 (Windows NT 5.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
    'Mozilla/4.0 (compatible; MSIE 9.0; Windows NT 6.1)',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0)',
    'Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (Windows NT 6.2; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.0; Trident/5.0)',
    'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0)',
    'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/6.0)',
    'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; .NET CLR 2.0.50727; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729)'
]


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

amazon = 'https://amazon.com'

def search_amazon_price(game, loc, ext=False):
    if loc == 'us':
        url = amazon + '/s?k={}&i=toys&ref=nb_sb_noss'
    if loc == 'au':
        url = amazon + '.' + loc + '/s?k={}&i=toys&ref=nb_sb_noss'
    search_param = quote_plus(game)
    search_result = None
    headers = None

    # search_result = requests.get(url.format(search_param))
    # if search_result.ok:
    #     print('OK')

    # if not search_result.ok:
    for _ in range(1, 6):
        user_agent = random.choice(user_agent_list)
        headers = {'User-Agent': user_agent}
        search_result = requests.get(url.format(search_param), headers=headers)
        if search_result.ok:
            break
        print('///')

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
            if loc == 'au':
                link = amazon + '.au' + t.attrs['href']
            elif loc == 'us':
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

        if best_match[0] == 1.0:
            break

    if not len(best_match) > 1:
        if similar_games:
            best_match = next(iter(similar_games.values()))

    if len(best_match) > 1:
        price = retrieve_amazon_price(best_match[2])
        best_match = [best_match[1], best_match[2]]
        best_match.append(price)
        return best_match
    else:
        return False

def retrieve_amazon_price(url):
    headers = None
    #price_page = requests.get(url)

    #if not price_page.ok:
    for _ in range(1, 6):
        user_agent = random.choice(user_agent_list)
        headers = {'User-Agent': user_agent}
        price_page = requests.get(url, headers)
        if price_page.ok:
            break
        print('...')

    if price_page.ok:
        src = price_page.content
        soup = BeautifulSoup(src, 'html.parser')
        span = soup.find('span', {'id' : 'priceblock_ourprice'})
        price = span.text
        return price
    else:
        return

         
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
    price = get_amazon_price(game, 'au')
    #print(price)



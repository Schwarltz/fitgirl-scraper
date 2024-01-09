import requests
import re
import json
from bs4 import BeautifulSoup

def main():
    curr_page = 1
    soup = make_soup(f'https://fitgirl-repacks.site/all-my-repacks-a-z/?lcp_page0={curr_page}')

    max_pages = find_max_pages(soup)
    if (max_pages < 0):
        print('Error: could not retrieve max pages')
        return

    games_list = dict()

    for i in range(1,max_pages):
        print(f'Retrieving page {i} of {max_pages}')
        soup = make_soup(f'https://fitgirl-repacks.site/all-my-repacks-a-z/?lcp_page0={i}')
        retrieve_list(soup, games_list)
    
    with open('data.jaon', 'w') as out_file:
        json.dump(games_list, out_file, sort_keys = True, indent = 4,
                ensure_ascii = False)

def make_soup(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    r = requests.get(url, headers=headers)
    return BeautifulSoup(r.content, 'html.parser')

def find_max_pages(soup):
    paginator = soup.find('ul', class_='lcp_paginator')    
    paginator_elements = paginator.find_all('li')
    if len(paginator_elements) >= 2:
        max_pages = paginator_elements[-2].text
        return int(max_pages)
    else:
        return -1

def retrieve_list(soup, games_list):
    ul = soup.find('ul', id='lcp_instance_0')
    li_elements = ul.find_all('li')

    for li in li_elements:
        anchor = li.find('a')
        if anchor:
            text_content = anchor.text
            title = filter_title(text_content)
            href_value = anchor['href']
            games_list[title] = href_value
        else:
            print(f'Text: {li.text}, Href: Not Found')

def filter_title(text):
    filters = [
        r' – ver[\d+|\.]', 
        r' – v[\d+|\.]', 
        r' – vv[\d+|\.]', 
        r', v[\d+|\.]', 
        r' v[\d+|\.]', 
        r' \(v[\d+|\.]',
        r' Version'
        r' – Build', 
        r'[:–] (\w+ )+([Ee]dition|[Cc]ollection|[Bb]undle|[Bb]uild)',
        r'\+( \w+)'
    ]   
    for filter in filters:
        text = re.split(filter, text)[0].strip()
    
    return text

def test_regex(text):
    print(filter_title(text))
    

if __name__ == '__main__':
    main()
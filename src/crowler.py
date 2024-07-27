import requests
from bs4 import BeautifulSoup

def crawl_yahoo_finance(type):
    '''
    yahoo finance로부터 경제뉴스 목록을 크롤링해오는 코드
    '''
    url = f'https://finance.yahoo.com/topic/{type}/'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    articles = soup.find_all('li', class_='js-stream-content')
    #articles = soup.find_all('h3', class_='Mb(5px)')
    article_data = []
    
    for article in articles:
        header = article.find('h3', class_='Mb(5px)')
        if header:
            title = header.text.strip()
            link = article.find('a')['href']
            if not link.startswith('http'):
                link = 'https://finance.yahoo.com' + link
            article_data.append({'title': title, 'link': link})
    
    return article_data

from src.crowler import *
from src.db_manager import *
from src.summerizer import *

def collect_data(db_name = './database/economic_articles.db', table_name = 'articles'):
    create_database()

    types = ['latest-news', 'economic-news', 'crypto']

    for type in types:
        articles = crawl_yahoo_finance(type)
        summarizer = Summarizer()

        for article in articles:
            title = article['title']
            link = article['link']

            # Fetch the full article content
            response = requests.get(link)
            soup = BeautifulSoup(response.content, 'html.parser')
            paragraphs = soup.find_all('p')
            article_text = ' '.join([p.get_text() for p in paragraphs])

            old_articles = fetch_title_data_from_db(db_name, table_name)

            if title not in old_articles:
                # Summarize the article using GPT
                summary = summarizer.summarize_article(article_text)

                # Determine the economic type (this is a placeholder, implement as needed)
                insert_article(title, type, link, summary)

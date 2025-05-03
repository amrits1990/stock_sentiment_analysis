# Google News scraper
from GoogleNews import GoogleNews

def fetch_google_news_sentiment(company, since, num_items):
    googlenews = GoogleNews(start=since)
    googlenews.search(company)
    results = googlenews.result()[:num_items]
    texts = [item['title'] + ' ' + item['desc'] for item in results]
    return texts
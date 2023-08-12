import json
import requests
from bs4 import BeautifulSoup


def lambda_handler(event, context):
    return get_jp_json_feed()


def get_jp_json_feed():
    jp_url = 'https://slate.com/news-and-politics/jurisprudence'
    page = requests.get(jp_url)
    soup = BeautifulSoup(page.content, 'html.parser')

    items = []
    for article in soup.find_all('a', {'class': 'topic-story'}):
        current_url = article.get(key='href')
        current_soup = BeautifulSoup(requests.get(current_url).content, 'html.parser')
        current_body = current_soup.find('div', {'class': 'article__content'})

        for junk in (current_body("aside") + current_body('div', {'class': 'slate-ad__label'})
                     + current_body('div', {'class': 'social-share'})):
            junk.decompose()

        current_article = {
            'id': current_url,
            'title': article.find_next('b', {'class': 'topic-story__hed'}).text.strip(),
            'author': {'name': article.find_next('span', {'class': 'topic-story__author'}).text},
            'url': current_url,
            'content_html': str(current_body),
            'date_published': current_soup.find('time').get(key='content')
        }
        items.append(current_article)

    feed = {
        'version': 'https://jsonfeed.org/version/1.1',
        'title': 'Jurisprudence Feed',
        'home_page_url': jp_url,
        'feed_url': 'https://tp5npvslue2a4p76gp5m3ivf4i0aedgk.lambda-url.us-east-2.on.aws/',
        'items': items
    }
    return json.dumps(feed, indent=2)


if __name__ == '__main__':
    get_jp_json_feed()

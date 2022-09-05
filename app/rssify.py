import configparser
from datetime import datetime
import requests
from feedgen.feed import FeedGenerator
from bs4 import BeautifulSoup
from pytz import timezone
from configobj import ConfigObj
from dateutil import parser

config = ConfigObj('./config.ini')

def get_creator_feed(creator):
    print(f"Getting feed for {creator}")
    print(config)
    if not creator in config:
        return None

    fg = FeedGenerator()
    fg.title(creator)
    fg.description(creator)
    fg.link(href=f'http://indiefan.duckdns.org/feeds/{creator}', rel='alternate')

    for feed in config[creator].values():
        r = requests.get(feed['url'])
        soup = BeautifulSoup(r.text, 'lxml')
        titles = soup.select(feed['item_title'])
        urls = soup.select(feed['item_url'])

        if 'item_date' in feed:
            dates = soup.select(feed['item_date'])
        else:
            dates = None

        for i in range(len(titles)):
            if i > len(urls) - 1:
                break

            fe = fg.add_entry()
            fe.title(titles[i].text)
            fe.link(href=urls[i].get('href'), rel='alternate')
            if dates is not None:
                date = parser.parse(dates[i].text.strip())
                if 'item_timezone' in feed:
                    localtz = timezone(feed['item_timezone'])        
                    date = localtz.localize(date)
            else:
                date = '1970-01-01 00:00:00+02:00'

            fe.published(date)
    return fg.rss_str()

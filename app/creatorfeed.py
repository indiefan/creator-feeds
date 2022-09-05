import configparser
from datetime import datetime
import requests
from feedgen.feed import FeedGenerator
from bs4 import BeautifulSoup
from pytz import timezone
from configobj import ConfigObj
from dateutil import parser
from genshi.template import TextTemplate

class CreatorFeed:
    def __init__(self, name):
        self.name = name
        self.creator_feed_items = []
        self.config = ConfigObj('config.ini')

    def parse_feed(self):
        if not self.name in self.config:
            return

        self.creator_feed_items = []
        for config in self.config[self.name].values():
            feed = Feed(config)
            self.creator_feed_items.extend(feed.get_feed())
        self.creator_feed_items.sort(key=lambda item:item['published']) 
        
    def get_feed(self):
        self.parse_feed()

        fg = FeedGenerator()
        fg.title(self.name)
        fg.description(self.name)
        fg.link(href=f'http://indiefan.duckdns.org/feeds/{self.name}', rel='alternate')

        for item in self.creator_feed_items:
            fe = fg.add_entry()
            fe.title(item['title'])
            fe.link(href=item['link'], rel='alternate')
            fe.published(item['published'])

        return fg.rss_str()

class Feed:
    def __init__(self, config):
        self.config = config
        self.items = []

    def get_feed(self):
        self.parse_feed()
        return self.items

    def parse_feed(self):
        self.items = []

        r = requests.get(self.config['url'])
        soup = BeautifulSoup(r.text, 'lxml')

        items_contents = soup.select(self.config['item']['selector'])

        for item_content in items_contents:
            item = {}

            selected_content = {}
            for name, selector in self.config['item']['selectors'].items():
                selection = item_content.select_one(selector)
                if selection:
                    selected_content[name] = selection.text.strip()
                    attrs_name = f"{name}_attrs"
                    selected_content[attrs_name] = {}
                    for attr, value in selection.attrs.items():
                        selected_content[attrs_name][attr] = value
                else:
                    selected_content[name] = ''

            for attr in ('title', 'link'):
                if attr in self.config['item']:
                    # Template exists for the attribute, so format it from selected content
                    template = TextTemplate(self.config['item'][attr])
                    item[attr] = template.generate(**selected_content).render('xml')
                elif attr in selected_content:
                    # Populate attribute directly from selected content
                    item[attr] = selected_content[attr]

            date = '1970-01-01 00:00:00+02:00'
            if 'date' in selected_content:
                date = parser.parse(selected_content['date'])
                if 'timezone' in self.config['item']:
                    localtz = timezone(self.config['item']['timezone'])
                    date = localtz.localize(date)
            item['published'] = date
            self.items.append(item)

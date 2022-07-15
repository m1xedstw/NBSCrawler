import scrapy
import json
from jsonschema import validate
from bs4 import BeautifulSoup
from articles.items import ArticlesItem
import os


class ArticleSpider(scrapy.Spider):

    name = 'article'
    allowed_domains = ['nbs.sk']
    start_urls = ['https://nbs.sk/en/press/news-overview/']

    headers = {
            "Accept": "application/json, */*;q=0.1",
            "Content-Type": "application/json"
        }
    
    payload = {
            "limit": 20,
            "offset": 0,
            "filter": {
                "lang": "en",
                "tags": [32447, 33218]
            },
            "onlyData": True
    }

    def start_requests(self):
        req_payload = json.dumps(self.payload)
        yield scrapy.Request('https://nbs.sk/wp-json/nbs/v1/post/list?_locale=user',
        method='POST', headers=self.headers, body=req_payload)

    def parse(self, response):
        self.is_valid_json(response.text)
        post_links = [link.replace('\\','').replace('"', '') for link in response.css('a::attr(href)').getall()]
        for link in post_links:
            yield response.follow(link, callback=self.get_post_details)

    def is_valid_json(self, response):
        """ 
        The response from the '/nbs/v1/post/list' API needs to be in the expected format
        in order to extract all article URLs and continue scraping.
        """
        schema_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'schema.json')
        with open(schema_path) as s:
            schema = json.load(s)
        try:
            validate(instance=json.loads(response), schema=schema)
        except Exception as e:
            raise

    def get_post_details(self, response):
        """
        Load all the information from a specific article page and return an ArticlesItem object 
        """
        soup = BeautifulSoup(response.css('div.nbs-post__content').get(), 'lxml')
        post_content = " ".join([tag.text.strip() for tag in soup.find_all(['p', 'li', 'blockquote'])[:-2]])
        post_name = response.css('h1.headline::text').get()
        post_date = response.css('div.nbs-post__date::text').get().replace(" ", "")
        post_labels = response.xpath("//div[contains(@class, 'label--sm')]/text()").getall()
        post_link = response.request.url
        article = ArticlesItem(name=post_name, link=post_link, labels=post_labels, date=post_date, content=post_content)
        yield article
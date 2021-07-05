import scrapy
import time;

class QuotesSpider(scrapy.Spider):
    name = "quotes"
    start_urls = [
        'http://quotes.toscrape.com/page/1/',
        'http://quotes.toscrape.com/page/2/',
    ]

    def parse(self, response):
        page = response.url.split("/")[-2]
        for quote in response.css('div.quote'):
            text = quote.css('span.text::text').get()
            author = quote.css('small.author::text').get()
            tags = quote.css('div.tags a.tag::text').getall()
            rule = 0

            if (author == 'Mark Twain' and 'life' in tags):
                rule = 1
            elif ('truth' in text):
                rule = 2
            else:
                continue

            yield {
                'text': text,
                'author': author,
                'tags': tags,
                'page': page,
                'rule': rule,
                'file': 'storage/txt/' + page + '_' + author.lower().replace(' ', '_') + time.time() + '.txt'
            }

        # page = response.url.split("/")[-2]
        # filename = f'quotes-{page}.html'
        # with open(filename, 'wb') as f:
        #     f.write(response.body)
        # self.log(f'Saved file {filename}')
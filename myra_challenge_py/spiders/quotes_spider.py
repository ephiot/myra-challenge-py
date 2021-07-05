import scrapy
import time;

class QuotesSpider(scrapy.Spider):
    name = "quotes"
    start_urls = ['http://quotes.toscrape.com/login']

    def parse(self, response):
        yield scrapy.FormRequest.from_response(
            response,
            formdata={
                'username': 'scrapy.bot',
                'password': '4w3s0m3n3ss',
            },
            callback=self.parse_quotes,
        )

    def parse_quotes(self, response):
        if not response.css('a[href="/logout"]').extract_first():
            raise CloseSpider('Authentication Failed!')

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
                'file': 'storage/txt/' + page + '_' + author.lower().replace(' ', '_') + '_' + str(time.time()) + '.txt'
            }

        next_page = response.css('li.next a::attr(href)').extract_first()
        if next_page:
            yield scrapy.Request(
                url=response.urljoin(next_page),
                callback=self.parse_quotes,
            )

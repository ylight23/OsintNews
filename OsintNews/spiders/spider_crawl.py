import scrapy
from datetime import datetime
from OsintNews.items import OsintnewsItem


class ViettanSpider(scrapy.Spider):
    name = "spider_crawl"
    allowed_domains = ["viettan.org"]
    start_urls = ["https://viettan.org/quan-diem"]

    # def parse(self, response):
    #     pass

    def parse(self, response):
        # Request tới từng bai báo có trong danh sách dựa vào href
        for item_url in response.css("article.elementor-post > a ::attr(href)").extract():
            yield scrapy.Request(response.urljoin(item_url), callback=self.parse_article)
            #print("URL KIEM TRA", item_url)
         # nếu có bài kế tiếp thì tiếp tục crawl
        next_page = response.css("a.next ::attr(href)").extract_first()
        if next_page:
            yield scrapy.Request(response.urljoin(next_page), callback=self.parse)

    def parse_article(self, response):
        item = OsintnewsItem()

        item['title'] = response.css(
            'div.elementor-widget-container > h1 ::text').extract_first()  # Tên từng bài báo
        
        div_selector = response.css('div.elementor-image')[1]
        item['image_url'] = div_selector.css('img::attr(src)').extract_first()
        item['content'] = response.css(
            'div.elementor-widget-container p::text').extract()
        item['url'] = response.css(
            'div.elementor-post__text > h3 > a ::attr(href)').extract_first()
        
        category_selector = response.css('span.elementor-post-info__terms-list')[0]
        item['category'] = category_selector.css(" a:nth-of-type(3)::text").extract_first()

        # item['author'] = response.xpath(
        #     "//div[@class='elementor-widget-container']//li[@itemprop='author']//span[@class='elementor-icon-list-text elementor-post-info__item elementor-post-info__item--type-author']/text()").get()
        author_raw = response.css(
            '.elementor-post-info__item--type-author ::text').extract_first()
        if author_raw:
            author_cleaned = author_raw.strip()
            item['author'] = author_cleaned
        else:
            item['author'] = None
        item['sentiment'] = "tieu-cuc"
        item['is_fake'] = "True"

        yield item

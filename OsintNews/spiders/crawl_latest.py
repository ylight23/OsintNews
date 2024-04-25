import scrapy


class CrawlLatestSpider(scrapy.Spider):
    name = "crawl_latest"
    allowed_domains = ["viettan.org"]
    start_urls = ["https://viettan.org/sitemap_index.xml"]

    # def parse(self, response):
    #     pass
    def parse(self, response):
        # Phân tích sitemap.xml để tìm các URL của các bài báo mới nhất
        urls = response.xpath('//url/loc/text()').extract()
        for url in urls:
            yield scrapy.Request(url, callback=self.parse_article)

    def parse_article(self, response):
        # Phân tích thông tin từ bài báo và tạo một mục ArticleItem
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
import scrapy
from datetime import datetime
from OsintNews.items import OsintnewsItem


class ViettanSpider(scrapy.Spider):
    name = "crawl_date"
    allowed_domains = ["viettan.org"]
     # Hàm khởi tạo Spider, nhận vào ngày, tháng, năm
     
    def __init__(self, year=None, month=None, day=None, *args, **kwargs):
        super(ViettanSpider, self).__init__(*args, **kwargs)
        if day:
            self.start_urls = [f"https://viettan.org/{year}/{month}/{day}"]
        else:
            self.start_urls = [f"https://viettan.org/{year}/{month}"]
        
        if month:
            self.start_urls = [f"https://viettan.org/{year}/{month}"]
        else:
            self.start_urls = [f"https://viettan.org/{year}"]
        
    def parse(self, response):
        # Request tới từng bài báo có trong danh sách dựa vào href
        for item_url in response.css("article.elementor-post > a ::attr(href)").extract():
            yield scrapy.Request(response.urljoin(item_url), callback=self.parse_article)

        # nếu có bài kế tiếp thì tiếp tục crawl
        next_page = response.css("a.next ::attr(href)").extract_first()
        if next_page:
            yield scrapy.Request(response.urljoin(next_page), callback=self.parse)

    def parse_article(self, response):
        item = OsintnewsItem()

        item['title'] = response.css('div.elementor-widget-container > h1 ::text').extract_first()  # Tiêu đề bài báo

        # Lấy URL ảnh đại diện của bài báo
        div_selector = response.css('div.elementor-image')[1]
        item['image_url'] = div_selector.css('img::attr(src)').extract_first()

        # Lấy nội dung của bài báo
        item['content'] = response.css('div.elementor-widget-container p::text').extract()

        # Lấy URL của bài báo
        item['url'] = response.css('div.elementor-post__text > h3 > a ::attr(href)').extract_first()

        # Lấy danh mục của bài báo
        category_selector = response.css('span.elementor-post-info__terms-list')[0]
        item['category'] = category_selector.css(" a:nth-of-type(3)::text").extract_first()

        # Lấy tên tác giả của bài báo
        author_raw = response.css('.elementor-post-info__item--type-author ::text').extract_first()
        if author_raw:
            author_cleaned = author_raw.strip()
            item['author'] = author_cleaned
        else:
            item['author'] = None

        # Đánh giá tâm trạng của bài báo
        item['sentiment'] = "tieu-cuc"

        # Bài báo có phải là giả mạo không
        item['is_fake'] = "True"

        # Lấy thời gian xuất bản của bài báo
        publish_raw = response.css('.elementor-post-info__item--type-date::text').extract_first()
        if publish_raw:
            publish_clean = publish_raw.strip()
            item['published_at'] = publish_clean
        else:
            item['published_at'] = None

        yield item
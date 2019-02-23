import scrapy
import logging

logging.basicConfig(filename='wordpress_crawling.log', level=logging.DEBUG)


class WordpressSpider(scrapy.Spider):
    name = 'wordpress'

    @staticmethod
    def fix_link(link):
        """Attaches http part at the beginning of the link for Scrapy needs it."""
        return ('' if link.startswith('http') else 'http://www.') + link

    def start_requests(self):

        # getting links split by \n from a txt file
        with open('wordpress/input/links.txt') as file:
            urls = file.read().splitlines()

        # sending requests
        for url in urls:
            url = self.fix_link(url)
            request = scrapy.Request(
                url=url + '/wp-content/uploads/',
                callback=self.parse
            )
            yield request

    def parse(self, response):
        """
        A function we apply to the response for getting the data.
        Checks a title in the <head> element of the page,
        gets all links;
        recursively follows folders, yields items with saved links of .php files.
        """

        if 'Index of /wp-content/uploads' in response.xpath('//head/title/text()').extract()[0]:

            # getting links
            all_links = response.xpath("//body//a/@href").extract()
            all_links = list(filter(lambda x: not x.startswith('?'), all_links))  # getting rid of 'sorting' links
            logging.info(f'Found {len(all_links)} links in {response.url}')

            # discovering links
            for index, link in enumerate(all_links):
                    if link.endswith('.php'):  # yielding  a .php file
                        logging.info(f'{response.urljoin(link)} has been found.')
                        yield {'link': response.urljoin(link)}
                    elif link.endswith('/') and 'wp-content' not in link:  # making a request for a folder
                        absolute_link = response.urljoin(link)
                        yield scrapy.Request(
                            url=absolute_link,
                            callback=self.parse)

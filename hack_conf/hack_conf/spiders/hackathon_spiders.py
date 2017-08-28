"""Spiders for scraping hackathons' information.

* Think about converting time from a string to a time object.
* If description is short enough, it will be added to subtitle, and description
value would be None.
* If prize is null, it need not imply that there are no prizes; one can always
visit the hackathon link for more info.
"""

from bs4 import BeautifulSoup  # Eventually migrate to lxml.
from lxml import html
import scrapy
from hack_conf.items import HackData  # Imports metadata.
import re


class HackathonDotComSpider(scrapy.Spider):
    name = "hackathon_dot_com"
    start_urls = [
        'http://www.hackathon.com/city',
    ]

    def parse(self, response):
        block = response.xpath(
            "body/div[@class='ht-page__content']/div[@class='row']"
        )[1]
        cities_links = block.xpath(
            ".//a[@class='ht-all-card']/@href"
        ).extract()
        for city_link in cities_links:
            yield response.follow(city_link, callback=self.parse_final)
        yield response.follow(
            "https://www.hackathon.com/online",
            callback=self.parse_final
        )

    def parse_final(self, response):
        block = response.xpath("//div[@class='row align-center']")[0]
        city_hacks = block.xpath('.//div[@class="ht-eb-card"]')

        def parse_hackathonDotcom(ele):
            data = HackData()
            # Data from this source contains image as well, but presently
            # images aren't supported here. Maybe later they will be.
            data['source'] = 'http://www.hackathon.com'

            try:
                data['location'] = ele.xpath(
                    ".//span[@class='ht-eb-card__location__place']/text()"
                )[0].strip()
            except Exception:
                pass

            try:
                title_selector = ele.xpath(
                    ".//a[@class='ht-eb-card__title']"
                )[0]
                data['title'] = title_selector.xpath("text()")[0].strip()
            except Exception:
                pass

            try:
                # Scrapes out link (href) about the hackathon.
                data['link'] = title_selector.attrib["href"]
            except Exception:
                pass

            try:
                # Description perhaps not clean! contains \n and stuff.
                # (probably unicode stuff)
                data['description'] = ele.xpath(
                    ".//div[@class='ht-eb-card__description']/text()"
                    )[0].strip()  # Scrapes out hackathon description.
            except Exception:
                pass

            try:  # This block scrapes time of hackathon.
                time = ele.xpath(".//div[@class='ht-eb-card__date ']")[0]
                time = time.text_content()
                index = time.find("Ends")
                if index != -1:
                    time = time[:index] + ", Ends" + time[index+4:]
                data['time'] = ' '.join(re.split(r'(\d+)', time))
            except Exception:
                pass

            try:  # This block scrapes tags (if available).
                data['tags'] = ele.xpath(".//div[@class='ht-card-tags']")[0]
                data['tags'] = data['tags'].xpath("./a/text()")
            except Exception:
                pass

            try:  # This gets the hackathon's prize info.
                data['prize'] = ele.xpath(
                    ".//div[@class='ht-eb-card__prize__name']/text()"
                    )[0].strip()
            except Exception:
                pass

            return data

        for hackathon in city_hacks:
            yield parse_hackathonDotcom(html.fromstring(hackathon.extract()))

        more_button = response.xpath(
            "//a[@data-pagination-more-link='hackathons']"
        )
        while more_button:
            yield response.follow(more_button[0], callback=self.parse_final)


class HackathonDotIoSpider(scrapy.Spider):
    name = "hackathon_dot_io"
    start_urls = ["http://www.hackathon.io"]

    def parse(self, response):
        def parse_hackathon_dot_io(ele):
            data = HackData()
            data['source'] = 'http://www.hackathon.io'
            try:
                data['time'] = ele.find('div', {'class': 'two columns time'})
                data['time'] = data['time'].contents[2].strip()
            except Exception as e:
                print(e)
            try:
                data['link'] = data['source'] + ele.find('h4').contents[0]
                data['link'] = data['link']['href']
            except Exception as e:
                print(e)
            try:
                data['title'] = ele.find('h4').contents[0].contents[0].strip()
            except Exception as e:
                print(e)
            try:
                data['subtitle'] = ele.find('h5').contents[0].contents[0]
                data['subtitle'] = data['subtitle'].strip()
            except Exception as e:
                print(e)
            try:
                data['location'] = ele.find('div',
                    {'class':'two columns location'}
                    ).contents[1].contents[1].strip()
            except Exception as e:
                print(e)

            return data

        soup = BeautifulSoup(response.text, 'html.parser')
        container = soup.find('div', {'class': 'event-results'})
        every = container.find_all('div', {'class': 'event-teaser'})
        for ele in every:
            yield parse_hackathon_dot_io(ele)
        
        more_button = response.xpath(
            "//*[starts-with(@id, 'page_')]/a"
        )
        if more_button:
            yield response.follow(more_button[0], callback=self.parse)

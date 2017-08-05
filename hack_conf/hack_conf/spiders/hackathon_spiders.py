"""Spiders for scraping hackathons' information."""

from bs4 import BeautifulSoup  # Eventually migrate to lxml.
from lxml import html
import scrapy
from .hack_constants import *  # Imports metadata.
import re

#think about converting time from a string to a time object
#if description is short enough, it will be added to subtitle, and description value would be None
#if prize is null, it need not imply that there are no prizes; one can always visit the hackathon link for more info


class HackathonDotComSpider(scrapy.Spider):
    name = "hackathon_dot_com"
    start_urls = [
        'http://www.hackathon.com/city',
    ]

    def parse(self, response):
        block = response.xpath("body/div[@class='ht-page__content']/div[@class='row']")[1]
        cities_links = block.xpath(".//a[@class='ht-all-card']/@href").extract()
        for city_link in cities_links:
            yield response.follow(city_link, callback=self.parse_final)
        yield response.follow("https://www.hackathon.com/online", callback=self.parse_final)


    def parse_final(self, response):
        block = response.xpath("//div[@class='row align-center']")[0]
        city_hacks = block.xpath('.//div[@class="ht-eb-card"]')

        def parse_hackathonDotcom(ele):
            data = dict.fromkeys(metadata)
            #data from this source contains image as well, but presently images aren't supported here. Maybe later they will be.
            data['source'] = 'http://www.hackathon.com'

            try:
                data['location'] = ele.xpath(".//span[@class='ht-eb-card__location__place']/text()")[0].strip()
            except Exception:
                pass

            try:
                title_selector = ele.xpath(".//a[@class='ht-eb-card__title']")[0]
                data['title'] = title_selector.xpath("text()")[0].strip()
            except Exception:
                pass

            try:
                data['link'] = title_selector.attrib["href"] #scrapes out link about hackathon, link which is href of title
            except Exception:
                pass

            try:
                data['description'] = ele.xpath(".//div[@class='ht-eb-card__description']/text()")[0].strip() #scrapes out hackathon description
                #description perhaps not clean! contains \n and stuff (probably unicode stuff)
            except Exception:
                pass

            try: #this block scrapes time of hackathon
                time = ele.xpath(".//div[@class='ht-eb-card__date ']")[0].text_content()
                index = time.find("Ends")
                if index != -1:
                    time = time[:index] + ", Ends" + time[index+4:]
                data['time'] = ' '.join(re.split(r'(\d+)', time))
            except Exception:
                pass

            try: #this block scrapes tags (if available)
                data['tags'] = ele.xpath(".//div[@class='ht-card-tags']")[0].xpath("./a/text()")
            except Exception:
                pass

            try:  # This gets the hackathon's prize info.
                data['prize'] = ele.xpath(".//div[@class='ht-eb-card__prize__name']/text()")[0].strip()
            except Exception:
                pass

            return data

        for hackathon in city_hacks:
            yield parse_hackathonDotcom(html.fromstring(hackathon.extract()))

        more_button = response.xpath("//a[@data-pagination-more-link='hackathons']")
        while more_button:
            yield response.follow(more_button[0], callback=self.parse_final)

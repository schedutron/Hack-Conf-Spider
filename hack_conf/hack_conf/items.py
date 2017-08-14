# -*- coding: utf-8 -*-
from scrapy import Field, Item


class HackData(Item):
    title = Field()
    subtitle = Field()
    description = Field()
    time = Field()
    location = Field()
    tags = Field()
    source = Field()
    link = Field()
    prize = Field()
    cost = Field()


class ConfData(Item):
    title = Field()
    description = Field()
    time = Field()
    location = Field()
    tags = Field()
    source = Field()
    link = Field()

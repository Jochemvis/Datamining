# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class DataminingItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

# class AlbumItem(scrapy.Item):
#     Album = scrapy.Field()
#     Metascore = scrapy.Field()
#     User_score = scrapy.Field()
#     Releasedate = scrapy.Field()
#     Artist = scrapy.Field()
#     Genre = scrapy.Field()
#     Recordlabel = scrapy.Field()

# class ReviewItem(scrapy.Item):
#     Album = scrapy.Field()
#     CriticName = scrapy.Field()
#     CriticScore = scrapy.Field()
#     CriticReviewDate = scrapy.Field()
#     CriticReviewText = scrapy.Field()
import scrapy
import json
import subprocess
import csv
import pandas as pd

class CriticReviewsSpider(scrapy.Spider):
    name = 'datamining'
    allowed_domains = ['metacritic.com']
    start_urls = [
        'https://www.metacritic.com/browse/albums/genre/date/alt-country',
        # 'https://www.metacritic.com/browse/albums/genre/date/dance',
        # 'https://www.metacritic.com/browse/albums/genre/date/alternative',
        # 'https://www.metacritic.com/browse/albums/genre/date/blues',
        # 'https://www.metacritic.com/browse/albums/genre/date/comedy',
        # 'https://www.metacritic.com/browse/albums/genre/date/country',
        # 'https://www.metacritic.com/browse/albums/genre/date/electronic',
        # 'https://www.metacritic.com/browse/albums/genre/date/experimental',
        # 'https://www.metacritic.com/browse/albums/genre/date/folk',
        # 'https://www.metacritic.com/browse/albums/genre/date/house',
        # 'https://www.metacritic.com/browse/albums/genre/date/indie',
        # 'https://www.metacritic.com/browse/albums/genre/date/jazz',
        # 'https://www.metacritic.com/browse/albums/genre/date/latin',
        # 'https://www.metacritic.com/browse/albums/genre/date/metal',
        # 'https://www.metacritic.com/browse/albums/genre/date/pop',
        # 'https://www.metacritic.com/browse/albums/genre/date/psychedelic',
        # 'https://www.metacritic.com/browse/albums/genre/date/punk',
        # 'https://www.metacritic.com/browse/albums/genre/date/rap',
        # 'https://www.metacritic.com/browse/albums/genre/date/rb',
        # 'https://www.metacritic.com/browse/albums/genre/date/reggae',
        # 'https://www.metacritic.com/browse/albums/genre/date/rock',
        # 'https://www.metacritic.com/browse/albums/genre/date/singer-songwriter',
        # 'https://www.metacritic.com/browse/albums/genre/date/soul',
        # 'https://www.metacritic.com/browse/albums/genre/date/soundtrack',
        # 'https://www.metacritic.com/browse/albums/genre/date/techno',
        # 'https://www.metacritic.com/browse/albums/genre/date/vocal',
        # 'https://www.metacritic.com/browse/albums/genre/date/world'
    ]

    def __init__(self, *args, **kwargs):
        super(CriticReviewsSpider, self).__init__(*args, **kwargs)
        self.page_count = 0
        self.max_pages = 1  # Set the maximum number of pages here

    def parse(self, response):
        # Extracting URLs of individual albums from the current page (Jochem)
        urls = response.css('a.title::attr(href)').extract()
        for link in urls:
            # Sending requests for each album to extract details and critic reviews
            yield scrapy.Request(url='https://www.metacritic.com' + link, callback=self.parse_details_credits_link)

        # Checking if there are more pages to crawl (Daan)
        if self.page_count < self.max_pages:
            next_page = response.xpath("//a[@class='action' and @rel='next']/@href").get()
            if next_page:
                # Sending a request for the next page
                yield scrapy.Request(url='https://www.metacritic.com' + next_page, callback=self.parse)

    def parse_details_credits_link(self, response):
        # Extracting the link to the details page for the current album (Bart)
        detailslink = response.css('a.action[href$="/details"]::attr(href)').get()
        if detailslink:
            # Sending a request for the details page to extract album details and critic reviews
            yield scrapy.Request(url='https://www.metacritic.com' + detailslink, callback=self.parse_details)

    def parse_details(self, response):
        # Extracting details of the current album (Jayshree)
        Album = response.css('div.product_title a h1::text').get()
        Metascore = response.css('div.metascore_w span[itemprop="ratingValue"]::text').get()
        Genre = response.css('div.genres span.data::text').getall()
        Genre = [genre.strip() for genre in Genre]
        ReleaseDate = response.css('li.summary_detail.release span.data::text').get()
        Artist = response.css('div.product_artist a span.band_name::text').get()
        user_score_elem = response.css('div.userscore_wrap span[itemprop="ratingValue"]::text').get()
        User_score = [user_score_elem.strip() if user_score_elem else 'tbd']
        Record_label = response.css('div > span.label:contains("Record Label") + span.data::text').get()

        # Creating a dictionary with album details (Jochem)
        data = {
            'Album': Album,
            'Metascore': Metascore,
            'User score': User_score,
            'Releasedate': ReleaseDate,
            'Artist': Artist,
            'Genre': Genre,
            'Recordlabel': Record_label
        }

        # Extracting the link to critic reviews for the current album (Daan)
        criticslink = 'https://www.metacritic.com' + response.css(
            'li.nav.nav_critic_reviews > span > span > a::attr(href)').get()
        if criticslink:
            # Sending a request for critic reviews to extract critic details
            yield scrapy.Request(url=criticslink, callback=self.parse_critics_details, meta={'data': data})

    def parse_critics_details(self, response):
        # Extracting critic details from the reviews section (Bart)
        data = response.meta['data']
        critic_names = []
        critic_scores = []
        critic_review_dates = []
        critic_review_texts = []

        # Extracting individual critic reviews from the page (jochem)
        reviews = response.xpath('//ol[@class="reviews critic_reviews"]/li[contains(@class, "review critic_review")]')

        for critics in reviews:
            # Extracting critic name (Daan)
            critic_name = critics.css('div.review_stats div.review_critic div.source a::text').get()
            
            # Check if critic_name is not None and is a string (Bart)
            if critic_name is not None and isinstance(critic_name, str):
                critic_names.append(critic_name)
            else:
                critic_names.append('Unknown Critic')  # Replace with a default value if not a string

            # Extracting critic score (Jayshree)
            critic_scores.append(critics.css('div.review_stats div.review_grade div::text').get())
            
            # Extracting critic review date (Daan)
            critic_date_elem = critics.css('div.review_stats div.review_critic div.date::text').get()
            if critic_date_elem is not None and isinstance(critic_date_elem, str):
                critic_review_dates.append(critic_date_elem)
            else:
                critic_review_dates.append('Unknown Date')
            
            # Extracting critic review text (Jochem)
            critic_review_texts.append(
                str(critics.css('div div:nth-child(1) div.review_body::text').get()).strip().replace('\n', ''))

        # Updating the data dictionary with critic details (Jayshree)
        data.update({
            'CriticNames': '@'.join(critic_names),
            'CriticScores': '@'.join(critic_scores),
            'CriticReviewDates': '@'.join(critic_review_dates),
            'CriticReviewTexts': '@'.join(critic_review_texts),
        })
        yield data

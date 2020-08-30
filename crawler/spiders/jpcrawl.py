""" Scrapy spiders """
import scrapy


class JpSpider(scrapy.Spider):
    """ Japanese release spider """
    name = "jp"
    start_urls = [
        'https://www.discogs.com/Yellow-Magic-Orchestra-Solid-State-Survivor/master/45171',
        'https://www.discogs.com/Chiemi-Manabe-%E4%B8%8D%E6%80%9D%E8%AD%B0%E5%B0%91%E5%A5%B3/master/543107',
        'https://www.discogs.com/Tatsuro-Yamashita-Spacy/release/1006498',
        'https://www.discogs.com/Portable-Rock-Beginnings/master/625070'
    ]

    def parse(self, response):
        """ parse the album to find credits """
        if "/release/" in response.url:
            list_of_artists = response.css(".list_no_style > li > a::text").getall()
            artist_links = response.css(".list_no_style > li > a::attr(href)").getall()
        else:
            list_of_artists = response.css(".credit_name::text").getall()
            artist_links = response.css(".credit-link::attr(href)").getall()

        album_artist = response.css("#profile_title > span:nth-child(1) > span:nth-child(1) > a:nth-child(1)::text").get()

        album_title = response.css("#profile_title > span:nth-child(2)::text").get()
        album_title = album_title.replace('\n', '').strip()

        album_string = "%s,%s,%s\n" % (album_artist, album_title, list_of_artists)

        filename = "credits.csv"
        with open(filename, 'a') as credits_file:
            credits_file.write(album_string)
        self.log('Wrote %s to file' % album_title)

        artist_links = [x for x in artist_links if not "label" in x]
        yield from response.follow_all(artist_links, callback=self.parse_artist)

    def parse_artist(self, response):
        """ parse the artist entries to discover more albums """
        album_links = response.css(".title > a::attr(href)").getall()
        yield from response.follow_all(album_links, callback=self.parse)

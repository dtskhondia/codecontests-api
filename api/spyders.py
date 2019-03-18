import scrapy
import time
import numpy as np
import logging
from . import services
from django.utils import timezone
from datetime import datetime,timedelta
import pytz

class AtCoderSpider(scrapy.Spider):
    #Spider Mandatory Fields
    name="AtCoder"
    start_urls = ['https://atcoder.jp/contests/']
    
    #Custom Fields
    path = 'https://atcoder.jp'

    def parse(self, response):
        contests = response.xpath('//h3[contains(text(),"Upcoming Contests")]/following-sibling::div[1]//tbody/tr')
        for contest in contests:
            name = contest.xpath('td[2]//text()').extract_first() 
            startTime = datetime.strptime(contest.xpath('td[1]//text()').extract_first(), '%Y-%m-%d %H:%M:%S%z').astimezone(pytz.utc)
            durationExtract = contest.xpath('td[3]//text()').extract_first().split(':') 
            durationExtract = list(map(int,durationExtract if len(durationExtract)>2 else ["00"]+durationExtract))
            duration = timedelta(days=durationExtract[0],hours=durationExtract[1],minutes=durationExtract[2])            
            services.save_contest({
                'name': name,
                'startTime': startTime,
                'endTime': startTime + duration,
                'site':AtCoderSpider.name,
                'url':AtCoderSpider.path + contest.xpath('td[2]//@href').extract_first()
            })

class CodeChefSpider(scrapy.Spider):
    #Spider Mandatory Fields
    name="CodeChef"
    start_urls = ['https://www.codechef.com/contests']
    
    #Custom Fields
    path = 'https://www.codechef.com/'
    
    def parse(self, response):
        contests = response.xpath('//h3[contains(text(),"Future Contests")]/following-sibling::div[1]//tbody/tr')
        for contest in contests:
            services.save_contest({
                'name': contest.xpath('td[2]//text()').extract_first(),
                'startTime': datetime.strptime(contest.xpath('td[3]//@data-starttime').extract_first(), '%Y-%m-%dT%H:%M:%S%z').astimezone(pytz.utc),
                'endTime': datetime.strptime(contest.xpath('td[4]//@data-endtime').extract_first(), '%Y-%m-%dT%H:%M:%S%z').astimezone(pytz.utc),
                'site' : CodeChefSpider.name,
                'url': CodeChefSpider.path + contest.xpath('td[1]//text()').extract_first()
            })


class HackerRankSpider(scrapy.Spider):
    #Spider Mandatory Fields
    name = "HackerRank"
    start_urls = ['https://www.hackerrank.com/contests']
    
    #Custom Fields
    path = "https://www.hackerrank.com/contests"

    def parse(self, response):
        contests = response.xpath('//div[@data-contest-state="Active"]')
        for contest in contests:
            name = contest.xpath('div[1]//text()').extract_first()
            startTimeUTC = contest.xpath('div[2]//meta[@itemprop="startDate"]//@content').extract_first()
            startTime = datetime.strptime(startTimeUTC[:19], '%Y-%m-%dT%H:%M:%S') if startTimeUTC is not None else None
            endTimeUTC = contest.xpath('div[2]//meta[@itemprop="endDate"]//@content').extract_first()
            endTime = datetime.strptime(endTimeUTC[:19], '%Y-%m-%dT%H:%M:%S') if endTimeUTC is not None else None

            services.save_contest({
                'name': name,
                'startTime': startTime,
                'endTime': endTime,
                'site' : HackerRankSpider.name,
                'url': HackerRankSpider.path
            })
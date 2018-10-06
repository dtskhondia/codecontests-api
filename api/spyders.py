import scrapy
import time
import numpy as np
import logging
from . import services
from django.utils import timezone
from datetime import datetime,timedelta

class AtCoderSpider(scrapy.Spider):
    name="atCoder"
    start_urls = ['http://atcoder.jp/contest']
    def parse(self, response):
        contests = response.xpath('//h3[contains(text(),"Upcoming Contests")]/following-sibling::div[1]//tbody/tr')
        for contest in contests:
            name = contest.xpath('td[2]//text()').extract_first() 
            startTime = datetime.strptime(contest.xpath('td[1]//text()').extract_first(), '%Y/%m/%d %H:%M')
            delta = timedelta(hours=9)
            startTime -= delta
            durationExtract = contest.xpath('td[3]//text()').extract_first().split(':') 
            durationExtract = list(map(int,durationExtract if len(durationExtract)>2 else ["00"]+durationExtract))
            duration = timedelta(days=durationExtract[0],hours=durationExtract[1],minutes=durationExtract[2])            
            services.save_contest({
                'name': name,
                'startTime': startTime,
                'endTime': startTime + duration,
                'site':'AtCoder'
            })

class CodeChefSpider(scrapy.Spider):
    name="codeChef"
    start_urls = ['https://www.codechef.com/contests']
    def parse(self, response):
        contests = response.xpath('//h3[contains(text(),"Future Contests")]/following-sibling::div[1]//tbody/tr')
        for contest in contests:
            name = contest.xpath('td[2]//text()').extract_first()
            startTimeIST = datetime.strptime(contest.xpath('td[3]//@data-starttime').extract_first()[:19], '%Y-%m-%dT%H:%M:%S')
            gmt = contest.xpath('td[3]//@data-starttime').extract_first()[19:]
            delta = timedelta(hours=int(gmt[1:3]),minutes=int(gmt[4:6]))
            startTime = (startTimeIST - delta if gmt[0]=='+' else startTimeIST + delta)
            endTimeIST = datetime.strptime(contest.xpath('td[4]//@data-endtime').extract_first()[:19], '%Y-%m-%dT%H:%M:%S')
            endTime = (endTimeIST - delta if gmt[0]=='+' else endTimeIST + delta)
            services.save_contest({
                'name': name,
                'startTime': startTime,
                'endTime': endTime,
                'site' : 'CodeChef'
            })


class HackerRankSpider(scrapy.Spider):
    name="hackerRank"
    start_urls = ['https://www.hackerrank.com/contests']
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
                'site' : 'HackerRank'
            })
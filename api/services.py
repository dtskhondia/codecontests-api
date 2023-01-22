from rest_framework.response import Response
from .models import Contest
from .serializers import ContestSerializer
from .spyders import AtCoderSpider, CodeChefSpider, HackerRankSpider, HackerEarthSpider
from rest_framework import status
from twisted.internet import reactor
import scrapy
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
from datetime import datetime, timedelta, tzinfo
from django.utils import timezone
import requests


def get_codeforce():
    site_name = 'Codeforces'
    url = 'http://codeforces.com/api/contest.list?gym=false'
    contests = requests.get(url)
    for contest in contests.json()['result']:
        if contest['phase'] == 'BEFORE':
            startTime = timezone.datetime.utcfromtimestamp(
                contest['startTimeSeconds'])
            endTime = timezone.datetime.utcfromtimestamp(
                contest['startTimeSeconds'] + contest['durationSeconds'])
            save_contest({'name': contest['name'],
                          'startTime': startTime,
                          'endTime': endTime,
                          'site': site_name,
                          'url': 'https://codeforces.com/contests/'+str(contest['id'])})


def get_crawl():
    runner = CrawlerRunner({
        'USER_AGENT': 'Chrome/41.0.2228.0'
    })
    runner.crawl(CodeChefSpider)
    runner.crawl(AtCoderSpider)
    runner.crawl(HackerRankSpider)
    runner.crawl(HackerEarthSpider)
    d = runner.join()
    d.addBoth(lambda _: reactor.stop())
    reactor.run(installSignalHandlers=0)


def save_contest(item):
    name = item['name']
    startTime = item['startTime']
    endTime = item['endTime']
    site = item['site']
    url = item['url']
    if name and startTime and endTime and site:
        contestObj = Contest(name=name,
                             startTime=startTime if timezone.is_aware(
                                 startTime) else timezone.make_aware(startTime),
                             endTime=endTime if timezone.is_aware(
                                 endTime) else timezone.make_aware(endTime),
                             site=site,
                             url=url)
        contestObj.save()


def load_contests():
    Contest.objects.all().delete()
    get_codeforce()
    get_crawl()

# -*- coding: utf-8 -*-
import scrapy
import dateparser as dp
import traceback


class LoginSpider(scrapy.Spider):
  name = 'ipo'
  website_url = 'https://www.asx.com.au/asx/research/recentFloats.do'
  tzinfo = 'Australia/Sydney'
  uptick_name = 'asx'

  def start_requests(self):
    yield scrapy.Request(self.website_url, callback=self.parse)

  def parse(self, response):
    # from scrapy.shell import inspect_response
    # inspect_response(response, self)
    row_list = response.xpath('//table//tr[td/@class="name"]')
    for r in row_list:
      try:
        name = r.xpath('./td[1]/text()').extract_first().strip()
        ric = r.xpath('string(./td[2])').extract_first().strip()
        date_str = r.xpath('string(./td[3])').extract_first().strip()
        date = dp.parse(
            date_str,
            date_formats=['%d/%m/%Y'],
            settings={
                'TIMEZONE': self.tzinfo,
                'RETURN_AS_TIMEZONE_AWARE': True
            })
        yield {
            "name": name,
            "ric": ric,
            "date": date,
            "tzinfo": self.tzinfo,
            "uptick_name": self.uptick_name,
            "error": False
        }
      except Exception as e:  # not news row, skip
        yield {
            'error': True,
            'row_html': r.extract(),
            'error_message': '%s: %s' % (e.__class__, str(e)),
            'traceback': traceback.format_exc(),
        }

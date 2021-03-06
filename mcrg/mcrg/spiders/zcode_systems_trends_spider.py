import scrapy
import requests
import json
from scrapy.selector import Selector
from mcrg.items import ZcodeSystemsTrendsItem
import logging
from scrapy.utils.log import configure_logging
from datetime import datetime, timedelta
from collections import namedtuple
import requests
from scrapy.selector import HtmlXPathSelector
import re
# sports = ["AM_FOOTBALL","MLB","AUSSIE","BASKETBALL","ESPORTS","HOCKEY","NBA","NHL","RUGBY","SOCCER","TENNIS","VOLLEYBALL","NCAAB","KHL","NCAAF","NFL","WNBA"]
# trends = ["92","2084","286","1957","283","285","2040","2027","179","1670","136","1244","19","2113","1245","67","323","1738","303","2115","2074","1961","1429","390","1868","1948","1515","1753","2437","1812","216","2435","1932","1787","2431","531","1956","183","1210","1946","2075","60","2438","1500","1869","49","1897","50","489","1424","404","1401","1514","1512","1601","1959","1323","2114","2447","1322","302","1943","1166","2076","1928","1826","98","1960","1264","294","1454","2436","1672","1758","1540","1453","299","1664","1321","1541","1167","1671","371","1752","1543","1544","1931","2374","1542","345","1406","55","1327","1248","359","1326","1177","1320","1328","304","1324","1545","2108","1200","77","1914","613","1292","376","614","2044","2244","1862","846","1830","1112","812","1225","1206","1913","1318","2450","1703","1325","369","1441","1460","53","1754","1","20","258","1829","1513","1461","1911","292","836","1421","1747","301","1246","33","358","3","181","1265","1501","1815","56","93","21","472","1312","180","73","351","2","58","51","321","32","22","86","52","57","54","68","357","2026","94","31","97","355"]

configure_logging(install_root_handler=False)
logging.basicConfig(
        filename='log.txt',
        format='%(levelname)s: %(message)s',
        level=logging.INFO)

class zcodeSystemsTrendsSpider(scrapy.Spider):
    id = 9
    name = 'zcode_systems_trends_spider'
    download_delay = 2
    start_urls = ['http://zcodesystem.com/vipclub/login.php']
	
    def parse(self, response):
        return scrapy.FormRequest.from_response(
            response,
            formdata={'emailaddress': 'grao@castlerockresearch.com', 'password': 'Salmana29$'},
            callback=self.after_login
        )   
    def after_login(self, response):
        # check login succeed before going on
        if b"Password is incorrect" in response.body:
            self.logger.error("Login failed")
            return

        # continue scraping with authenticated session...
        if b"Welcome to the VIP Club" in response.body:
            request = scrapy.Request("http://zcodesystem.com/sports_trader/start.php", callback=self.parse_sportstrader)
            yield request

    # fetch all the html for passed trends       
    def parse_sportstrader(self, response):
        self.logger.info("Just arrived at %s", response.url)
        urls = "http://zcodesystem.com/sports_trader/get_active_signals.php"
        payload = {'sports': '["SOCCER"]','trends': '["133"]','typecalc': 'unitsize','unitsize': '100','asort_mode': '0','psort_mode': '0','asignals': '[]'}
        headers = {
        'origin': "http://zcodesystem.com",
        'user-agent': "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36",
        'content-type': "application/x-www-form-urlencoded",
        'accept': "text/html, */*; q=0.01",
        'x-devtools-emulate-network-conditions-client-id': "e5b8391b-5289-4df6-9973-4e2c6d2dc1f1",
        'x-requested-with': "XMLHttpRequest",
        'x-devtools-request-id': "5516.3762",
        'referer': "http://zcodesystem.com/sports_trader/start.php",
        'accept-encoding': "gzip, deflate",
        'accept-language': "en-US,en;q=0.8",	
        'cookie': "ZC_LANG=en; referrer=27.255.222.81%3Azcodesystem.com%252Fsports_trader%252Fstart.php%3Azcodesystem.com%252Fvipclub%252Fdo_login_ns; floaddt=1501734547; mp_6b62034815c12d29db73e6f6fcbd92c2_mixpanel=%7B%22distinct_id%22%3A%20%2215da65ac858129-01077374a2c639-474a0721-100200-15da65ac859ee%22%2C%22%24initial_referrer%22%3A%20%22%24direct%22%2C%22%24initial_referring_domain%22%3A%20%22%24direct%22%7D; phpbb3_1wd74_u=1; phpbb3_1wd74_k=; phpbb3_1wd74_sid=197df12ae45695aeb5c5c06b5b916711; _ga=GA1.2.2077156676.1501656646; _gid=GA1.2.558992684.1501832117; sessid2=sessid20170731061749636; PHPSESSID=b0208e1960e20894bfe171532904fcea; show_club_menu=0; show_picks_menu=1; ST_APP_MODE=Hbd6eooh",
        'cache-control': "no-cache"
        }
        response = requests.request("POST", urls, data=payload, headers=headers)
        jsonresponse = response.json()
        #print(jsonresponse)
        jsonstr = jsonresponse["past_html"]		
        uls = Selector(text = jsonstr).xpath('//ul[@id="TrendList"]').extract()
        print(uls)
        #item = {}
        #for tr in trs:
            #td = Selector(text=tr).xpath('//td').extract()
            #bet_status = ''.join(Selector(text=td[0]).xpath('//td/div[@class="iplaced"]/span[contains(@class, "bet_result-1") or contains(@class, "bet_result1")]/text()').extract())
            #system_name=''.join(Selector(text=td[0]).xpath('//td//div[contains(@class, "left_shift") and contains(@class, "system_name")]/text()').extract())
            #trend_name=''.join(Selector(text=td[0]).xpath('//td//div[@class="left_shift"][1]/text()').extract())
            #bet_team_name=''.join(Selector(text=td[0]).xpath('//td//div[@class="left_shift"]/div[@class="teamName"]//div[@class="Text"]/text()').extract())
            #rotational_number=''.join(Selector(text=td[0]).xpath('//td//div[@class="left_shift"]/div[@class="teamName"]//div[@class="Text"]/div[@class="rot_num"]/text()').extract())
            #item['bet_status'] = bet_status
           
            #print("==========================")
            #print(item)
            #print("==========================")
            #yield item
            #yield item		
	# iterate each row and  save data to database
    
from datetime import date, datetime
import pytz


import http.client
from bs4 import BeautifulSoup


from .models import lunch_log

def what_now_time():
    fmt = "%Y-%m-%d %H:%M:%S"
    fmt2 = "%Y.%m.%d"
    KST = datetime.now(pytz.timezone('Asia/Seoul'))
    return KST.strftime(fmt), KST.strftime(fmt2), KST.weekday() + 1


def main():
    fmt_time, nice_time, nice_time_weekday = what_now_time()

    conn = http.client.HTTPSConnection("stu.sen.go.kr")
    conn.request("GET","/sts_sci_md01_001.do?schulCode=B100001369&schulCrseScCode=3&schulKndScCode=03&schYmd="+"2020.10.17")
    data = conn.getresponse().read()
    conn.close()

    data = data.decode()
    soup = BeautifulSoup(data,'html.parser')
    site = soup.find_all("tr")
    site = site[2].find_all('td')
    
    if len(site)==0:
        today_lunch = '오늘은 급식이 없어요'

    else:
        today_lunch = str(site[nice_time_weekday])
        today_lunch = today_lunch.replace('<td class="textC last">', '')
        today_lunch = today_lunch.replace('<td class="textC">', '')

    
    lunch_log(log_time=fmt_time,today_lunch=today_lunch).save()


from django.shortcuts import render
from .models import *
#여기까지 장고


from datetime import datetime
import pytz
import requests
from bs4 import BeautifulSoup
from .models import lunch_log


def what_now_time():
    fmt = "%Y-%m-%d %H:%M:%S"
    fmt2 = "%Y.%m.%d"
    KST = datetime.now(pytz.timezone('Asia/Seoul'))
    return KST.strftime(fmt), KST.strftime(fmt2), KST.weekday() + 1


def main():
    fmt_time, nice_time, nice_time_weekday = what_now_time()
    html = requests.get("http://sts_sci_md01_001.do?schulCode=B100000659&schulCrseScCode=3&schulKndScCode=03&schYmd="+nice_time)
    soup = BeautifulSoup(html.text,'html.parser')
    site = soup.find_all("tr")
    site = site[2].find_all('td')
    
    if len(site)==0:
        today_lunch = '오늘은 급식이 없어요'

    else:
        today_lunch = str(site[nice_time_weekday])
        today_lunch = today_lunch.replace('<td class="textC last">', '')
        today_lunch = today_lunch.replace('<td class="textC">', '')
        today_lunch = today_lunch.replace('<td>', '')
        today_lunch = today_lunch.replace('.', '')
        for i in range(0x30,0x3A):
            today_lunch = today_lunch.replace(chr(i), '')
    
    lunch_log(log_time=fmt_time,today_lunch=today_lunch).save()


# 인덱스 함수 선언
def index(request):
    ip = request.META.get('REMOTE_ADDR')                    # 사용자 ip구하기
    
    now_time = datetime.today()                             # 현재 시간 받아오기
    user_info(user_ip=ip, connect_time=now_time).save()     # db에 ip, 시간 저장

    a =lunch_log.objects.last()
    if str(a.log_time)[:10] != str(now_time)[:10]:
        print('날짜 다름 새롭게 db 만듬')
        main()

    a = lunch_log.objects.last()

    context = {'last_lunch' : a.today_lunch, 'now_time':now_time.strftime('%Y-%m-%d')}

    return render(request,'lunch/index.html',context)               
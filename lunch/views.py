from django.shortcuts import render
from .models import *
#여기까지 장고


from datetime import datetime





# 인덱스 함수 선언
def index(request):
    ip = request.META.get('REMOTE_ADDR')                    # 사용자 ip구하기
    
    now_time = datetime.today()                             # 현재 시간 받아오기
    user_info(user_ip=ip, connect_time=now_time).save()     # db에 ip, 시간 저장

    a =lunch_log.objects.last()
    context = {'last_lunch' : a.today_lunch, 'now_time':now_time.strftime('%Y-%m-%d')}

    return render(request,'lunch/index.html',context)               
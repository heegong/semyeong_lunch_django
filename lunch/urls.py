from django.urls import path
from . import views

urlpatterns = [
    path('',views.index),
]






from .db_control import db_control
import schedule
from threading import Thread


check_flag = True

def Thread_func():
    global check_flag
    check_flag= False
    schedule.every().day.at("00:02").do(db_control.main)
    while True:
        schedule.run_pending()


if check_flag:
    print('스레드 실행')
    Thread(target=Thread_func).start()
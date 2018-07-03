from django.core.management.base import BaseCommand, CommandError
from water_app.models import *
from django.db.models import Model
from django.utils.timezone import now, timedelta
import datetime
import time

class Command(BaseCommand):
    help = '日志数据自动化管理任务'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        date = datetime.date.today()
        Smoke_data_day_v2.objects.all().delete()
        print(str(date)+'烟感日志表已清空')
        Water_data_day_v2.objects.all().delete()
        print(str(date)+'水压日志表已清空')
        Door_data_day_v2.objects.all().delete()
        print(str(date)+'门禁日志表已清空')
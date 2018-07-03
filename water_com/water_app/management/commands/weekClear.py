from django.core.management.base import BaseCommand, CommandError
from water_app.models import *
from django.db.models import Model
from django.utils.timezone import now, timedelta
import datetime
import time


class Command(BaseCommand):
    help = 'clear Week_data'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        Week_data.objects.all().delete()
        date = datetime.date.today()
        print(str(date)+'Week_data has been cleared')
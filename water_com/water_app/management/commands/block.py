from django.core.management.base import BaseCommand, CommandError
from water_app.models import Getdata, Block
from django.db.models import Model


class Command(BaseCommand):
    help = 'get Data and save block'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        area_name = {'area_name'}
        area_id = {'area_id'}
        street_id = {'street_id'}
        street_name = {'street_name'}
        village_id = {'village_id'}
        village_name = {'village.name'}

        for data in Block.objects.all():
            area_id.add(data.area_id)
            area_name.add(data.area_name)
            street_id.add(data.street_id)
            street_name.add(data.street_name)
            village_id.add(data.village_id)
            village_name.add(data.village_name)

        for data in Getdata.objects.all():
            block = Block()
            block.village_id = data.committee_id
            block.village_name = data.committee_name

            block.street_id = data.region_id
            if not block.street_id:
                block.street_id = '无'

            block.street_name = data.region_name
            if not block.street_name:
                block.street_name = '无'

            block.area_id = data.piece_id
            if not block.area_id:
                # 没有片区id的话
                block.area_id = '无'

            block.area_name = data.piece_name
            if not block.area_name:
                # 没有片区名字的话
                block.area_name = '普陀区'      
            if block.area_name not in area_name or block.street_name not in street_name or block.village_name not in village_name or block.area_id not in area_id or block.street_id not in street_id or block.village_id not in village_id:
                block.save()
                village_name.add(block.village_name)
                street_name.add(block.street_name)
                area_name.add(block.area_name)
                street_id.add(block.street_id)
                area_id.add(block.area_id)
                village_id.add(block.village_id)
                print('done')
        print(area_name)
        print(street_name)
        print(village_name)
        print(street_id)
        print(area_id)
        print(village_id)

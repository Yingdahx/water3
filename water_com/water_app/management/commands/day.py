from django.core.management.base import BaseCommand, CommandError
from water_app.models import *
import requests,hashlib



class Command(BaseCommand):
    help = 'get Data and save local'

    def add_arguments(self, parser):
        pass
    def handle(self, *args, **options):
        url = 'http://47.97.210.144/brain2/usersystem/user/login.do'
        platformId = 1
        password = 'fire123456'
        # md加密
        p1 = hashlib.md5()
        p1.update(password.encode(encoding='utf-8'))

        login_params = {
            'platformId': platformId,
            'loginName': 'fire',
            'password': p1.hexdigest(),
        }

        login_response = requests.post(url, params=login_params).json()

        token = ''
        for key, value in login_response.items():
            if key == 'Data':
                for k, v in value.items():
                    if isinstance(v, dict):
                        for k, v in v.items():
                            if k == 'Authenticator':
                                token = v

        print(token)

        url = 'http://47.97.210.144/brain2/fire/getSensorList.do'
        post_params = {
            'type': 1,
            'Authenticator': token,
        }

        post_response = requests.post(url, params=post_params).json()
        for data in post_response:
            getdata = Getdata()
            getdata.account_id = data['accountId']
            getdata.account_name = data['accountName']
            getdata.address = data['address']
            getdata.belonged_account = data['belongedAccount']
            getdata.belonged_account_group_id = data['belongedAccountGroupId']
            getdata.belonged_account_group_id_name = data['belongedAccountGroupName']
            getdata.build_time = data['buildTime']
            getdata.cluster = data['cluster']
            getdata.committee_id = data['committeeId']
            getdata.committee_name = data['committeeName']
            getdata.create_time = data['createTime']
            getdata.create_user = data['createUser']
            getdata.height = data['height']
            getdata.high = data['high']
            getdata.image_url = data['imageUrl']
            getdata.is_available = data['isAvailable']
            getdata.lat = data['lat']
            getdata.lng = data['lng']
            getdata.location = data['location']
            getdata.photo_url = data['photoUrl']
            getdata.piece_id = data['pieceId']
            getdata.piece_name = data['pieceName']
            getdata.point_id = data['pointId']
            getdata.point_type = data['pointType']
            getdata.received_time = data['received_time']
            getdata.region_id = data['regionId']
            getdata.region_name = data['regionName']
            getdata.sensor_id = data['sensorId']
            getdata.sensor_name = data['sensorName']
            getdata.sensor_number = data['sensorNumber']
            getdata.sensor_point_id = data['sensorPointId']
            getdata.sensor_type = data['sensorType']
            getdata.size = data['size']
            getdata.source = data['source']
            getdata.status = data['status']
            getdata.g_type = data['sourceType']
            getdata.updata_time = data['updateTime']
            getdata.update_user = data['updateUser']
            getdata.video_url = data['videoUrl']
            getdata.water_type = data['waterType']
            getdata.save()

            # 类型解析
            Equipment_type.objects.all().delete()
            e = Equipment_type.objects.filter(type_id=data['sensorType']).first()
            if not e:
                e_t = Equipment_type()
                e_t.type_id = data['sensorType']
                e_t.imageUrl = data['imageUrl']
                e_t.height = data['height']
                e_t.count = 1
                e_t.save()
            else :
                a = e.count 
                a += 1
                e.count = a
                print(e.count)
                e.save()
            print(data['sensorPointId'])

            #物品解析
            e = Equipment.objects.filter(sensor_id=data['sensorId']).first()
            if not e:
                e_new = Equipment()
                e_new.e_id = data['sensorId']
                e_new.name = data['sensorName']
                e_new.area = data['pieceId']
                e_new.street = data['regionId']
                e_new.village = data['committeeId']
                e_new.address = data['address']
                e_new.location_x = data['lat']
                e_new.location_y = data['lng']
                e_new.equipment_type = Equipment_type.objects.filter(type_id=data['sensorType']).first()
                e_new.save()
                print(getdata.sensor_point_id)

            #区域解析
            b_ex = Block.objects.filter(street_id=data['regionId'],village_id=data['committeeId']).first()
            if not b_ex:
                block = Block()
                block.area_id = data['pieceId']
                block.area_name = data['pieceName']
                block.street_id = data['regionId']
                block.street_name = data['regionName']
                block.village_id = data['committeeId']
                block.village_name = data['committeeName']
                block.save()


            

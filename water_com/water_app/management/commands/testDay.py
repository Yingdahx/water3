from django.core.management.base import BaseCommand, CommandError
from water_app.models import *
import requests,hashlib
from django.db.models import Model
from django.utils.timezone import now, timedelta
import datetime
import time


class Command(BaseCommand):
    help = 'get Data and save local'

    def add_arguments(self, parser):
        pass
    def handle(self, *args, **options):
        date = datetime.date.today()
        print('----------'+str(date)+'：定时任务开始----------')
        #登录
        print('----------'+str(date)+'：登录----------')
        url = 'http://47.97.210.144/brain2/usersystem/user/login.do'
        platformId =  1
        password = 'fire123456'
        #md加密
        p1 = hashlib.md5()
        p1.update(password.encode(encoding='utf-8'))

        login_params = {
            'platformId' : platformId,
            'loginName' : 'fire',
            'password' : p1.hexdigest(),
            }

        login_response = requests.post(url, params=login_params).json()

        Authenticator = login_response['Data']['extraInfoObject']['Authenticator']
        login = Login()
        login.Authenticator = Authenticator
        login.save()
        print('登录获取的token：'+Authenticator)
        print('----------'+str(date)+'：登录结束----------')

        Block.objects.all().delete()
        Getdata_v2.objects.all().delete()
        Equipment_type.objects.all().delete()
        Equipment.objects.all().delete()

        #关闭多余网络连接 
        s = requests.session()
        s.keep_alive = False

        print('----------'+str(date)+'：请求meta数据----------')
        au = Login.objects.all().order_by('-add_time').first().Authenticator
        codes = ['DATA_ROKUVNQU','DATA_YNUXZLMW','DATA_TYLCDREW','DATA_QAYHBUCY','DATA_ZLPQXEOV','DATA_CRPUEZTF',
                 'DATA_OCEWLFLS','DATA_WLBZWFBF','DATA_HKPSQWCX','DATA_EYBSLXCI','DATA_KALNNEVQ',
                 'DATA_KQDYAAUK','DATA_OEVIPMPA'] #'DATA_AEHBABKR'-人体红外感应返回fail
        names = ['烟感','门磁','视频','垃圾满溢','地磁','水压','红外周界','电弧灭弧','人脸识别','充电桩','电梯','PH','溶解氧']

        for code in codes:
            post_params = {
                "dataCode": code
                # "startTime":1525104000,
                # "endTime":1530115200
            }
            url = 'http://47.97.210.144/brain2/dataResource/getDataList.do'
            headerdata = {"Content-type": "application/x-www-form-urlencoded","Authenticator": au,}

            #关闭多余网络连接 
            s = requests.session()
            s.keep_alive = False

            post_response = requests.post(url,data=post_params,headers=headerdata).json()
            datas = post_response['Data']
            for data in datas:
                #meta数据落地
                g = Getdata_v2()
                g.device_type = code
                g.sensor_id = data['sensorId']
                g.sensor_name = data['sensorName']
                g.point_type = data['pointType']
                g.point_type_name = data['pointTypeName']
                g.point_id = data['pointId']
                g.point_name = data['pointName']
                g.address = data['address']
                g.photo_url = data['photoUrl']
                g.build_time = data['buildTime']
                g.lng = data['lng']
                g.lat = data['lat']
                g.floor = data['floor']
                g.region_id = data['regionId']
                g.region_name = data['regionName']
                g.piece_id = data['pieceId']
                g.piece_name = data['pieceName']
                g.committee_id = data['committeeId']
                g.committee_name = data['committeeName']
                g.verdor_id = data['vendorID']
                g.verdor_name = data['vendorName']
                g.app_classify_id = data['appClassifyId']
                g.app_classify_name = data['appClassifyName']
                g.save()

                # 2.类型解析 类型数量解析
                e = Equipment_type.objects.filter(type_id=code).first()
                if not e:
                    e_t = Equipment_type()
                    e_t.name = names[codes.index(code)]
                    e_t.type_id = code
                    e_t.count = 1
                    e_t.save()
                else :
                    e.count += 1
                    e.save()

                #3.区域解析
                b_ex = Block.objects.filter(area_id=data['pieceId'],street_id=data['regionId'],village_id=data['committeeId']).first()
                if not b_ex:
                    block = Block()
                    block.area_id = data['pieceId']
                    block.area_name = data['pieceName']
                    block.street_id = data['regionId']
                    block.street_name = data['regionName']
                    block.village_id = data['committeeId']
                    block.village_name = data['committeeName']
                    block.save()

                #4.解析为传感器信息
                e = Equipment.objects.filter(sensor_id=data['sensorId']).first()
                if not e:
                    e_new = Equipment()
                    e_new.sensor_id = data['sensorId']
                    e_new.sensor_name = data['sensorName']
                    e_new.point_type = data['pointType']
                    e_new.point_type_name = data['pointTypeName']
                    e_new.point_id = data['pointId']
                    e_new.point_name = data['pointName']
                    e_new.address = data['address']
                    e_new.build_time = data['buildTime']
                    e_new.lat = data['lat']
                    e_new.lng = data['lng']
                    e_new.floor = data['floor']
                    e_new.region_id = data['regionId']
                    e_new.region_name = data['regionName']
                    e_new.piece_id = data['pieceId']
                    e_new.piece_name = data['pieceName']
                    e_new.committee_id = data['committeeId']
                    e_new.committee_name = data['committeeName']
                    e_new.equipment_type = Equipment_type.objects.filter(type_id=code).first()
                    e_new.save()
            print('----------'+str(date)+'：'+names[codes.index(code)]+'类型数据重置完成！')
        print('----------'+str(date)+'：meta数据拉取完成'+'----------')

            

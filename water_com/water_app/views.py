from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.http import HttpResponse, JsonResponse, HttpRequest
from django.views.decorators.csrf import csrf_exempt
from django.db.utils import IntegrityError
from django.core.exceptions import ValidationError,ObjectDoesNotExist
from django.db.models import Model
from django.db import transaction,connection
from django.utils import timezone
from django.conf import settings

from django.utils.timezone import now, timedelta

import os
import base64
import http.client
import hashlib
import urllib
import urllib.request
import datetime
import time
import json
import pprint
import sys
import requests
import calendar
import random
import uuid
import re


from .models import *

def testPic(requests):
    url = requests.POST.get('picUrl')
    ack = '24.0c14d95c6e48e933f9e329e3443d568b.2592000.1530154541.282335-11312195'

    # url = 'http://39.107.231.143/static/img/101086996163522941.jpg'
    img = requests.get(url)
    img = base64.b64encode(img.content)

    ts = '75eeb3b776c653bdf6bc339f5181abe5'
    headers = {'Content-Type':'application/x-www-form-urlencoded'}
    data = {'image':img,'templateSign':ts,'access_token':ack}
    r = requests.post('https://aip.baidubce.com/rest/2.0/solution/v1/iocr/recognise',headers=headers,data=data)

    with open("em.json",'w+',encoding='utf-8') as json_file:
        json.dump(json.loads(r.text),json_file,ensure_ascii=False)
    
    return JsonResponse(json.loads(r.text))

@csrf_exempt
def demo(requests,haha):
    return HttpResponse(haha)

# 区域admin定制
# 级联菜单
@csrf_exempt
def getAreas(request):
    return render(request,'block.html')

#获得区
@csrf_exempt
def getProvince(request):
    l = list(Block.objects.all())
    re = []
    for i in range(len(l)):
        re.append({
            'area_name':l[i].area_name,
            'street_name':l[i].street_name,
            'village_name':l[i].village_name,
        })
    return JsonResponse({'blocks':re},safe=False)

#获得街道
@csrf_exempt
def getCity(request):
    area_name = request.POST.get('area_name')
    cities = Block.objects.values('street_name','street_id').filter(area_name=area_name)
    # street_name = []
    street_id = []
    for i in cities:
        for k,v in i.items():
            if k=='street_id':
                if v not in street_id:
                    street_id.append(v)
    return JsonResponse({'street_id':street_id})

#获得居委
@csrf_exempt
def getDistrict(request):
    street_id = request.POST.get('street_id')
    villages = Block.objects.values('village_name','village_id').filter(street_id=street_id)
    res = []
    for i in villages:
        res.append(i)
    return JsonResponse({'villages': res})


# 文章方面的增删改查
@csrf_exempt
def article(request):
    ctx = {}
    if request.method == 'POST':
        action = request.POST.get('action', '')
        # 添加文章
        if action == "addRelease":
            release_title = request.POST.get('title', '')
            if not release_title:
                ctx['code'] = 0
                ctx['message'] = "文章标题不能为空"
                return JsonResponse(ctx,safe=False)
            isExist_title = Article.objects.filter(release_title=release_title).first()
            if isExist_title:
                ctx['code'] = 0
                ctx['message'] = str(release_title)+"该文章标题已存在"
                return JsonResponse(ctx,safe=False)
            release_name = request.POST.get('name', '')
            if not release_name:
                ctx['code'] = 0
                ctx['message'] = "发布人姓名不能为空"
                return JsonResponse(ctx,safe=False)
            comment = request.POST.get('comment', '')
            if not comment:
                ctx['code'] = 0
                ctx['message'] = "发布内容不能为空"
                return JsonResponse(ctx,safe=False)
            status = request.POST.get('status', '')
            if not status:
                ctx['code'] = 0
                ctx['message'] = "发布状态不能为空"
                return JsonResponse(ctx,safe=False)
            article = Article()
            article.release_title = release_title
            article.release_name = release_name
            article.comment = comment
            article.status = status
            article.save()
            ctx['code'] = 1
            ctx['message'] = "文章提交成功"
            return JsonResponse(ctx,safe=False)

        # 查询文章列表
        if action == "listRelease":
            article = Article.objects.filter(status=0)  # 在页面展示的文章列表
            if article:
                articles = article.filter().order_by('-release_time')  # 按录入倒序
                articles_list = []
                for article in articles:
                    a = {}
                    a['title'] = article.release_title
                    a['name']=article.release_name
                    a['time']=article.release_time
                    a['comment']=article.comment
                    a['status']=article.status
                    articles_list.append(a)
                ctx['code'] = 1
                ctx['data'] = articles_list
                return JsonResponse(ctx,safe=False)
            else:
                ctx['code'] = 0
                ctx['message'] = '查询失败'
                return JsonResponse(ctx,safe=False)

        # 根据标题关键字进行查询
        if action == "findRelease":
            search_title = request.POST.get('title', '')
            if search_title:
                articles = Article.objects.filter(release_title__contains=search_title)
                if articles:   
                    article_list = []
                    for article in articles:
                        a = {}
                        a['title'] = article.release_title
                        a['name'] = article.release_name
                        a['time'] = article.release_time
                        a['comment'] = article.comment
                        a['status'] = article.status
                        article_list.append(a)
                    ctx['code'] = 1
                    ctx['data'] = article_list
                    return JsonResponse(ctx,safe=False)
                else:
                    ctx['code'] = 0
                    ctx['message'] = '无相关标题的文章'
                    return JsonResponse(ctx,safe=False)
            ctx['code'] = 0
            ctx['message'] = '无查询标题关键字'
            return JsonResponse(ctx,safe=False)

        # 删除文章
        if action == "deleteRelease":
            search_title = request.POST.get('title', '')
            if search_title:
                get_object_or_404(Article, release_title=search_title).delete()
                ctx['code'] = 1
                ctx['message'] = "删除文章成功"
                return JsonResponse(ctx,safe=False)
            else:
                ctx['code'] = 0
                ctx['message'] = "请输入要删除的文章标题"
                return JsonResponse(ctx,safe=False)

        # 修改文章信息
        if action == "updateRelease":
            search_title = request.POST.get('title', '')
            if search_title:
                article = Article.objects.filter(release_title=search_title).first()
                if article:
                    release_name = request.POST.get('name', '')
                    if release_name:
                        article.release_name = release_name
                    comment = request.POST.get('comment', '')
                    if comment:
                        article.comment = comment
                    status = request.POST.get('status', '')
                    if status:
                        article.status = status
                    article.save()
                    ctx['code'] = 1
                    ctx['message'] = "修改文章成功"
                    return JsonResponse(ctx,safe=False)
                ctx['code'] = 0
                ctx['message'] = search_title + '文章不存在'
                return JsonResponse(ctx,safe=False)
            ctx['code'] = 0
            ctx['message'] = "请输入要修改的文章标题"
            return JsonResponse(ctx,safe=False)
        ctx['code'] = 0
        ctx['message'] = "action参数异常"
        return JsonResponse(ctx,safe=False)

#用户会员模块
def member(request):
    ctx = {}
    # ctx['member'] = member = Member.objects.all().order_by('-create_time')
    # print(member)
    if request.method == 'POST':
        action = request.POST.get('action','')
        print(action)
        #添加用户信息
        if action == "addMember":
            name= request.POST.get('name','')
            if not name:
                ctx['code'] = 0
                ctx['message'] = '登陆名不能为空'
                return JsonResponse(ctx,safe=False)
            phone= request.POST.get('phone','')
            if not phone:
                ctx['code'] = 0
                ctx['message'] = '手机号码不能为空'
                return JsonResponse(ctx,safe=False)
            isExist_phone = Member.objects.filter(phone=phone).first()
            if isExist_phone:
                ctx['code'] = 0
                ctx['message'] = '该手机号码已存在'
                return JsonResponse(ctx,safe=False)
            password= request.POST.get('password','')
            if not password:
                ctx['code'] = 0
                ctx['message'] = '密码不能为空'
                return JsonResponse(ctx,safe=False)
            permissionsList = request.POST.getlist('permissions')
            addUser = []
            if not permissionsList:
                ctx['code'] = 0
                ctx['message'] = '权限不能为空'
                return JsonResponse(ctx,safe=False)
                #md加密
            pd = hashlib.md5()
            pd.update(password.encode(encoding='utf-8'))
            member = Member()
            member.name = name
            member.phone = phone
            member.password = pd.hexdigest()
            member.save()
            addUser.append("添加用户信息成功")
            print(permissionsList)
            print(type(permissionsList))
            ctx['success'] = success = []
            ctx['error'] = error = []
            for permissions in permissionsList:
                permission = Permissions()
                m = Member.objects.get(phone=phone)
                permission.phone = m
                a = Area.objects.filter(area_name=permissions).first()
                if a:
                    permission.authority = a
                    permission.save()
                    success.append(str(a)+":添加成功")
                else:
                    error.append(str(permissions)+":添加失败")
            return JsonResponse(ctx,safe=False)

        #用户信息更新
        if action == "updateMember":
            search_phone = request.POST.get('phone','')
            member = Member.objects.get(phone = search_phone)
            name = request.POST.get('name','')
            if name:
                member.name = name
            password = request.POST.get('password','')
            if password:
                pd = hashlib.md5()
                pd.update(password.encode(encoding='utf-8'))
                member.password = pd.hexdigest()
            status = request.POST.get('status','')
            if status:
                member.status = status
            member.save()
            permissionsList = request.POST.getlist('permissions')
            if permissionsList:
                #删除旧权限
                Permissions.objects.filter(phone=Member.objects.get(phone=search_phone)).delete()
                for permissions in permissionsList:
                    permission = Permissions()
                    m = Member.objects.get(phone=Member.objects.get(phone=search_phone))
                    permission.phone = m
                    a = Area.objects.filter(area_name=permissions).first()
                    if a:
                        permission.authority = a
                        permission.save()
                    else:
                        return HttpResponse("该区域不存在")
            return HttpResponse("修改用户信息成功")

        #查询全部状态为0的用户信息列表
        if action =="findUserByType":
            member = Member.objects.filter(userType= 0)
            if member:
                member = member.filter()
                if member:
                    members = member.all().order_by('-create_time')[0:6]  #按录入倒序
                    member_list = []
                    for member in members:
                        a = {}
                        a['name'] = member.name
                        a['phone']=member.phone
                        a['password']=member.password
                        a['create_time']=member.create_time
                        a['userType']=member.userType
                        a['status']=member.status
                        member_list.append(a)

                    return JsonResponse(member_list,safe=False)
        
        #选择用户类型根据用户电话号码进行筛选
        if action =="findByTypeAndName":
            member = Member.objects.filter()
            print(member)
            if member:
                search_phone = request.POST.get('phone','')
                members = member.filter(phone__contains = search_phone)
                if members:
                    member_list = []
                    for member in members:
                        a = {}
                        a['name'] = member.name
                        a['phone']=member.phone
                        a['password']=member.password
                        a['create_time']=member.create_time
                        a['userType']=member.userType
                        a['status']=member.status

                        permissions_list = Permissions.objects.filter(phone=member)
                        print(permissions_list)
                        p=[]
                        for permission in permissions_list:
                            p.append(permission.authority.area_name)

                        print(' '.join(p))
                        a['permission'] = (' '.join(p))

                        member_list.append(str(a))
                    return JsonResponse(member_list,safe=False)
                else:
                    return HttpResponse("未查询到用户信息，请重新输入！")
            else:
                return HttpResponse("未添加用户或用户已全部被删除！")

        #删除一个用户(只是把用户的状态修改为1(停用状态) )
        if action == "deleteMember":
            search_phone = request.POST.get('phone','')
            if search_phone:
                member = Member.objects.filter(phone=search_phone).first()
                if member:
                    member.status = 1
                    member.save()
                    return HttpResponse("删除用户成功")
                else:
                    return HttpResponse("删除用户失败")
#物品类型
def equipmentType(request):
    ctx = {}
    if request.method == 'POST':
        action = request.POST.get('action','')
        #添加用户信息
        if action == "addEquipmentType":
            name = request.POST.get('name','')
            if not name:
                return HttpResponse("设备种类名称不能为空!")
            equipmentTypeName = Equipment_type.objects.filter(name = name).first()
            if equipmentTypeName:
                return HttpResponse("该设备名称已存在")
            t_id = request.POST.get('id','') 
            imageUrl= request.POST.get('imageUrl','')
            height= request.POST.get('height','')
            equipmentType = Equipment_type()
            equipmentType.name = name
            equipmentType.type_id = t_id
            equipmentType.imageUrl = imageUrl
            equipmentType.height = height
            equipmentType.save()
            ctx['code'] = 1
            ctx['message'] = '新增设备类型成功'
            return JsonResponse(ctx,safe=False)

        #修改设备类型信息
        if action == "upEquipmentType":
            search_name = request.POST.get('name','')
            equipmentType = Equipment_type.objects.get(name = search_name)
            if equipmentType:
                t_id = request.POST.get('id','')
                if t_id:
                    equipmentType.type_id = t_id
                imageUrl = request.POST.get('imageUrl', '')
                if imageUrl:
                    equipmentType.imageUrl = imageUrl
                height = request.POST.get('height', '')
                if height:
                    equipmentType.height = height
                status = request.POST.get('status', '')
                if status:
                    equipmentType.status = status
                equipmentType.save()
                ctx['code'] = 1
                ctx['message'] = '修改设备类型成功'
                return JsonResponse(ctx,safe=False)
            ctx['code'] = 0
            ctx['message'] = '未能根据名字找到设备类型'
            return JsonResponse(ctx,safe=False)

        #查询设备类型列表信息(准确查找[停用或正常设备])
        if action == "findByNameList":
            e_type = Equipment_type.objects.all()
            equipmentTypeList = e_type.order_by('-build_time')  #按录入倒序
            if equipmentTypeList:
                equipmentType_list = []
                for equipmentType in equipmentTypeList:
                    a = {}
                    a['name'] = equipmentType.name
                    a['id'] = equipmentType.type_id
                    a['imageUrl'] = equipmentType.imageUrl
                    a['height'] = equipmentType.height
                    a['count'] = equipmentType.count
                    a['status'] = equipmentType.status
                    equipmentType_list.append(a)
                ctx['code'] = 1
                ctx['data'] = equipmentType_list
                return JsonResponse(ctx,safe=False)
            ctx['code'] = 0
            ctx['message'] = '暂无设备类型'
            return JsonResponse(ctx,safe=False)

        #根据关键字进行模糊查询
        if action == "fuzzyFindByName":
            fuzzy_name = request.POST.get('name','')
            if fuzzy_name:
                fuzzyFind = Equipment_type.objects.all()
                if fuzzyFind:
                    fuzzy_list = []
                    fuzzyNameList = fuzzyFind.filter(name__contains = fuzzy_name)
                    if fuzzyNameList:
                        for fuzzyName in fuzzyNameList:
                            a = {}
                            a['name'] = fuzzyName.name
                            a['id'] = fuzzyName.type_id
                            a['imageUrl'] = fuzzyName.imageUrl
                            a['height'] = fuzzyName.height
                            a['count'] = fuzzyName.count
                            a['status'] = fuzzyName.status
                            fuzzy_list.append(a)
                        ctx['code'] = 1
                        ctx['data'] = fuzzy_list
                        return JsonResponse(ctx,safe=False)
                    ctx['code'] = 0
                    ctx['message'] = '未查询到相关设备类型信息！'
                    return JsonResponse(ctx,safe=False)
                ctx['code'] = 0
                ctx['message'] = '暂无设备类型'
                return JsonResponse(ctx,safe=False)
            ctx['code'] = 0
            ctx['message'] = '清输入查询的设备类型名字'
            return JsonResponse(ctx,safe=False)

        #删除某个设备类型
        if action == "deleEquipmentType":
            #得到前台传递来的设备种类名称
            delete_name = request.POST.get('name','')
            if delete_name:
                equipmentType = Equipment_type.objects.filter(name=delete_name).first()
                if equipmentType:
                    equipmentType.status = 1
                    #需要操作人信息-->储存到
                    equipmentType.save()
                    ctx['code'] = 1
                    ctx['message'] = '删除'+ equipmentType.name + '成功'
                    return JsonResponse(ctx,safe=False)
                ctx['code'] = 0
                ctx['message'] = '没有' + equipmentType.name + '类型'
                return JsonResponse(ctx,safe=False)
            ctx['code'] = 0
            ctx['message'] = '请输入要删除的设备类型名称'
            return JsonResponse(ctx,safe=False)

# warning 用户POST请求 model的default字段一定要设置为""(空字符串)
def autoConfig(clzz, req,ef=("id"),re=[]):
    obj = clzz()
    if not isinstance(obj,Model):
        return "type error 非Model子类"
    exclude_fields = ef
    l = [f.name for f in clzz._meta.fields if f.name not in exclude_fields]
    for i in l:
        if req.POST.get(i):
            setattr(obj, i, req.POST.get(i))
    if re:
        for r in re:
            if not getattr(obj,r):
                return None
    return obj

def replaceObj(clzz,origin,new,ef=("id")):
    exclude_fields=ef
    if not (isinstance(origin,clzz) and isinstance(new,clzz)):
        return None

    l = [f.name for f in clzz._meta.fields if f.name not in exclude_fields]
    for i in l:
        s = getattr(new, i)
        if s:
            setattr(origin,i,s)
    return origin

def catchException(func):

    def wrapper(*args,**kwargs):
        try:
            data = func(*args,**kwargs)
            return JsonResponse({'code':1,'message':data})
        except ObjectDoesNotExist as e:
            return JsonResponse({'code':0,'message:':str(e)})
        except IntegrityError as e:
            return JsonResponse({'code':0,'message:':str(e)})
        except ValidationError as e:
            return JsonResponse({'code':0,'message:':str(e)})
        except RequireException as e:
            return JsonResponse({'code':0,'message:':str(e)})
        except Exception as e:
            return JsonResponse({'code':0,'message:':str(e)})
    return wrapper

class RequireException(Exception):
    pass


@catchException
def notice(request, action):
    if request.method == 'POST':
        if action:
            f = request.POST.get('is_list')
            if f and f=='true':
                if action == 'select':
                    return str(Notice.objects.all().order_by('-id'))
                elif action == 'insert':
                    return "not done"
                elif action == 'update':
                    return "not done"
                elif action == 'insert':
                    return "not done"
            else:
                nt = autoConfig(Notice, request)
                re = 'notice ' +action + ' success!'
                if not nt.notice_title:
                    raise RequireException("notice_title is required")
                if action == 'insert':
                    nt.save()
                    return re
                elif action == 'update':
                    origin = Notice.objects.get(notice_title=nt.notice_title)
                    replaceObj(Notice, origin, nt, ef=('id', 'notice_title')).save()
                    return re
                elif action == 'delete':
                    Notice.objects.get(notice_title=nt.notice_title).delete()
                    return re
                elif action == 'select':
                    notice = Notice.objects.get(notice_title=nt.notice_title)
                    n = {}
                    n['title'] = notice.notice_title
                    n['name']=notice.comment      #富文本
                    n['time']=notice.notice_time
                    n['comment']=notice.status
                    return n

# @transaction.atomic()
@catchException
def place(request,model,action):
    if request.method == 'POST':
        if model and action:
            if model == 'area':
                if action == 'select':
                    return str(Area.objects.all())
                else:
                    area = autoConfig(Area, request, re=["area_name"])
                    if not area:raise RequireException("area_name is required")
                    if action == 'insert':
                            area.save()
                            return "save area"
                    elif action == 'delete':
                        Area.objects.get(area_name=area.area_name).delete()
                        return "delete area"
                    elif action == 'update':
                        update_str = request.POST.get("update_str")
                        if update_str and area != update_str:
                            origin = Area.objects.get(area_name=area.area_name)
                            replaceObj(Area,origin,Area(area_name=update_str)).save()
                            return "update area"
                        else:
                            raise RequireException("update_str is required and area_name!=update_str")
            elif model == 'street':
                if action == 'select':
                    return str(Street.objects.all())
                else:
                    street = autoConfig(Street, request, ef=("id", "s_area"), re=["street_name"])
                    if not street:raise RequireException("street_name is required")
                    if action == 'insert':
                        area = autoConfig(Area, request, re=["area_name"])
                        if not area:raise RequireException("area_name is required")
                        area = Area.objects.get(area_name=area.area_name)
                        street.s_area = area
                        street.save()
                        return "save street"
                    elif action == 'delete':
                        Street.objects.get(street_name=street.street_name).delete()
                        return "delete street"
                    elif action == 'update':
                        update_str = request.POST.get("update_str")
                        if update_str and street.street_name != update_str:
                            origin = Street.objects.get(street_name=street.street_name)
                            replaceObj(Street,origin,Street(street_name=update_str),ef=("id","s_area")).save()
                            return "update street"
                        else:
                            raise RequireException("update_str is required and street_name!=update_str")
            elif model == 'village':
                if action == 'select':
                    return str(Village.objects.all())
                else:
                    village = autoConfig(Village, request, ef=("id", "v_street"), re=["village_name"])
                    if not village:raise RequireException("village_name is required")

                    if action == 'insert':
                        street = autoConfig(Street, request, ef=("id", "s_area"), re=["street_name"])
                        if street:
                            street = Street.objects.get(street_name=street.street_name)
                            village.v_street = street
                            village.save()
                            return "save village"
                        else:
                            raise RequireException("street_name is required")
                    elif action == 'delete':
                        Village.objects.get(village_name=village.village_name).delete()
                        return "delete village"
                    elif action == 'update':
                        update_str = request.POST.get("update_str")
                        if update_str and village != update_str:
                            origin = Village.objects.get(village_name=village.village_name)
                            replaceObj(Village,origin,Village(village_name=update_str),ef=("id","v_street")).save()
                            return "update village"


#拉取数据账户登录
def login(request):
    ctx = {}
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

    ctx['Authenticator'] = Authenticator = login_response['Data']['extraInfoObject']['Authenticator']
    ctx['message'] = message = 'login success'

    login = Login()
    login.Authenticator = Authenticator
    login.save()

    return HttpResponse(message)

#拉取传感器信息数据入库
def getdata(request):
    ctx = {}
    url = 'http://47.97.210.144/brain2/fire/getSensorList.do'
    data_type =  1
    login = Login.objects.all().order_by('-add_time').first()
    print(login)
    Authenticator = login.Authenticator
    print(Authenticator)
    post_params = {
        'type' : data_type,
        'Authenticator': Authenticator,
        }

    post_response = requests.post(url, params=post_params)#.json()
    print(post_response[0])

    # i = 0

    # for data in post_response:
    #     getdata = Getdata()
    #     getdata.account_id = data['accountId']
    #     getdata.account_name = data['accountName']
    #     getdata.address = data['address']
    #     getdata.belonged_account = data['belongedAccount']
    #     getdata.belonged_account_group_id = data['belongedAccountGroupId']
    #     getdata.belonged_account_group_id_name = data['belongedAccountGroupName']
    #     getdata.build_time = data['buildTime']
    #     getdata.cluster = data['cluster']
    #     getdata.committee_id = data['committeeId']
    #     getdata.committee_name = data['committeeName']
    #     getdata.create_time = data['createTime']
    #     getdata.create_user = data['createUser']
    #     getdata.height = data['height']
    #     getdata.high = data['high']
    #     getdata.image_url = data['imageUrl']
    #     getdata.is_available = data['isAvailable']
    #     getdata.lat = data['lat']
    #     getdata.lng = data['lng']
    #     getdata.location = data['location']
    #     getdata.photo_url = data['photoUrl']
    #     getdata.piece_id = data['pieceId']
    #     getdata.piece_name = data['pieceName']
    #     getdata.point_id = data['pointId']
    #     getdata.point_type = data['pointType']
    #     getdata.received_time = data['received_time']
    #     getdata.region_id = data['regionId']
    #     getdata.region_name = data['regionName']
    #     getdata.sensor_id = data['sensorId']
    #     getdata.sensor_name = data['sensorName']
    #     getdata.sensor_number = data['sensorNumber']
    #     getdata.sensor_point_id = data['sensorPointId']
    #     getdata.sensor_type = data['sensorType']
    #     getdata.size = data['size']
    #     getdata.source = data['source']
    #     getdata.status = data['status']
    #     getdata.g_type = data['sourceType']
    #     getdata.updata_time = data['updateTime']
    #     getdata.update_user = data['updateUser']
    #     getdata.video_url = data['videoUrl']
    #     getdata.water_type = data['waterType']
    #     getdata.floor = data['floor']
    #     getdata.save()

    #     i = i + 1
    #     print(i)

    #     # # 类型解析
    #     # e = Equipment_type.objects.filter(type_id=data['sensorType']).first()
    #     # if not e:
    #     #     e_t = Equipment_type()
    #     #     e_t.type_id = data['sensorType']
    #     #     e_t.imageUrl = data['imageUrl']
    #     #     e_t.height = data['height']
    #     #     e_t.count = 1
    #     #     e_t.save()
    #     # else :
    #     #     print('old type: count +1!')
    #     #     a = e.count 
    #     #     a += 1
    #     #     e.count = a
    #     #     print(e.count)
    #     #     e.save()
    #     # print(data['sensorPointId'])

    #     #物品解析
    #     e_new = Equipment()
    #     e_new.e_id = data['sensorId']
    #     e_new.name = data['sensorName']
    #     e_new.area = data['pieceId']
    #     e_new.street = data['regionId']
    #     e_new.village = data['committeeId']
    #     e_new.address = data['address']
    #     e_new.location_x = data['lat']
    #     e_new.location_y = data['lng']
    #     e_new.equipment_type = Equipment_type.objects.filter(type_id=data['sensorType']).first()
    #     e_new.save()
    #     print(getdata.sensor_point_id)
    #     ctx['message'] = message = 'save data :' + str(i)
    ctx['message'] = message = 'test success'
    return HttpResponse(message)


#警报数据接收
@csrf_exempt
def push(request):

    if request.method != 'POST':
        return JsonResponse({ 'success': False, 'code': -1, 'msg': '只支持POST' }, status=405)

    raw = json.loads(request.body.decode('utf-8'))
    json_root = settings.MEDIA_ROOT + '/json/' + '%d.json' % time.time()  #json保存路径

    with open(json_root, 'w') as f:
        f.write(json.dumps(raw, indent=4))

    #原数据
    data = Data()
    data.device_type = raw['device_type']
    data.create_time = raw['create_time']
    data.state = raw['state']
    data.battery_voltage = raw['battery_voltage']
    data.device_id = raw['device_id']
    data.received_time = raw['received_time']
    data.info_type = raw['info_type']
    data.protocol_version = raw['protocol_version']
    data.software_version = raw['software_version']
    data.smoke_concentration= raw['smoke_concentration']
    data.save()

    #日数据
    d_data = Day_data()
    d_data.device_type = raw['device_type']
    d_data.create_time = raw['create_time']
    d_data.state = raw['state']
    d_data.battery_voltage = raw['battery_voltage']
    d_data.device_id = raw['device_id']
    d_data.received_time = raw['received_time']
    d_data.info_type = raw['info_type']
    d_data.protocol_version = raw['protocol_version']
    d_data.software_version = raw['software_version']
    d_data.smoke_concentration= raw['smoke_concentration']
    d_data.save()

    #周数据
    w_data = Week_data()
    w_data.device_type = raw['device_type']
    w_data.create_time = raw['create_time']
    w_data.state = raw['state']
    w_data.battery_voltage = raw['battery_voltage']
    w_data.device_id = raw['device_id']
    w_data.received_time = raw['received_time']
    w_data.info_type = raw['info_type']
    w_data.protocol_version = raw['protocol_version']
    w_data.software_version = raw['software_version']
    w_data.smoke_concentration= raw['smoke_concentration']
    w_data.save()

    #月数据
    m_data = Month_data()
    m_data.device_type = raw['device_type']
    m_data.create_time = raw['create_time']
    m_data.state = raw['state']
    m_data.battery_voltage = raw['battery_voltage']
    m_data.device_id = raw['device_id']
    m_data.received_time = raw['received_time']
    m_data.info_type = raw['info_type']
    m_data.protocol_version = raw['protocol_version']
    m_data.software_version = raw['software_version']
    m_data.smoke_concentration= raw['smoke_concentration']
    m_data.save()

    if raw['info_type'] == '1': #报警记录
        #实时报警数据
        f_data = Focus_data()
        f_data.device_type = raw['device_type']
        f_data.create_time = raw['create_time']
        f_data.state = raw['state']
        f_data.battery_voltage = raw['battery_voltage']
        f_data.device_id = raw['device_id']
        f_data.received_time = raw['received_time']
        f_data.info_type = raw['info_type']
        f_data.protocol_version = raw['protocol_version']
        f_data.software_version = raw['software_version']
        f_data.smoke_concentration= raw['smoke_concentration']
        f_data.save()

        #火警事件数据
        w = Warning_data.objects.filter(device_id=raw['device_id']).first()
        if w:
            w.delete()
        warn_data = Warning_data()
        warn_data.device_type = raw['device_type']
        warn_data.create_time = raw['create_time']
        warn_data.state = raw['state']
        warn_data.battery_voltage = raw['battery_voltage']
        warn_data.device_id = raw['device_id']
        warn_data.received_time = raw['received_time']
        warn_data.info_type = raw['info_type']
        warn_data.protocol_version = raw['protocol_version']
        warn_data.software_version = raw['software_version']
        warn_data.smoke_concentration= raw['smoke_concentration']
        warn_data.save()
    else :                      
        #未报警取消历史报警数据
        f = Focus_data.objects.filter(device_id=raw['device_id']).first()
        if f:
            f.delete()
        #覆盖报警状态的改变状态值
        w = Warning_data.objects.filter(device_id=raw['device_id']).first()
        if w:
            w.create_time = raw['create_time']
            w.received_time = raw['received_time']
            w.info_type = raw['info_type']
            w.status = 'Change'
            w.save()

    if raw['info_type'] == '7':
        e = Event_data.objects.filter(device_id=raw['device_id']).first()
        if w:
            w.status = 'Change Normal'
            w.save()
    else:
        e = Event_data.objects.filter(device_id=raw['device_id']).first()
        if e:
            e.delete()
        e_data = Event_data()
        e_data.device_type = raw['device_type']
        e_data.create_time = raw['create_time']
        e_data.state = raw['state']
        e_data.battery_voltage = raw['battery_voltage']
        e_data.device_id = raw['device_id']
        e_data.received_time = raw['received_time']
        e_data.info_type = raw['info_type']
        e_data.protocol_version = raw['protocol_version']
        e_data.software_version = raw['software_version']
        e_data.smoke_concentration= raw['smoke_concentration']
        e_data.save()

    #传感器状态
    e = Equipment.objects.filter(e_id=raw['device_id']).first()
    if e:  #有未知传感器警报数据
        e.status = int(raw['info_type'])
        e.save()

    return JsonResponse({ 'success': True })

def day(request):
    ctx = {}
    #左上
    ctx['e_ts'] = e_ts = Equipment_type.objects.all()

    #日志分页数据
    ONE_PAGE_OF_DATA = 21

    try:
        pageNo = int(request.GET.get('pageNo', '1'))
        allPage = int(request.GET.get('allPage','1'))
        pageType = str(request.GET.get('pageType', ''))
    except ValueError:
        pageNo = 1
        allPage = 1
        pageType = ''
    #判断点击了【下一页】还是【上一页】
    if pageType == 'pageDown':
        pageNo += 1
    elif pageType == 'pageUp':
        pageNo -= 1
    startPos = (pageNo - 1) * ONE_PAGE_OF_DATA
    endPos = startPos + ONE_PAGE_OF_DATA
    ctx['day_record'] = day_record = Day_data.objects.all().order_by('-get_time')[startPos:endPos]
    ctx['day_records'] = day_records = []
    for da in day_record:
        addr = Getdata.objects.filter(sensor_id=da.device_id).first()
        if addr:
            a = {}
            a['name'] = addr.address
            a['info_type'] = da.info_type
            a['create_time'] = da.create_time
            day_records.append(a)
    if pageNo == 1 and allPage == 1: #标记1
        allPostCounts = Day_data.objects.count()
        allPage = allPostCounts // ONE_PAGE_OF_DATA
        print(allPage)
        remainPost = allPostCounts % ONE_PAGE_OF_DATA
        if remainPost > 0:
            allPage += 1
    ctx['allPage'] = allPage
    ctx['pageNo'] = pageNo

    #右侧数据
    ctx['right'] = right = []
    blocks = Block.objects.all()
    #街道遍历
    for b in range(len(blocks)):            
        num = 0
        #传感器遍历                
        gs = Getdata.objects.filter(region_id=blocks[b].street_id,committee_id=blocks[b].village_id).values('sensor_id')
        num += Focus_data.objects.filter(device_id__in=[_['sensor_id'] for _ in gs]).count()  
        #是否包装
        if num != 0:                   
            r = {}
            r['name'] = blocks[b].street_name
            r['lat'] = blocks[b].street_lat
            r['lng'] = blocks[b].street_lng
            r['num'] = num
            right.append(r)

    return render(request,'day.html',ctx)

def police_day(request):
    ctx = {}
    ctx['e_ts'] = e_ts = Equipment_type.objects.all()

    #今日报警数据分页
    ONE_PAGE_OF_DATA = 15

    try:
        pageNo = int(request.GET.get('pageNo', '1'))
        allPage = int(request.GET.get('allPage','1'))
        pageType = str(request.GET.get('pageType', ''))
    except ValueError:
        pageNo = 1
        allPage = 1
        pageType = ''
    #判断点击了【下一页】还是【上一页】
    if pageType == 'pageDown':
        pageNo += 1
    elif pageType == 'pageUp':
        pageNo -= 1
    startPos = (pageNo - 1) * ONE_PAGE_OF_DATA
    endPos = startPos + ONE_PAGE_OF_DATA
    ctx['day_focus'] = day_focus = Day_data.objects.filter(info_type='1').order_by('-get_time')[startPos:endPos]
    ctx['day_focuss'] = day_focuss = []
    for da in day_focus:
        addr = Getdata.objects.filter(sensor_id=da.device_id).first()
        if addr:
            a = {}
            a['name'] = addr.address
            a['info_type'] = da.info_type
            a['create_time'] = da.create_time
            day_focuss.append(a)
    if pageNo == 1 and allPage == 1: #标记1
        allPostCounts = Day_data.objects.filter(info_type='1').count()
        allPage = allPostCounts // ONE_PAGE_OF_DATA
        print(allPage)
        remainPost = allPostCounts % ONE_PAGE_OF_DATA
        if remainPost > 0:
            allPage += 1
    ctx['allPage'] = allPage
    ctx['pageNo'] = pageNo

    #右侧数据
    ctx['right'] = right = []
    blocks = Block.objects.all()
    #街道遍历
    for b in range(len(blocks)):            
        num = 0                   
        #传感器遍历                
        gs = Getdata.objects.filter(region_id=blocks[b].street_id,committee_id=blocks[b].village_id).values('sensor_id')
        num += Focus_data.objects.filter(device_id__in=[_['sensor_id'] for _ in gs]).count()   
        #是否包装
        if num != 0:                   
            r = {}
            r['name'] = blocks[b].street_name
            r['lat'] = blocks[b].street_lat
            r['lng'] = blocks[b].street_lng
            r['num'] = num
            right.append(r)

    return render(request,'police_day.html',ctx)

def month(request):
    ctx = {}

    ctx['e_ts'] = e_ts = Equipment_type.objects.all()

    date = datetime.date.today()  #今天日期
    _, last_day_num = calendar.monthrange(date.year, date.month)  #月最大天数
    last_day = datetime.date(date.year, date.month, last_day_num)  #月末
    first_day = datetime.date(date.year,date.month,1) #月初
    last_week = last_day + datetime.timedelta(6 - last_day.weekday()) #最后一天所在周的最后一天
    week_first = first_day   #第一周开始日期 周首
    week_last = first_day + datetime.timedelta(6 - first_day.weekday()) #星期日日期 周尾

    ctx['ls'] = ls = []
    while week_last !=  last_week:
        monthdata = Month_data.objects.filter(get_time__range=(str(week_first),str(week_last))).values('device_id') #周数据
        num = 0
        g = Getdata.objects.filter(sensor_id__in=[_['device_id'] for _ in monthdata],sensor_type='1').count()
        num += g
        l = {}
        l['time'] = str(week_first) + '~' +str(week_last)
        l['num'] = num
        ls.append(l)

        week_first = week_last + datetime.timedelta(days=1)                 #下周周一
        week_last = week_first + datetime.timedelta(6 - week_first.weekday()) #下周周日

    monthdata = Month_data.objects.filter(get_time__range=(str(week_first),str(week_last))).values('device_id') #周数据
    num = 0
    g = Getdata.objects.filter(sensor_id__in=[_['device_id'] for _ in monthdata],sensor_type='1').count()
    num += g
    l = {}
    l['time'] = str(week_first) + '~' +str(week_last)
    l['num'] = num
    ls.append(l)
    
    #右侧数据
    ctx['right'] = right = []
    blocks = Block.objects.all()
    #街道遍历
    for b in range(len(blocks)):            
        num = 0
        #传感器遍历                
        gs = Getdata.objects.filter(region_id=blocks[b].street_id,committee_id=blocks[b].village_id).values('sensor_id')
        num += Focus_data.objects.filter(device_id__in=[_['sensor_id'] for _ in gs]).count()
        #是否包装
        if num != 0:                   
            r = {}
            r['name'] = blocks[b].street_name
            r['lat'] = blocks[b].street_lat
            r['lng'] = blocks[b].street_lng
            r['num'] = num
            right.append(r)
     
    print(ctx)

    return render(request,'month.html',ctx)

def police_month(request):
    ctx = {}
    ctx['e_ts'] = e_ts = Equipment_type.objects.all()

    date = datetime.date.today()  #今天日期
    _, last_day_num = calendar.monthrange(date.year, date.month)  #月最后一天号数
    last_day = datetime.date(date.year, date.month, last_day_num)  #月末
    first_day = datetime.date(date.year,date.month,1) #月初

    last_week = last_day + datetime.timedelta(6 - last_day.weekday()) #最后一天所在周的最后一天

    week_first = first_day   #第一周开始日期
    week_last = first_day + datetime.timedelta(6 - first_day.weekday()) #星期日日期

    print(week_last)
    ctx['ls'] = ls = []

    while week_last !=  last_week:
        monthdata = Month_data.objects.filter(get_time__range=(str(week_first),str(week_last)),info_type='1') #周数据
        num_week = monthdata.count() #周数据总数
        
        num = 0
        for m in monthdata:
            g = Getdata.objects.filter(sensor_id=m.device_id)
            if g:
                if g.first().sensor_type == '1': #报警数据(设备ID)->物品数据(传感器类型)
                    num = num + 1

        l = {}
        l['time'] = str(week_first) + '~' +str(week_last)
        l['num'] = num
        ls.append(l)

        week_first = week_last + datetime.timedelta(days=1)                 #下周周一
        week_last = week_first + datetime.timedelta(6 - week_first.weekday()) #下周周日

    monthdata = Focus_data.objects.filter(get_time__range=(str(week_first),str(last_day)),info_type='1') #周数据
    num_week = monthdata.count() #最后一周取到最后一号

    num = 0

    for m in monthdata:
        g = Getdata.objects.filter(sensor_id=m.device_id)
        if g:
            if g.first().sensor_type == '1': #报警数据(设备ID)->物品数据(传感器类型)
                num = num + 1

    l = {}
    l['time'] = str(week_first) + '~' +str(last_day)
    l['num'] = num
    ls.append(l)
    
    #右侧数据
    ctx['right'] = right = []
    blocks = Block.objects.all()
    #街道遍历
    for b in range(len(blocks)):            
        num = 0
        #传感器遍历                
        gs = Getdata.objects.filter(region_id=blocks[b].street_id,committee_id=blocks[b].village_id).values('sensor_id')

        num += Focus_data.objects.filter(device_id__in=[_['sensor_id'] for _ in gs]).count()
            
        #是否包装
        if num != 0:                   
            r = {}
            r['name'] = blocks[b].street_name
            r['lat'] = blocks[b].street_lat
            r['lng'] = blocks[b].street_lng
            r['num'] = num
            right.append(r)

    return render(request,'police_month.html',ctx)

def Week(request):
    ctx = {}
    ctx['e_ts'] = e_ts = Equipment_type.objects.all()

    date = datetime.date.today() #今天
    week_last = date + datetime.timedelta(6 - date.weekday()) #本周日
    week_first = date - datetime.timedelta(date.weekday()) #本周一

    week_record = Week_data.objects.all() #本周数据

    # types = Equipment_type.objects.all() 类型遍历...

    ctx['r'] = r = [] #结果

    z = 0
    while z < 7:
        day = week_first + datetime.timedelta(days=z)        #遍历日期
        record = week_record.filter(get_time__contains=str(day)).values('device_id')  #当日数据
        num = 0
        num += Getdata.objects.filter(sensor_id__in=[_['device_id'] for _ in record],sensor_type='1').count()
        ctx['i'] = i = {}
        i['week_day'] = day
        i['num'] = num
        r.append(i)
        z = z + 1

    #右侧数据
    ctx['right'] = right = []
    blocks = Block.objects.all()
    #街道遍历
    for b in range(len(blocks)):            
        num = 0
        #传感器遍历                
        gs = Getdata.objects.filter(region_id=blocks[b].street_id,committee_id=blocks[b].village_id).values('sensor_id')

        num += Focus_data.objects.filter(device_id__in=[_['sensor_id'] for _ in gs]).count()
            
        #是否包装
        if num != 0:                   
            r = {}
            r['name'] = blocks[b].street_name
            r['lat'] = blocks[b].street_lat
            r['lng'] = blocks[b].street_lng
            r['num'] = num
            right.append(r)

    return render(request,'Week.html',ctx)

def police_Week(request):
    ctx = {}
    ctx['e_ts'] = e_ts = Equipment_type.objects.all()

    date = datetime.date.today() #今天
    week_last = date + datetime.timedelta(6 - date.weekday()) #周日
    week_first = date - datetime.timedelta(date.weekday()) #周一

    week_record = Week_data.objects.filter(get_time__range=(str(week_first),str(week_last)),info_type='1') #本周报警数据

    ctx['r'] = r = [] #结果集

    z = 0    #0-6 
    while z < 7:
        day = week_first + datetime.timedelta(days=z)        #日期
        record = week_record.filter(get_time__contains=str(day))  #当日报警数据
        num = 0
        for data in record:                            
            g = Getdata.objects.filter(sensor_id=data.device_id)
            if g:
                if g.first().sensor_type == '1': #烟感
                    num = num + 1
        ctx['i'] = i = {}
        i['week_day'] = day
        i['num'] = num
        r.append(i)
        z = z + 1

    #右侧数据
    ctx['right'] = right = []
    blocks = Block.objects.all()
    #街道遍历
    for b in range(len(blocks)):            
        num = 0
        #传感器遍历                   
        gs = Getdata.objects.filter(region_id=blocks[b].street_id,committee_id=blocks[b].village_id).values('sensor_id')

        num += Focus_data.objects.filter(device_id__in=[_['sensor_id'] for _ in gs]).count()
            
        #是否包装
        if num != 0:                   
            r = {}
            r['name'] = blocks[b].street_name
            r['lat'] = blocks[b].street_lat
            r['lng'] = blocks[b].street_lng
            r['num'] = num
            right.append(r)

    print(ctx)
    return render(request,'police_week.html',ctx)

def index(request):

    ctx = {}

    #左侧数据
    ctx['e_ts'] = e_ts = Equipment_type.objects.all() 
    
    # #右侧数据
    # ctx['right'] = right = []
    # blocks = Block.objects.all()
    # #街道遍历
    # for b in range(len(blocks)):            
    #     num = 0
    #     #传感器遍历                
    #     gs = Getdata.objects.filter(region_id=blocks[b].street_id,committee_id=blocks[b].village_id).values('sensor_id')

    #     num += Focus_data.objects.filter(device_id__in=[_['sensor_id'] for _ in gs]).count()
            
    #     #是否包装
    #     if num != 0:                   
    #         r = {}
    #         r['name'] = blocks[b].street_name
    #         r['lat'] = blocks[b].street_lat
    #         r['lng'] = blocks[b].street_lng
    #         r['num'] = num
    #         right.append(r)

    #debug test 
    ets = ['烟感','水压']
    ss_t = ['7','8']
    res = {}
    
    #中间地图描点数据
    res['center'] = center = []
    #实时报警数据
    fs = Focus_data.objects.values_list('device_id',flat=True).distinct()
    #外层点
    blocks = Block.objects.all()
    for b in blocks:
        bj = {}
        bj['name'] = b.street_name + b.village_name   #外层街道小区点 名
        bj['level'] = 3                               #初始化默认为正常
        bj['lat'] = b.street_lat        #外层点坐标
        bj['lng'] = b.street_lng

        #外层标签
        bj['data_type'] = data_type = []              
        #遍历类型
        al = {}
        al['type_name'] = '安装设备共'
        al_num = Getdata.objects.filter(region_id=b.street_id,committee_id=b.village_id)
        al['type_num'] = str(al_num.count()) + '个'
        data_type.append(al)
        for ss in ss_t:
            t = {}
            t['type_name'] = ets[ss_t.index(ss)] + '传感器'
            type_num = al_num.filter(sensor_type=ss).count()
            t['type_num'] = str(type_num) + '个'
            if type_num != 0:
                data_type.append(t)
        #遍历结束

        bj['child'] = child = []        #内层点
        # 内层地址列表
        adds = al_num.values('address').distinct()

        #外层点报警计数器
        at = {}
        at['type_name'] = '区域报警数'
        at_num = 0
        for a in adds: #内层地址遍历
            c_data = {}
            #内层点标签信息
            c_data['area'] = b.area_name
            c_data['village'] = b.village_name
            c_data['street_name'] = b.street_name
            c_data['address'] = a['address']  #地址 
            c_data['level'] = 3 #初始化默认正常
            ai = al_num.filter(address=a['address']).values('lat','lng').first()
            c_data['lat'] = ai['lat']
            c_data['lng'] = ai['lng']
            c_data['focus_list'] = focus_list = []    #内层报警位置详情列表

            #该地址传感器总数
            gs = al_num.filter(address=a['address']).values('sensor_id','address','sensor_type','lat','lng') 
            count = gs.count()
            c_data['count'] = str(count) + '个'

            #标签三个状态字段
            sensor_t = ''
            sta = ''
            sensor_s = ''
            #烟感 水压 遍历
            for ss in ss_t:
                #传感器类型
                st_str = ets[ss_t.index(ss)] + ':正常  '
                #该类型数量
                ggs = gs.filter(sensor_type=ss)
                gg = ggs.count()
                if gg != 0:
                    ss_str =  ets[ss_t.index(ss)] + ':' + str(gg) + '个  '  #类型个数
                    sensor_t += ss_str
                    #内层点报警计数器
                    i = 0
                    for g in ggs:
                        if g['sensor_id'] in fs: #内层报警
                            print('判断语句通过 捕捉到报警传感器')    
                            focus_list.append(g['address'] + '：' + g['sensor_id'])  #报警列表记录到地图标签
                            bj['level'] = 1                         #外层受影响显示为红色
                            st_str = ets[ss_t.index(ss)] + ':报警  ' #内层状态改变 
                            c_data['level'] = 1                     #内层显示红色
                            i += 1                                  #计数器
                        print(i)
                    #外层报警数据器叠加
                    at_num += i
                    #标签状态总结
                    sen_str = ets[ss_t.index(ss)] + ':(报警：' + str(i) + '个，正常' + str(gg-i) +'个)\r'
                    sensor_s += sen_str
                    sta += st_str

            c_data['sensor_status'] = sensor_s
            c_data['sensor_type'] = sensor_t  #传感器类型
            c_data['status'] = sta            #报警类型
            child.append(c_data)
        #外层报警计数包装
        at['type_num'] = str(at_num) + '个'
        data_type.append(at)
        center.append(bj)
            
    return render(request,'index.html',ctx)


def details(request):
    ctx = {}
    lat = request.GET.get('lat')  
    lng = request.GET.get('lng')    
    block = Block.objects.filter(street_lat=lat,street_lng=lng).first() #子页面区域
    if block:
        #左侧数据
        ctx['left'] = left = []
        e_ts = Equipment_type.objects.all() #遍历类型
        for e_t in e_ts:
            t_num = Getdata.objects.filter(region_id=block.street_id,sensor_type=e_t.type_id).count() #区域内传感器数量
            if t_num != 0:
                l = {}
                l['name'] = e_t.name
                l['num'] = t_num
                left.append(l)

        #右侧数据
        ctx['right'] = right = []
        bs = Block.objects.filter(street_lat=lat,street_lng=lng) #街道遍历
        for b in bs:
            num = 0 
            #传感器遍历                
            gs = Getdata.objects.filter(region_id=b.street_id,committee_id=b.village_id).values('sensor_id')

            num += Focus_data.objects.filter(device_id__in=[_['sensor_id'] for _ in gs]).count()
            if num != 0:
                r = {}
                r['name'] = b.village_name
                r['num'] = num 
                right.append(r)
        ctx['lat'] = lat 
        ctx['lng'] = lng 
        return render(request,'details.html',ctx)
    else :
        #左侧数据
        ctx['e_ts'] = e_ts = Equipment_type.objects.all() 
        return render(request,'index.html',ctx)

#本地测试调数据
def analysis(request):
    ctx = {}

    # #登录
    # print('----------登录----------')
    # url = 'http://47.97.210.144/brain2/usersystem/user/login.do'
    # platformId =  1
    # password = 'fire123456'
    # #md加密
    # p1 = hashlib.md5()
    # p1.update(password.encode(encoding='utf-8'))

    # login_params = {
    #     'platformId' : platformId,
    #     'loginName' : 'fire',
    #     'password' : p1.hexdigest(),
    #     }

    # login_response = requests.post(url, params=login_params).json()

    # print(login_response)
    # ctx['Authenticator'] = Authenticator = login_response['Data']['extraInfoObject']['Authenticator']
    # ctx['message'] = message = 'login success'

    # login = Login()
    # login.Authenticator = Authenticator
    # login.save()
    # print('登录获取的token：'+Authenticator)
    # print('----------登录结束----------')

    # Block.objects.all().delete()
    # Getdata_v2.objects.all().delete()
    # Equipment_type.objects.all().delete()
    # Equipment.objects.all().delete()
    # #关闭多余网络连接 
    # s = requests.session()
    # s.keep_alive = False

    # print('----------请求meta数据----------')
    # au = Login.objects.all().order_by('-add_time').first().Authenticator
    # codes = ['DATA_ROKUVNQU','DATA_YNUXZLMW','DATA_TYLCDREW','DATA_QAYHBUCY','DATA_ZLPQXEOV','DATA_CRPUEZTF',
    #          'DATA_OCEWLFLS','DATA_WLBZWFBF','DATA_HKPSQWCX','DATA_EYBSLXCI','DATA_KALNNEVQ',
    #          'DATA_KQDYAAUK','DATA_OEVIPMPA'] #'DATA_AEHBABKR'-人体红外感应返回fail
    # names = ['烟感','门磁','视频','垃圾满溢','地磁','水压','红外周界','电弧灭弧','人脸识别','充电桩','电梯','PH','溶解氧']

    # for code in codes:
    #     post_params = {
    #         "dataCode": code
    #         # "startTime":1525104000,
    #         # "endTime":1530115200
    #     }
    #     url = 'http://47.97.210.144/brain2/dataResource/getDataList.do'
    #     headerdata = {"Content-type": "application/x-www-form-urlencoded","Authenticator": au,}

    #     #关闭多余网络连接 
    #     s = requests.session()
    #     s.keep_alive = False

    #     post_response = requests.post(url,data=post_params,headers=headerdata).json()
    #     datas = post_response['Data']
    #     for data in datas:
    #         #meta数据落地
    #         g = Getdata_v2()
    #         g.device_type = code
    #         g.sensor_id = data['sensorId']
    #         g.sensor_name = data['sensorName']
    #         g.point_type = data['pointType']
    #         g.point_type_name = data['pointTypeName']
    #         g.point_id = data['pointId']
    #         g.point_name = data['pointName']
    #         g.address = data['address']
    #         g.photo_url = data['photoUrl']
    #         g.build_time = data['buildTime']
    #         g.lng = data['lng']
    #         g.lat = data['lat']
    #         g.floor = data['floor']
    #         g.region_id = data['regionId']
    #         g.region_name = data['regionName']
    #         g.piece_id = data['pieceId']
    #         g.piece_name = data['pieceName']
    #         g.committee_id = data['committeeId']
    #         g.committee_name = data['committeeName']
    #         g.verdor_id = data['vendorID']
    #         g.verdor_name = data['vendorName']
    #         g.app_classify_id = data['appClassifyId']
    #         g.app_classify_name = data['appClassifyName']
    #         g.save()

    #         # 2.类型解析 类型数量解析
    #         e = Equipment_type.objects.filter(type_id=code).first()
    #         if not e:
    #             e_t = Equipment_type()
    #             e_t.name = names[codes.index(code)]
    #             e_t.type_id = code
    #             e_t.count = 1
    #             e_t.save()
    #         else :
    #             e.count += 1
    #             e.save()
    #             print(e.name+'类型传感器数量增加到：'+str(e.count))
    #         #3.区域解析
    #         b_ex = Block.objects.filter(area_id=data['pieceId'],street_id=data['regionId'],village_id=data['committeeId']).first()
    #         if not b_ex:
    #             block = Block()
    #             block.area_id = data['pieceId']
    #             block.area_name = data['pieceName']
    #             block.street_id = data['regionId']
    #             block.street_name = data['regionName']
    #             block.village_id = data['committeeId']
    #             block.village_name = data['committeeName']
    #             block.save()
    #         #4.解析为传感器信息
    #         e = Equipment.objects.filter(sensor_id=data['sensorId']).first()
    #         if not e:
    #             e_new = Equipment()
    #             e_new.sensor_id = data['sensorId']
    #             e_new.sensor_name = data['sensorName']
    #             e_new.point_type = data['pointType']
    #             e_new.point_type_name = data['pointTypeName']
    #             e_new.point_id = data['pointId']
    #             e_new.point_name = data['pointName']
    #             e_new.address = data['address']
    #             e_new.build_time = data['buildTime']
    #             e_new.lat = data['lat']
    #             e_new.lng = data['lng']
    #             e_new.floor = data['floor']
    #             e_new.region_id = data['regionId']
    #             e_new.region_name = data['regionName']
    #             e_new.piece_id = data['pieceId']
    #             e_new.piece_name = data['pieceName']
    #             e_new.committee_id = data['committeeId']
    #             e_new.committee_name = data['committeeName']
    #             e_new.equipment_type= Equipment_type.objects.filter(type_id=code).first()
    #             e_new.save()
    #             print('新传感器:'+data['sensorId'])

    # #带时间参数测试
    # url = 'http://47.97.210.144/brain2/usersystem/user/login.do'
    # platformId =  1
    # password = 'fire123456'
    # #md加密
    # p1 = hashlib.md5()
    # p1.update(password.encode(encoding='utf-8'))

    # login_params = {
    #     'platformId' : platformId,
    #     'loginName' : 'fire',
    #     'password' : p1.hexdigest(),
    #     }

    # login_response = requests.post(url, params=login_params).json()

    # au = login_response['Data']['extraInfoObject']['Authenticator']

    # date = datetime.date.today()
    # lastday = date - datetime.timedelta(days=1)
    # print(str(date))
    # print(str(lastday))
    # post_params = {
    #         "dataCode": 'DATA_ROKUVNQU',
    #         "startTime": "2017-03-10",
    #         "endTime": str(lastday)
    # }
    # url = 'http://47.97.210.144/brain2/dataResource/getDataList.do'
    # headerdata = {"Content-type": "application/x-www-form-urlencoded","Authenticator": au,}

    # #关闭多余网络连接 
    # s = requests.session()
    # s.keep_alive = False

    # post_response = requests.post(url,data=post_params,headers=headerdata).json()
    # datas = post_response['Data']
    # print(datas)

    #正式环境的测试
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
        'type': 7,
        'Authenticator': token,
    }

    post_response = requests.post(url, params=post_params).json()
    print(post_response)
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
        print(data['sensorPointId'])



    ctx['message'] = message = 'success'
    return render(request,'analysis.html',ctx)

#报警描点接口
@csrf_exempt
def all(request):
    res = {}
    #右边实时报警列表
    res['right'] = right = []
    blocks = Block.objects.all()
    ets = ['烟感','水压']
    ss_t = ['1','8']
    #街道遍历
    for b in range(len(blocks)):
        for ss in ss_t:            
            num = 0
            #传感器遍历                
            gs = Getdata.objects.filter(region_id=blocks[b].street_id,committee_id=blocks[b].village_id).values('sensor_id')

            num += Focus_data.objects.filter(device_id__in=[_['sensor_id'] for _ in gs],device_type=ss).count()
                
            #是否包装
            if num != 0:                   
                r = {}
                r['name'] = blocks[b].street_name
                r['lat'] = blocks[b].street_lat
                r['lng'] = blocks[b].street_lng
                r['num'] = num
                r['type'] = ets[ss_t.index(ss)]
                right.append(r)


    #中间地图描点数据
    res['center'] = center = []
    #实时报警数据
    fs = Focus_data.objects.values_list('device_id',flat=True).distinct()
    #外层点
    blocks = Block.objects.all()
    for b in blocks:
        bj = {}
        bj['name'] = b.street_name + b.village_name   #外层街道小区点 名
        bj['level'] = 3                               #初始化默认为正常
        bj['lat'] = b.street_lat        #外层点坐标
        bj['lng'] = b.street_lng

        #外层标签
        bj['data_type'] = data_type = []              
        #遍历类型
        al = {}
        al['type_name'] = '安装设备共'
        al_num = Getdata.objects.filter(region_id=b.street_id,committee_id=b.village_id)
        al['type_num'] = str(al_num.count()) + '个'
        data_type.append(al)
        for ss in ss_t:
            t = {}
            t['type_name'] = ets[ss_t.index(ss)] + '传感器'
            type_num = al_num.filter(sensor_type=ss).count()
            t['type_num'] = str(type_num) + '个'
            if type_num != 0:
                data_type.append(t)
        #遍历结束

        bj['child'] = child = []        #内层点
        # 内层地址列表
        adds = al_num.values('address').distinct()

        #外层点报警计数器
        at = {}
        at['type_name'] = '区域报警数'
        at_num = 0
        for a in adds: #内层地址遍历
            c_data = {}
            #内层点标签信息
            c_data['area'] = b.area_name
            c_data['village'] = b.village_name
            c_data['street_name'] = b.street_name
            c_data['address'] = a['address']  #地址 
            c_data['level'] = 3 #初始化默认正常
            ai = al_num.filter(address=a['address']).values('lat','lng').first()
            c_data['lat'] = ai['lat']
            c_data['lng'] = ai['lng']
            c_data['focus_list'] = focus_list = []    #内层报警位置详情列表

            #该地址传感器总数
            gs = al_num.filter(address=a['address']).values('sensor_id','address','sensor_type','lat','lng') 
            count = gs.count()
            c_data['count'] = str(count) + '个'

            #标签三个状态字段
            sensor_t = ''
            sta = ''
            sensor_s = ''
            #烟感 水压 遍历
            for ss in ss_t:
                #传感器类型
                st_str = ets[ss_t.index(ss)] + ':正常  '
                #该类型数量
                ggs = gs.filter(sensor_type=ss)
                gg = ggs.count()
                if gg != 0:
                    ss_str =  ets[ss_t.index(ss)] + ':' + str(gg) + '个  '  #类型个数
                    sensor_t += ss_str
                    #内层点报警计数器
                    i = 0
                    for g in ggs:
                        if g['sensor_id'] in fs: #内层报警
                            print('判断语句通过 捕捉到报警传感器')    
                            focus_list.append(g['address'] + '：' + g['sensor_id'])  #报警列表记录到地图标签
                            bj['level'] = 1                         #外层受影响显示为红色
                            st_str = ets[ss_t.index(ss)] + ':报警  ' #内层状态改变 
                            c_data['level'] = 1                     #内层显示红色
                            i += 1                                  #计数器
                        print(i)
                    #外层报警数据器叠加
                    at_num += i
                    #标签状态总结
                    sen_str = ets[ss_t.index(ss)] + ':(报警：' + str(i) + '个，正常' + str(gg-i) +'个)\r'
                    sensor_s += sen_str
                    sta += st_str

            c_data['sensor_status'] = sensor_s
            c_data['sensor_type'] = sensor_t  #传感器类型
            c_data['status'] = sta            #报警类型
            child.append(c_data)
        #外层报警计数包装
        at['type_num'] = str(at_num) + '个'
        data_type.append(at)
        center.append(bj)

    return HttpResponse(json.dumps(res,ensure_ascii=False), content_type='application/json')

    

@csrf_exempt
def notices_list(request):
    ctx = {}
    try:
        pageNo = int(request.POST.get('pageNo', ''))
        pageSize = int(request.POST.get('pageSize',''))
    except ValueError:
        pageNo = 1
        pageSize = 5
    
    startPos = (pageNo - 1) * pageSize
    endPos = startPos + pageSize

    notices = Notice.objects.filter(status=0).order_by('-notice_time')[startPos:endPos]
    if notices:   
        ctx['code'] = 1
        ctx['err'] = ''
        ctx['data'] = data = []
        for notice in notices:
            n = {}
            n['id'] = notice.id
            n['title'] = notice.notice_title
            n['push_time'] = notice.notice_time.strftime('20%y-%m-%d %H:%M')
            n['comment'] = notice.comment
            data.append(n)
        return JsonResponse(ctx,safe=False)
    else:
        ctx['code'] = 0
        ctx['err'] = '暂无公告'
        ctx['data'] = []
        return JsonResponse(ctx,safe=False)

@csrf_exempt
def knowledge_list(request):
    ctx = {}
    try:
        pageNo = int(request.POST.get('pageNo', ''))
        pageSize = int(request.POST.get('pageSize',''))
    except ValueError:
        pageNo = 1
        pageSize = 5

    startPos = (pageNo - 1) * pageSize
    endPos = startPos + pageSize
    
    article = Article.objects.filter(status=0)  # 展示的文章列表
    if article:
        articles = article.filter().order_by('-release_time')[startPos:endPos]  # 按录入倒序
        articles_list = []
        for article in articles:
            a = {}
            a['id'] = article.id
            a['title'] = article.release_title
            a['source'] = article.release_name
            if article.release_icon:
                a['icon'] = 'http://39.104.85.167:8087/media/' + str(article.release_icon)
            else :
                a['icon'] = ''
            a['time'] = article.release_time.strftime('20%y-%m-%d %H:%M')
            articles_list.append(a)
        ctx['code'] = 1
        ctx['err'] = ''
        ctx['data'] = articles_list
        return JsonResponse(ctx,safe=False)
    else:
        ctx['code'] = 0
        ctx['err'] = '暂无显示知识'
        ctx['data'] = []
        return JsonResponse(ctx,safe=False)


@csrf_exempt
def event_list(request):
    ctx = {}
    try:
        pageNo = int(request.POST.get('pageNo', ''))
        pageSize = int(request.POST.get('pageSize',''))
    except ValueError:
        pageNo = 1
        pageSize = 5

    startPos = (pageNo - 1) * pageSize
    endPos = startPos + pageSize
 
    #报警-1   巡检-模拟2   维护-模拟3   保养-模拟4    全部-0

    event_type = request.POST.get('type','') #入参

    ctx['code'] = 1
    ctx['err'] = ''
    ctx['data'] = data = []
    data_out_list = []

    block_list = []

    #事件全部数据 
    events = Event_data.objects.filter(status='True').order_by('-get_time')
    if event_type == '0':
        types = ['1','2','3','4']
        for t in types:
            eventss = events.filter(info_type=t)
            if eventss:
                for event in eventss:
                    e = Getdata.objects.filter(sensor_id=event.device_id).first()
                    if e:
                        b = Block.objects.filter(street_id=e.region_id).first()       #所属区域
                        if b :
                            if b.street_name + t not in block_list:
                                c = {}
                                c['title'] = b.area_name + b.street_name + b.village_name
                                c['push_time'] = event.get_time.strftime('20%y-%m-%d %H:%M')
                                c['type'] = t
                                data_out_list.append(c)
                                block_list.append(b.street_name + t)
        for data_out in data_out_list:
            if data_out_list.index(data_out) >= startPos and data_out_list.index(data_out) < endPos :
                data.append(data_out)
        return JsonResponse(ctx,safe=False)
    if event_type == '1':
        #报警数据
        events = events.filter(info_type='1')
    elif event_type == '2':
        #巡检数据
        events = events.filter(info_type='2') 
    elif event_type == '3':
        #维护数据
        events = events.filter(info_type='3')
    elif event_type == '4':
        #保养数据
        events = events.filter(info_type='4')
    if events:
        for event in events:
            e = Getdata.objects.filter(sensor_id=event.device_id).first()
            if e:
                b = Block.objects.filter(street_id=e.region_id).first()       #所属区域
                if b:
                    if b not in block_list:
                        c = {}
                        c['title'] = b.area_name + b.street_name + b.village_name
                        c['push_time'] = event.get_time.strftime('20%y-%m-%d %H:%M')
                        c['type'] = event.info_type
                        data_out_list.append(c)
                        block_list.append(b)
    for data_out in data_out_list:
        if data_out_list.index(data_out) >= startPos and data_out_list.index(data_out) <endPos :
            data.append(data_out)
    return JsonResponse(ctx,safe=False)

@csrf_exempt
def app_login(request):
    ctx = {}

    phone = request.POST.get('phone','')
    password = request.POST.get('password','')
    user = Member.objects.filter(phone=phone,password=password).first()
    if user:
        if user.status ==0:
            token = uuid.uuid4().hex                  #生成token
            user.token = token 
            user.save()
            ctx['code'] = 1
            ctx['err'] = ''
            ctx['data'] = {}

            ctx['data']['token'] = user.token
            ctx['data']['id'] = user.id
            ctx['data']['phone'] = user.phone
            ctx['data']['name'] = user.name
            if user.icon:
                ctx['data']['icon'] = 'http://39.104.85.167:8087/media/' + str(user.icon)
            else :
                ctx['data']['icon'] = ''
            ctx['data']['area'] = json.loads(user.area)['infoInser']
            
            w_key = Warning_data.objects.all().count()

            ctx['data']['fault_count'] = 90        #故障数量
            ctx['data']['fire_count'] = w_key     #火警数量
            ctx['data']['shield_count'] = 65       #屏蔽数量

            ctx['data']['message_count'] = 0      #未读消息

            return JsonResponse(ctx,safe=False)
        else :
            ctx['code'] = 0
            ctx['err'] = '账号已停用'
            ctx['data'] = {}
            return JsonResponse(ctx,safe=False)
    ctx['code'] = 0
    ctx['err'] = '手机号或密码错误'
    ctx['data'] = {}
    return JsonResponse(ctx,safe=False)

@csrf_exempt
def login_out(request):
    ctx = {}
    user_id = request.POST.get('id','')
    try:
        user = Member.objects.get(id=user_id)
    except :
        pass
    if user:
        user.token = ''
        user.save()
        ctx['code'] = 1
        ctx['err'] = ''
        ctx['data'] = {}
        ctx['data']['message'] = '登出成功'
        return JsonResponse(ctx,safe=False)
    else :
        ctx['code'] = 0 
        ctx['err'] = '无该用户 请确认您的用户ID正确性'
        ctx['data'] = {}
        return  JsonResponse(ctx,safe=False)

@csrf_exempt
def password_change(request):
    ctx = {}
    
    user_id = request.POST.get('id','')
    old_password = request.POST.get('old_password','')
    new_password = request.POST.get('new_password','')
    if new_password:
        user = Member.objects.get(id=user_id)
        if user.password == old_password:
            user.password = new_password
            user.save()
            ctx['code'] = 1
            ctx['err'] = ''
            ctx['data'] = {}
            ctx['data']['message'] = '修改密码成功'
            return JsonResponse(ctx,safe=False)
        ctx['code'] = 0
        ctx['err'] = '旧密码错误'
        ctx['data'] = {}
        return JsonResponse(ctx,safe=False)
    ctx['code'] = 0
    ctx['err'] = '新密码不能为空'
    ctx['data'] = {}
    return JsonResponse(ctx,safe=False)

#修改电话验证码
@csrf_exempt
def chang_get_code(request):
    ctx = {}
    new_phone = request.POST.get('new_phone','')
    user_id = request.POST.get('id','')
    user = Member.objects.get(id=user_id)
    if user:
        code = send_code(new_phone)
        user.code = code
        user.save()
        ctx['code'] = 1
        ctx['err'] = ''
        ctx['data'] = {}
        ctx['data']['message'] = '已发送短信验证码'
        return JsonResponse(ctx,safe=False)
    ctx['code'] = 0
    ctx['err'] = '该用户不存在'
    ctx['data'] = {}
    return JsonResponse(ctx,safe=False)

#修改手机
@csrf_exempt
def phone_change(request):
    ctx = {}
    user_id = request.POST.get('id','')
    new_phone = request.POST.get('new_phone','')
    code = request.POST.get('code','')

    user = Member.objects.get(id=user_id)
    if user.code == code:        
        user.phone = new_phone
        user.save()
        ctx['code'] = 1
        ctx['err'] = ''
        ctx['data'] = {}
        ctx['data']['message'] = '修改绑定电话成功'
        return JsonResponse(ctx,safe=False)
    ctx['code'] = 0
    ctx['err'] = '验证码错误'
    ctx['data'] = {}
    return JsonResponse(ctx,safe=False)

#知识详情
@csrf_exempt
def knowledge_detail(request):
    ctx = {}
    knowledge_id = request.GET.get('id','')
    ctx['article'] = article = Article.objects.get(id=knowledge_id)
    return render(request,'knowledge_detail.html',ctx)

#发送短信
@csrf_exempt
def send_code(number):

    num = random.randint(1000,9999)

    dic = {
        'message':num,
        'code':0
    }

    # request.session['vcode'] = num

    apikey = settings.YUNPIAN_KEY
    text = "亲爱的用户，您的验证码是%d。有效期为24小时，请尽快验证" % num
    sms_host = "sms.yunpian.com"
    port = 443
    sms_send_uri = "/v2/sms/single_send.json"

    params = urllib.parse.urlencode({'apikey': apikey, 'text': text, 'mobile':number})
    headers = {
        "Content-type": "application/x-www-form-urlencoded",
        "Accept": "text/plain"
    }
    conn = http.client.HTTPSConnection(sms_host, port=port, timeout=30)
    conn.request("POST", sms_send_uri, params, headers)
    response = conn.getresponse()
    response_str = response.read()
    conn.close()
    return num

#登录短信验证码
@csrf_exempt
def get_code(request):
    ctx = {}
    phone = request.POST.get('phone','')
    user = Member.objects.filter(phone=phone).first()
    if user:
        code = send_code(phone)
        user.code = code
        user.save()
        ctx['code'] = 1
        ctx['err'] = ''
        ctx['data'] = {}
        ctx['data']['message'] = '已发送短信验证码'
        return JsonResponse(ctx,safe=False)
    ctx['code'] = 0
    ctx['err'] = '该用户不存在'
    ctx['data'] = {}
    return JsonResponse(ctx,safe=False)

#手机登录
@csrf_exempt
def login_by_phone(request):
    ctx = {}

    phone = request.POST.get('phone','')
    code = request.POST.get('code','')
    user = Member.objects.filter(phone=phone,code=code).first()
    if user:
        if user.status ==0:
            token = uuid.uuid4().hex                  #生成token
            user.token = token 
            user.save()
            ctx['code'] = 1
            ctx['err'] = ''
            ctx['data'] = {}

            ctx['data']['token'] = user.token
            ctx['data']['id'] = user.id
            ctx['data']['phone'] = user.phone
            ctx['data']['name'] = user.name
            if user.icon:
                ctx['data']['icon'] = 'http://39.104.85.167:8087/media/' + str(user.icon)
            else :
                ctx['data']['icon'] = ''
            ctx['data']['area'] = json.loads(user.area)['infoInser']

            w_key = Warning_data.objects.all().count()

            ctx['data']['fault_count'] = 90        #故障数量
            ctx['data']['fire_count'] = w_key     #火警数量
            ctx['data']['shield_count'] = 65       #屏蔽数量

            ctx['data']['message_count'] = 0      #未读消息

            return JsonResponse(ctx,safe=False)
        else :
            ctx['code'] = 0
            ctx['err'] = '账号已停用'
            ctx['data'] = {}
            return JsonResponse(ctx,safe=False)
    ctx['code'] = 0
    ctx['err'] = '验证码错误'
    ctx['data'] = {}
    return JsonResponse(ctx,safe=False)


#我的资料
@csrf_exempt
def user(request):
    ctx = {}
    user_id = request.POST.get('id','')
    user = Member.objects.get(id=user_id)
    if user:
        if user.status ==0:
            ctx['code'] = 1
            ctx['err'] = ''
            ctx['data'] = {}

            ctx['data']['id'] = user_id
            ctx['data']['phone'] = user.phone
            ctx['data']['name'] = user.name
            if user.icon:
                ctx['data']['icon'] = 'http://39.104.85.167:8087/media/' + str(user.icon)
            else :
                ctx['data']['icon'] = ''
            ctx['data']['area'] = json.loads(user.area)['infoInser']
            return JsonResponse(ctx,safe=False)
        else :
            ctx['code'] = 0
            ctx['err'] = '账号已停用'
            ctx['data'] = {}
            return JsonResponse(ctx,safe=False)
    ctx['code'] = 0
    ctx['err'] = '无该用户信息'
    ctx['data'] = {}
    return JsonResponse(ctx,safe=False)

#修改资料
@csrf_exempt
def user_change(request):
    ctx = {}
    user_id = request.POST.get('id','')
    new_name = request.POST.get('new_name','')
    new_icon_base64 = request.POST.get('new_icon_base64','')

    user = Member.objects.get(id=user_id)
    if user:
        if user.status ==0:
            user.name = new_name
            if new_icon_base64:       #头像处理
                now = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
                icon_name = user.name + now     #图片名字：用户名+时间戳
                
                icon_type = new_icon_base64[0:new_icon_base64.index(';')][11:]  #图片格式后缀
                icon_root = settings.MEDIA_ROOT + '/member/' + icon_name + '.' + icon_type  #写入图片路径

                # icon_root = settings.MEDIA_ROOT + '/member/' + icon_name +'.jpg'  #写入图片路径

                image_base64 = new_icon_base64[new_icon_base64.index(',')+1:]   #逗号以后是base64
                imgdata = base64.b64decode(image_base64)  
                file = open(icon_root,'wb')  
                file.write(imgdata)  
                file.close() 
                user.icon = 'member/' + icon_name + '.' + icon_type
            user.save()

            ctx['code'] = 1
            ctx['err'] = ''
            ctx['data'] = {}
            ctx['data']['token'] = user.token
            ctx['data']['id'] = user.id
            ctx['data']['phone'] = user.phone
            ctx['data']['name'] = user.name
            if user.icon:
                ctx['data']['icon'] = 'http://39.104.85.167:8087/media/' + str(user.icon)
            else :
                ctx['data']['icon'] = ''
            ctx['data']['area'] = json.loads(user.area)['infoInser']
            return JsonResponse(ctx,safe=False)
        else :
            ctx['code'] = 0
            ctx['err'] = '账号已停用'
            ctx['data'] = {}
            return JsonResponse(ctx,safe=False)
    ctx['code'] = 0
    ctx['err'] = '无该用户信息'
    ctx['data'] = {}
    return JsonResponse(ctx,safe=False)


@csrf_exempt
def nervous_list(request):
    ctx = {}

    ctx['code'] = 1
    ctx['err'] = ''
    ctx['data'] = data =[]

    fds = Event_data.objects.filter(info_type='1',status='True').order_by('-get_time') #历史报警数据
    if fds:
        for fd in fds:
            e = Getdata.objects.filter(sensor_id=fd.device_id).first()       #传感器
            if e:
                b = Block.objects.filter(street_id=e.region_id).first()       #所属区域
                if b:
                    c = {}
                    c['address'] = b.area_name + b.street_name + b.village_name + e.address 
                    c['event_id'] = e.sensor_point_id
                    c['time'] = fd.get_time.strftime('20%y-%m-%d %H:%M')
                    c['type'] = fd.info_type
                    data.append(c)

    return JsonResponse(ctx,safe=False)


@csrf_exempt
def check_fire(request):
    ctx = {}
    status = request.POST.get('status','')
    event_id = request.POST.get('event_id','')
    e = Getdata.objects.get(sensor_point_id=event_id)
    w = Warning_data.objects.filter(device_id=e.sensor_id,status='True').first()
    if w:
        w.status = status
        w.save()
        ctx['code'] = 1
        ctx['err'] = ''
        ctx['data'] = {}
        ctx['data']['message'] = '状态修改成功'
        return JsonResponse(ctx,safe=False)
    ctx['code'] = 0
    ctx['err'] = '该数据已不是待处理状态'
    ctx['data'] = {}
    return JsonResponse(ctx,safe=False)


@csrf_exempt
def message_list(request):
    ctx = {}
    user_id = request.POST.get('id','')
    message_type = request.POST.get('message_type','')

    try:
        pageNo = int(request.POST.get('pageNo', ''))
        pageSize = int(request.POST.get('pageSize',''))
    except ValueError:
        pageNo = 1
        pageSize = 5

    startPos = (pageNo - 1) * pageSize
    endPos = startPos + pageSize

    ctx['code'] = 1
    ctx['err'] = ''
    ctx['data'] = data = []
    data_out_list = []
    names = ['火警消息','系统消息','巡检消息','监控消息','其他消息']
    
    fds = Event_data.objects.filter(status='True').order_by('-get_time') 
    if message_type == '0':
        c = {}
        c['content'] = 'APP3.0版本发布成功，欢迎来APP store更新'
        now = datetime.datetime.now().strftime('20%y-%m-%d %H:%M')
        c['time'] = now
        c['type'] = '2'
        c['name'] = '系统消息'
        data_out_list.append(c)

        types = ['1','3','4','5']
        for t in types:
            fdss = fds.filter(info_type=t)
            if fdss:
                for fd in fdss:
                    e = Getdata.objects.filter(sensor_id=fd.device_id).first()       #传感器
                    if e:
                        b = Block.objects.filter(street_id=e.region_id).first()       #所属区域
                        if b:
                            c = {}
                            c['content'] = b.area_name + b.street_name + b.village_name + e.address 
                            c['event_id'] = e.sensor_point_id
                            c['time'] = fd.get_time.strftime('20%y-%m-%d %H:%M')
                            c['type'] = fd.info_type
                            c['name'] = names[int(t)-1]
                            data_out_list.append(c)
        for data_out in data_out_list:
            if data_out_list.index(data_out) >= startPos and data_out_list.index(data_out) <endPos :
                data.append(data_out)
        return JsonResponse(ctx,safe=False)
    if message_type == '2':
        c = {}
        c['content'] = 'APP3.0版本发布成功，欢迎来APP store更新'
        now = datetime.datetime.now().strftime('20%m.%d %H:%M')
        c['time'] = now
        c['type'] = '2'
        c['name'] = '系统消息'
        data_out_list.append(c)
    else:
        if message_type == '1':
            fds = fds.filter(info_type='1')
        elif message_type == '3':
           fds = fds.filter(info_type='3')
        elif message_type == '4':
            fds = fds.filter(info_type='4')
        elif message_type == '5':
            fds = fds.filter(info_type='5')
        if fds:
            for fd in fds:
                e = Getdata.objects.filter(sensor_id=fd.device_id).first()       #传感器
                if e:
                    b = Block.objects.filter(street_id=e.region_id).first()       #所属区域
                    c = {}
                    c['content'] = b.area_name + b.street_name + b.village_name + e.address 
                    c['event_id'] = e.sensor_point_id
                    c['time'] = fd.get_time.strftime('20%y-%m-%d %H:%M')
                    c['type'] = message_type
                    c['name'] = names[int(message_type)-1]
                    data_out_list.append(c)
    for data_out in data_out_list:
        if data_out_list.index(data_out) >= startPos and data_out_list.index(data_out) <endPos :
            data.append(data_out)
    return JsonResponse(ctx,safe=False)

#意见反馈
@csrf_exempt
def suggestion(request):
    ctx = {}

    user_id = request.POST.get('id','')
    suggestion = request.POST.get('suggestion','')

    image_base64 = request.POST.get('image_base64','')

    if suggestion:
        user = Member.objects.get(id=user_id)

        app_suggestion = App_suggestion()
        app_suggestion.suggestion = suggestion
        app_suggestion.suggest_user_name = user.name
        app_suggestion.suggest_user_phone = user.phone
        #图片处理
        if image_base64:          
            now = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
            iamge_name = user.name + now     #图片名字：用户名+时间戳

            # image_str = request.POST.get('image_str','')
            # image_type = image_str[0:image_str.index(';')][11:]
            # print(image_type) 
            image_type = image_base64[0:image_base64.index(';')][11:]  #图片格式后缀

            image_root = settings.MEDIA_ROOT + '/suggestion/' + iamge_name + '.' + image_type  #写入图片路径

            image_base64 = image_base64[image_base64.index(',')+1:] #逗号以后是base64
            imgdata = base64.b64decode(image_base64)  
            file = open(image_root,'wb')  
            file.write(imgdata)  
            file.close() 

            #转换为外链接保存
            image_url = 'http://39.104.85.167:8087' + settings.MEDIA_URL + 'suggestion/' + iamge_name + '.' + image_type 
            image = 'suggestion/' + iamge_name +'.jpeg' #ImageField字段存路径
            app_suggestion.image_url = image_url
            app_suggestion.image = image
        app_suggestion.save()

        ctx['code'] = 1
        ctx['err'] = ''
        ctx['data'] = {}
        ctx['data']['message'] = '意见反馈提交成功'
        return JsonResponse(ctx,safe=False)

    ctx['code'] = 0
    ctx['err'] = '提交内容不能为空'
    ctx['data'] = {}
    return JsonResponse(ctx,safe=False)

@csrf_exempt
def event_type(request):
    ctx = {}
 
    #报警-1   巡检-模拟2   维护-模拟3   保养-模拟4    全部-0

    # event_type = request.POST.get('type','') #入参

    ctx['code'] = 1
    ctx['err'] = ''
    ctx['data'] = data = []

    #事件全部数据 
    a_events = Event_data.objects.filter(status='True').order_by('-get_time')
    event_types = ['1','2','3','4']
    names = ['报警','巡检','维护','保养']
    for event_type in event_types:
        data_out_list = []
        block_list = []
        if event_type == '1':
            #报警数据
            events = a_events.filter(info_type='1')
        elif event_type == '2':
            #巡检数据
            events = a_events.filter(info_type='2') 
        elif event_type == '3':
            #维护数据
            events = a_events.filter(info_type='3')
        elif event_type == '4':
            #保养数据
            events = a_events.filter(info_type='4')
        if events:
            for event in events:
                e = Getdata.objects.filter(sensor_id=event.device_id).first()
                if e:
                    b = Block.objects.filter(street_id=e.region_id).first()       #所属区域
                    if b:
                        if b not in block_list:
                            c = {}
                            c['title'] = b.area_name + b.street_name + b.village_name
                            c['push_time'] = event.get_time.strftime('20%y-%m-%d %H:%M')
                            c['type'] = event.info_type
                            data_out_list.append(c)
                            block_list.append(b)
        c = {}
        c['type'] = event_type
        c['count'] = len(data_out_list)
        c['name'] =  names[int(event_type)-1]
        data.append(c)
    return JsonResponse(ctx,safe=False)

@csrf_exempt
def event_detail(request):
    ctx = {}
    event_type = request.POST.get('type','')
    event_title = request.POST.get('title','')
    nervous_list = []
    normal_list = []
    #事件全部数据 
    events = Event_data.objects.filter(info_type=event_type).order_by('-get_time')
    if events:
        for event in events:
            e = Getdata.objects.filter(sensor_id=event.device_id).first()
            if e:
                b = Block.objects.filter(street_id=e.region_id).first()       #所属区域
                if b:
                    if event_title == b.area_name + b.street_name + b.village_name: #该类数据报警属于此区域事件
                        c = {}
                        c['title'] = e.address               #详细地址
                        c['event_id'] = e.sensor_point_id
                        c['push_time'] = event.get_time.strftime('20%y-%m-%d %H:%M')
                        c['type'] = event.info_type
                        if event.status == 'True':       #按状态分开
                            nervous_list.append(c)
                        else:
                            normal_list.append(c)
    ctx['code'] = 1
    ctx['err'] = ''
    ctx['data'] = {}

    ctx['data']['nervous_list'] = nervous_list
    ctx['data']['normal_list'] = normal_list
    return JsonResponse(ctx,safe=False)

@csrf_exempt
def auto_login(request):
    ctx = {}

    token = request.POST.get('token','')
    if token:
        user = Member.objects.filter(token=token).first()
        if user:
            if user.status ==0:
                ctx['code'] = 1
                ctx['err'] = ''
                ctx['data'] = {}

                ctx['data']['token'] = user.token
                ctx['data']['id'] = user.id
                ctx['data']['phone'] = user.phone
                ctx['data']['name'] = user.name
                if user.icon:
                    ctx['data']['icon'] = 'http://39.104.85.167:8087/media/' + str(user.icon)
                else :
                    ctx['data']['icon'] = ''
                ctx['data']['area'] = json.loads(user.area)['infoInser']
                
                w_key = Warning_data.objects.all().count()

                ctx['data']['fault_count'] = 90        #故障数量
                ctx['data']['fire_count'] = w_key     #火警数量
                ctx['data']['shield_count'] = 65       #屏蔽数量

                ctx['data']['message_count'] = 0      #未读消息

                return JsonResponse(ctx,safe=False)
            else :
                ctx['code'] = 0
                ctx['err'] = '账号已停用'
                ctx['data'] = {}
                return JsonResponse(ctx,safe=False)
        ctx['code'] = 0
        ctx['err'] = 'token匹配不上 请手动登录'
        ctx['data'] = {}
        return JsonResponse(ctx,safe=False)
    ctx['code'] = 0
    ctx['err'] = 'token不能为空'
    ctx['data'] = {}
    return JsonResponse(ctx,safe=False)


# def getdatav2(request):



@csrf_exempt
def pushv2(request):
    if request.method != 'POST':
        return JsonResponse({ 'success': False, 'code': -1, 'msg': '只支持POST' }, status=405)

    raw = json.loads(request.body.decode('utf-8'))
    json_root = settings.MEDIA_ROOT + '/json/' + '%d.json' % time.time()  #json保存路径

    with open(json_root, 'w') as f:
        f.write(json.dumps(raw, indent=4))

    #按类型落地

    #烟雾报警器
    if raw['device_type'] == 'DATA_ROKUVNQU': 
        #原数据落地
        data = Smoke_data_v2()
        data_day = Smoke_data_day_v2()
        data_week = Smoke_data_week_v2()
        data_month = Smoke_data_month_v2()
        data.device_id = data_day.device_id = data_week.device_id = data_month.device_id = raw['data']['device_id']
        data.software_version = data_day.software_version = data_week.software_version = data_month.software_version = raw['data']['software_version']
        data.protocol_version = data_day.protocol_version = data_week.protocol_version = data_month.protocol_version = raw['data']['protocol_version']
        data.device_type = data_day.device_type = data_week.device_type = data_month.device_type = raw['data']['device_type']
        data.info_type = data_day.info_type = data_week.info_type = data_month.info_type = raw['data']['info_type']
        data.battery_voltage = data_day.battery_voltage = data_week.battery_voltage = data_month.battery_voltage = raw['data']['battery_voltage']
        data.smoke_concentration = data_day.smoke_concentration = data_week.smoke_concentration = data_month.smoke_concentration = raw['data']['smoke_concentration']
        data.received_time = data_day.received_time = data_week.received_time = data_month.received_time = raw['data']['received_time']
        data.save()
        data_day.save()
        data_week.save()
        data_month.save()
        print('烟雾报警器log数据接收成功')
    #门磁传感器
    elif raw['device_type'] == 'DATA_YNUXZLMW':  
        #原数据落地
        data = Door_data_v2()
        data_day = Door_data_day_v2()
        data_week = Door_data_week_v2()
        data_month = Door_data_month_v2()
        data.device_id = data_day.device_id = data_week.device_id = data_month.device_id = raw['data']['device_id']
        data.status = data_day.status = data_week.status = data_month.status = raw['data']['status']
        data.battery = data_day.battery = data_week.battery = data_month.battery = raw['data']['battery']
        data.received_time = data_day.received_time = data_week.received_time = data_month.received_time = raw['data']['received_time']
        data.save()
        data_day.save()
        data_week.save()
        data_month.save()
        print('门磁传感器log数据接收成功')

    #视频监控摄像头 无log信息???
    elif raw['device_type'] == 'DATA_TYLCDREW':  
        #原数据落地
        print('视频监控摄像头log数据暂无定义')

    #垃圾满溢传感器
    elif raw['device_type'] == 'DATA_QAYHBUCY':  
        #原数据落地
        data = Dirty_data_v2()
        data.device_id = raw['data']['device_id']
        data.temperature =  raw['data']['temperature']
        data.bat = raw['data']['bat']
        data.height =  raw['data']['height']
        data.lng = raw['data']['lng']
        data.lat = raw['data']['lat']
        data.height_status = raw['data']['height_status']        
        data.received_time = raw['data']['received_time']
        data.save()
        print('垃圾满溢传感器log数据接收成功')

    #地磁传感器
    elif raw['device_type'] == 'DATA_ZLPQXEOV': 
        #原数据落地
        data = Ground_data_v2()
        data.device_id = raw['data']['device_id']
        data.status =  raw['data']['status']
        data.start_symbol = raw['data']['start_symbol']
        data.region_number =  raw['data']['region_number']
        data.parking_log_id = raw['data']['parking_log_id']
        data.serial_number = raw['data']['serial_number']
        data.signal_strength = raw['data']['signal_strength']
        data.battery = raw['data']['battery']
        data.received_time = raw['data']['received_time']
        data.save()
        print('地磁传感器log数据接收成功')

    #水压传感器
    elif raw['device_type'] == 'DATA_CRPUEZTF':  
        #原数据落地
        data = Water_data_v2()
        data_day = Water_data_day_v2()
        data_week = Water_data_week_v2()
        data_month = Water_data_month_v2()
        data.device_id = data_day.device_id = data_week.device_id = data_month.device_id = raw['data']['device_id']
        data.STATETYPE = data_day.STATETYPE = data_week.STATETYPE = data_month.STATETYPE = raw['data']['STATETYPE']
        data.STATENAME = data_day.STATENAME = data_week.STATENAME = data_month.STATENAME = raw['data']['STATENAME']
        data.DSNUM = data_day.DSNUM = data_week.DSNUM = data_month.DSNUM = raw['data']['DSNUM']
        data.HYDRANTTYPE = data_day.HYDRANTTYPE = data_week.HYDRANTTYPE = data_month.HYDRANTTYPE = raw['data']['HYDRANTTYPE']
        data.WATERTYPE = data_day.WATERTYPE = data_week.WATERTYPE = data_month.WATERTYPE = raw['data']['WATERTYPE']
        data.RSSI = data_day.RSSI = data_week.RSSI = data_month.RSSI = raw['data']['RSSI']
        data.lon = data_day.lon = data_week.lon = data_month.lon = raw['data']['lon']
        data.lat = data_day.lat = data_week.lat = data_month.lat = raw['data']['lat']
        data.PRESSURE = data_day.PRESSURE = data_week.PRESSURE = data_month.PRESSURE = raw['data']['PRESSURE']
        data.DUMP_ENERGY = data_day.DUMP_ENERGY = data_week.DUMP_ENERGY = data_month.DUMP_ENERGY = raw['data']['DUMP_ENERGY']
        data.received_time = data_day.received_time = data_week.received_time = data_month.received_time = raw['data']['received_time']
        data.save()
        data_day.save()
        data_week.save()
        data_month.save()
        print('水压传感器log数据接收成功')

    #红外周界
    elif raw['device_type'] == 'DATA_OCEWLFLS':  
        #原数据落地
        data = Infrared_data_v2()
        data.device_id = raw['data']['device_id']
        data.status = raw['data']['status']
        data.received_time = raw['data']['received_time']
        data.save()
        print('红外周界log数据接收成功')

    #电弧灭弧保护器
    elif raw['device_type'] == 'DATA_WLBZWFBF':  
        #原数据落地
        data = Arc_data_v2()
        data.device_id = raw['data']['device_id']
        data.src = raw['data']['src']
        data.status = raw['data']['status']
        data.msgType = raw['data']['msgType']
        data.devType = raw['data']['devType']
        data.ld = raw['data']['ld']
        data.ia = raw['data']['ia']
        data.ua = raw['data']['ua']
        data.ta = raw['data']['ta']
        data.tb = raw['data']['tb']
        data.received_time = raw['data']['received_time']
        data.save()
        print('电弧灭弧保护器log数据接收成功')

    #人脸识别
    elif raw['device_type'] == 'DATA_HKPSQWCX': 
        #原数据落地
        data = Recognition_data_v2()
        data.device_id = raw['data']['device_id']
        data.sex = raw['data']['sex']
        data.age = raw['data']['age']
        data.glass = raw['data']['glass']
        data.emotion = raw['data']['emotion']
        data.personName = raw['data']['personName']
        data.imageWidth = raw['data']['imageWidth']
        data.imageHeight = raw['data']['imageHeight']
        data.fileLength = raw['data']['fileLength']
        data.rawInBase64 = raw['data']['rawInBase64']
        data.received_time = raw['data']['received_time']
        data.save()
        print('人脸识别log数据接收成功')

    #充电桩
    elif raw['device_type'] == 'DATA_EYBSLXCI':  
        #原数据落地
        data = Charge_data_v2()
        data.device_id = raw['data']['device_id']
        data.pile_type = raw['data']['type'] #type为关键字
        data.plugNumber = raw['data']['plugNumber']
        data.unitPrice = raw['data']['unitPrice']
        data.minPrice = raw['data']['minPrice']
        data.attachPrice = raw['data']['attachPrice']
        data.overdraft = raw['data']['overdraft']
        data.factor = raw['data']['factor']
        data.maxPlugPower = raw['data']['maxPlugPower']
        data.maxDevicePower = raw['data']['maxDevicePower']
        data.area = raw['data']['area']
        data.location = raw['data']['location']
        data.inusePlugNumber = raw['data']['inusePlugNumber']
        data.isOnline = raw['data']['isOnline']
        data.plugs1 = raw['data']['plugs1']
        data.plugs2 = raw['data']['plugs2']
        data.plugs3 = raw['data']['plugs3']
        data.plugs4 = raw['data']['plugs4']
        data.plugs5 = raw['data']['plugs5']
        data.plugs6 = raw['data']['plugs6']
        data.plugs7 = raw['data']['plugs7']
        data.plugs8 = raw['data']['plugs8']
        data.plugs9 = raw['data']['plugs9']
        data.plugs10 = raw['data']['plugs10']
        data.received_time = raw['data']['received_time']
        data.save()
        print('充电桩log数据接收成功')

    #电梯传感器
    elif raw['device_type'] == 'DATA_KALNNEVQ':  
        #原数据落地
        data = Lift_data_v2()
        data.device_id = raw['data']['device_id']
        data.lift_type = raw['data']['lift_type']
        data.lift_len = raw['data']['lift_len']
        data.address = raw['data']['address']
        data.cmd = raw['data']['cmd']
        data.lift_data = raw['data']['data']
        data.down = raw['data']['down']
        data.up = raw['data']['up']
        data.current_level = raw['data']['current_level']
        data.highest = raw['data']['highest']
        data.received_time = raw['data']['received_time']
        data.save()
        print('电梯传感器log数据接收成功')

    #人体红外感应
    elif raw['device_type'] == 'DATA_AEHBABKR':  
        #原数据落地
        data = Human_data_v2()
        data.device_id = raw['data']['device_id']
        data.bat = raw['data']['bat']
        data.temperature = raw['data']['temperature']
        data.illuminance = raw['data']['illuminance']
        data.occupy = raw['data']['occupy']
        data.received_time = raw['data']['received_time']
        data.save()
        print('人体红外感应log数据接收成功')

    #PH传感器
    elif raw['device_type'] == 'DATA_KQDYAAUK':  
        #原数据落地
        data = PH_data_v2()
        data.device_id = raw['data']['device_id']
        data.num = raw['data']['num']
        data.ph_len = raw['data']['ph_len']
        data.bat = raw['data']['bat']
        data.ph = raw['data']['ph']
        data.temperature = raw['data']['temperature']
        data.t_style = raw['data']['t_style']
        data.received_time = raw['data']['received_time']
        data.save()
        print('PH传感器log数据接收成功')

    #溶解氧传感器
    elif raw['device_type'] == 'DATA_OEVIPMPA':  
        #原数据落地
        data = Oxygen_data_v2()
        data.device_id = raw['data']['device_id']
        data.num = raw['data']['num']
        data.ox_len = raw['data']['len']
        data.bat = raw['data']['bat']
        data.doxy = raw['data']['doxy']
        data.doxys = raw['data']['doxys']
        data.temperature = raw['data']['temperature']
        data.t_style = raw['data']['t_style']
        data.received_time = raw['data']['received_time']
        data.save()
        print('溶解氧传感器log数据接收成功')

    else:
        print('device_type为'+raw['device_type']+'! 不能匹配的未知log信息')

    #创建测试环境 项目存档 2018.6.26 17.22 
    return JsonResponse({ 'success': True })

@csrf_exempt
def web_login(request):
    ctx = {}

    phone = request.POST.get('phone','')
    password = request.POST.get('password','')
    user = Member.objects.filter(phone=phone).first()
    if user:
        if user.status == 0 :
            if user.password == password:
                token = uuid.uuid4().hex                  #生成token
                user.token = token

                print(user.area)
                a = json.loads(user.area)['infoInser']
                print(a)
                print(a['普陀区'])

                #右边街道权限
                keys = []

                #地图描点权限
                power = []
                for key in a['普陀区']:
                    keys.append(key)
                    vs = a['普陀区'][key]
                    for x in vs:
                        power.append(key+x)
                ctx['keys'] = keys
                if len(power) == 1:
                    ctx['power'] = power[0]   #str
                else: #防止物业管理多个小区情况 
                    ctx['power'] = power      #list
                ctx['message'] = message = '登陆成功'
                ctx['user'] = user 
                return render(request,'index.html',ctx)
            else:
                ctx['err'] = err = '密码不正确'
                return render(request,'web_login.html',ctx)
        else :
            ctx['err'] = err = '该用户已被停用'
            return render(request,'web_login.html',ctx)
    ctx['err'] = err ='该用户不存在'
    return render(request,'web_login.html',ctx)


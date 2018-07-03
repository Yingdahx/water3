from django.contrib import admin


from .models import *

admin.site.site_title = admin.site.site_header = 'water'


class ArticleAdmin(admin.ModelAdmin):

    list_display = ('release_title', 'release_name',
                    'release_time', 'release_update', 'comment', 'status')

    class Media:
        # 在管理后台的HTML文件中加入js文件，每一个路径都会追加STATIC_URL/
        js = (
            'js/kindeditor/kindeditor-all.js',
            'js/kindeditor/lang/zh_CN.js',
            'js/kindeditor/config.js',
        )


class NoticeAdmin(admin.ModelAdmin):

    list_display = ('notice_title', 'comment', 'notice_time', 'status')

    class Media:
        # 在管理后台的HTML文件中加入js文件，每一个路径都会追加STATIC_URL/
        js = (
            'js/kindeditor/kindeditor-all.js',
            'js/kindeditor/lang/zh_CN.js',
            'js/kindeditor/config.js',
        )


class BlockAdmin(admin.ModelAdmin):
    list_display = ('area_id', 'area_name', 'street_id',
                    'street_name', 'village_id', 'village_name','street_lat','street_lng')  # list

    list_display_links = ('area_id', 'street_id','village_id')

    fieldsets = (
        ['Main',{
            'fields':('area_id', 'area_name', 'street_id',
                    'street_name', 'village_id', 'village_name','street_lat','street_lng'),#add后显示属性
        }],

    )


class MemberAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone','password','icon')
    change_form_template = 'block.html'
    add_form_template = 'blockadd.html'
   

class Equipment_typeAdmin(admin.ModelAdmin):
    # 列表显示字段
    list_display = ('name', 'type_id', 'build_time',
                    'updata_time', 'count')  # list

    # 进入编辑字段
    list_display_links = ('name', 'type_id')

    # 筛选器
    list_filter = ('name','type_id')  # 过滤器

    search_fields = ('name','type_id')  # 搜索字段 上方搜索字段

    # inlines = [TagInline]  # Inline #内联显示

    fieldsets = (
        ['Main', {  # add可控字段
            # add后显示属性
            'fields': ('name', 'type_id', 'imageUrl', 'height','count'),
        }],

    )


class DataAdmin(admin.ModelAdmin):
    # 列表显示字段
    list_display = ('device_id', 'device_type',
                    'info_type', 'get_time')  # list

    # 筛选器
    list_filter = ('device_type', 'info_type', 'get_time')  # 过滤器

    int_hierarchy = 'info_type'    # 详细分层筛选　右边分类字段
    search_fields = ('device_id',)  # 搜索字段 上方搜索字段

    # inlines = [TagInline]  # Inline #内联显示

    fieldsets = (
        ['Main', {  # add可控字段
            'fields': ('device_type', 'state', 'battery_voltage', 'device_id', 'received_time', 'info_type', 'protocol_version', 'software_version', 'smoke_concentration'),  # add后显示属性
        }],

    )

class Day_dataAdmin(admin.ModelAdmin):
    # 列表显示字段
    list_display = ('device_id', 'device_type',
                    'info_type', 'get_time')  # list

    # 筛选器
    list_filter = ('device_type', 'info_type', 'get_time')  # 过滤器

    int_hierarchy = 'info_type'    # 详细分层筛选　右边分类字段
    search_fields = ('device_id',)  # 搜索字段 上方搜索字段

    # inlines = [TagInline]  # Inline #内联显示

    fieldsets = (
        ['Main', {  # add可控字段
            'fields': ('device_type', 'state', 'battery_voltage', 'device_id', 'received_time', 'info_type', 'protocol_version', 'software_version', 'smoke_concentration'),  # add后显示属性
        }],

    )

class Week_dataAdmin(admin.ModelAdmin):
    # 列表显示字段
    list_display = ('device_id', 'device_type',
                    'info_type', 'get_time')  # list

    # 筛选器
    list_filter = ('device_type', 'info_type', 'get_time')  # 过滤器

    int_hierarchy = 'info_type'    # 详细分层筛选　右边分类字段
    search_fields = ('device_id',)  # 搜索字段 上方搜索字段

    # inlines = [TagInline]  # Inline #内联显示

    fieldsets = (
        ['Main', {  # add可控字段
            'fields': ('device_type', 'state', 'battery_voltage', 'device_id', 'received_time', 'info_type', 'protocol_version', 'software_version', 'smoke_concentration'),  # add后显示属性
        }],

    )

class Month_dataAdmin(admin.ModelAdmin):
    # 列表显示字段
    list_display = ('device_id', 'device_type',
                    'info_type', 'get_time')  # list

    # 筛选器
    list_filter = ('device_type', 'info_type', 'get_time')  # 过滤器

    int_hierarchy = 'info_type'    # 详细分层筛选　右边分类字段
    search_fields = ('device_id',)  # 搜索字段 上方搜索字段

    # inlines = [TagInline]  # Inline #内联显示

    fieldsets = (
        ['Main', {  # add可控字段
            'fields': ('device_type', 'state', 'battery_voltage', 'device_id', 'received_time', 'info_type', 'protocol_version', 'software_version', 'smoke_concentration'),  # add后显示属性
        }],

    )

class Focus_dataAdmin(admin.ModelAdmin):
    # 列表显示字段
    list_display = ('device_id', 'device_type',
                    'info_type', 'get_time')  # list

    # 筛选器
    list_filter = ('device_type', 'info_type', 'get_time')  # 过滤器

    int_hierarchy = 'info_type'    # 详细分层筛选　右边分类字段
    search_fields = ('device_id',)  # 搜索字段 上方搜索字段

    # inlines = [TagInline]  # Inline #内联显示

    fieldsets = (
        ['Main', {  # add可控字段
            'fields': ('device_type', 'state', 'battery_voltage', 'device_id', 'received_time', 'info_type', 'protocol_version', 'software_version', 'smoke_concentration'),  # add后显示属性
        }],

    )

class Event_dataAdmin(admin.ModelAdmin):
    # 列表显示字段
    list_display = ('device_id', 'device_type',
                    'info_type', 'get_time','status')  # list

    # 筛选器
    list_filter = ('device_type', 'info_type', 'get_time')  # 过滤器

    int_hierarchy = 'info_type'    # 详细分层筛选　右边分类字段
    search_fields = ('device_id','status')  # 搜索字段 上方搜索字段

    # inlines = [TagInline]  # Inline #内联显示

    fieldsets = (
        ['Main', {  # add可控字段
            'fields': ('device_type', 'state', 'battery_voltage', 'device_id', 'received_time', 'info_type', 'protocol_version', 'software_version', 'smoke_concentration','status'),  # add后显示属性
        }],

    )



class GetdataAdmin(admin.ModelAdmin):
    # 列表显示字段
    list_display = ('sensor_point_id', 'sensor_id', 'sensor_name', 'sensor_type',
                    'address', 'piece_id', 'region_id', 'committee_id', 'committee_name')  # list

    # 筛选器
    list_filter = ('sensor_type', 'piece_id',
                   'region_id', 'committee_id')  # 过滤器

    # int_hierarchy = 'info_type'    # 详细分层筛选　右边分类字段
    search_fields = ('sensor_point_id', 'sensor_id',
                     'sensor_type', 'address', 'piece_id', 'region_id', 'committee_id', 'committee_name')  # 搜索字段 上方搜索字段


class EquipmentAdmin(admin.ModelAdmin):
    # 列表显示字段
    list_display = ('sensor_id', 'sensor_name', 'address', 'lat','lng','floor','equipment_type','status','change_time')  # list

    # # 进入编辑字段
    # list_display_links = ('name', 'type_id')

    # 筛选器
    list_filter = ('equipment_type','status','region_name','piece_name','committee_name')  # 过滤器

    # int_hierarchy = 'status'    # 详细分层筛选　右边分类字段
    search_fields = ('sensor_id','address','floor','equipment_type','status')  # 搜索字段 上方搜索字段

    # inlines = [TagInline]  # Inline #内联显示

class App_suggestionAdmin(admin.ModelAdmin):
    # 列表显示字段
    list_display = ('add_time','suggestion','suggest_user_name','suggest_user_phone')  # list

    # # 进入编辑字段
    # list_display_links = ('name', 'type_id')

    # 筛选器
    list_filter = ('suggest_user_name','suggest_user_phone','add_time')  # 过滤器

    # int_hierarchy = 'status'    # 详细分层筛选　右边分类字段
    search_fields = ('suggest_user_name', 'suggest_user_phone','add_time')  # 搜索字段 上方搜索字段

    # inlines = [TagInline]  # Inline #内联显示


class Getdata_v2Admin(admin.ModelAdmin):
    # 列表显示字段
    list_display = ('device_type', 'sensor_id', 'sensor_name', 
                    'address', 'piece_id', 'region_id', 'committee_id', 'floor')  # list

    # 筛选器
    list_filter = ('device_type', 'piece_id',
                   'region_id', 'committee_id')  # 过滤器

    # int_hierarchy = 'info_type'    # 详细分层筛选　右边分类字段
    search_fields = ('device_type', 'sensor_id', 'address', 
                    'piece_id', 'region_id', 'committee_id', 'floor')  # 搜索字段 上方搜索字段


    

admin.site.register(Block, BlockAdmin)
admin.site.register(Equipment_type, Equipment_typeAdmin)
admin.site.register(Equipment, EquipmentAdmin)
admin.site.register(Member, MemberAdmin)
admin.site.register(Article, ArticleAdmin)
admin.site.register(Notice, NoticeAdmin)
admin.site.register(Getdata, GetdataAdmin)
admin.site.register(Login)
admin.site.register(Data, DataAdmin)
admin.site.register(Day_data, Day_dataAdmin)
admin.site.register(Week_data, Week_dataAdmin)
admin.site.register(Month_data, Month_dataAdmin)
admin.site.register(Focus_data, Focus_dataAdmin)
admin.site.register(Warning_data)
admin.site.register(App_suggestion,App_suggestionAdmin)
admin.site.register(Event_data,Event_dataAdmin)
admin.site.register(Getdata_v2,Getdata_v2Admin)
admin.site.register(Smoke_data_v2)
admin.site.register(Smoke_data_day_v2)
admin.site.register(Smoke_data_week_v2)
admin.site.register(Smoke_data_month_v2)
admin.site.register(Door_data_v2)
admin.site.register(Door_data_day_v2)
admin.site.register(Door_data_week_v2)
admin.site.register(Door_data_month_v2)
admin.site.register(Dirty_data_v2)
admin.site.register(Ground_data_v2)
admin.site.register(Water_data_v2)
admin.site.register(Water_data_day_v2)
admin.site.register(Water_data_week_v2)
admin.site.register(Water_data_month_v2)
admin.site.register(Infrared_data_v2)
admin.site.register(Arc_data_v2)
admin.site.register(Recognition_data_v2)
admin.site.register(Charge_data_v2)
admin.site.register(Lift_data_v2)
admin.site.register(Human_data_v2)
admin.site.register(PH_data_v2)
admin.site.register(Oxygen_data_v2)



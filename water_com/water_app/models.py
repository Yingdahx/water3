from django.db import models

class Block(models.Model):
	class Meta:
		verbose_name = verbose_name_plural = '区域街道居委'

	area_id = models.CharField(max_length=200,default='',verbose_name='区域编号',)
	area_name = models.CharField(max_length=200,default='',verbose_name='区域名字',)
	street_id = models.CharField(max_length=200,default='',verbose_name='街道编号',)
	street_name = models.CharField(max_length=200,default='',verbose_name='街道名字',)
	village_id = models.CharField(max_length=200,default='',verbose_name='居委会编号',)
	village_name = models.CharField(max_length=200,default='',verbose_name='居委会名字',)
	street_lat = models.CharField(max_length=200,default='',verbose_name='街道纬度',)
	street_lng = models.CharField(max_length=200,default='',verbose_name='街道经度',)
	count = models.IntegerField(default=0, verbose_name='区域报警数量')

	def __str__(self):
		return self.area_id 
		

class Equipment_type(models.Model):
	class Meta:
		verbose_name = verbose_name_plural = '传感器监控类型(物品类型)'

	name = models.CharField(max_length=200,verbose_name='设备类型名字')
	type_id = models.CharField(max_length=50,verbose_name='类型编号')
	imageUrl = models.CharField(blank=True,null=True,max_length=200,verbose_name='缩略图')
	build_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
	height = models.CharField(blank=True,null=True,max_length=50,verbose_name='图片高度')
	updata_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')
	count = models.IntegerField(default=0, verbose_name='数量')
	status = models.IntegerField(default=0, choices=[(0, '正常'), (1, '停用')], verbose_name='状态')

	def __str__(self):
		return self.name+self.type_id

class Equipment(models.Model):
	class Meta:
		verbose_name = verbose_name_plural = '传感器(物品)'

	sensor_id = models.CharField(max_length=50,null=True,verbose_name='设备标识ID')
	sensor_name = models.CharField(max_length=200,null=True,verbose_name='设备名字')
	point_type = models.CharField(max_length=255,null=True,verbose_name='关联事件类型') #数字
	point_type_name = models.CharField(max_length=255,null=True,verbose_name='关联事件类型名字')
	point_id = models.CharField(max_length=255,null=True,verbose_name='关联事件ID') #数字
	point_name = models.CharField(max_length=255,null=True,verbose_name='关联事件名字')
	address = models.CharField(max_length=255,null=True,verbose_name='安装地址')
	build_time = models.CharField(max_length=255,null=True,verbose_name='安装时间')
	lat = models.CharField(max_length=100,null=True,verbose_name='纬度')
	lng = models.CharField(max_length=100,null=True,verbose_name='经度')
	floor = models.CharField(max_length=255,null=True,verbose_name='安装楼层') #数字
	region_id = models.CharField(max_length=255,null=True,verbose_name='所属街道ID')
	region_name = models.CharField(max_length=255,null=True,verbose_name='所属街道名称')
	piece_id = models.CharField(max_length=255,null=True,verbose_name='所属片区ID')
	piece_name = models.CharField(max_length=255,null=True,verbose_name='所属片区名字')
	committee_id = models.CharField(max_length=255,null=True,verbose_name='所属居委ID')
	committee_name = models.CharField(max_length=255,null=True,verbose_name='所属居委名字')
	equipment_type= models.ForeignKey(Equipment_type,on_delete=models.CASCADE,verbose_name='传感器类型',null=True)
	status = models.IntegerField(choices=[(7,'正常'),(4,'低电压'),(1,'报警'),(0,'未知')],default=0,verbose_name='传感器状态')
	change_time = models.DateTimeField(auto_now=True,verbose_name='状态改变时间')

	def __str__(self):
		return '传感器编号：'+self.sensor_id



class Member(models.Model):
	class Meta:
		verbose_name = verbose_name_plural = '会员'

	name = models.CharField(max_length=50,verbose_name='用户昵称')
	password = models.CharField(max_length=50,verbose_name='密码')
	phone = models.CharField(max_length=11,verbose_name='手机号')
	code = models.CharField(max_length=50,null=True,blank=True,verbose_name='验证码')
	create_time = models.DateTimeField(auto_now_add=True,verbose_name='创建时间')
	update_time = models.DateTimeField(auto_now=True,verbose_name='更新时间')
	status = models.IntegerField(default=0, choices=[(0, '正常'), (1, '停用')], verbose_name='状态')
	icon = models.ImageField(upload_to='member/',null=True,verbose_name='用户头像')
	token = models.CharField(max_length=50,null=True,blank=True,default='',verbose_name='登录生成token')
	message_view = models.CharField(max_length=9999,null=True,default='',blank=True,verbose_name='消息view记录')
	area = models.CharField(default='',max_length=2000,choices=(),verbose_name='权限选项')

	def __str__(self):
		return str(self.phone+','+self.name)



class Data(models.Model):
	class Meta:
		verbose_name = verbose_name_plural = '警报(原数据)'
			
	device_type = models.CharField(max_length=20,null=True,default='',verbose_name='设备类型')
	create_time = models.DateTimeField(null=True,verbose_name='发出时间')
	state = models.CharField(max_length=20,null=True,default='',verbose_name='报警状态')
	battery_voltage = models.CharField(max_length=255,null=True,default='',verbose_name='电压')
	device_id = models.CharField(max_length=50,null=True,default='',verbose_name='设备编号')
	received_time = models.DateTimeField(null=True,verbose_name='接收时间')
	info_type = models.CharField(max_length=20,null=True,default='',verbose_name='数据状态类型')
	protocol_version = models.CharField(max_length=255,null=True,default='',verbose_name='协议版本')
	software_version = models.CharField(max_length=255,null=True,default='',verbose_name='软件版本')
	smoke_concentration = models.CharField(max_length=255,null=True,default='',verbose_name='烟感点')
	get_time = models.DateTimeField(auto_now_add=True,verbose_name='入表时间')

	def __str__(self):
		return '设备:'+self.device_id+',类型:'+self.device_type+',状态:'+self.info_type+'入表时间:'+str(self.get_time)

class Day_data(models.Model):
	class Meta:
		verbose_name = verbose_name_plural = '烟感日志'
			
	device_type = models.CharField(max_length=20,null=True,default='',verbose_name='设备类型')
	create_time = models.DateTimeField(null=True,verbose_name='发出时间')
	state = models.CharField(max_length=20,null=True,default='',verbose_name='报警状态')
	battery_voltage = models.CharField(max_length=255,null=True,default='',verbose_name='电压')
	device_id = models.CharField(max_length=50,null=True,default='',verbose_name='设备编号')
	received_time = models.DateTimeField(null=True,verbose_name='接收时间')
	info_type = models.CharField(max_length=20,null=True,default='',verbose_name='数据状态类型')
	protocol_version = models.CharField(max_length=255,null=True,default='',verbose_name='协议版本')
	software_version = models.CharField(max_length=255,null=True,default='',verbose_name='软件版本')
	smoke_concentration = models.CharField(max_length=255,null=True,default='',verbose_name='烟感点')
	get_time = models.DateTimeField(auto_now_add=True,verbose_name='入表时间')

	def __str__(self):
		return '设备:'+self.device_id+',类型:'+self.device_type+',状态:'+self.info_type+'入表时间:'+str(self.get_time)

class Week_data(models.Model):
	class Meta:
		verbose_name = verbose_name_plural = '烟感周志'
			
	device_type = models.CharField(max_length=20,null=True,default='',verbose_name='设备类型')
	create_time = models.DateTimeField(null=True,verbose_name='发出时间')
	state = models.CharField(max_length=20,null=True,default='',verbose_name='报警状态')
	battery_voltage = models.CharField(max_length=255,null=True,default='',verbose_name='电压')
	device_id = models.CharField(max_length=50,null=True,default='',verbose_name='设备编号')
	received_time = models.DateTimeField(null=True,verbose_name='接收时间')
	info_type = models.CharField(max_length=20,null=True,default='',verbose_name='数据状态类型')
	protocol_version = models.CharField(max_length=255,null=True,default='',verbose_name='协议版本')
	software_version = models.CharField(max_length=255,null=True,default='',verbose_name='软件版本')
	smoke_concentration = models.CharField(max_length=255,null=True,default='',verbose_name='烟感点')
	get_time = models.DateTimeField(auto_now_add=True,verbose_name='入表时间')

	def __str__(self):
		return '设备:'+self.device_id+',类型:'+self.device_type+',状态:'+self.info_type+'入表时间:'+str(self.get_time)

class Month_data(models.Model):
	class Meta:
		verbose_name = verbose_name_plural = '烟感月志'
			
	device_type = models.CharField(max_length=20,null=True,default='',verbose_name='设备类型')
	create_time = models.DateTimeField(null=True,verbose_name='发出时间')
	state = models.CharField(max_length=20,null=True,default='',verbose_name='报警状态')
	battery_voltage = models.CharField(max_length=255,null=True,default='',verbose_name='电压')
	device_id = models.CharField(max_length=50,null=True,default='',verbose_name='设备编号')
	received_time = models.DateTimeField(null=True,verbose_name='接收时间')
	info_type = models.CharField(max_length=20,null=True,default='',verbose_name='数据状态类型')
	protocol_version = models.CharField(max_length=255,null=True,default='',verbose_name='协议版本')
	software_version = models.CharField(max_length=255,null=True,default='',verbose_name='软件版本')
	smoke_concentration = models.CharField(max_length=255,null=True,default='',verbose_name='烟感点')
	get_time = models.DateTimeField(auto_now_add=True,verbose_name='入表时间')

	def __str__(self):
		return '设备:'+self.device_id+',类型:'+self.device_type+',状态:'+self.info_type+'入表时间:'+str(self.get_time)

class Focus_data(models.Model):
	class Meta:
		verbose_name = verbose_name_plural = '烟感实时报警'
			
	device_type = models.CharField(max_length=20,null=True,default='',verbose_name='设备类型')
	create_time = models.DateTimeField(null=True,verbose_name='发出时间')
	state = models.CharField(max_length=20,null=True,default='',verbose_name='报警状态')
	battery_voltage = models.CharField(max_length=255,null=True,default='',verbose_name='电压')
	device_id = models.CharField(max_length=50,null=True,default='',verbose_name='设备编号')
	received_time = models.DateTimeField(null=True,verbose_name='接收时间')
	info_type = models.CharField(max_length=20,null=True,default='',verbose_name='数据状态类型')
	protocol_version = models.CharField(max_length=255,null=True,default='',verbose_name='协议版本')
	software_version = models.CharField(max_length=255,null=True,default='',verbose_name='软件版本')
	smoke_concentration = models.CharField(max_length=255,null=True,default='',verbose_name='烟感点')
	get_time = models.DateTimeField(auto_now_add=True,verbose_name='入表时间')

	def __str__(self):
		return '设备:'+self.device_id+',类型:'+self.device_type+',状态:'+self.info_type+'入表时间:'+str(self.get_time)

class Warning_data(models.Model):
	class Meta:
		verbose_name = verbose_name_plural = '火警事件'
	
	device_type = models.CharField(max_length=20,null=True,default='',verbose_name='设备类型')
	create_time = models.DateTimeField(null=True,verbose_name='发出时间')
	state = models.CharField(max_length=20,null=True,default='',verbose_name='报警状态')
	battery_voltage = models.CharField(max_length=255,null=True,default='',verbose_name='电压')
	device_id = models.CharField(max_length=50,null=True,default='',verbose_name='设备编号')
	received_time = models.DateTimeField(null=True,verbose_name='接收时间')
	info_type = models.CharField(max_length=20,null=True,default='',verbose_name='数据状态类型')
	protocol_version = models.CharField(max_length=255,null=True,default='',verbose_name='协议版本')
	software_version = models.CharField(max_length=255,null=True,default='',verbose_name='软件版本')
	smoke_concentration = models.CharField(max_length=255,null=True,default='',verbose_name='烟感点')
	get_time = models.DateTimeField(auto_now_add=True,verbose_name='入表时间')
	status = models.CharField(max_length=50,null=True,default='True',verbose_name='处理标识')

	def __str__(self):
		return '设备:'+self.device_id+',类型:'+self.device_type+',状态:'+self.info_type+'入表时间:'+str(self.get_time)

		
		

		
		
		
		
class Article(models.Model):
	class Meta:
		verbose_name_plural = verbose_name = '知识表'

	release_title = models.CharField(unique=True,max_length=50, verbose_name='文章标题')
	release_name = models.CharField(max_length=20, verbose_name='来源')
	release_icon = models.ImageField(upload_to='Article/',null=True,verbose_name='缩略图')
	release_time = models.DateTimeField(auto_now_add=True,null=True, verbose_name='发布时间')
	release_update = models.DateTimeField(auto_now=True,null=True, verbose_name='更新时间')
	comment = models.TextField(default='', verbose_name='发布内容')
	status = models.IntegerField(default=0, choices=[(0, '显示'), (1, '不显示')], verbose_name='状态')

	def	__str__(self):
		return self.release_title

		

class Notice(models.Model):
	class Meta:
		verbose_name_plural = verbose_name = '公告表'
	notice_title = models.CharField(unique=True,max_length=50, verbose_name='公告标题',default='')
	comment = models.TextField(default='', verbose_name='公告内容')
	notice_time = models.DateTimeField(auto_now_add=True, verbose_name='发布时间')
	status = models.IntegerField(default=0, choices=[(0, '显示'), (1, '不显示')], verbose_name='状态')

	def toString(self):
		return '公告标题: {},公告内容:{},发布时间:{},状态(0:显示,1:不):{}'.format(self.notice_title,self.comment,self.notice_time,self.status)


	def __str__(self):
		return self.notice_title


class Getdata(models.Model):
	class Meta:
		verbose_name_plural = verbose_name = '传感器信息(原数据)'

	account_id = models.CharField(max_length=200,null=True,verbose_name='客户id')
	account_name = models.CharField(max_length=20,null=True,verbose_name='客户名称')
	address = models.CharField(max_length=255,null=True,verbose_name='地址')
	belonged_account = models.CharField(max_length=200,null=True,verbose_name='所属客户')
	belonged_account_group_id = models.CharField(max_length=200,null=True,verbose_name='客户分组id')
	belonged_account_group_name = models.CharField(max_length=255,null=True,verbose_name='分组名称')
	build_time = models.CharField(null=True,max_length=200,verbose_name='安装时间')
	cluster = models.CharField(max_length=200,null=True,verbose_name='cluster')
	committee_id = models.CharField(max_length=200,null=True,verbose_name='居委会id')
	committee_name = models.CharField(max_length=255,null=True,verbose_name='所属居委名称')
	create_time = models.DateTimeField(null=True,max_length=255,verbose_name='创建时间')
	create_user = models.CharField(max_length=255,null=True,verbose_name='记录创建人')
	height = models.CharField(max_length=50,null=True,verbose_name='高度')
	high = models.CharField(max_length=50,null=True,verbose_name='高度')
	image_url = models.CharField(max_length=255,null=True,verbose_name='图片链接')
	is_available = models.CharField(max_length=20,null=True,verbose_name='是否可用')
	lat = models.CharField(max_length=100,null=True,verbose_name='纬度')
	lng = models.CharField(max_length=100,null=True,verbose_name='经度')
	location = models.CharField(max_length=200,null=True,verbose_name='地区')
	photo_url = models.CharField(max_length=255,null=True,verbose_name='图片url')
	piece_id = models.CharField(max_length=200,null=True,verbose_name='片区ID')
	piece_name = models.CharField(max_length=200,null=True,verbose_name='部件名字')
	point_id = models.CharField(max_length=200,null=True,verbose_name='点位id')
	point_type = models.CharField(max_length=200,null=True,verbose_name='点位类型')
	received_time= models.CharField(null=True,max_length=200,verbose_name='接受时间')
	region_id = models.CharField(max_length=200,null=True,verbose_name='街道id')
	region_name = models.CharField(max_length=200,null=True,verbose_name='所属区域名称')
	sensor_id = models.CharField(max_length=200,null=True,verbose_name='传感器id')
	sensor_name = models.CharField(max_length=200,null=True,verbose_name='传感器名称')
	sensor_number = models.CharField(max_length=50,null=True,verbose_name='传感器编号')
	sensor_point_id = models.CharField(primary_key=True,max_length=200,verbose_name='主键id')
	sensor_type = models.CharField(max_length=20,null=True,verbose_name='传感器类型')
	size = models. CharField(max_length=20,null=True,verbose_name='大小')
	source = models. CharField(max_length=20,null=True,verbose_name='来源')
	status = models.CharField(max_length=20,null=True,verbose_name='状态')
	g_type = models.CharField(max_length=20,null=True,verbose_name='类型')
	updata_time = models.CharField(null=True,max_length=200,verbose_name='更新时间')
	update_user = models.CharField(max_length=255,null=True,verbose_name='更新人')
	video_url = models.CharField(max_length=500,null=True,verbose_name='视频url')
	water_type = models.CharField(max_length=20,null=True,verbose_name='water_type')
	floor = models.CharField(max_length=20,null=True,verbose_name='楼层')

	def __str__(self):
		return str(self.sensor_point_id)


class Login(models.Model):
	class Meta:
		verbose_name = verbose_name_plural = 'web拉数据登录凭证'

	Authenticator = models.CharField(max_length=500,verbose_name='用户凭证')
	add_time = models.DateTimeField(auto_now_add=True,verbose_name='保存时间')
	update_time = models.DateTimeField(auto_now=True,verbose_name='修改时间')


	def __str__(self):
		return str(self.add_time)



class App_suggestion(models.Model):
	class Meta:
		verbose_name = verbose_name_plural = 'APP 反馈意见表'

	suggestion = models.TextField(default='',verbose_name='提交内容')
	image = models.ImageField(upload_to='suggestion/',null=True,verbose_name='附图')
	image_url = models.CharField(max_length=200,null=True,verbose_name='反馈意见附图链接')
	suggest_user_name = models.CharField(max_length=50,verbose_name='提交用户昵称')
	suggest_user_phone = models.CharField(max_length=11,verbose_name='提交用户手机号')
	add_time = models.DateTimeField(auto_now_add=True,verbose_name='提交时间') 

	def __str__(self):
		return self.suggest_user_name+str(self.add_time)

class Event_data(models.Model):
	class Meta:
		verbose_name = verbose_name_plural = '事件'
	
	device_type = models.CharField(max_length=20,null=True,default='',verbose_name='设备类型')
	create_time = models.DateTimeField(null=True,verbose_name='发出时间')
	state = models.CharField(max_length=20,null=True,default='',verbose_name='报警状态')
	battery_voltage = models.CharField(max_length=255,null=True,default='',verbose_name='电压')
	device_id = models.CharField(max_length=50,null=True,default='',verbose_name='设备编号')
	received_time = models.DateTimeField(null=True,verbose_name='接收时间')
	info_type = models.CharField(max_length=20,null=True,default='',verbose_name='数据状态类型')
	protocol_version = models.CharField(max_length=255,null=True,default='',verbose_name='协议版本')
	software_version = models.CharField(max_length=255,null=True,default='',verbose_name='软件版本')
	smoke_concentration = models.CharField(max_length=255,null=True,default='',verbose_name='烟感点')
	get_time = models.DateTimeField(auto_now_add=True,verbose_name='入表时间')
	status = models.CharField(max_length=50,null=True,default='True',verbose_name='处理标识')

	def __str__(self):
		return '设备:'+self.device_id+',类型:'+self.device_type+',状态:'+self.info_type+'入表时间:'+str(self.get_time)

class Getdata_v2(models.Model):
	class Meta:
		verbose_name = verbose_name_plural = '物联设备meta数据'

	device_type = models.CharField(max_length=255,null=True,verbose_name='设备类型')
	sensor_id = models.CharField(max_length=255,null=True,verbose_name='设备ID')
	sensor_name = models.CharField(max_length=255,null=True,verbose_name='设备名字')
	point_type = models.CharField(max_length=255,null=True,verbose_name='关联事件类型') #数字
	point_type_name = models.CharField(max_length=255,null=True,verbose_name='关联事件类型名字')
	point_id = models.CharField(max_length=255,null=True,verbose_name='关联事件ID') #数字
	point_name = models.CharField(max_length=255,null=True,verbose_name='关联事件名字')
	address = models.CharField(max_length=255,null=True,verbose_name='安装地址')
	photo_url = models.CharField(max_length=255,null=True,verbose_name='现场照片URL')
	build_time = models.CharField(max_length=255,null=True,verbose_name='安装时间')
	lng = models.CharField(max_length=255,null=True,verbose_name='经度')
	lat = models.CharField(max_length=255,null=True,verbose_name='纬度')
	floor = models.CharField(max_length=255,null=True,verbose_name='安装楼层') #数字
	region_id = models.CharField(max_length=255,null=True,verbose_name='所属街道ID')
	region_name = models.CharField(max_length=255,null=True,verbose_name='所属街道名称')
	piece_id = models.CharField(max_length=255,null=True,verbose_name='所属片区ID')
	piece_name = models.CharField(max_length=255,null=True,verbose_name='所属片区名字')
	committee_id = models.CharField(max_length=255,null=True,verbose_name='所属居委ID')
	committee_name = models.CharField(max_length=255,null=True,verbose_name='所属居委名字')
	verdor_id = models.CharField(max_length=255,null=True,verbose_name='所属供应商ID')
	verdor_name = models.CharField(max_length=255,null=True,verbose_name='所属供应商名字')
	app_classify_id = models.CharField(max_length=255,null=True,verbose_name='应用分类ID')
	app_classify_name = models.CharField(max_length=255,null=True,verbose_name='应用分类名字')
	get_time = models.DateTimeField(auto_now_add=True,null=True,verbose_name='数据落地时间')

	def __str__(self):
		return self.device_type + self.sensor_id + self.sensor_name + self.region_name + self.piece_name + self.committee_name + self.floor



class Smoke_data_v2(models.Model):
	class Meta:
		verbose_name = verbose_name_plural = '烟雾log原信息v2'
			
	device_id = models.CharField(max_length=255,null=True,default='',verbose_name='设备编号')
	software_version = models.CharField(max_length=255,null=True,default='',verbose_name='软件版本')
	protocol_version = models.CharField(max_length=255,null=True,default='',verbose_name='协议版本')
	device_type = models.CharField(max_length=255,null=True,default='',verbose_name='设备类型')
	info_type = models.CharField(max_length=255,null=True,default='',verbose_name='信息类型')
	battery_voltage = models.CharField(max_length=255,null=True,default='',verbose_name='电磁电压')
	smoke_concentration = models.CharField(max_length=255,null=True,default='',verbose_name='烟浓度')
	received_time = models.DateTimeField(null=True,verbose_name='日志时间')
	get_time = models.DateTimeField(auto_now_add=True,verbose_name='入表时间')

	def __str__(self):
		return '设备:' + self.device_id + '入表时间:' + str(self.get_time)

class Smoke_data_day_v2(models.Model):
	class Meta:
		verbose_name = verbose_name_plural = '烟雾日志log信息v2'
			
	device_id = models.CharField(max_length=255,null=True,default='',verbose_name='设备编号')
	software_version = models.CharField(max_length=255,null=True,default='',verbose_name='软件版本')
	protocol_version = models.CharField(max_length=255,null=True,default='',verbose_name='协议版本')
	device_type = models.CharField(max_length=255,null=True,default='',verbose_name='设备类型')
	info_type = models.CharField(max_length=255,null=True,default='',verbose_name='信息类型')
	battery_voltage = models.CharField(max_length=255,null=True,default='',verbose_name='电磁电压')
	smoke_concentration = models.CharField(max_length=255,null=True,default='',verbose_name='烟浓度')
	received_time = models.DateTimeField(null=True,verbose_name='日志时间')
	get_time = models.DateTimeField(auto_now_add=True,verbose_name='入表时间')

	def __str__(self):
		return '设备:' + self.device_id + '入表时间:' + str(self.get_time)

class Smoke_data_week_v2(models.Model):
	class Meta:
		verbose_name = verbose_name_plural = '烟雾周志log信息v2'
			
	device_id = models.CharField(max_length=255,null=True,default='',verbose_name='设备编号')
	software_version = models.CharField(max_length=255,null=True,default='',verbose_name='软件版本')
	protocol_version = models.CharField(max_length=255,null=True,default='',verbose_name='协议版本')
	device_type = models.CharField(max_length=255,null=True,default='',verbose_name='设备类型')
	info_type = models.CharField(max_length=255,null=True,default='',verbose_name='信息类型')
	battery_voltage = models.CharField(max_length=255,null=True,default='',verbose_name='电磁电压')
	smoke_concentration = models.CharField(max_length=255,null=True,default='',verbose_name='烟浓度')
	received_time = models.DateTimeField(null=True,verbose_name='日志时间')
	get_time = models.DateTimeField(auto_now_add=True,verbose_name='入表时间')

	def __str__(self):
		return '设备:' + self.device_id + '入表时间:' + str(self.get_time)

class Smoke_data_month_v2(models.Model):
	class Meta:
		verbose_name = verbose_name_plural = '烟雾月志log信息v2'
			
	device_id = models.CharField(max_length=255,null=True,default='',verbose_name='设备编号')
	software_version = models.CharField(max_length=255,null=True,default='',verbose_name='软件版本')
	protocol_version = models.CharField(max_length=255,null=True,default='',verbose_name='协议版本')
	device_type = models.CharField(max_length=255,null=True,default='',verbose_name='设备类型')
	info_type = models.CharField(max_length=255,null=True,default='',verbose_name='信息类型')
	battery_voltage = models.CharField(max_length=255,null=True,default='',verbose_name='电磁电压')
	smoke_concentration = models.CharField(max_length=255,null=True,default='',verbose_name='烟浓度')
	received_time = models.DateTimeField(null=True,verbose_name='日志时间')
	get_time = models.DateTimeField(auto_now_add=True,verbose_name='入表时间')

	def __str__(self):
		return '设备:' + self.device_id + '入表时间:' + str(self.get_time)

class Door_data_v2(models.Model):
	class Meta:
		verbose_name = verbose_name_plural = '门磁log原信息v2'
			
	device_id = models.CharField(max_length=255,null=True,default='',verbose_name='设备编号')
	status = models.CharField(max_length=255,null=True,default='',verbose_name='状态')
	battery = models.CharField(max_length=255,null=True,default='',verbose_name='电池电量')
	received_time = models.DateTimeField(null=True,verbose_name='接收时间')
	get_time = models.DateTimeField(auto_now_add=True,verbose_name='入表时间')

	def __str__(self):
		return '设备:' + self.device_id + '入表时间:' + str(self.get_time)

class Door_data_day_v2(models.Model):
	class Meta:
		verbose_name = verbose_name_plural = '门磁log日志信息v2'
			
	device_id = models.CharField(max_length=255,null=True,default='',verbose_name='设备编号')
	status = models.CharField(max_length=255,null=True,default='',verbose_name='状态')
	battery = models.CharField(max_length=255,null=True,default='',verbose_name='电池电量')
	received_time = models.DateTimeField(null=True,verbose_name='接收时间')
	get_time = models.DateTimeField(auto_now_add=True,verbose_name='入表时间')

	def __str__(self):
		return '设备:' + self.device_id + '入表时间:' + str(self.get_time)

class Door_data_week_v2(models.Model):
	class Meta:
		verbose_name = verbose_name_plural = '门磁log周志信息v2'
			
	device_id = models.CharField(max_length=255,null=True,default='',verbose_name='设备编号')
	status = models.CharField(max_length=255,null=True,default='',verbose_name='状态')
	battery = models.CharField(max_length=255,null=True,default='',verbose_name='电池电量')
	received_time = models.DateTimeField(null=True,verbose_name='接收时间')
	get_time = models.DateTimeField(auto_now_add=True,verbose_name='入表时间')

	def __str__(self):
		return '设备:' + self.device_id + '入表时间:' + str(self.get_time)

class Door_data_month_v2(models.Model):
	class Meta:
		verbose_name = verbose_name_plural = '门磁log月志信息v2'
			
	device_id = models.CharField(max_length=255,null=True,default='',verbose_name='设备编号')
	status = models.CharField(max_length=255,null=True,default='',verbose_name='状态')
	battery = models.CharField(max_length=255,null=True,default='',verbose_name='电池电量')
	received_time = models.DateTimeField(null=True,verbose_name='接收时间')
	get_time = models.DateTimeField(auto_now_add=True,verbose_name='入表时间')

	def __str__(self):
		return '设备:' + self.device_id + '入表时间:' + str(self.get_time)

class Dirty_data_v2(models.Model):
	class Meta:
		verbose_name = verbose_name_plural = '垃圾满溢log原信息v2'
			
	device_id = models.CharField(max_length=255,null=True,default='',verbose_name='设备编号')
	temperature = models.CharField(max_length=255,null=True,default='',verbose_name='温度')
	bat = models.CharField(max_length=255,null=True,default='',verbose_name='电池电量')
	height = models.CharField(max_length=255,null=True,default='',verbose_name='高度')
	lng = models.CharField(max_length=255,null=True,default='',verbose_name='经度')
	lat = models.CharField(max_length=255,null=True,default='',verbose_name='纬度')
	height_status= models.CharField(max_length=255,null=True,default='',verbose_name='高度状态')
	received_time = models.DateTimeField(null=True,verbose_name='接收时间')
	get_time = models.DateTimeField(auto_now_add=True,verbose_name='入表时间')

	def __str__(self):
		return '设备:' + self.device_id + '入表时间:' + str(self.get_time)

class Ground_data_v2(models.Model):
	class Meta:
		verbose_name = verbose_name_plural = '地磁log原信息v2'
			
	device_id = models.CharField(max_length=255,null=True,default='',verbose_name='设备编号')
	status = models.CharField(max_length=255,null=True,default='',verbose_name='状态')
	start_symbol = models.CharField(max_length=255,null=True,default='',verbose_name='起始符号')
	region_number = models.CharField(max_length=255,null=True,default='',verbose_name='区域号码')
	parking_log_id = models.CharField(max_length=255,null=True,default='',verbose_name='停车场标识')
	serial_number = models.CharField(max_length=255,null=True,default='',verbose_name='序列号')
	signal_strength = models.CharField(max_length=255,null=True,default='',verbose_name='信号强度')
	battery = models.CharField(max_length=255,null=True,default='',verbose_name='电池')
	received_time = models.DateTimeField(null=True,verbose_name='接收时间')
	get_time = models.DateTimeField(auto_now_add=True,verbose_name='入表时间')

	def __str__(self):
		return '设备:' + self.device_id + '入表时间:' + str(self.get_time)

class Water_data_v2(models.Model):
	class Meta:
		verbose_name = verbose_name_plural = '水压log原信息v2'
	
	device_id = models.CharField(max_length=255,null=True,default='',verbose_name='设备编号')
	STATETYPE = models.CharField(max_length=255,null=True,default='',verbose_name='水压状态类型ID')
	STATENAME = models.CharField(max_length=255,null=True,default='',verbose_name='水压状态类型名称')
	DSNUM = models.CharField(max_length=255,null=True,default='',verbose_name='唯一标识')
	HYDRANTTYPE = models.CharField(max_length=255,null=True,default='',verbose_name='类型')
	WATERTYPE = models.CharField(max_length=255,null=True,default='',verbose_name='仪表')
	RSSI = models.CharField(max_length=255,null=True,default='',verbose_name='信号RSSI')
	lon = models.CharField(max_length=255,null=True,default='',verbose_name='经度')
	lat = models.CharField(max_length=255,null=True,default='',verbose_name='维度')
	PRESSURE = models.CharField(max_length=255,null=True,default='',verbose_name='水压')
	DUMP_ENERGY = models.CharField(max_length=255,null=True,default='',verbose_name='倾倒能量的百分比')
	received_time = models.DateTimeField(null=True,verbose_name='日志时间')
	get_time = models.DateTimeField(auto_now_add=True,verbose_name='入表时间')

	def __str__(self):
		return '设备:' + self.device_id + '入表时间:' + str(self.get_time)

class Water_data_day_v2(models.Model):
	class Meta:
		verbose_name = verbose_name_plural = '水压log日志信息v2'
	
	device_id = models.CharField(max_length=255,null=True,default='',verbose_name='设备编号')
	STATETYPE = models.CharField(max_length=255,null=True,default='',verbose_name='水压状态类型ID')
	STATENAME = models.CharField(max_length=255,null=True,default='',verbose_name='水压状态类型名称')
	DSNUM = models.CharField(max_length=255,null=True,default='',verbose_name='唯一标识')
	HYDRANTTYPE = models.CharField(max_length=255,null=True,default='',verbose_name='类型')
	WATERTYPE = models.CharField(max_length=255,null=True,default='',verbose_name='仪表')
	RSSI = models.CharField(max_length=255,null=True,default='',verbose_name='信号RSSI')
	lon = models.CharField(max_length=255,null=True,default='',verbose_name='经度')
	lat = models.CharField(max_length=255,null=True,default='',verbose_name='维度')
	PRESSURE = models.CharField(max_length=255,null=True,default='',verbose_name='水压')
	DUMP_ENERGY = models.CharField(max_length=255,null=True,default='',verbose_name='倾倒能量的百分比')
	received_time = models.DateTimeField(null=True,verbose_name='日志时间')
	get_time = models.DateTimeField(auto_now_add=True,verbose_name='入表时间')

	def __str__(self):
		return '设备:' + self.device_id + '入表时间:' + str(self.get_time)

class Water_data_week_v2(models.Model):
	class Meta:
		verbose_name = verbose_name_plural = '水压log周志信息v2'
	
	device_id = models.CharField(max_length=255,null=True,default='',verbose_name='设备编号')
	STATETYPE = models.CharField(max_length=255,null=True,default='',verbose_name='水压状态类型ID')
	STATENAME = models.CharField(max_length=255,null=True,default='',verbose_name='水压状态类型名称')
	DSNUM = models.CharField(max_length=255,null=True,default='',verbose_name='唯一标识')
	HYDRANTTYPE = models.CharField(max_length=255,null=True,default='',verbose_name='类型')
	WATERTYPE = models.CharField(max_length=255,null=True,default='',verbose_name='仪表')
	RSSI = models.CharField(max_length=255,null=True,default='',verbose_name='信号RSSI')
	lon = models.CharField(max_length=255,null=True,default='',verbose_name='经度')
	lat = models.CharField(max_length=255,null=True,default='',verbose_name='维度')
	PRESSURE = models.CharField(max_length=255,null=True,default='',verbose_name='水压')
	DUMP_ENERGY = models.CharField(max_length=255,null=True,default='',verbose_name='倾倒能量的百分比')
	received_time = models.DateTimeField(null=True,verbose_name='日志时间')
	get_time = models.DateTimeField(auto_now_add=True,verbose_name='入表时间')

	def __str__(self):
		return '设备:' + self.device_id + '入表时间:' + str(self.get_time)

class Water_data_month_v2(models.Model):
	class Meta:
		verbose_name = verbose_name_plural = '水压log月志信息v2'
	
	device_id = models.CharField(max_length=255,null=True,default='',verbose_name='设备编号')
	STATETYPE = models.CharField(max_length=255,null=True,default='',verbose_name='水压状态类型ID')
	STATENAME = models.CharField(max_length=255,null=True,default='',verbose_name='水压状态类型名称')
	DSNUM = models.CharField(max_length=255,null=True,default='',verbose_name='唯一标识')
	HYDRANTTYPE = models.CharField(max_length=255,null=True,default='',verbose_name='类型')
	WATERTYPE = models.CharField(max_length=255,null=True,default='',verbose_name='仪表')
	RSSI = models.CharField(max_length=255,null=True,default='',verbose_name='信号RSSI')
	lon = models.CharField(max_length=255,null=True,default='',verbose_name='经度')
	lat = models.CharField(max_length=255,null=True,default='',verbose_name='维度')
	PRESSURE = models.CharField(max_length=255,null=True,default='',verbose_name='水压')
	DUMP_ENERGY = models.CharField(max_length=255,null=True,default='',verbose_name='倾倒能量的百分比')
	received_time = models.DateTimeField(null=True,verbose_name='日志时间')
	get_time = models.DateTimeField(auto_now_add=True,verbose_name='入表时间')

	def __str__(self):
		return '设备:' + self.device_id + '入表时间:' + str(self.get_time)

class Infrared_data_v2(models.Model):
	class Meta:
		verbose_name = verbose_name_plural = '红外周界log原信息v2'
	
	device_id = models.CharField(max_length=255,null=True,default='',verbose_name='设备编号')
	status = models.CharField(max_length=255,null=True,default='',verbose_name='状态')
	received_time = models.DateTimeField(null=True,verbose_name='日志时间')
	get_time = models.DateTimeField(auto_now_add=True,verbose_name='入表时间')

	def __str__(self):
		return '设备:' + self.device_id + '入表时间:' + str(self.get_time)

class Arc_data_v2(models.Model):
	class Meta:
		verbose_name = verbose_name_plural = '电弧灭弧log原信息v2'

	device_id = models.CharField(max_length=255,null=True,default='',verbose_name='设备编号')
	src = models.CharField(max_length=255,null=True,default='',verbose_name='电弧状态')
	status = models.CharField(max_length=255,null=True,default='',verbose_name='状态描述')
	msgType = models.CharField(max_length=255,null=True,default='',verbose_name='消息类型')
	devType = models.CharField(max_length=255,null=True,default='',verbose_name='设备类型')
	ld = models.CharField(max_length=255,null=True,default='',verbose_name='漏损量')
	ia = models.CharField(max_length=255,null=True,default='',verbose_name='电流')
	ua = models.CharField(max_length=255,null=True,default='',verbose_name='电压')
	ta = models.CharField(max_length=255,null=True,default='',verbose_name='温度1')
	tb = models.CharField(max_length=255,null=True,default='',verbose_name='温度2')
	received_time = models.DateTimeField(null=True,verbose_name='日志时间')
	get_time = models.DateTimeField(auto_now_add=True,verbose_name='入表时间')

	def __str__(self):
		return '设备:' + self.device_id + '入表时间:' + str(self.get_time)
	
class Recognition_data_v2(models.Model):
	class Meta:
		verbose_name = verbose_name_plural = '人脸识别log原信息v2'

	device_id = models.CharField(max_length=255,null=True,default='',verbose_name='设备编号')
	sex = models.CharField(max_length=255,null=True,default='',verbose_name='性别')
	age = models.CharField(max_length=255,null=True,default='',verbose_name='年龄')
	glass = models.CharField(max_length=255,null=True,default='',verbose_name='是否戴眼镜')
	emotion = models.CharField(max_length=255,null=True,default='',verbose_name='表情')
	personName = models.CharField(max_length=255,null=True,default='',verbose_name='姓名')
	imageWidth = models.CharField(max_length=255,null=True,default='',verbose_name='图片宽度')
	imageHeight = models.CharField(max_length=255,null=True,default='',verbose_name='图片高度')
	fileLength = models.CharField(max_length=255,null=True,default='',verbose_name='图片大小')
	rawInBase64 = models.CharField(max_length=255,null=True,default='',verbose_name='图片URL')
	received_time = models.DateTimeField(null=True,verbose_name='日志时间')
	get_time = models.DateTimeField(auto_now_add=True,verbose_name='入表时间')

	def __str__(self):
		return '设备:' + self.device_id + '入表时间:' + str(self.get_time)

class Charge_data_v2(models.Model):
	class Meta:
		verbose_name = verbose_name_plural = '充电桩log原信息v2'

	device_id = models.CharField(max_length=255,null=True,default='',verbose_name='设备编号')
	pile_type = models.CharField(max_length=255,null=True,default='',verbose_name='类型')
	plugNumber = models.IntegerField(verbose_name='充电口编号')
	unitPrice = models.CharField(max_length=255,null=True,default='',verbose_name='电费单价')
	minPrice = models.CharField(max_length=255,null=True,default='',verbose_name='电费最低价格')
	attachPrice = models.CharField(max_length=255,null=True,default='',verbose_name='电费附加费')
	overdraft = models.CharField(max_length=255,null=True,default='',verbose_name='透支系数')
	factor = models.CharField(max_length=255,null=True,default='',verbose_name='校正因子')
	maxPlugPower = models.CharField(max_length=255,null=True,default='',verbose_name='插头的最大功率')
	maxDevicePower = models.CharField(max_length=255,null=True,default='',verbose_name='设备的最大功率')
	area = models.CharField(max_length=255,null=True,default='',verbose_name='地区名称')
	location = models.CharField(max_length=255,null=True,default='',verbose_name='设备位置')
	inusePlugNumber = models.IntegerField(verbose_name='插头数量')
	isOnline = models.CharField(max_length=255,null=True,default='',verbose_name='联机状态')
	plugs1 = models.CharField(max_length=255,null=True,default='',verbose_name='插口1')
	plugs2 = models.CharField(max_length=255,null=True,default='',verbose_name='插口2')
	plugs3 = models.CharField(max_length=255,null=True,default='',verbose_name='插口3')
	plugs4 = models.CharField(max_length=255,null=True,default='',verbose_name='插口4')
	plugs5 = models.CharField(max_length=255,null=True,default='',verbose_name='插口5')
	plugs6 = models.CharField(max_length=255,null=True,default='',verbose_name='插口6')
	plugs7 = models.CharField(max_length=255,null=True,default='',verbose_name='插口7')
	plugs8 = models.CharField(max_length=255,null=True,default='',verbose_name='插口8')
	plugs9 = models.CharField(max_length=255,null=True,default='',verbose_name='插口9')
	plugs10 = models.CharField(max_length=255,null=True,default='',verbose_name='插口10')
	received_time = models.DateTimeField(null=True,verbose_name='日志时间')
	get_time = models.DateTimeField(auto_now_add=True,verbose_name='入表时间')

	def __str__(self):
		return '设备:' + self.device_id + '入表时间:' + str(self.get_time)

class Lift_data_v2(models.Model):
	class Meta:
		verbose_name = verbose_name_plural = '电梯传感器log原信息v2'

	device_id = models.CharField(max_length=255,null=True,default='',verbose_name='设备编号')
	lift_type = models.CharField(max_length=255,null=True,default='',verbose_name='类型')
	lift_len = models.CharField(max_length=255,null=True,default='',verbose_name='长度')
	address = models.CharField(max_length=255,null=True,default='',verbose_name='地址')
	cmd = models.CharField(max_length=255,null=True,default='',verbose_name='命令')
	lift_data = models.CharField(max_length=255,null=True,default='',verbose_name='类型值')
	down = models.CharField(max_length=255,null=True,default='',verbose_name='上行')
	up = models.CharField(max_length=255,null=True,default='',verbose_name='下行')
	current_level = models.CharField(max_length=255,null=True,default='',verbose_name='当前层')
	highest = models.CharField(max_length=255,null=True,default='',verbose_name='最高层')
	received_time = models.DateTimeField(null=True,verbose_name='日志时间')
	get_time = models.DateTimeField(auto_now_add=True,verbose_name='入表时间')

	def __str__(self):
		return '设备:' + self.device_id + '入表时间:' + str(self.get_time)

class Human_data_v2(models.Model):
	class Meta:
		verbose_name = verbose_name_plural = '人体红外感应log原信息v2'

	device_id = models.CharField(max_length=255,null=True,default='',verbose_name='设备编号')
	bat = models.CharField(max_length=255,null=True,default='',verbose_name='电量')
	temperature = models.CharField(max_length=255,null=True,default='',verbose_name='温度')
	illuminance = models.CharField(max_length=255,null=True,default='',verbose_name='照度')
	occupy = models.CharField(max_length=255,null=True,default='',verbose_name='有无动静')
	received_time = models.DateTimeField(null=True,verbose_name='日志时间')
	get_time = models.DateTimeField(auto_now_add=True,verbose_name='入表时间')

	def __str__(self):
		return '设备:' + self.device_id + '入表时间:' + str(self.get_time)

class PH_data_v2(models.Model):
	class Meta:
		verbose_name = verbose_name_plural = 'PH传感log原信息v2'

	device_id = models.CharField(max_length=255,null=True,default='',verbose_name='设备编号')
	num = models.CharField(max_length=255,null=True,default='',verbose_name='num')
	ph_len = models.CharField(max_length=255,null=True,default='',verbose_name='len')
	bat = models.CharField(max_length=255,null=True,default='',verbose_name='电池电压')
	ph = models.CharField(max_length=255,null=True,default='',verbose_name='PH值')
	temperature = models.CharField(max_length=255,null=True,default='',verbose_name='温度')
	t_style = models.CharField(max_length=255,null=True,default='',verbose_name='周期')
	received_time = models.DateTimeField(null=True,verbose_name='日志时间')
	get_time = models.DateTimeField(auto_now_add=True,verbose_name='入表时间')

	def __str__(self):
		return '设备:' + self.device_id + '入表时间:' + str(self.get_time)

class Oxygen_data_v2(models.Model):
	class Meta:
		verbose_name = verbose_name_plural = '溶解氧log原信息v2'

	device_id = models.CharField(max_length=255,null=True,default='',verbose_name='设备编号')
	num = models.CharField(max_length=255,null=True,default='',verbose_name='num')
	ox_len = models.CharField(max_length=255,null=True,default='',verbose_name='len')
	bat = models.CharField(max_length=255,null=True,default='',verbose_name='电池电压')
	doxy = models.CharField(max_length=255,null=True,default='',verbose_name='溶解氧mg/l')
	doxys = models.CharField(max_length=255,null=True,default='',verbose_name='溶解氧饱和度%')
	temperature = models.CharField(max_length=255,null=True,default='',verbose_name='温度')
	t_style = models.CharField(max_length=255,null=True,default='',verbose_name='周期')
	received_time = models.DateTimeField(null=True,verbose_name='日志时间')
	get_time = models.DateTimeField(auto_now_add=True,verbose_name='入表时间')

	def __str__(self):
		return '设备:' + self.device_id + '入表时间:' + str(self.get_time)

	









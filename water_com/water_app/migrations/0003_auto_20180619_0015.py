# Generated by Django 2.0.5 on 2018-06-19 00:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('water_app', '0002_auto_20180618_2352'),
    ]

    operations = [
        migrations.AlterField(
            model_name='getdata',
            name='account_id',
            field=models.CharField(max_length=200, null=True, verbose_name='客户id'),
        ),
        migrations.AlterField(
            model_name='getdata',
            name='account_name',
            field=models.CharField(max_length=20, null=True, verbose_name='客户名称'),
        ),
        migrations.AlterField(
            model_name='getdata',
            name='address',
            field=models.CharField(max_length=255, null=True, verbose_name='地址'),
        ),
        migrations.AlterField(
            model_name='getdata',
            name='belonged_account',
            field=models.CharField(max_length=200, null=True, verbose_name='所属客户'),
        ),
        migrations.AlterField(
            model_name='getdata',
            name='belonged_account_group_id',
            field=models.CharField(max_length=200, null=True, verbose_name='客户分组id'),
        ),
        migrations.AlterField(
            model_name='getdata',
            name='belonged_account_group_name',
            field=models.CharField(max_length=255, null=True, verbose_name='分组名称'),
        ),
        migrations.AlterField(
            model_name='getdata',
            name='cluster',
            field=models.CharField(max_length=200, null=True, verbose_name='cluster'),
        ),
        migrations.AlterField(
            model_name='getdata',
            name='committee_id',
            field=models.CharField(max_length=200, null=True, verbose_name='居委会id'),
        ),
        migrations.AlterField(
            model_name='getdata',
            name='committee_name',
            field=models.CharField(max_length=255, null=True, verbose_name='所属居委名称'),
        ),
        migrations.AlterField(
            model_name='getdata',
            name='create_user',
            field=models.CharField(max_length=255, null=True, verbose_name='记录创建人'),
        ),
        migrations.AlterField(
            model_name='getdata',
            name='g_type',
            field=models.CharField(max_length=20, null=True, verbose_name='类型'),
        ),
        migrations.AlterField(
            model_name='getdata',
            name='height',
            field=models.CharField(max_length=50, null=True, verbose_name='高度'),
        ),
        migrations.AlterField(
            model_name='getdata',
            name='high',
            field=models.CharField(max_length=50, null=True, verbose_name='高度'),
        ),
        migrations.AlterField(
            model_name='getdata',
            name='image_url',
            field=models.CharField(max_length=255, null=True, verbose_name='图片链接'),
        ),
        migrations.AlterField(
            model_name='getdata',
            name='is_available',
            field=models.CharField(max_length=20, null=True, verbose_name='是否可用'),
        ),
        migrations.AlterField(
            model_name='getdata',
            name='lat',
            field=models.CharField(max_length=100, null=True, verbose_name='纬度'),
        ),
        migrations.AlterField(
            model_name='getdata',
            name='lng',
            field=models.CharField(max_length=100, null=True, verbose_name='经度'),
        ),
        migrations.AlterField(
            model_name='getdata',
            name='location',
            field=models.CharField(max_length=200, null=True, verbose_name='地区'),
        ),
        migrations.AlterField(
            model_name='getdata',
            name='photo_url',
            field=models.CharField(max_length=255, null=True, verbose_name='图片url'),
        ),
        migrations.AlterField(
            model_name='getdata',
            name='piece_id',
            field=models.CharField(max_length=200, null=True, verbose_name='片区ID'),
        ),
        migrations.AlterField(
            model_name='getdata',
            name='piece_name',
            field=models.CharField(max_length=200, null=True, verbose_name='部件名字'),
        ),
        migrations.AlterField(
            model_name='getdata',
            name='point_id',
            field=models.CharField(max_length=200, null=True, verbose_name='点位id'),
        ),
        migrations.AlterField(
            model_name='getdata',
            name='point_type',
            field=models.CharField(max_length=200, null=True, verbose_name='点位类型'),
        ),
        migrations.AlterField(
            model_name='getdata',
            name='region_id',
            field=models.CharField(max_length=200, null=True, verbose_name='街道id'),
        ),
        migrations.AlterField(
            model_name='getdata',
            name='region_name',
            field=models.CharField(max_length=200, null=True, verbose_name='所属区域名称'),
        ),
        migrations.AlterField(
            model_name='getdata',
            name='sensor_id',
            field=models.CharField(max_length=200, null=True, verbose_name='传感器id'),
        ),
        migrations.AlterField(
            model_name='getdata',
            name='sensor_name',
            field=models.CharField(max_length=200, null=True, verbose_name='传感器名称'),
        ),
        migrations.AlterField(
            model_name='getdata',
            name='sensor_number',
            field=models.CharField(max_length=50, null=True, verbose_name='传感器编号'),
        ),
        migrations.AlterField(
            model_name='getdata',
            name='sensor_type',
            field=models.CharField(max_length=20, null=True, verbose_name='传感器类型'),
        ),
        migrations.AlterField(
            model_name='getdata',
            name='size',
            field=models.CharField(max_length=20, null=True, verbose_name='大小'),
        ),
        migrations.AlterField(
            model_name='getdata',
            name='source',
            field=models.CharField(max_length=20, null=True, verbose_name='来源'),
        ),
        migrations.AlterField(
            model_name='getdata',
            name='status',
            field=models.CharField(max_length=20, null=True, verbose_name='状态'),
        ),
        migrations.AlterField(
            model_name='getdata',
            name='update_user',
            field=models.CharField(max_length=255, null=True, verbose_name='更新人'),
        ),
        migrations.AlterField(
            model_name='getdata',
            name='video_url',
            field=models.CharField(max_length=500, null=True, verbose_name='视频url'),
        ),
        migrations.AlterField(
            model_name='getdata',
            name='water_type',
            field=models.CharField(max_length=20, null=True, verbose_name='water_type'),
        ),
    ]

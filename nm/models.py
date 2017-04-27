from django.db import models
from django.core import urlresolvers


class Vendor(models.Model):
    name = models.CharField('厂商',max_length=20)
    full_name = models.CharField('全称', max_length=100)
    chinese_name = models.CharField('中文名称', max_length=100)

    class Meta:
        verbose_name = '厂商'
        verbose_name_plural = '厂商'

    def __str__(self):
        return self.name


class VendorModel(models.Model):
    name = models.CharField('型号', max_length=100)
    vendor = models.ForeignKey(Vendor)

    class Meta:
        verbose_name = '品牌型号'
        verbose_name_plural = '品牌型号'

    def __str__(self):
        return self.vendor.name + '_' + self.name

    @property
    def full_name(self):
        return self.vendor.name + '_' + self.name

class AuthProfile(models.Model):
    ACCESS_METHOD=(
        ('ssh', 'SSH'),
        ('telnet', 'Telnet'),
    )
    name = models.CharField('名称', max_length=50)
    access_method = models.CharField('访问方法', max_length=20, choices=ACCESS_METHOD, default='telnet')
    username = models.CharField('用户名', max_length=20)
    password = models.CharField('密码', max_length=20)
    super_password = models.CharField('超级密码', max_length=20)

    class Meta:
        verbose_name = '认证配置文件'
        verbose_name_plural = '认证配置文件'
    def __str__(self):
        return self.name


class SnmpCommunity(models.Model):
    VERSION=(
        ('v2', 'V2'),
        ('v2c', 'V2c'),
        ('v3', 'V3'),
    )
    name = models.CharField('名称', max_length=100, null=False)
    version = models.CharField('版本', max_length=20, choices=VERSION)
    ro = models.CharField('RO值', max_length=50)
    rw = models.CharField('RW值', max_length=50)

    class Meta:
        verbose_name = 'SNMP团体'
        verbose_name_plural = 'SNMP团体'

    def __str__(self):
        return self.name


class Device(models.Model):
    hostname = models.CharField('主机名', max_length=100, )
    vendor_model = models.ForeignKey(VendorModel, verbose_name='品牌型号')
    #type = models.CharField(max_length=100)
    #mgmt_ip = models.GenericIPAddressField(blank=True, null=True)
    #mgmt_port = models.OneToOneField(Port)
    auth_profile = models.ForeignKey(AuthProfile, verbose_name='认证配置文件', blank=True, null=True)
    snmp_community = models.ForeignKey(SnmpCommunity, verbose_name='SNMP团体', blank=True, null=True)

    class Meta:
        verbose_name = '设备'
        verbose_name_plural = '设备'

    def __str__(self):
        return self.hostname


class Port(models.Model):
    name = models.CharField('接口名', max_length=100)
    device = models.ForeignKey(Device, verbose_name='所属设备')
    ip = models.GenericIPAddressField('IP地址', null=True, blank=True)
    mask = models.IntegerField('子网掩码', default=24)
    is_mgmt_port = models.BooleanField('是否管理接口', default=False)
    is_sub_port = models.BooleanField('是否子接口', default=False)
    father_port = models.ForeignKey('self', null= True, blank= True)
    class Meta:
        verbose_name = '接口'
        verbose_name_plural = '接口'

    def __str__(self):
        return self.device.hostname + '_' + self.name

    def changeform_link(self):
        if self.id:
            # Replace "myapp" with the name of the app containing
            # your Certificate model:
            changeform_url = urlresolvers.reverse(
                'admin:nm_port_change', args=(self.id,)
            )
            return u'<a href="%s" target="_blank">详情</a>' % changeform_url
        return u''

    changeform_link.allow_tags = True
    changeform_link.short_description = '子接口'  # omit column header


class SubPort(models.Model):
    name = models.CharField('子接口名', max_length=100)
    port = models.ForeignKey(Port, verbose_name='所属端口')
    ip = models.GenericIPAddressField('IP地址', null=True, blank=True)
    mask = models.IntegerField('子网掩码', default=24)


    class Meta:
        verbose_name = '子接口'
        verbose_name_plural = '子接口'

    def __str__(self):
        return self.port.device.hostname + '_' + self.port.name + '_' + self.name


class Task(models.Model):
    name = models.CharField('任务名称', max_length=50)
    description = models.TextField('描述', max_length=1000)
    cmd = models.CharField ('执行命令', max_length=100)
    device = models.ManyToManyField(Device, verbose_name='关联设备')

from django.db import models


class SubPort(models.Model):
    name = models.CharField(max_length=100)
    ip = models.GenericIPAddressField(null=True, blank=True)

    def __str__(self):
        return self.port.device.hostname + '_' + self.port.name + '_' + self.name


class Port(models.Model):
    name = models.CharField(max_length=100)
    ip = models.GenericIPAddressField(null=True, blank=True)
    sub_port = models.OneToOneField(SubPort, blank=True, null=True)

    def __str__(self):
        return self.device.hostname + '_' + self.name


class Vendor(models.Model):
    name = models.CharField(max_length=20)
    full_name = models.CharField(max_length=100)
    chinese_name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class VendorModel(models.Model):
    name = models.CharField(max_length=100)
    vendor = models.ForeignKey(Vendor)

    def __str__(self):
        return self.vendor.name + '_' + self.name


class AuthProfile(models.Model):
    ACCESS_METHOD=(
        ('ssh', 'SSH'),
        ('telnet', 'Telnet'),
    )
    name = models.CharField(max_length=50)
    access_method = models.CharField(max_length=20, choices=ACCESS_METHOD, default='telnet')
    username = models.CharField(max_length=20)
    password = models.CharField(max_length=20)
    super_password = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class SnmpCommunity(models.Model):
    VERSION=(
        ('v2', 'V2'),
        ('v2c', 'V2c'),
        ('v3', 'V3'),
    )
    name = models.CharField(max_length=100, null=False)
    version = models.CharField(max_length=20, choices=VERSION)
    ro = models.CharField(max_length=50)
    rw = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Device(models.Model):
    #vendor = models.CharField(max_length=100)
    model = models.ForeignKey(VendorModel)
    #type = models.CharField(max_length=100)

    hostname = models.CharField(max_length=100)
    mgmt_ip = models.GenericIPAddressField(blank=True, null=True)
    port = models.OneToOneField(Port, blank=True, null=True)
    auth_profile = models.ForeignKey(AuthProfile, blank=True, null=True)
    snmp_community = models.ForeignKey(SnmpCommunity, blank=True, null=True)

    def __str__(self):
        return self.hostname













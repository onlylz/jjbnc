from django.db import models

class Device(models.Model):
    vendor = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    type = models.CharField(max_length=100)

    hostname = models.CharField(max_length=100)
    mgmt_ip = models.CharField(max_length=100)
    interface = models.ForeignKey(Interface)

    auth_schema = models.ForeignKey(AuthSchema)
    snmp_community = models.ForeignKey(SnmpCommunity)


class Interface(models.Model):
    name = models.CharField(max_length=100)
    ip = models.CharField(max_length=100)
    sub_interface = models.ForeignKey(SubInterface)

class SubInterface(models.Model):
    name = models.CharField(max_length=100)
    ip = models.CharField(max_length=100)


class Vendor(models.Model):



class Model(models.Model):


class AuthSchema(models.Model):
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    super_password = models.CharField(max_length=100)

class SnmpCommunity(models.Model):







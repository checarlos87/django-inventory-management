from __future__ import unicode_literals

from django.core.exceptions import ValidationError
from django.core.validators import validate_email, validate_ipv4_address
from django.db import models
from django.utils.encoding import python_2_unicode_compatible

### Equipment and subclasses ###

@python_2_unicode_compatible
class Equipment(models.Model):
    name = models.CharField(max_length = 30, unique=True)
    property_num = models.CharField(max_length = 10, blank=True)
    building = models.ForeignKey('Building', on_delete=models.PROTECT, null=True)
    description = models.TextField()

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

class PC(Equipment):
    custodial = models.ForeignKey('Employee', on_delete=models.PROTECT, blank=True)
    brand = models.CharField(max_length = 15, blank=True)
    series = models.CharField(max_length = 15, blank=True)
    # This refers to a machine's model, not a Django model.
    model = models.CharField(max_length = 10, blank=True)

    def get_pc_model(self):
        pc_model = self.brand + " " + self.series + " " + self.model
        if pc_model == "  ":
            return "---"
        else:
            return pc_model

# Included in this section because it's so closely tied to PC.
@python_2_unicode_compatible
class Employee(models.Model):
    first_name = models.CharField(max_length = 15)
    middle_name = models.CharField(max_length = 15, blank=True)
    last_name = models.CharField(max_length = 15)
    email = models.CharField(max_length = 40, validators = [validate_email], unique=True)
    ext = models.CharField(max_length = 4, blank=True)

    class Meta:
        ordering = ['first_name']

    def __str__(self):
        if self.middle_name:
            return self.first_name + " " + self.middle_name + " " + self.last_name
        else:
            return self.first_name + " " + self.last_name

class Misc(Equipment):
    equip_type = models.ForeignKey('MiscType', on_delete=models.PROTECT)

# Class to hold the different kinds of
# misc equipment.
@python_2_unicode_compatible
class MiscType(models.Model):
    misc_type = models.CharField(max_length = 15, unique=True)

    class Meta:
        ordering = ['misc_type']

    def __str__(self):
        return self.misc_type

class Switch(Equipment):
    ETHERNET = 'ETH'
    INFINIBAND = 'IB'
    TYPE_CHOICES = (
        (ETHERNET, 'Ethernet'),
        (INFINIBAND, 'Infiniband')
    )

    ip = models.CharField(max_length = 15, validators = [validate_ipv4_address], blank=True)
    switch_type = models.CharField(
        max_length = 3,
        choices = TYPE_CHOICES,
        default = ETHERNET,
    )
    os = models.ForeignKey('SwitchOS', on_delete=models.PROTECT, blank=True, null=True)
    brand = models.CharField(max_length = 15, blank=True)
    series = models.CharField(max_length = 15, blank=True)
    # This refers to a machine's model, not a Django model.
    model = models.CharField(max_length = 10, blank=True)
    rack = models.CharField(max_length = 15, blank=True)
    bay_from = models.IntegerField(blank=True, null=True)
    bay_to = models.IntegerField(blank=True, null=True)

    def clean(self):
        if not self.bay_from is None and not self.bay_to is None and self.bay_from > self.bay_to:
            raise ValidationError('Start bay position cannot be greater than end bay position.')

    def get_switch_model(self):
        switch_model = self.brand + " " + self.series + " " + self.model
        if switch_model == "  ":
            return "---"
        else:
            return switch_model

class Jbod(Equipment):
    brand = models.CharField(max_length = 15, blank=True)
    series = models.CharField(max_length = 15, blank=True)
    # This refers to a machine's model, not a Django model.
    model = models.CharField(max_length = 10, blank=True)
    rack = models.CharField(max_length = 15, blank=True)
    bay_from = models.IntegerField(blank=True, null=True)
    bay_to = models.IntegerField(blank=True, null=True)
    managers = models.ManyToManyField('Host')

    def clean(self):
        if not self.bay_from is None and not self.bay_to is None and self.bay_from > self.bay_to:
            raise ValidationError('Start bay position cannot be greater than end bay position.')

    def get_jbod_model(self):
        jbod_model = self.brand + " " + self.series + " " + self.model
        if jbod_model == "  ":
            return "---"
        else:
            return jbod_model

# The main class in this model.
class Host(Equipment):
    services = models.ManyToManyField('Service', blank=True)
    os = models.ForeignKey('HostOS', on_delete=models.PROTECT, blank=True, null=True)
    is_bacula_fd = models.BooleanField(default=False)
    is_ansible_managed = models.BooleanField(default=False)

    def get_netiface_ip(self):
        try:
            return Netiface.objects.filter(host_id = self.id)[0].ip
        except(IndexError):
            return '---'
    get_netiface_ip.short_description = 'Public IP'

class PhysHost(Host):
    brand = models.CharField(max_length = 15, blank=True)
    series = models.CharField(max_length = 15, blank=True)
    # This refers to a machine's model, not a Django model.
    model = models.CharField(max_length = 10, blank=True)
    rack = models.CharField(max_length = 15, blank=True)
    bay_from = models.IntegerField(blank=True, null=True)
    bay_to = models.IntegerField(blank=True, null=True)

    def clean(self):
        if not self.bay_from is None and not self.bay_to is None and self.bay_from > self.bay_to:
            raise ValidationError('Start bay position cannot be greater than end bay position.')

    def get_computer_model(self):
        computer_model = self.brand + " " + self.series + " " + self.model
        if computer_model == "  ":
            return "---"
        else:
            return computer_model

class VMHost(Host):
    host_machine = models.ForeignKey(PhysHost, on_delete=models.PROTECT)

# This is a small abstract class for defining "Member" classes.
# It is meant to be used to group hosts into "clouds" of computers
# that work as part of a single system. An example "BaculaCloudMember"
# is defined below.
class CloudMember(models.Model):
    # Noite: A OneToOneField as PK is the same thing as an "IS A" relationship,
    # which is usually expressed in Django through multi-table inheritance.
    # However, creating the relationship this way avoids the pitfalls of polymorphism
    # introduced by multi-table inheritance. 

    member = models.OneToOneField(Host, on_delete=models.CASCADE, primary_key = True)

    class Meta:
        abstract = True
        ordering = ['member']

    def get_member_name(self):
        return self.member.name
    get_member_name.short_description = 'Member Name'

@python_2_unicode_compatible
class BaculaCloudMember(CloudMember):
    DIRECTOR = 'DIR'
    SD = 'SD'
    ROLE_CHOICES = (
        (DIRECTOR, 'Director'),
        (SD, 'Storage Daemon'),
    )

    # Note: In real life, a Bacula host may be both a director and an SD, but
    # we simplify our schema by allowing only one of them to be chosen based
    # on the following rule:
    # - a Bacula host that is just an SD will be registered as "SD"
    # - a Bacula host that is a director (and possibly other roles as well)
    #   is registered as a director.
    #
    # 'FD' is not listed as a role here, because this relation is meant to 
    # contain hosts involved in the management side of Bacula.  That is the
    # reason we set the FD role simply as a BooleanField on the Host relation.

    role = models.CharField(max_length = 3, choices = ROLE_CHOICES, default = SD)

    def __str__(self):
        return "Bacula - " + self.role + " - " + str(self.member.id)

### === ###

### Other Entities related to hosts. ###

@python_2_unicode_compatible
class Building(models.Model):
    name = models.CharField(max_length = 30, unique=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

@python_2_unicode_compatible
class WebSite(models.Model):
    web_host = models.ForeignKey(Host, on_delete=models.PROTECT)
    fqdn = models.CharField(max_length = 40, unique=True)

    class Meta:
        ordering = ['fqdn']
        unique_together = (("web_host", "fqdn"),)

    def get_webhost_name(self):
        return self.web_host.name
    get_webhost_name.short_description = 'Web Host Name'

    def get_webhost_ip(self):
        return self.web_host.get_netiface_ip()
    get_webhost_ip.short_description = 'IP Address'

    def __str__(self):
        return self.fqdn

@python_2_unicode_compatible
class Netiface(models.Model):
    host_id = models.OneToOneField(Host, on_delete=models.CASCADE, primary_key=True)
    mac = models.CharField(max_length = 17, blank=True)
    ip = models.CharField(max_length = 15, validators = [validate_ipv4_address], blank=True)
    iface_name = models.CharField(max_length = 10, blank=True)

    class Meta:
        ordering = ['ip']

    def __str__(self):
        return self.ip

@python_2_unicode_compatible
class Service(models.Model):
    name = models.CharField(max_length = 10, unique=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

@python_2_unicode_compatible
class HostOS(models.Model):
    name = models.CharField(max_length = 10)
    version = models.CharField(max_length = 10, blank=True)

    class Meta:
        ordering = ['name']
        unique_together = (("name", "version"),)

    def __str__(self):
        return self.name + "-" + self.version

@python_2_unicode_compatible
class SwitchOS(models.Model):
    name = models.CharField(max_length = 30, unique=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

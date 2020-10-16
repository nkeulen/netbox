import django_tables2 as tables
from django_tables2.utils import Accessor

from dcim.models import (
    ConsolePort, ConsoleServerPort, Device, DeviceBay, DeviceRole, FrontPort, Interface, InventoryItem, Platform,
    PowerOutlet, PowerPort, RearPort, VirtualChassis,
)
from tenancy.tables import COL_TENANT
from utilities.tables import (
    BaseTable, BooleanColumn, ButtonsColumn, ChoiceFieldColumn, ColorColumn, ColoredLabelColumn, LinkedCountColumn,
    TagColumn, ToggleColumn,
)
from .template_code import DEVICE_LINK, INTERFACE_IPADDRESSES, INTERFACE_TAGGED_VLANS

__all__ = (
    'ConsolePortTable',
    'ConsoleServerPortTable',
    'DeviceImportTable',
    'DeviceTable',
    'DeviceBayTable',
    'DeviceRoleTable',
    'FrontPortTable',
    'InterfaceTable',
    'InventoryItemTable',
    'PlatformTable',
    'PowerOutletTable',
    'PowerPortTable',
    'RearPortTable',
    'VirtualChassisTable',
)


#
# Device roles
#

class DeviceRoleTable(BaseTable):
    pk = ToggleColumn()
    device_count = LinkedCountColumn(
        viewname='dcim:device_list',
        url_params={'role': 'slug'},
        verbose_name='Devices'
    )
    vm_count = LinkedCountColumn(
        viewname='virtualization:virtualmachine_list',
        url_params={'role': 'slug'},
        verbose_name='VMs'
    )
    color = ColorColumn()
    vm_role = BooleanColumn()
    actions = ButtonsColumn(DeviceRole, pk_field='slug')

    class Meta(BaseTable.Meta):
        model = DeviceRole
        fields = ('pk', 'name', 'device_count', 'vm_count', 'color', 'vm_role', 'description', 'slug', 'actions')
        default_columns = ('pk', 'name', 'device_count', 'vm_count', 'color', 'vm_role', 'description', 'actions')


#
# Platforms
#

class PlatformTable(BaseTable):
    pk = ToggleColumn()
    device_count = LinkedCountColumn(
        viewname='dcim:device_list',
        url_params={'platform': 'slug'},
        verbose_name='Devices'
    )
    vm_count = LinkedCountColumn(
        viewname='virtualization:virtualmachine_list',
        url_params={'platform': 'slug'},
        verbose_name='VMs'
    )
    actions = ButtonsColumn(Platform, pk_field='slug')

    class Meta(BaseTable.Meta):
        model = Platform
        fields = (
            'pk', 'name', 'manufacturer', 'device_count', 'vm_count', 'slug', 'napalm_driver', 'napalm_args',
            'description', 'actions',
        )
        default_columns = (
            'pk', 'name', 'manufacturer', 'device_count', 'vm_count', 'napalm_driver', 'description', 'actions',
        )


#
# Devices
#

class DeviceTable(BaseTable):
    pk = ToggleColumn()
    name = tables.TemplateColumn(
        order_by=('_name',),
        template_code=DEVICE_LINK
    )
    status = ChoiceFieldColumn()
    tenant = tables.TemplateColumn(
        template_code=COL_TENANT
    )
    site = tables.Column(
        linkify=True
    )
    rack = tables.Column(
        linkify=True
    )
    device_role = ColoredLabelColumn(
        verbose_name='Role'
    )
    device_type = tables.LinkColumn(
        viewname='dcim:devicetype',
        args=[Accessor('device_type__pk')],
        verbose_name='Type',
        text=lambda record: record.device_type.display_name
    )
    primary_ip = tables.Column(
        linkify=True,
        verbose_name='IP Address'
    )
    primary_ip4 = tables.Column(
        linkify=True,
        verbose_name='IPv4 Address'
    )
    primary_ip6 = tables.Column(
        linkify=True,
        verbose_name='IPv6 Address'
    )
    cluster = tables.LinkColumn(
        viewname='virtualization:cluster',
        args=[Accessor('cluster__pk')]
    )
    virtual_chassis = tables.LinkColumn(
        viewname='dcim:virtualchassis',
        args=[Accessor('virtual_chassis__pk')]
    )
    vc_position = tables.Column(
        verbose_name='VC Position'
    )
    vc_priority = tables.Column(
        verbose_name='VC Priority'
    )
    tags = TagColumn(
        url_name='dcim:device_list'
    )

    class Meta(BaseTable.Meta):
        model = Device
        fields = (
            'pk', 'name', 'status', 'tenant', 'device_role', 'device_type', 'platform', 'serial', 'asset_tag', 'site',
            'rack', 'position', 'face', 'primary_ip', 'primary_ip4', 'primary_ip6', 'cluster', 'virtual_chassis',
            'vc_position', 'vc_priority', 'tags',
        )
        default_columns = (
            'pk', 'name', 'status', 'tenant', 'site', 'rack', 'device_role', 'device_type', 'primary_ip',
        )


class DeviceImportTable(BaseTable):
    name = tables.TemplateColumn(
        template_code=DEVICE_LINK
    )
    status = ChoiceFieldColumn()
    tenant = tables.TemplateColumn(
        template_code=COL_TENANT
    )
    site = tables.Column(
        linkify=True
    )
    rack = tables.Column(
        linkify=True
    )
    device_role = tables.Column(
        verbose_name='Role'
    )
    device_type = tables.Column(
        verbose_name='Type'
    )

    class Meta(BaseTable.Meta):
        model = Device
        fields = ('name', 'status', 'tenant', 'site', 'rack', 'position', 'device_role', 'device_type')
        empty_text = False


#
# Device components
#

class DeviceComponentTable(BaseTable):
    pk = ToggleColumn()
    device = tables.Column(
        linkify=True
    )
    name = tables.Column(
        linkify=True,
        order_by=('_name',)
    )
    cable = tables.Column(
        linkify=True
    )

    class Meta(BaseTable.Meta):
        order_by = ('device', 'name')


class ConsolePortTable(DeviceComponentTable):
    tags = TagColumn(
        url_name='dcim:consoleport_list'
    )

    class Meta(DeviceComponentTable.Meta):
        model = ConsolePort
        fields = ('pk', 'device', 'name', 'label', 'type', 'description', 'cable', 'tags')
        default_columns = ('pk', 'device', 'name', 'label', 'type', 'description')


class ConsoleServerPortTable(DeviceComponentTable):
    tags = TagColumn(
        url_name='dcim:consoleserverport_list'
    )

    class Meta(DeviceComponentTable.Meta):
        model = ConsoleServerPort
        fields = ('pk', 'device', 'name', 'label', 'type', 'description', 'cable', 'tags')
        default_columns = ('pk', 'device', 'name', 'label', 'type', 'description')


class PowerPortTable(DeviceComponentTable):
    tags = TagColumn(
        url_name='dcim:powerport_list'
    )

    class Meta(DeviceComponentTable.Meta):
        model = PowerPort
        fields = (
            'pk', 'device', 'name', 'label', 'type', 'description', 'maximum_draw', 'allocated_draw', 'cable', 'tags',
        )
        default_columns = ('pk', 'device', 'name', 'label', 'type', 'maximum_draw', 'allocated_draw', 'description')


class PowerOutletTable(DeviceComponentTable):
    tags = TagColumn(
        url_name='dcim:poweroutlet_list'
    )

    class Meta(DeviceComponentTable.Meta):
        model = PowerOutlet
        fields = ('pk', 'device', 'name', 'label', 'type', 'description', 'power_port', 'feed_leg', 'cable', 'tags')
        default_columns = ('pk', 'device', 'name', 'label', 'type', 'power_port', 'feed_leg', 'description')


class BaseInterfaceTable(BaseTable):
    enabled = BooleanColumn()
    ip_addresses = tables.TemplateColumn(
        template_code=INTERFACE_IPADDRESSES,
        orderable=False,
        verbose_name='IP Addresses'
    )
    untagged_vlan = tables.Column(linkify=True)
    tagged_vlans = tables.TemplateColumn(
        template_code=INTERFACE_TAGGED_VLANS,
        orderable=False,
        verbose_name='Tagged VLANs'
    )


class InterfaceTable(DeviceComponentTable, BaseInterfaceTable):
    tags = TagColumn(
        url_name='dcim:interface_list'
    )

    class Meta(DeviceComponentTable.Meta):
        model = Interface
        fields = (
            'pk', 'device', 'name', 'label', 'enabled', 'type', 'mgmt_only', 'mtu', 'mode', 'mac_address',
            'description', 'cable', 'tags', 'ip_addresses', 'untagged_vlan', 'tagged_vlans',
        )
        default_columns = ('pk', 'device', 'name', 'label', 'enabled', 'type', 'description')


class FrontPortTable(DeviceComponentTable):
    rear_port_position = tables.Column(
        verbose_name='Position'
    )
    tags = TagColumn(
        url_name='dcim:frontport_list'
    )

    class Meta(DeviceComponentTable.Meta):
        model = FrontPort
        fields = (
            'pk', 'device', 'name', 'label', 'type', 'rear_port', 'rear_port_position', 'description', 'cable', 'tags',
        )
        default_columns = ('pk', 'device', 'name', 'label', 'type', 'rear_port', 'rear_port_position', 'description')


class RearPortTable(DeviceComponentTable):
    tags = TagColumn(
        url_name='dcim:rearport_list'
    )

    class Meta(DeviceComponentTable.Meta):
        model = RearPort
        fields = ('pk', 'device', 'name', 'label', 'type', 'positions', 'description', 'cable', 'tags')
        default_columns = ('pk', 'device', 'name', 'label', 'type', 'description')


class DeviceBayTable(DeviceComponentTable):
    installed_device = tables.Column(
        linkify=True
    )
    tags = TagColumn(
        url_name='dcim:devicebay_list'
    )

    class Meta(DeviceComponentTable.Meta):
        model = DeviceBay
        fields = ('pk', 'device', 'name', 'label', 'installed_device', 'description', 'tags')
        default_columns = ('pk', 'device', 'name', 'label', 'installed_device', 'description')


class InventoryItemTable(DeviceComponentTable):
    manufacturer = tables.Column(
        linkify=True
    )
    discovered = BooleanColumn()
    tags = TagColumn(
        url_name='dcim:inventoryitem_list'
    )
    cable = None  # Override DeviceComponentTable

    class Meta(DeviceComponentTable.Meta):
        model = InventoryItem
        fields = (
            'pk', 'device', 'name', 'label', 'manufacturer', 'part_id', 'serial', 'asset_tag', 'description',
            'discovered', 'tags',
        )
        default_columns = ('pk', 'device', 'name', 'label', 'manufacturer', 'part_id', 'serial', 'asset_tag')


#
# Virtual chassis
#

class VirtualChassisTable(BaseTable):
    pk = ToggleColumn()
    name = tables.Column(
        linkify=True
    )
    master = tables.Column(
        linkify=True
    )
    member_count = LinkedCountColumn(
        viewname='dcim:device_list',
        url_params={'virtual_chassis_id': 'pk'},
        verbose_name='Members'
    )
    tags = TagColumn(
        url_name='dcim:virtualchassis_list'
    )

    class Meta(BaseTable.Meta):
        model = VirtualChassis
        fields = ('pk', 'name', 'domain', 'master', 'member_count', 'tags')
        default_columns = ('pk', 'name', 'domain', 'master', 'member_count')
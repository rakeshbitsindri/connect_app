from django.shortcuts import render
from ncclient import manager
import xmltodict

def index(request):
    device = {
        "host": "10.10.20.177",
        "port": "22",
        "username": "admin",
        "password": "admin",
    }

    with manager.connect(
        host=device["host"],
        port=device["port"],
        username=device["username"],
        password=device["password"],
        hostkey_verify=False,
        allow_agent=False,
        look_for_keys=False,
    ) as conn:
        interfaces_filter = '''
        <interfaces xmlns="http://openconfig.net/yang/interfaces">
            <interface></interface>
        </interfaces>
        '''
        interfaces = conn.get(filter=('subtree', interfaces_filter)).data_xml
        interfaces_dict = xmltodict.parse(interfaces)["rpc-reply"]["data"]
        physical_table_data = []
        port_channel_data = []

        for interface in interfaces_dict["interfaces"]["interface"]:
            name = interface["name"]
            if "config" in interface and "description" in interface["config"]:
                description = interface["config"]["description"]
            else:
                description = ""
            if "state" in interface and "oper-status" in interface["state"]:
                oper_status = interface["state"]["oper-status"]
            else:
                oper_status = ""
            if "state" in interface and "speed" in interface["state"]:
                speed = interface["state"]["speed"]
            else:
                speed = ""
            if "ether-options" in interface and "ieee-802.3ad" in interface["ether-options"]:
                if "bundle" in interface["ether-options"]["ieee-802.3ad"]:
                    port_channel = interface["ether-options"]["ieee-802.3ad"]["bundle"]["bundle-id"]
                    port_channel_data.append(
                        {
                            "name": name,
                            "status": oper_status,
                            "speed": speed,
                            "description": description,
                            "port_channel": port_channel,
                        }
                    )
            else:
                physical_table_data.append(
                    {"name": name, "status": oper_status, "speed": speed, "description": description}
                )

        vlan_filter = '''
        <vlans xmlns="http://openconfig.net/yang/vlan">
            <vlan></vlan>
        </vlans>
        '''
        vlans = conn.get(filter=('subtree', vlan_filter)).data_xml
        vlans_dict = xmltodict.parse(vlans)["rpc-reply"]["data"]
        vlan_data = []

        for vlan in vlans_dict["vlans"]["vlan"]:
            name = vlan["config"]["name"]
            status = vlan["state"]["status"]
            interfaces = vlan["members"]["member"]
            for interface in interfaces:
                vlan_data.append({"name": interface, "status": status})

    context = {
        "physical_table_data": physical_table_data,
        "vlan_data": vlan_data,
        "port_channel_data": port_channel_data,
    }

    return render(request, "arista_data.html", context)

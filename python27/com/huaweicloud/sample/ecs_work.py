# -*-coding:utf-8 -*-
from openstack import connection
import requests
from openstack import utils
import sys

# open debug mode
# utils.enable_logging(debug=True, stream=sys.stdout)

# igore ssl warnning
requests.packages.urllib3.disable_warnings()

domain = "myhuaweicloud.com"  # cdn use: domain = "myhwclouds.com"
region = "cn-north-1"         # example: region = "cn-north-1"

def handler(event, context):
    logger = context.getLogger()

    ak = context.getAccessKey()
    sk = context.getSecretKey()
    projectId = context.getProjectID()
    logger = context.getLogger()

    if ak == "" or sk == "":
        logger.error("Failed to operate because no temporary AK, SK, or token has been obtained. Please set an agency.")
        return ("Failed to operate because no temporary AK, SK, or token has been obtained. Please set an agency.")

    if projectId == "":
        logger.error("Failed to aoperate because projectId is empty")
        return ("Failed tooperate because projectId is empty.")

    # create connection
    conn = connection.Connection(verify=False,
                                 project_id=projectId,
                                 domain=domain,
                                 region=region,
                                 ak=ak,
                                 sk=sk)

    # example for list server
    server = list_servers(conn, 2)
    print(server)
    return None


# create server
def create_server(_conn):
    # here is ecs create server api wiki[https://support.huaweicloud.com/api-ecs/ecs_02_0101.html]
    # en-us : https://support.huaweicloud.com/en-us/api-ecs/ecs_02_0101.html
    data = {
        "availability_zone": "az1.dc1",
        "name": "kk",
        "imageRef": "###############",
        "root_volume": {
            "volumetype": "SATA"
        },
        "data_volumes": [
            {
                "volumetype": "SATA",
                "size": 50
            },
            {
                "volumetype": "SSD",
                "size": 10,
                "multiattach": "true",
                "hw:passthrough": "false"
            }
        ],
        "isAutoRename": "true",
        "flavorRef": "c1.xlarge",
        "personality": [
            {
                "path": "/etc/banner.txt",
                "contents": "ICAgICAgDQoiQmFjaA=="
            }
        ],
        "security_groups": [
            {
                "id": "#####################"
            }
        ],
        "vpcid": "##############",
        "nics": [
            {
                "subnet_id": "#############"
            }
        ],
        "publicip": {
            "eip": {
                "iptype": "5_bgp",
                "bandwidth": {
                    "size": 1,
                    "sharetype": "PER"
                }
            }
        },
        "key_name": "KeyPair-1565",
        "count": 1,
        "metadata": {
            "ss": "ss"
        },
        "extendparam": {
            "chargingMode": "postPaid",
            "periodType": "month",
            "periodNum": 1,
            "isAutoRenew": "true",
            "isAutoPay": "true",
            "regionID": "southchina"
        },
        "os:scheduler_hints": {
            "group": "###################"
        }
    }


    server = _conn.compute.create_server(**data)
    return server


# get list of server
def list_servers(_conn, limit=1):
    servers = _conn.compute.servers(limit=limit)
    for server in servers:
        print(server)


# show server detail
def show_server(_conn, server_id):
    server = _conn.compute.get_server(server_id)
    return server

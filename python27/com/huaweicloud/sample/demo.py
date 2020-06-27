# -*-coding:utf-8 -*-

from openstack import connection
import requests
import sys
from openstack import utils

# open debug mode
# utils.enable_logging(debug=True, stream=sys.stdout)

# igore ssl warnning
requests.packages.urllib3.disable_warnings()

domain = "myhuaweicloud.com"  # cdn use: domain = "myhuaweicloud.com"
region = "cn-north-1"  # example: region = "cn-north-1"


def handler(event, context):
    ak = context.getAccessKey()
    sk = context.getSecretKey()
    projectId = context.getProjectID()

    logger = context.getLogger()

    if ak == "" or sk == "":
        logger.error(
            "Failed to access EVS because no temporary AK, SK, or token has been obtained. Please set an agency.")
        return ("Failed to access EVS because no temporary AK, SK, or token has been obtained. Please set an agency.")

    if projectId == "":
        logger.error("Failed to access EVS because projectId is empty")
        return ("Failed to access EVS because projectId is empty.")

    conn = connection.Connection(verify=False,
                                 project_id=projectId,
                                 domain=domain,
                                 region=region,
                                 ak=ak,
                                 sk=sk)
    create_volume_by_args(conn)


# create volume
def create_volume_by_args(_conn):
    data = {
        "availability_zone": "az1.dc1",
        "size": 10,
        "name": "volume_by_no_resource_key",
        "volume_type": "SSD",
        "count": 1,
        "metadata": {
            "__system__encrypted": "0",
            "hw:passthrough": "false"
        },
        "multiattach": True
    }

    ff = _conn.evs.create_volume(**data)
    print(ff)


# get volume
def get_volume(_conn, volume_id):
    detail = _conn.evs.get_volume(volume_id)
    print(detail.name)


# list volume
def list_volumes_with_limit(_conn, limit):
    generator = _conn.evs.volumes(paginated=False, limit=limit)
    for volumes_list in generator:
        for volume in volumes_list.volumes:
            print(volume['name'])


# update volume
def update_volume_data(_conn, volume_id, data=None):
    if data == None:
        data = {
            "name": "update_name_by_sdk",
            "description": "update_description_by_sdk",
        }
    cls = _conn.evs.update_volume(volume_id, **data)
    print(cls)


# versions
def versions(_conn):
    print(type(_conn.evs.get_version("v2")))
    for index in _conn.evs.get_version("v2"):
        print(index)

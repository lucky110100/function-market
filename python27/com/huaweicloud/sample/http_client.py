# -*- coding:utf-8 -*-

import requests, json

def get_token():
    github_url = "https://iam.cn-north-1.myhuaweicloud.com/v3/auth/tokens"
    data = json.dumps({})
    r = requests.post(github_url, data)
    print r.headers.get("X-Subject-Token")
    print str(r.headers)
    print str(r.content)


def get_vm_list():
    token = ""
    headers = {"Content-Type": "application/json;charset=UTF-8", "X-Auth-Token": token}
    url = "https://ecs.cn-north-1.myhuaweicloud.com/v1/da2d96081e954e42b900edbe2dc27b2b/cloudservers/detail?offset=1&limit=10"
    r = requests.get(url, headers=headers)
    print r.text

if __name__ == "__main__":
    get_token()
    # get_vm_list()
# -*- coding:utf-8 -*-

import json
import requests

def handler(event, context):
    return get_token(event['user_name'], event['user_pwd'], event['domain_name'], event['project_name'])


def get_token(user_name, user_pwd, domain_name, project_name):
    iam_url = "https://iam.cn-north-1.myhuaweicloud.com/v3/auth/tokens"
    data = json.dumps({
        "auth": {
            "identity": {
                "methods": [
                    "password"
                ],
                "password": {
                    "user": {
                        "domain": {
                            "name": user_name
                        },
                        "name": domain_name,
                        "password": user_pwd
                    }
                }
            },
            "scope": {
                "project": {
                    "name": project_name
                }
            }
        }
    })
    r = requests.post(iam_url, data)
    # print str(r.headers)
    # print str(r.content)
    # print r.headers.get("X-Subject-Token")
    return r.headers.get("X-Subject-Token")

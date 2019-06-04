"""
for making and deleting the group only
"""

import requests
import pandas as pd

BASE_URL = "https://westus.api.cognitive.microsoft.com/face/v1.0"
SUBSCRIPTION_KEY = "d86f335d754946b7a54529b6aa4a14b4"
GROUP_NAME = "avactress"

#  delete the person group
def deleteGroup():
    end_point = BASE_URL + "/persongroups/" + GROUP_NAME
    headers = {
        "Ocp-Apim-Subscription-Key": SUBSCRIPTION_KEY
    }
    r = requests.delete(
        end_point,
        headers=headers
    )
    print(r.text)


# Send a request to make a group
def makeGroup():
    end_point = BASE_URL + "/persongroups/" + GROUP_NAME
    payload = {
        "name": GROUP_NAME
    }
    headers = {
        "Ocp-Apim-Subscription-Key": SUBSCRIPTION_KEY
    }
    r = requests.put(  # PUTリクエスト
        end_point,
        headers=headers,
        json=payload
    )
    print(r.text)






import requests
import pandas as pd
from time import sleep

BASE_URL = "https://westus.api.cognitive.microsoft.com/face/v1.0"
SUBSCRIPTION_KEY = "d86f335d754946b7a54529b6aa4a14b4"
GROUP_NAME = "avactress"


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

# add people to the group
def makePerson(name):
    end_point = BASE_URL + "/persongroups/" + GROUP_NAME + "/persons"
    headers = {
        "Ocp-Apim-Subscription-Key": SUBSCRIPTION_KEY
    }
    payload = {
        "name": name
    }
    r = requests.post(
        end_point,
        headers=headers,
        json=payload
    )
    try:
        personId = r.json()["personId"]
    except Exception as e:
        personId = None
        print(r.json()["error"])
    return personId


# add images to each actress
def addFaceToPerson(personId, imageUrl):
    if personId != None:
        end_point = BASE_URL + "/persongroups/" + GROUP_NAME + "/persons/" + personId + "/persistedFaces"
        print(end_point)
        headers = {
            "Ocp-Apim-Subscription-Key": SUBSCRIPTION_KEY
        }
        payload = {
            "url": imageUrl
        }
        r = requests.post(
            end_point,
            headers=headers,
            json=payload
        )
        try:
            persistedFaceId = r.json()["persistedFaceId"]
            print("Successfuly added face to person")
        except Exception as e:
            print("Failed to add a face to person")
            persistedFaceId = None
        return persistedFaceId
    else:
        print("personId is not set")
        return None


# learning the images
def trainGroup(groupId):
    end_point = BASE_URL + "/persongroups/" + GROUP_NAME + "/train"
    headers = {
        "Ocp-Apim-Subscription-Key": SUBSCRIPTION_KEY
    }
    r = requests.post(
        end_point,
        headers=headers,
    )
    print(r.text)


# detect the features of the sent image
def detectFace(imageUrl):
    end_point = BASE_URL + "/detect"
    headers = {
        "Ocp-Apim-Subscription-Key": SUBSCRIPTION_KEY
    }
    payload = {
        "url": imageUrl
    }
    r = requests.post(
        end_point,
        json=payload,
        headers=headers
    )
    try:
        faceId = r.json()[0]["faceId"]  # 0 means that the first parameter is the index
        print("faceId Found: {}".format(faceId))
        return r.json()[0]
    except Exception as e:
        print("faceId not found:{}".format(e))
        return None


# Find the most similar face in the person group
def identifyPerson(faceId):
    end_point = BASE_URL + "/identify"
    headers = {
        "Ocp-Apim-Subscription-Key": SUBSCRIPTION_KEY
    }
    faceIds = [faceId]
    payload = {
        "faceIds": faceIds,
        "personGroupId": GROUP_NAME,
    }
    r = requests.post(
        end_point,
        json=payload,
        headers=headers
    )
    print (r.text)
    return r.json()





# get the info of the person from her person ID
def getPersonInfoByPersonId(personId):
    end_point = BASE_URL + "/persongroups/" + GROUP_NAME + "/persons/" + personId
    headers = {
        "Ocp-Apim-Subscription-Key": SUBSCRIPTION_KEY
    }
    r = requests.get(
        end_point,
        headers=headers,
    )
    return r.json()


if __name__ == "__main__":  # if python runs this file directly
    """
    df = pd.read_csv("final.csv", index_col=0)
    df2 = pd.read_csv("learning-default.csv", index_col=0)
    for i, row in df.iterrows():
        name = row["name"]
        image = row["image"]
        dmmimage = row["dmmimage"]

        #  実行部分
        #  一分当たりの呼び出し回数20
        personId = makePerson(name)  # get a personId
        addFaceToPerson(personId, image)  # add an image to the person with the personId
        addFaceToPerson(personId, dmmimage)
        se = pd.Series([name, image, dmmimage, personId], ["name", "image", "dmmimage", "personId"])
        df2 = df2.append(se, ignore_index=True)
        print(df2)
    
    """

    """
    trainGroup(GROUP_NAME)  # train the faces
    """

    image = "http://www.shokyo.jp/wp-content/uploads/2015/10/%E9%A1%94%E5%86%99%E7%9C%9F.jpg"
    faceId = detectFace(image)
    person = identifyPerson(faceId["faceId"])
    if person[0]["candidates"]:  # 学習データに候補があれば
        personId = person[0]["candidates"][0]["personId"]
        personInfo = getPersonInfoByPersonId(personId)
        print(personInfo["name"])
    else:
        print("No candidates found")


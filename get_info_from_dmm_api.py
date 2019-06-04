import pandas as pd
import requests

# setting for API
DMM_AFFILIATE_ID = "Carlos-999"
DMM_API_ID = "kacVr4K4gdmK4VDEP0AE"
API_END_POINT = "https://api.dmm.com/affiliate/v3/ActressSearch?api_id=" + DMM_API_ID + "&affiliate_id=" + DMM_AFFILIATE_ID + "&keyword={}" + "&output=json"

# Counter
count = 0
skipped_count = 0

# DataFrames
df1 = pd.read_csv("output.csv")
df = pd.read_csv("default.csv", index_col=0)
for i, rows in df1.iterrows():
    name = rows["name"]
    image = rows["image"]
    try:
        end_point = API_END_POINT.format(name)
        r = requests.get(end_point)
        data = r.json()
        actress = data["result"]["actress"][0]["name"]
        if name == actress:
            dmmimage = data["result"]["actress"][0]["imageURL"]["large"]
            birthday = data["result"]["actress"][0]["birthday"]
            height = data["result"]["actress"][0]["height"]
            B = data["result"]["actress"][0]["bust"]
            C = data["result"]["actress"][0]["cup"]
            W = data["result"]["actress"][0]["waist"]
            H = data["result"]["actress"][0]["hip"]
            print("name={}".format(name))
            print("image={}".format(image))
            print("dmmimage={}".format(dmmimage))
            print("height={}".format(height))
            print("birthday={}".format(birthday))
            print("bust={}".format(B))
            print("cup={}".format(C))
            print("hip={}".format(H))
            print("waist={}".format(W))
    except Exception as e:
        print(e)
        skipped_count +=1
        print("{}をスキップしました：スキップ数：{}".format(name,skipped_count))
        dmmimage = ""
        birthday = ""
        height = ""
        B = ""
        C = ""
        H = ""
        W = ""
    se = pd.Series([name,image,dmmimage,height,birthday,B,C,W,H],["name","image", "dmmimage","height","birthday","B","C","W","H"])
    df = df.append(se,ignore_index=True)
    print(df)
df.to_csv("final.csv")
print("DONE")

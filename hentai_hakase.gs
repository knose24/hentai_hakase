///Importing the property
var PROPERTIES = PropertiesService.getScriptProperties()

///Line APIの設定
var LINE_ACCESS_TOKEN = PROPERTIES.getProperty("LINE_ACCESS_TOKEN")
var LINE_END_POINT = "https://api.line.me/v2/bot/message/reply"
///イベントに対して応答メッセージを送るAPI

///Microsoft Zure Face APIの設定
var FACE_API_SUBSCRIPTION_KEY = PROPERTIES.getProperty("FACE_API_SUBSCRIPTION_KEY")
var FACE_API_PERSON_GROUP = "avactress"
var FACE_API_BASE_END_POINT = "https://westus.api.cognitive.microsoft.com/face/v1.0/"

///DMM API
var DMM_API_ID = PROPERTIES.getProperty("DMM_API_ID")
var DMM_AFFILIATE_ID = PROPERTIES.getProperty("AFFILIATE_ID")

///わからない設定
var reply_token;
var imageUrl;
var id;

///Line endpoint
function doGet() {
 return HtmlService.createTemplateFromFile("test.html").evaluate();
}

///activated when POST request is received from LINE
function doPost(e){
  if (typeof e === "undefined") {
    imageEndPoint = "http://eropalace21.com/wordpress/wp-content/uploads/2016/01/sakuramana_thumb.jpg"
  } else{
  ///when getting a URL from LINE
    var json = JSON.parse(e.postData.contents);
    //var json = e.postData.contents;
    reply_token = json.events[0].replyToken;
    imageEndPoint = json.events[0].message.text;
  }
  Logger.log("以下のURLから、画像を取得します：" + imageEndPoint)
  //ログは出力時間と出力結果を表す
  console.log(imageEndPoint)
  //return imageEndPoint
  try {
  //画像データ取得
    var faceId = detectFaceId(imageEndPoint)
    var personIdAndConfidence = getPersonIdAndConfidence(faceId)
    var personId = personIdAndConfidence["personId"]
    var confidence = personIdAndConfidence["confidence"]
    var name = getActressName(personId)

    var profileImageUrlAndItemsInfoUrl = getProfileImageUrlAndItemsInfoUrl(name)
    var profileImageUrl = profileImageUrlAndItemsInfoUrl["profileImageUrl"]
    var itemsInfoUrl = profileImageUrlAndItemsInfoUrl["itemInfoUrl"]

    sendLine(name, confidence, profileImageUrl, itemsInfoUrl)
  } catch(err) {
    Logger.log("Error：" + err)
    sendLine(name, undefined, undefined, undefined)
  }
}


function detectFaceId(uri){
 end_point = FACE_API_BASE_END_POINT + "detect"
 try {
   payload = {
     "url":uri
   }
   headers = {
     "Ocp-Apim-Subscription-Key": FACE_API_SUBSCRIPTION_KEY,
     "Content-Type": "application/json"
   };
   var res = UrlFetchApp.fetch(
     end_point,
     {
       'method': 'POST',
       'headers': headers,
       'payload': JSON.stringify(payload)
     }
   );
   res = JSON.parse(res)
   faceId = res[0]["faceId"]
   Logger.log("faceId: " + faceId)
   return faceId
 } catch (e){
   Logger.log("faceIdの取得に失敗しました")
   Logger.log("エラーメッセージ：" + e)
   throw new Error(e);
   //return new Error(e);
 }
}

function getPersonIdAndConfidence(faceId){
  end_point = FACE_API_BASE_END_POINT + "identify"
  try{
    headers = {
      "Ocp-Apim-Subscription-Key": FACE_API_SUBSCRIPTION_KEY,
      "Content-Type": "application/json"
    }
    var faceIds = [faceId]
    payload = {
      "personGroupId": FACE_API_PERSON_GROUP,
      "faceIds": faceIds,
    }
    var res = UrlFetchApp.fetch(
      end_point,
      {
        "method":"POST",
        "headers":headers,
        "payload":JSON.stringify(payload),
      }
    );
    res = JSON.parse(res)
    var personId = res[0]["candidates"][0]["personId"]
    var confidence = res[0]["candidates"][0]["confidence"]
    Logger.log("personIdを取得しました: " + personId )
    Logger.log("confidenceを取得しました: " + confidence)
    personIdAndConfidence = {
      "personId": personId,
      "confidence": confidence
    }
    return personIdAndConfidence;
  }catch(e){
    Logger.log("personId,confidenceの取得に失敗しました")
    Logger.log(e)
    throw new Error(e);
    return e
  }
}

function getActressName(personId){
  end_point = FACE_API_BASE_END_POINT + "persongroups/" + FACE_API_PERSON_GROUP + "/persons/" + personId
  try{
    headers = {
      "Ocp-Apim-Subscription-Key": FACE_API_SUBSCRIPTION_KEY,
    }
    res = UrlFetchApp.fetch(
    end_point,
      {
        "method":"GET",
        "headers":headers,
      }
    );
    res = JSON.parse(res)
    name = res["name"]
    Logger.log("女優名を取得しました: " + name)
   return name;
 } catch (e){
   Logger.log("女優名を取得できませんでした")
   Logger.log(e)
   throw new Error(e);
   return e
 }
}

function getProfileImageUrlAndItemsInfoUrl(name){
  try{
    var encoded_query = encodeURI(name);
    Logger.log("encoded uri: " + encoded_query)
    var DMM_end_point = "https://api.dmm.com/affiliate/v3/ActressSearch?"
    + "api_id=" + DMM_API_ID
    + "&affiliate_id=" + DMM_AFFILIATE_ID
    + "&keyword=" + encoded_query
    + "&output=json"
    var response = UrlFetchApp.fetch(DMM_end_point)
    Logger.log("got response from dmm: " + response)
    var txt = response.getContentText();
    var json = JSON.parse(txt)
    var actress = json.result.actress[0]
    Logger.log("actress: " + actress)
    var profileImageUrl = actress.imageURL.large
    profileImageUrl = profileImageUrl.replace(/^http?\:\/\//i, "https://");

    ///なぜ必要？
    Logger.log("プロフィール画像を取得しました：" + profileImageUrl)
    var itemsInfoUrl = actress.listURL.digital
    itemsInfoUrl = itemsInfoUrl.replace(/^http?\:\/\//i, "https://");
    Logger.log("女優情報詳細ページURLを取得しました： " + itemsInfoUrl)
    var profileImageUrlAndItemsInfoUrl = {
      "profileImageUrl":profileImageUrl,
      "itemInfoUrl":itemsInfoUrl,
    }
    return profileImageUrlAndItemsInfoUrl;
  } catch (e){
    Logger.log("プロフィール写真と、女優情報詳細ページURLが取得できませんでした:" + e)
    throw new Error(e);
    return e
  }
}


function sendLine(name, confidence, actressImageUrl, actressInfoUrl){

 Logger.log("name: "+ name)
 Logger.log("confidence: "+ confidence)
 Logger.log("actressImageUrl: "+ actressImageUrl)
 Logger.log("actressInfoUrl:" + actressInfoUrl)
 if (typeof confidence === "undefined"){
   var messages = [{
     "type": "template",
     "altText": "すまん、みつからんかったのじゃ",
     "template": {
       "type": "buttons",
       "thumbnailImageUrl": 'https://media.npr.org/assets/img/2016/03/29/ap_090911089838_sq-3271237f28995f6530d9634ff27228cae88e3440-s1100-c15.jpg',
       "title": "あなたのスケベな願望に答えられませんでした。",
       "text": "一致するAV女優が見つかりませんでした。とりあえずPornHubで抜いてください",
       "actions": [
       {
       "type": "uri",
       "label": "PornHubへ",
       "uri": "https://pornhub.com"
     }
     ]
   }
   }];

 } else {
   var messages = [{
     "type": "template",
     "altText": "おすすめのAV女優はこれじゃ。",
     "template": {
       "type": "buttons",
       "thumbnailImageUrl": actressImageUrl,
       "title": name,
       "text": "一致度は" + (Math.round(confidence * 100)) + "%じゃ",
       "actions": [
       {
       "type": "uri",
       "label": "動画一覧ページに移動！",
       "uri": actressInfoUrl
     }
     ]
   }
   }];
  }
 try {
   UrlFetchApp.fetch(LINE_END_POINT, {
     'headers': {
       'Content-Type': 'application/json; charset=UTF-8',
       'Authorization': 'Bearer ' + LINE_ACCESS_TOKEN,
     },
     'method': 'post',
     'payload': JSON.stringify({
       'replyToken': reply_token,
       'messages': messages,
     }),
   });
   return ContentService.createTextOutput(JSON.stringify({'content': 'post ok'})).setMimeType(ContentService.MimeType.JSON);
 } catch (e){
   Logger.log("LINEへのメッセージ送信に失敗しました")
   Logger.log(e)
 }
}

function sendLineLog(log){
   var messages = [{
     "type": "text",
     "text": log,
   }];

 try {
   UrlFetchApp.fetch(LINE_END_POINT, {
     'headers': {
       'Content-Type': 'application/json; charset=UTF-8',
       'Authorization': 'Bearer ' + LINE_ACCESS_TOKEN,
     },
     'method': 'post',
     'payload': JSON.stringify({
       'replyToken': reply_token,
       'messages': messages,
     }),
   });
   return ContentService.createTextOutput(JSON.stringify({'content': 'post ok'})).setMimeType(ContentService.MimeType.JSON);
 } catch (e){
   Logger.log("LINEへのメッセージ送信に失敗しました")
   Logger.log(e)
 }
}
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)
import json
from linebot.models import *
from utli.LineEvent import LineEvent
from utli.User import User, states, groups
from utli.fireBase import dataBase
import utli.flexBuilder as flexBuilder
from utli.flow import startFlow, caseFlow, meetingFlow, issueFlow
def lineServer(event, db, endpoint):
    token = ""
    secret = ""
    channelId = ""
    destination = json.loads(event['body'])['destination']

    lineEvent = LineEvent(json.loads(event['body']))
    text = lineEvent.message.text
    
    doc = db.getConfigData_byCode(text).items()
    if(len(doc) > 0):
        id, doc = list(doc)[0]
        doc['destination'] = destination
        token = doc['token']
        secret = doc['secret']
        channelId = doc['channelId']
        db.updateConfigData(id,doc)
        line_bot_api = LineBotApi(token)
        handler = WebhookHandler(secret)
        message = TextSendMessage("驗證成功")
        line_bot_api.reply_message(lineEvent.replyToken, message)
        return 

    
    doc = db.getConfigData_byEndPoint(endpoint)
    
    if(len(doc) == 0):
        print('invalid destination')
        return
    for k, v in doc.items():
        token = v['token']
        secret = v['secret']
        channelId = v['channelId']
    print(token)
    print(secret)
    print(channelId)
    line_bot_api = LineBotApi(token)
    handler = WebhookHandler(secret)
    profile = line_bot_api.get_profile(lineEvent.source.userId)
    print(json.loads(event['body']))


    doc = db.getUserData(lineEvent.source.userId)
    if (doc == None):
        print('account not fond')
        db.newUserData(lineEvent.source.userId, profile)
        doc = db.getUserData(lineEvent.source.userId)
    user = db.doc2User(doc)

    if user.state == states.START.value:
        user = startFlow(user, db, line_bot_api, handler, lineEvent)
    else:
        if user.group == groups.MEETING.value:
            user = meetingFlow(user, db, line_bot_api, handler, lineEvent)
        elif user.group == groups.ISSUE.value:
            user = issueFlow(user, db, line_bot_api, handler, lineEvent)
        elif user.group == groups.CASE.value:
            user = caseFlow(user, db, line_bot_api, handler, lineEvent)

    db.updateUserData(user)
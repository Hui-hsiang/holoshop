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


def startFlow(user, db, line_bot_api, handler, lineEvent):
    text = lineEvent.message.text
    if (text == '新增會議記錄'):
        message = TextSendMessage("請輸入會議名稱")
        line_bot_api.reply_message(lineEvent.replyToken, message)
        user.state += 1
        user.group = groups.MEETING.value
    elif (text == '新增議題記錄'):
        message = TextSendMessage("請輸入議題名稱")
        line_bot_api.reply_message(lineEvent.replyToken, message)
        user.state += 1
        user.group = groups.ISSUE.value
    elif (text == '新增測試案例'):
        message = TextSendMessage("請輸入測試案例名稱")
        line_bot_api.reply_message(lineEvent.replyToken, message)
        user.state += 1
        user.group = groups.CASE.value
    elif (text == '帳號資訊'):
        message = TextSendMessage("coming soon")
        line_bot_api.reply_message(lineEvent.replyToken, message)
    elif (text == '查看會議記錄'):
        meeting = db.getMeetingData('all', True)
        contents = []
        for k,v in meeting.items():
            print(v)
            contents.append(flexBuilder.historyMeetingFlex(name = v['name'], date = v['time'], deadline = v['deadline'], item = v['item'], todo = v['todo'], id = k))
        if len(contents) != 0:
            carouselContents = {
                "type": "carousel",
                "contents": contents}
            line_bot_api.reply_message(lineEvent.replyToken,
                FlexSendMessage('會議記錄', carouselContents)
            )
        else:
            line_bot_api.reply_message(lineEvent.replyToken,
                TextSendMessage('目前沒有記錄喔')
            )
    elif (text == '查看議題記錄'):
        issue = db.getIssueData('all', True)
        contents = []
        for k,v in issue.items():
            print(v)
            contents.append(flexBuilder.historyIssueFlex(name = v['name'], id = k, deadline = v['deadline'], content = v['content'], owner = v['owner']))
        if len(contents) != 0:
            carouselContents = {
                "type": "carousel",
                "contents": contents}
            line_bot_api.reply_message(lineEvent.replyToken,
                FlexSendMessage('議題記錄', carouselContents)
            )
        else:
            line_bot_api.reply_message(lineEvent.replyToken,
                TextSendMessage('目前沒有記錄喔')
            )
    elif (text == '查看測試案例記錄'):
        cases = db.getCaseData('all', True)
        contents = []
        for k,v in cases.items():
            contents.append(flexBuilder.historyCaseFlex(name = v['name'], date= str(v['createDate']), case = v['case'], id = k))
        if len(contents) != 0:
            carouselContents = {
                "type": "carousel",
                "contents": contents}
            line_bot_api.reply_message(lineEvent.replyToken,
                FlexSendMessage('測試案例記錄', carouselContents)
            )
        else:
            line_bot_api.reply_message(lineEvent.replyToken,
                TextSendMessage('目前沒有記錄喔')
            )
    elif (text == '查看記錄'):
        carousel_template_message = TemplateSendMessage(
            alt_text='選擇您要查看的記錄內容',
            template=CarouselTemplate(
                columns=[
                    CarouselColumn(
                        thumbnail_image_url='https://i.imgur.com/Y5OwYWV.png',
                        title='查看記錄',
                        text='選擇您要查看的記錄內容',
                        actions=[
                            MessageAction(
                                label = '會議記錄',
                                text = '查看會議記錄'
                            ),
                            MessageAction(
                                label = '議題記錄',
                                text = '查看議題記錄'
                            ),
                            MessageAction(
                                label = '測試案例記錄',
                                text = '查看測試案例記錄'
                            ),
                        ]
                    )
                ]
            )
        )
        line_bot_api.reply_message(lineEvent.replyToken, carousel_template_message)
    else:
        message = TextSendMessage("點選下方menu來開始")
        line_bot_api.reply_message(lineEvent.replyToken, message)

    return user

def caseFlow(user, db, line_bot_api, handler, lineEvent):
    text = lineEvent.message.text
    case = db.getCaseData(user, finished = False)
    if (len(case) == 0):
        db.newCaseData(user)
        case = db.getCaseData(user, finished = False)
    case_id = list(case.keys())[0]
    case = case[case_id]
    if text == '取消':
        db.deleteDB('case', case_id)
        user.state = states.START.value
        user.group = groups.START.value
        message = TextSendMessage("點選下方menu來開始")
        line_bot_api.reply_message(lineEvent.replyToken, message)
        return user
    if (user.state == states.NEW_NAME.value):
        message = TextSendMessage("請輸入使用情境")
        line_bot_api.reply_message(lineEvent.replyToken, message)
        user.state += 1
        case['name'] = text
    elif user.state == states.NEW_CASE.value:
        if (text == '完成'):
            case['finished'] = True
            case['createDate'] = datetime.today()
            
            contents = [flexBuilder.historyCaseFlex(name = case['name'], date= str(case['createDate']), case = case['case'], id = case_id)]
            carouselContents = {
                    "type": "carousel",
                    "contents": contents}
            line_bot_api.reply_message(lineEvent.replyToken,
                FlexSendMessage('會議記錄', carouselContents)
            )
            user.state = states.START.value
            user.group = groups.START.value

            
        else:
            message = TextSendMessage("請輸入操作步驟")
            line_bot_api.reply_message(lineEvent.replyToken, message)
            user.state += 1
            scenario = {
                'name' : text,
                'step' : [],
                'result' : '',
                'stepNum' : 0
            }                
            case['case'].append(scenario)
            case['caseNum'] += 1
    elif (user.state == states.NEW_STEP.value):
        if (text == '完成'):
            message = TextSendMessage("請輸入測試結果")
            line_bot_api.reply_message(lineEvent.replyToken, message)
            user.state = states.NEW_RESULT.value
        else:
            message = TextSendMessage("請輸入測試反應")
            line_bot_api.reply_message(lineEvent.replyToken, message)
            user.state += 1
            step = {
                'text' : text,
                'react' : ''
            }
            case['case'][case['caseNum'] - 1]['step'].append(step)
            case['case'][case['caseNum'] - 1]['stepNum'] += 1
    elif (user.state == states.NEW_REACT.value):
        message = TextSendMessage("請輸入下個步驟，或輸入 \"完成\" 離開此情境")
        line_bot_api.reply_message(lineEvent.replyToken, message)
        user.state = states.NEW_STEP.value
        stepIndex = case['case'][case['caseNum'] - 1]['stepNum'] - 1
        case['case'][case['caseNum'] - 1]['step'][stepIndex]['react'] = text
    elif (user.state == states.NEW_RESULT.value):
        message = TextSendMessage("請輸入下個使用情境，或輸入 \"完成\" 結束填寫")
        line_bot_api.reply_message(lineEvent.replyToken, message)
        user.state = states.NEW_CASE.value
        case['case'][case['caseNum'] - 1]['result'] = text
    else:
        message = TextSendMessage("HI!  " + profile.display_name)
        line_bot_api.reply_message(lineEvent.replyToken, message)
    
    db.updateCaseData(case_id, case)
    print(case)
    return user

def meetingFlow(user, db, line_bot_api, handler, lineEvent):
    text = lineEvent.message.text
    meeting = db.getMeetingData(user, finished = False)
    print(meeting)
    if (len(meeting) == 0):
        db.newMeetingData(user)
        meeting = db.getMeetingData(user, finished = False)
    meeting_id = list(meeting.keys())[0]
    meeting = meeting[meeting_id]
    if text == '取消':
        db.deleteDB('meeting', meeting_id)
        user.state = states.START.value
        user.group = groups.START.value
        message = TextSendMessage("點選下方menu來開始")
        line_bot_api.reply_message(lineEvent.replyToken, message)
        return user
    if (user.state == states.NEW_NAME.value):
        message = TextSendMessage("請輸入會議時間")
        line_bot_api.reply_message(lineEvent.replyToken, message)
        user.state = states.INPUT_TIME.value
        meeting['name'] = text
    elif (user.state == states.INPUT_TIME.value):
        message = TextSendMessage("請輸入項目主題")
        line_bot_api.reply_message(lineEvent.replyToken, message)
        user.state += 1
        meeting['time'] = text
    elif (user.state == states.INPUT_SUBJECT.value):
        if (text == '完成'):
            message = TextSendMessage("記錄完成，請輸入待辦項目,如果沒有待辦項目請輸入 \'跳過\'")
            line_bot_api.reply_message(lineEvent.replyToken, message)
            user.state = states.INPUT_TODO.value
        else:
            message = TextSendMessage("請輸入項目內容")
            line_bot_api.reply_message(lineEvent.replyToken, message)
            user.state += 1
            item = {
                'name' : text,
                'content' : [],
                'contentNum' : 0
            }                
            meeting['item'].append(item)
            meeting['itemNum'] += 1
    elif (user.state == states.INPUT_CONTENT.value): 
        if (text == '完成'):
            message = TextSendMessage("請輸入下個項目主題，或輸入 \"完成\" 結束填寫")
            line_bot_api.reply_message(lineEvent.replyToken, message)
            user.state = states.INPUT_SUBJECT.value
        else:
            message = TextSendMessage("請輸入下個內容，或輸入 \"完成\" 結束填寫")
            line_bot_api.reply_message(lineEvent.replyToken, message)
            content = {
                'text' : text,
            }
            meeting['item'][meeting['itemNum'] - 1]['content'].append(content)
            meeting['item'][meeting['itemNum'] - 1]['contentNum'] += 1
    elif (user.state == states.INPUT_TODO.value):
        if (text == '完成' or text == '跳過'):
            message = TextSendMessage("請輸入預計完成日")
            line_bot_api.reply_message(lineEvent.replyToken, message)
            user.state = states.INPUT_DEADLINE.value
        else:
            message = TextSendMessage("請輸入代辦項目負責人")
            line_bot_api.reply_message(lineEvent.replyToken, message)
            todo = {
                'text' : text,
                'owner' : '',
            }
            meeting['todo'].append(todo)
            meeting['todoNum'] += 1
            user.state = states.INPUT_OWNER.value
    elif (user.state == states.INPUT_OWNER.value):
        message = TextSendMessage("請輸入下個待辦項目，或輸入\"完成\" 結束填寫")
        line_bot_api.reply_message(lineEvent.replyToken, message)
        meeting['todo'][meeting['todoNum'] - 1]['owner'] = text
        user.state = states.INPUT_TODO.value
    elif (user.state == states.INPUT_DEADLINE.value):        
        meeting['deadline'] = text 
        meeting['finished'] = True
        
        contents = [flexBuilder.historyMeetingFlex(name = meeting['name'], date = meeting['time'], deadline = meeting['deadline'], item = meeting['item'], todo = meeting['todo'], id = meeting_id)]
        carouselContents = {
                "type": "carousel",
                "contents": contents}
        line_bot_api.reply_message(lineEvent.replyToken,
            FlexSendMessage('會議記錄', carouselContents)
        )

        user.state = states.START.value
        user.group = groups.START.value
    db.updateMeetingData(meeting_id, meeting)
    return user

def issueFlow(user, db, line_bot_api, handler, lineEvent):
    text = lineEvent.message.text
    issue = db.getIssueData(user, finished = False)
    print(issue)
    if (len(issue) == 0):
        db.newIssueData(user)
        issue = db.getIssueData(user, finished = False)
    issue_id = list(issue.keys())[0]
    issue = issue[issue_id]
    if text == '取消':
        db.deleteDB('issue', issue_id)
        user.state = states.START.value
        user.group = groups.START.value
        message = TextSendMessage("點選下方menu來開始")
        line_bot_api.reply_message(lineEvent.replyToken, message)
        return user
    if (user.state == states.NEW_NAME.value):
        message = TextSendMessage("請輸入項目內容")
        line_bot_api.reply_message(lineEvent.replyToken, message)
        user.state = states.INPUT_CONTENT.value
        issue['name'] = text
    elif (user.state == states.INPUT_CONTENT.value):
        
        message = TextSendMessage("請輸入負責人員")
        line_bot_api.reply_message(lineEvent.replyToken, message)
        user.state = states.INPUT_OWNER.value
        issue['content'] = text
    elif (user.state == states.INPUT_OWNER.value):
        message = TextSendMessage("預計完成時間")
        line_bot_api.reply_message(lineEvent.replyToken, message)
        issue['owner'] = text
        user.state = states.INPUT_DEADLINE.value
    elif (user.state == states.INPUT_DEADLINE.value):        
        issue['deadline'] = text 
        issue['finished'] = True
        
        contents = [flexBuilder.historyIssueFlex(name = issue['name'], id = issue_id, deadline = issue['deadline'], content = issue['content'], owner = issue['owner'])]
        carouselContents = {
                "type": "carousel",
                "contents": contents}
        line_bot_api.reply_message(lineEvent.replyToken,
            FlexSendMessage('議題記錄', carouselContents)
        )
        

        user.state = states.START.value
        user.group = groups.START.value
    db.updateIssueData(issue_id, issue)
    return user


def historyCaseFlex(name, id, date, case): 
    
    
    case_step = []
    
    for c in case:
        caseContents = []
        caseContents.append({
                    "type": "text",
                    "text": 'name: ' + c['name'],
                    "size": "sm",
                    "wrap": True,
                    "color": "#555555"
                })
        caseContents.append({
                    "type": "text",
                    "text": 'result: ' + c['result'],
                    "size": "sm",
                    "wrap": True,
                    "color": "#555555"
                })
        
        stepContents = []        
        for s in c['step']:
            stepContents.append({
                        "type": "text",
                        "text": "text: " + s['text'],
                        "size": "sm",
                        "wrap": True,
                        "color": "#555555"
                    })
            stepContents.append({
                        "type": "text",
                        "text": "react: " + s['react'],
                        "size": "sm",
                        "wrap": True,
                        "color": "#555555"
                    })
        stepBox = {
                "type": "box",
                "layout": "vertical",
                "contents": stepContents
            }
        caseContents.append(stepBox)
        casebox = {
            "type": "box",
            "layout": "vertical",
            "contents": caseContents
        }
        case_step.append(casebox)

    contents ={
        "type": "bubble",
        "body": {
        "type": "box",
        "layout": "vertical",
        "contents": [
        {
            "type": "text",
            "text": "case紀錄",
            "weight": "bold",
            "color": "#1DB446",
            "size": "sm"
        },
        {
            "type": "text",
            "text": id,
            "weight": "bold",
            "color": "#1DB446",
            "size": "sm"
        },
        {
            "type": "text",
            "text": name,
            "weight": "bold",
            "size": "xxl",
            "margin": "md"
        },                                                                                                                                          
        {
            "type": "separator",
            "margin": "xxl"
        },
        {
            "type": "box",
            "layout": "vertical",
            "margin": "xxl",
            "spacing": "sm",
            "contents": [
            {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                {
                    "type": "text",
                    "text": date,
                    "size": "sm",
                    "color": "#555555",
                    "flex": 0
                }
                ]
            },
            {
                "type": "box",
                "layout": "vertical",
                "contents": case_step
            },
            
            ]
        }
        ]
        },
        "styles": {
            "footer": {
            "separator": True
            }
        }
        }
    return contents
def historyMeetingFlex(name, id, date, deadline, item, todo): 
    todos = []
    for i,t in enumerate(todo):
        todos.append(
        {
            "type": "box",
            "layout": "baseline",
            "spacing": "sm",
            "contents": [
                {
                    "type": "text",
                    "text": str(i+1) + ':',
                    "color": "#aaaaaa",
                    "size": "sm",
                    "flex": 1
                },
                {
                    "type": "text",
                    "text": t['text'],
                    "wrap": True,
                    "color": "#666666",
                    "size": "sm",
                    "flex": 5
                },
                {
                    "type": "text",
                    "text": 'owner' + t['owner'],
                    "wrap": True,
                    "color": "#666666",
                    "size": "sm",
                    "flex": 6,
                    "align": "end"
                },
            ]
        }
        )
    
    item_content = []
    for i,m in enumerate(item):
        itemContents = []
        itemContents.append(
        {
            "type": "box",
            "layout": "baseline",
            "spacing": "sm",
            "contents": [
                {
                    "type": "text",
                    "text": str(i+1) + ":",
                    "color": "#aaaaaa",
                    "size": "sm",
                    "flex": 0
                },
                {
                    "type": "text",
                    "text": m['name'],
                    "wrap": True,
                    "color": "#666666",
                    "size": "sm",
                    "flex": 5,
                    "align": "start"
                }
            ]
        })
        contentContents = []        
        for s in m['content']:
            contentContents.append(
            {
                "type": "box",
                "layout": "baseline",
                "spacing": "sm",
                "contents": [
                    {
                        "type": "text",
                        "text": "*",
                        "color": "#aaaaaa",
                        "size": "sm",
                        "flex": 1,
                        "align": "end"
                    },
                    {
                        "type": "text",
                        "text": s['text'],
                        "wrap": True,
                        "color": "#666666",
                        "size": "sm",
                        "flex": 5
                    }
                ]
            })    
        contentBox = {
                "type": "box",
                "layout": "vertical",
                "contents": contentContents
            }
        itemContents.append(contentBox)
        itembox = {
            "type": "box",
            "layout": "vertical",
            "contents": itemContents
        }
        item_content.append(itembox)

    contents ={
        "type": "bubble",
        "body": {
        "type": "box",
        "layout": "vertical",
        "contents": [
        {
            "type": "text",
            "text": "會議紀錄",
            "weight": "bold",
            "color": "#1DB446",
            "size": "sm"
        },
        {
            "type": "text",
            "text": '會議日期： ' + date,
            "weight": "bold",
            "color": "#1DB446",
            "size": "sm"
        },
        {
            "type": "text",
            "text": name,
            "weight": "bold",
            "size": "xxl",
            "margin": "md"
        },                                                                                                                                          
        {
            "type": "separator",
            "margin": "xxl"
        },
        {
            "type": "box",
            "layout": "vertical",
            "margin": "xxl",
            "spacing": "sm",
            "contents": [
            {
                "type": "box",
                "layout": "vertical",
                "contents": item_content
            },
            {
                "type": "text",
                "text": '待辦項目：',
                "weight": "bold",
                "size": "sm",
                "margin": "sm"
            },  
            {
                "type": "box",
                "layout": "vertical",
                "contents": todos
            },
            {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                {
                    "type": "text",
                    "text": '預計完成日期:' + deadline,
                    "size": "sm",
                    "color": "#555555",
                    "flex": 0
                }
                ]
            },
            
            ]
        }
        ]
        },
        "styles": {
            "footer": {
            "separator": True
            }
        }
        }
    return contents
def historyIssueFlex(name, id, deadline, content, owner):   
    contents ={
        "type": "bubble",
        "body": {
        "type": "box",
        "layout": "vertical",
        "contents": [
        {
            "type": "text",
            "text": "議題紀錄",
            "weight": "bold",
            "color": "#1DB446",
            "size": "sm"
        },
        {
            "type": "text",
            "text": '負責人員： ' + owner,
            "weight": "bold",
            "color": "#1DB446",
            "size": "sm"
        },
        {
            "type": "text",
            "text": name,
            "weight": "bold",
            "size": "xxl",
            "margin": "md"
        },                                                                                                                                          
        {
            "type": "separator",
            "margin": "xxl"
        },
        {
            "type": "box",
            "layout": "vertical",
            "margin": "xxl",
            "spacing": "sm",
            "contents": [
            {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                {
                    "type": "text",
                    "text": '內容:' + content,
                    "size": "sm",
                    "color": "#555555",
                    "flex": 0
                }
                ]
            },
            {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                {
                    "type": "text",
                    "text": '預計完成日期:' + deadline,
                    "size": "sm",
                    "color": "#555555",
                    "flex": 0
                }
                ]
            },
            
            ]
        }
        ]
        },
        "styles": {
            "footer": {
            "separator": True
            }
        }
        }
    return contents
def productList(name, price, img, describe):
    contents ={
        "type": "bubble",
        "hero": {
        "type": "image",
        "url": img,
        "size": "full",
        "aspectRatio": "20:20",
        "aspectMode": "cover",
        },
        "body": {
        "type": "box",
        "layout": "vertical",
        "contents": [
        {
            "type": "text",
            "text": name,
            "weight": "bold",
            "color": "#1DB446",
            "size": "xl"
        },
        {
            "type": "text",
            "text": str(price) + ' NTD',
            "size": "sm",
            "color": "#555555",
            "flex": 0,
            "align": "end"
        },                                                                                                                     
        {
            "type": "separator",
            "margin": "xxl"
        },
        {
            "type": "box",
            "layout": "vertical",
            "margin": "xxl",
            "spacing": "sm",
            "contents": [
            {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                {
                    "type": "text",
                    "text": describe,
                    "size": "sm",
                    "color": "#555555",
                    "flex": 0
                }
                ]
            },
            
            ]
        }
        ]
        },
        "footer": {
        "type": "box",
        "layout": "vertical",
        "spacing": "sm",
        "contents":[
        {
            "type": "button",
            "style": "link",
            "height": "sm",
            "action": {
                "type": "uri",
                "label": "CALL",
                "uri": "https://linecorp.com"
            }
        }   
        ],
        "flex": 0
        },
        "styles": {
            "footer": {
            "separator": True
            
            }
        }
    }
    return contents
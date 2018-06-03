from src.db.daily_report_table import insert_into_report_table, select_from_report_table
from src.db.admin_org_table import admin_org_handler
from datetime import datetime as T
from datetime import timedelta as dT
from copy import deepcopy
import requests
import json
import time
import os

slackToken = "wk6GW3p1fzUbC7gNHbgxtsYa"
# slackToken = os.environ['SLACK_TOKEN']
botAccessToken = "xoxb-374384770263-374217359473-SfFw7D91EQWKz5qaxfS1hJVZ"
# botAccessToken = os.environ['BOT_ACCESS_TOKEN']
hasuraDataUrl = "http://data.hasura/v1/query"
chatUrl = "https://slack.com/api/chat.postMessage"



message ={
     "text": "Weekly report "+":clap:"*5,
     "token": botAccessToken,
     "channel": "",
     "attachments": []
    }
attachments = {
                "fallback": ":confused:",
                "color": "#36a64f",
                "pretext": "",
                "author_name": "WS ReportBot",
                "author_link": "http://flickr.com/bobby/",
                "author_icon": "http://flickr.com/icons/bobby.jpg",
                "title": "",
                "text": "",
                "fields": [
                    {
                        "title": "",
                        "value": "",
                        "short": "false"
                    }
                ],
                "footer": "Slack API",
                "footer_icon": "https://platform.slack-edge.com/img/default_application_icon.png",
                "ts": ""
            }




aoh = admin_org_handler()


def generate_payload(report,channel,date):
    payload = deepcopy(message)
    for user in report:
        attachment = deepcopy(attachments)
        attachment["title"] = user["name"]
        attachment["fields"][0]["title"] += "Commits "+str(user["no_of_commits"])
        attachment["fields"][0]["value"] += "Lines Added "+str(user["lines_added"])+'\n'
        attachment["fields"][0]["value"] += "Lines Removed "+str(user["lines_removed"])+'\n'
        attachment["fields"][0]["value"] += "PR open "+str(user["pr_open"])+'\n'
        attachment["fields"][0]["value"] += "PR Closed "+str(user["pr_closed"])+'\n'
        attachment["ts"] = time.mktime(T.strptime(date, "%d %b %Y").timetuple())
        print(attachment["fields"][0])
        payload["attachments"].append(attachment)
        del attachment
    payload["channel"] = channel
    return payload

def sendSlackReport(report, channel,date):
    print(date)
    payload = generate_payload(report,channel,date)
    # print(payload)
    headers = {
        'content-type': "application/json",
        'Authorization': 'Bearer '+botAccessToken
    }

    response = requests.request("POST", chatUrl, data=json.dumps(payload), headers=headers)
    # print(response.json())
    return "Completed :comet:"


def sendSlackLangReport(report, channel):
    date = T.now().strftime("%d %h %Y")
    msg = ""
    for r in report:
        msg += "_*"+r["lang"]+'*_  '+ str(r["w1"])+",  "+str(r["w2"])+'\n'

    payload = deepcopy(message)
    
    attachment = deepcopy(attachments)
    attachment["title"] =  "This Week,   Last Week"
    attachment["fields"][0]["value"] += msg
    attachment["ts"] = time.mktime(T.strptime(date, "%d %b %Y").timetuple())

    payload["attachments"].append(attachment)
    payload["channel"] = channel
    del attachment
    # payload = generate_payload(report,channel)
    # print(payload)
    headers = {
        'content-type': "application/json",
        'Authorization': 'Bearer '+botAccessToken
    }

    response = requests.request("POST", chatUrl, data=json.dumps(payload), headers=headers)
    # # print(response.json())
    return ":lantern:"

def get_org_project_dict(headers):
    org_project_dict = {}
    org_project_list = aoh.get_org_project(headers)
    for i in org_project_list:
        try:
            org_project_dict[i['organization']].append(i['project'])
        except:
            org_project_dict[i['organization']] = []
            org_project_dict[i['organization']].append(i['project'])
    return org_project_dict

# def get_contributors_list(org_name, projects,headers):
#     # @parul add the code to fetch contributors of a particular org working on its projects
#     return [['mulx10',"Mehul Kumar Nirala"],['parulagg27',"Parul Aggarwal"]]
#     
import requests
import json
from datetime import datetime, timedelta
from src.db.admin_org_table import admin_org_handler
from src.utils.login import login

aoh = admin_org_handler()

url = "https://data.graveside44.hasura-app.io/v1/query"

def insert_into_report_table(json_object, headers, date):
    for user in json_object: 
        dict_json = json_object[user] 
        projects = dict_json["projects"]
        for project in projects:
            org_name, project = project.split('/')
            print(aoh.get_admin(project = project,headers=headers))
            admin = aoh.get_admin(project = project,headers=headers)[0]['admin_username']

            requestPayload = {
                "type": "insert",
                "args": {
                    "table": "daily_report_table",
                    "objects": [
                        {
                            "admin_username": admin,
                            "org_name": org_name,
                            "project": project,
                            "contributor_handle": user,
                            "avatar_url": dict_json["avatar_url"],
                            "contributor_name": dict_json["name"],
                            "no_of_commits": dict_json["no_of_commits"],
                            "pr_open": dict_json["pr_open"] ,
                            "pr_closed": dict_json["pr_closed"],
                            "languages": dict_json["languages"],
                            "lines_added": dict_json["lines_added"],
                            "lines_removed": dict_json["lines_removed"],
                            "commits":dict_json["commits"],
                            "date":date
                        }
                    ]
                }
            }
            resp = requests.request("POST", url, data=json.dumps(requestPayload), headers=headers)
            print (json.loads(resp.content.decode('utf-8')))


def select_from_report_table(user, since=None,until=None,headers=None):
    if since is None:
        requestPayload = {
            "type": "select",
            "args": {
                "table": "daily_report_table",
                "columns": [
                    "*"
                ],
                "where": {
                    "contributor_handle": {
                        "$eq": user
                    }
                }
            }
        }
    else:
        requestPayload = {
            "type": "select",
            "args": {
                "table": "daily_report_table",
                "columns": [
                    "*"
                ],
                "where": {
                    "contributor_handle": {
                        "$eq": user
                    },
                    "$and": [
                        {
                            "date": {
                                "$gt": since
                            }
                        },
                        {
                            "date": {
                                "$lte": until
                            }
                        }
                    ]
                }
            }
        }
    resp = requests.request("POST", url, data=json.dumps(requestPayload), headers=headers)
    return json.loads(resp.content.decode('utf-8'))


if __name__ == '__main__':
    # with open('../gh_scrape/stats.json', 'r') as f:
        # stats = json.load(f)

    headers = login('mehul','mehul@hasura')
    # insert_into_report_table(stats,headers)
    T = datetime.now()
    dT = timedelta(days=7)
    T = datetime(month=5,day=16,year=2018)
    since = (T-dT).strftime("%d %h %Y")
    until = T.strftime("%d %h %Y")
    print (select_from_report_table(user = 'mulx10',
                                    since = since,
                                    until = until,
                                    headers = headers))
    
import requests
import json
from datetime import datetime
from admin_org_table import admin_org_handler
from utils.login import login

aoh = admin_org_handler()

url = "https://data.graveside44.hasura-app.io/v1/query"

# This is the json payload for the query
def insert_into_report_table(json_object, headers, date):
    # print(json_object)
    for user in json_object: 
        dict_json = json_object[user] 
        projects = dict_json["projects"]
        for project in projects:
            org_name, project = project.split('/')
            # print(org_name,project)
            # admin = aoh.get_admin(project = project,headers=headers)
            admin = aoh.get_admin(project = project,headers=headers)[0]['admin_username']
            # print(admin)
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
            # print(requestPayload)
            resp = requests.request("POST", url, data=json.dumps(requestPayload), headers=headers)
            # Setting headers


            # Make the query and store response in resp

            # resp.content contains the json response.
            print json.loads(resp.content)


def select_from_report_table(user, headers):
    # This is the json payload for the query
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

    # Make the query and store response in resp
    resp = requests.request("POST", url, data=json.dumps(requestPayload), headers=headers)

    # resp.content contains the json response.
    # print resp.content
    return json.loads(resp.content)

if __name__ == '__main__':
    with open('../gh_scrape/stats.json', 'r') as f:
        stats = json.load(f)

    headers = login('mehul','mehul@hasura')
    insert_into_report_table(stats,headers)
    # select_from_report_table('mulx10')
    
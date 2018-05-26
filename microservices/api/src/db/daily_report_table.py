import requests
import json
from datetime import datetime
from admin_org_table import admin_org_handler

aoh = admin_org_handler()
# This is the url to which the query is made
url = "https://data.graveside44.hasura-app.io/v1/query"


headers = {
    "Content-Type": "application/json",
    "Authorization": "Bearer 85642c50c2a669a9c281f6ef65e3772f63e672dd7a0808b2",
    "X-Hasura-Role": "admin"
}

# This is the json payload for the query
def insert_into_report_table(json_object):
    for user in json_object: 
        dict_json = json_object[user] 
        projects = dict_json["projects"]
        for project in projects:
            admin = aoh.get_data(project = project).split(":")[1].split("}")[0].strip("\"")
            # print(admin)
            org_name, project = project.split('/')
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
                            "time":int(datetime.utcnow().strftime("%s"))
                        }
                    ]
                }
            }
            resp = requests.request("POST", url, data=json.dumps(requestPayload), headers=headers)
            # Setting headers


            # Make the query and store response in resp

            # resp.content contains the json response.
            print resp.content


def select_user_from_report_table(user):
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
    print resp.content
    return resp.content

if __name__ == '__main__':
    with open('../gh_scrape/stats.json', 'r') as f:
        stats = json.load(f)
    insert_into_report_table(stats)
    select_user_from_report_table('mulx10')
    
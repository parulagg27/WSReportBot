import requests
import json

class admin_org_handler(object):
    """docstring for admin_org_handler"""
    def __init__(self):
        super(admin_org_handler, self).__init__()
        # This is the url to which the query is made
        self.url = "https://data.graveside44.hasura-app.io/v1/query"

        # self.login()
        # This is the json payload for the query

    def add_project(self,admin_username,project,organization=None,headers=None):
        if organization is None:
            organization = project.split('/')[0]
        requestPayload = {
            "type": "insert",
            "args": {
                "table": "admin_org_table",
                "objects": [
                    {
                        "admin_username": admin_username,
                        "organization": organization,
                        "project": project
                    }
                ]
            }
        }
        resp = requests.request("POST", self.url, data = json.dumps(requestPayload), headers = headers)
        return json.loads(resp.content.decode('utf-8'))
    
    def get_admin(self,project,headers=None):
        requestPayload = {
            "type": "select",
            "args": {
                "table": "admin_org_table",
                "columns": [
                    "admin_username"
                ],
                "where": {
                    "project": {
                        "$eq": project
                    }
                }
            }
        }
        resp = requests.request("POST", self.url, data = json.dumps(requestPayload), headers = headers)
        return json.loads(resp.content.decode('utf-8'))
    
    def get_project(self,admin_username=None,project=None,headers=None):
        requestPayload = {
            "type": "select",
            "args": {
                "table": "admin_org_table",
                "columns": [
                    "organization",
                    "project"
                ],
                "where": {
                    "admin_username": {
                        "$eq": admin_username
                    }
                }
            }
        }
        resp = requests.request("POST", self.url, data = json.dumps(requestPayload), headers = headers)
        print(resp.content)
        return json.loads(resp.content.decode('utf-8'))
        
    def get_org_project(self,headers=None):
        requestPayload = {
            "type": "select",
            "args": {
                "table": "admin_org_table",
                "columns": [
                    "organization",
                    "project"
                ]
            }
        }
        resp = requests.request("POST", self.url, data = json.dumps(requestPayload), headers = headers)
        return json.loads(resp.content.decode('utf-8'))


if __name__ == '__main__':
    aoh = admin_org_handler()
    print (aoh.add_project(admin_username = 'mulx10', project = 'robocup-stp',organization='KRSSG'))
    print (aoh.get_data(project='robocup-stp-asia'))
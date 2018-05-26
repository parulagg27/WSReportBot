import requests
import json

class admin_org_handler(object):
    """docstring for admin_org_handler"""
    def __init__(self):
        super(admin_org_handler, self).__init__()
        # This is the url to which the query is made
        self.url = "https://data.graveside44.hasura-app.io/v1/query"

        self.login()

    def login(self):
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer 85642c50c2a669a9c281f6ef65e3772f63e672dd7a0808b2",
            "X-Hasura-Role": "admin"
        }
        # This is the json payload for the query

    def add_project(self,admin_username,project,organization=None):
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
        resp = requests.request("POST", self.url, data = json.dumps(requestPayload), headers = self.headers)
        return resp.content

    def get_data(self,admin_username=None,project=None):
        if admin_username is not None:
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
        if project is not None:
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
        resp = requests.request("POST", self.url, data = json.dumps(requestPayload), headers = self.headers)
        return resp.content

if __name__ == '__main__':
    aoh = admin_org_handler()
    print aoh.add_project(admin_username = 'mulx10', project = 'robocup-stp',organization='KRSSG')
    print aoh.get_data(project='robocup-stp-asia')
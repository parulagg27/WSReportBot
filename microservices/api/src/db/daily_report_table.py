import requests
import json

# This is the url to which the query is made
url = "https://data.graveside44.hasura-app.io/v1/query"

# This is the json payload for the query
requestPayload = {
    "type": "insert",
    "args": {
        "table": "daily_report_table",
        "objects": [
            {
                "admin_username": "mulx10",
                "project": "KRSSG/robocup",
                "contributor_handle": "mulx10",
                "avatar_url": "url",
                "contributor_name": "Mehul Kumar Nirala",
                "no_of_commits": "45",
                "pr_open": "0",
                "pr_closed": "10",
                "languages": "python",
                "lines_added": "10000",
                "lines_removed": "1200",
                "commits": "15"
            }
        ]
    }
}

# Setting headers
headers = {
    "Content-Type": "application/json",
    "Authorization": "Bearer 85642c50c2a669a9c281f6ef65e3772f63e672dd7a0808b2",
    "X-Hasura-Role": "admin"
}

# Make the query and store response in resp
resp = requests.request("POST", url, data=json.dumps(requestPayload), headers=headers)

# resp.content contains the json response.
print resp.content
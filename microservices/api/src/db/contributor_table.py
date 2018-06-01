import requests
import json

# This is the url to which the query is made
url = "https://data.graveside44.hasura-app.io/v1/query"

def add_contributor(headers,org_name,project_name,contributors):
	requestPayload = {
	    "type": "insert",
	    "args": {
	        "table": "project_contributors_table",
	        "objects": [
	            {
	                "org_name": org_name,
	                "project_name": project_name,
	                "contributors": contributors
	            }
	        ]
	    }
	}
	resp = requests.request("POST", url, data=json.dumps(requestPayload), headers=headers)
	return json.loads(resp.content.decode('utf-8'))

def get_contributors_list(headers,org_name,project_name):
	requestPayload = {
	    "type": "select",
	    "args": {
	        "table": "project_contributors_table",
	        "columns": [
	            "contributors"
	        ],
	        "where": {
	            "$and": [
	                {
	                    "org_name": {
	                        "$eq": org_name
	                    }
	                },
	                {
	                    "project_name": {
	                        "$eq": project_name
	                    }
	                }
	            ]
	        }
	    }
	}
	resp = requests.request("POST", url, data=json.dumps(requestPayload), headers=headers)
	contributors = json.loads(resp.content.decode('utf-8'))[0]['contributors']
	return contributors
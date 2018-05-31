from src.db.admin_org_table import admin_org_handler
from src.db.daily_report_table import insert_into_report_table, select_from_report_table
from datetime import datetime as T
from datetime import timedelta as dT
import os
import json

aoh = admin_org_handler()

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
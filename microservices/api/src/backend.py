from gh_scrape.generate_scrape import GHScrape
from db.admin_org_table import admin_org_handler
from db.daily_report_table import insert_into_report_table, select_from_report_table
from datetime import datetime
from datetime import timedelta
from utils.login import login
from utils.utils import get_org_project_dict,get_contributors_list
import os
import json
dT = timedelta(days=1)

headers = login('mehul','mehul@hasura')
aoh = admin_org_handler()

def generate_report(headers):
    T = datetime.now()
    # T = datetime(month=5,day=16,year=2018)
    date = T.strftime("%d %h %Y")
    since = str(T).split(' ')[0]+'T00:00:00Z'
    until = str(T+dT).split(' ')[0]+'T00:00:00Z'
    # since = '2017-11-21T00:00:00Z'
    # until = '2019-01-01T00:00:00Z'
    org_project_dict = get_org_project_dict(headers)
    for org_name in org_project_dict.keys():
        projects = org_project_dict[org_name]
        print(projects)
        ghs = GHScrape(org_name = org_name)
        ghs.add_project(projects = projects)
        contributors = get_contributors_list(org_name = org_name, projects = projects, headers = headers)
        for user,name in contributors:
            ghs.add_user(user = user,name = name)
        stats = ghs.run(since,until)
        # print(stats)
        insert_into_report_table(stats, headers, date)
    

generate_report(headers)




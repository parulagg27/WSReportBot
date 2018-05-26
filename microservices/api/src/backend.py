from gh_scrape.generate_scrape import GHScrape
from db.admin_org_table import admin_org_handler
from db.daily_report_table import insert_into_report_table, select_from_report_table
from datetime import datetime
from datetime import timedelta
from utils.login import login
from utils.utils import get_org_project_dict,get_contributors_list
import os
import json


headers = login('mehul','mehul@hasura') 
# headers = login('parul','parul@hasura') 

def generate_daily_report(headers):
    T = datetime.now()
    dT = timedelta(days=1)
    # T = datetime(month=5,day=16,year=2018)
    date = T.strftime("%d %h %Y")
    since = str(T-dT).split(' ')[0]+'T00:00:00Z'
    until = str(T).split(' ')[0]+'T00:00:00Z'

    org_project_dict = get_org_project_dict(headers)
    for org_name in org_project_dict.keys():
        projects = org_project_dict[org_name]
        print(projects)
        ghs = GHScrape(org_name = org_name)
        ghs.add_project(projects = projects)
        contributors = get_contributors_list( org_name = org_name, 
                                                projects = projects, 
                                                headers = headers)
        for user,name in contributors:
            ghs.add_user(user = user,name = name)
        stats = ghs.run(since,until)
        insert_into_report_table(stats, headers, date)

def get_weekly_report(org_name,headers):
    T = datetime.now()
    # T = datetime(month=5,day=16,year=2018)
    dT = timedelta(days=7)
    since = (T-dT).strftime("%d %h %Y")
    until = T.strftime("%d %h %Y")

    org_project_dict = get_org_project_dict(headers = headers)
    projects = org_project_dict[org_name]

    contributors = get_contributors_list(org_name = org_name, 
                                            projects = projects, 
                                            headers = headers)
    report = {}
    '''
    key : user
    value :{
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
    '''
    for user,name in contributors:
        # print(user)
        report[user] = select_from_report_table(user=user,
                                    since = since,
                                    until = until,
                                    headers = headers)
    return report


if __name__ == '__main__':
    # Run daily
    generate_report(headers)

    # Run Weekly
    get_weekly_report(org_name = 'KRSSG',headers = headers)



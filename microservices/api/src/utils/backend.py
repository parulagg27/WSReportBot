"""
This serves the backend part for WSReportbot
"""
from src.gh_scrape.generate_scrape import GHScrape
from src.db.admin_org_table import admin_org_handler
from src.db.daily_report_table import insert_into_report_table, select_from_report_table
from src.utils.login import login
from src.utils.utils import get_org_project_dict,get_contributors_list
from datetime import datetime
from datetime import timedelta
import os
import json




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
                "avatar_url": as the name suggests :p ,
                "contributor_name": same as above,
                "no_of_commits": same as above,
                "pr_open": same as above ,
                "pr_closed": same as above,
                "languages": languages in which the patch was written
                "lines_added": ^^,
                "lines_removed": :p,
                "commits": json containing commit as 
                    key : message
                    value : type: string (Message of the commit)

                    key : project
                    value : type: string (Project this commit belongs to)

                    key : html_url
                    value : type: string (Link for the url)

                    key : lines_added
                    value : type: int (Lines added in the commit)

                    key : lines_removed
                    value : type: int (Lines removed in the commit)
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
    headers = login('mehul','mehul@hasura') 
    # headers = login('parul','parul@hasura') 
    # Run daily
    generate_report(headers)

    # Run Weekly
    report = get_weekly_report(org_name = 'KRSSG',headers = headers)
    # @parul get the required data from the above function and display it on the channel.
    # My code is messy, feel free to ask doubts :) 



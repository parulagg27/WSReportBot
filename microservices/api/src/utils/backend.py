"""
This serves the backend part for WSReportbot
"""
from src.gh_scrape.generate_scrape import GHScrape
from src.gh_scrape.get_contributors import get_contributors_list
from src.db.admin_org_table import admin_org_handler
from src.db.daily_report_table import insert_into_report_table, select_from_report_table, select_language_from_report_table
from src.utils.login import login
from src.utils.utils import get_org_project_dict
from datetime import datetime
from datetime import timedelta
from collections import Counter
import os
import json


def get_lang_report(headers,T):
    dT = timedelta(days=7)
    since = (T-dT).strftime("%d %h %Y")
    until = T.strftime("%d %h %Y")
    lang_report = select_language_from_report_table(since = since, 
                                                    until = until, 
                                                    headers = headers)
    languages = []
    for lr in lang_report:
        languages.extend(lr['languages'])
    languages = dict(Counter(map(str,languages)))

    return languages

def get_language_report_week(headers,day = None):
    if day is None:
        T = datetime.now()
    else:
        T = day
    dT = timedelta(days=7)
    lang_report1 = get_lang_report(headers,T-dT)
    lang_report2 = get_lang_report(headers,T)

    language_report = []
    keys = list(lang_report1.keys())+list(lang_report2.keys())
    for key in keys:
        lang = {}
        try:
            w1 = lang_report1[key]
        except :
            w1 = 0
        try:
            w2 = lang_report2[key]
        except :
            w2 = 0
        lang['lang'] = str(key)
        lang['w1'] = w1 
        lang['w2'] = w2
        language_report.append(lang)
    return language_report







def generate_daily_report(headers,day = None):
    if day is None:
        T = datetime.now()
    else:
        T = day
    dT = timedelta(days=1)
    date = T.strftime("%d %h %Y")
    since = str(T-dT).split(' ')[0]+'T00:00:00Z'
    until = str(T).split(' ')[0]+'T00:00:00Z'

    org_project_dict = get_org_project_dict(headers)
    for org_name in org_project_dict.keys():
        projects = org_project_dict[org_name]
        print(projects)
        ghs = GHScrape(org_name = org_name)
        ghs.add_project(projects = projects)
        contributors = []
        for prj in projects:
            contributors.extend(get_contributors_list(org_name = org_name,project_name=prj))
        contributors = list(list(set(map(tuple, contributors))))
        for user,name in contributors:
            ghs.add_user(user = user.lower(),name = name)
            print(user,name)
        stats = ghs.run(since,until)
        try:
            insert_into_report_table(stats, headers, date)
        except Exception as e:
            print(e)

def get_weekly_report(org_name,headers,day=None):
    if day is None:
        T = datetime.now()
    else:
        T = day
    # T = datetime(month=5,day=16,year=2018)
    dT = timedelta(days=7)
    since = (T-dT).strftime("%d %h %Y")
    until = T.strftime("%d %h %Y")

    org_project_dict = get_org_project_dict(headers = headers)
    projects = org_project_dict[org_name]

    contributors = []
    for prj in projects:
        print(get_contributors_list(org_name = org_name,project_name=prj))
    # print(contributors)
    contributors = list(list(set(map(tuple, contributors))))
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
    final_report = []
    # print(report)
    for user in report.keys():
        d = {}
        reps = report[user]
        if len(reps) < 1:
            continue
        else:
            for rep in reps:
                try:
                    d['lines_added'] += rep['lines_added']
                    d['lines_removed'] += rep['lines_removed']
                    d['no_of_commits'] += rep['no_of_commits']
                    d['pr_open'] += rep['pr_open']
                    d['pr_closed'] += rep['pr_closed']
                except Exception as e:
                    d['handle'] = user
                    d['avatar_url'] = rep['avatar_url']
                    d['name'] = rep['contributor_name']
                    d['lines_added'] = rep['lines_added']
                    d['lines_removed'] = rep['lines_removed']
                    d['no_of_commits'] = rep['no_of_commits']
                    d['pr_open'] = rep['pr_open']
                    d['pr_closed'] = rep['pr_closed']
            final_report.append(d)


    return final_report,until


if __name__ == '__main__':
    org_name = 'KRSSG'

    headers = login('mehul','mehul@hasura') 
    # headers = login('parul','parul@hasura') 
    ## Run daily
    # generate_daily_report(headers,day = T+dT)
    
    T = datetime(month=5,day=15,year=2018)+timedelta(days=7)
    # for i in range(4,12):
    #     dT = timedelta(days=i)
    #     print('at',i)
    #     generate_daily_report(headers,day = T+dT)

    ## Run Weekly
    report = get_weekly_report(org_name = org_name,headers = headers,day=T)
    # lang_report = get_language_report_week(headers = headers, day = T)
    # print(lang_report)
    # @parul get the required data from the above function and display it on the channel.
    # My code is messy, feel free to ask doubts :) 



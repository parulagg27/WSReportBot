import requests
import json
from datetime import datetime, timedelta
from src.db.admin_org_table import admin_org_handler
from src.utils.login import login
import src.gh_scrape.add_contributors as contributors_list
from datetime import datetime
from datetime import timedelta
from src.utils.backend import get_weekly_report, get_language_report_week
from src.utils.backend import generate_initial_report
from src.utils.login import login

aoh = admin_org_handler()
url = "https://data.graveside44.hasura-app.io/v1/query"



def main(admin_username,org_name,project,headers):
    aoh.add_project(admin_username = admin_username, 
                    project = project,
                    organization=org_name,
                    headers = headers)

    contributors_list.main(headers = headers,
                                org_name = org_name,
                                project_name = project)

    T = datetime.now() - timedelta(days=30)
    for i in range(30):
        dT = timedelta(days=i)
        print('at',i)
        generate_initial_report(headers = headers,
                                org_name = org_name,
                                project = project,
                                day = T+dT)
if __name__ == '__main__':
    headers = login('mehul','mehul@hasura') 
    import sys 
    org_name = sys.argv[1]
    prj_name = sys.argv[2]
    # main('mulx10','OpenGenus','cosmos',headers)
    print(org_name,prj_name)
    main('mulx10',org_name,prj_name,headers)




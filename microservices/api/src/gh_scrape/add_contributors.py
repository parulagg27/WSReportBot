from src.db.contributor_table import add_contributor
from src.db.contributor_table import get_contributors_list as getcon
from src.utils.login import login
import requests
import os
from base64 import encodestring as base64


token = os.environ.get('GH_API_KEY')
token = 'a8076a185ed1496d7d76526e16056b36e206d7f6'
encoded_auth = base64('%s:%s' % ('testme45', '12345678d')).replace('\n', '')
headers = {
    'Authorization': 'token ' + token
}
headers = {'Authorization': 'token %s' % encoded_auth}


def get_full_name(username):
    url = "https://api.github.com/users/"+username.encode('utf8')
    r=requests.get(url,auth=('testme45', '12345678d')).json()
    # r=requests.get(url,headers=headers).json()
    try:
        fullname = r['name']
    except Exception as e:
        print(r)
        return "NULL"
    return str(fullname)

def get_contributors(org_name,project_name):
    # https://api.github.com/repos/KRSSG/robocup-stp/contributors?page=1

    all_contributors = list()
    page_count = 1
    while True:
        url = "https://api.github.com/repos/"+org_name+'/'+project_name+"/contributors?page="+str(page_count)
        print(url)
        contributors = requests.get(url,auth=('testme45', '12345678d'))
        if contributors != None and contributors.status_code == 200 and len(contributors.json()) > 0:
            all_contributors = all_contributors + contributors.json()
            # print(page_count)
        else:
            # print("breaking")
            # print(contributors.json())
            break
        page_count = page_count + 1
    all_contributors = list(map(lambda x: x['login'],all_contributors))
    # print(all_contributors)
    return all_contributors


def get_contributors_list(org_name, project_name):
    print(org_name,project_name)
    contributors_username = get_contributors(org_name, project_name) 
    contributors_list = []
    for username in contributors_username:
        print(username)
        try:
            fullname = get_full_name(username)
            contributors_list.append([str(username),str(fullname)])
        except Exception as e:
            print(e)
            pass
    # print(contributors_list)

    return contributors_list
    return [['mulx10',"Mehul Kumar Nirala"],['parulagg27',"Parul Aggarwal"]]
    
def main(headers,org_name,project_name):
    contributors = get_contributors_list(org_name,project_name)
    print(contributors)
    add_contributor(headers=headers,org_name=org_name,project_name=project_name,contributors=contributors)
    print(getcon(headers=headers,org_name=org_name,project_name=project_name))
    
if __name__ == '__main__':
    # print(get_full_name('mulx10'))
    org_name = 'KRSSG'
    project_name = 'robocup-stp'
    
    headers = login('mehul','mehul@hasura') 
    main(headers,org_name,project_name)

    

    # contributors = get_contributors_list('KRSSG','robocup')
    # add_contributor(headers=headers,org_name='KRSSG',project_name='robocup',contributors=contributors)
    # print(getcon(headers=headers,org_name='KRSSG',project_name='robocup-stp'))
    # print(get_contributors('KRSSG','robocup-stp'))
    # print (get_contributors_list('KRSSG','robocup-stp'))
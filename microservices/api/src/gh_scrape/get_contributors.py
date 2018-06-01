from pygithub3 import Github
import requests
import os
pass_secret = os.environ.get('GH_API_KEY')
key_username = os.environ.get('KEY_USER_NAME')

# pass_secret = 'a8076a185ed1496d7d76526e16056b36e206d7f6'
# key_username = 'testme45'

gh = Github(key_username, pass_secret)
 
def get_full_name(username):
    return str(gh.users.get(username).name)

def get_contributors(org_name):
  contributors = gh.orgs.members.list(org_name).all()
  contributors_username = []
  for c in contributors:
    contributors_username.append(str(c).split('(')[1].split(')')[0])
  return contributors_username

def get_contributors_list(org_name):
    contributors_username = get_contributors(org_name) 
    contributors_list = []
    for username in contributors_username:
        fullname = get_full_name(username)
        contributors_list.append([str(username),str(fullname)])
    return contributors_list
    return [['mulx10',"Mehul Kumar Nirala"],['parulagg27',"Parul Aggarwal"]]

if __name__ == '__main__':
    print (get_contributors_list('KRSSG'))
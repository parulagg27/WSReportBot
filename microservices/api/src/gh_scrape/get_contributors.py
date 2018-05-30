from pygithub3 import Github
pass_secret = '04a088c6d9e158d61d65a6e0bec239ebbd7b5d6f'
gh = Github(user='testme45', token=pass_secret) 
def get_contributors(org_name):
  contributors = gh.orgs.members.list(org_name).all()
  return contributors 
 

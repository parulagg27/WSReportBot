import copy
import csv
import os
import json
import requests


dir_path = os.path.dirname(os.path.realpath(__file__))
root_dir = '/'.join(dir_path.split('/')[:-2])

token = os.environ.get('GH_API_KEY')
headers = {
    'Authorization': 'token ' + token
}
languages_json = json.load(open("languages.json", 'r'))

class GHScrape(object):
    """docstring for GHScrape"""
    def __init__(self, org_name):
        super(GHScrape, self).__init__()
        self.org_name = org_name
        self.projects = []
        self.stats = {}
        self.usernames = set()
        """
        Structure of stats :

        key : username (In lowercase)
        value : dict
            key     : avatar_url
            value   : string

            key     : name
            value   : string

            key     : projects
            value   : type: set (Projects the user is working on)

            key     : no_of_commits
            value   : type: int (Commits merged)

            key     : pr_open
            value   : type: int (Pull Requests opened)

            key     : pr_closed
            value   : type: int (Pull Requests closed/merged)

            key     : languages
            value   : type: set (Languages involved in commits/PRs)

            key     : lines_added
            value   : type: int (Total number of lines added)

            key     : lines_removed
            value   : type: int (Total number of lines removed)

            key     : commits
            value   : type : list of dicts
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
        """
        # Generate empty statistics
        

    def add_project(self,project):
        if 'list' in str(type(project)):
            project = map(lambda x:self.org_name+'/'+x,project)
            self.projects.extend(project)
        else:
            self.projects.append(self.org_name+'/'+project) 

    def add_user(self,user,name="NULL"):
        self.usernames.add(user)
        self.stats[user] = dict()
        self.stats[user]['avatar_url'] = ''
        self.stats[user]['name'] = name
        self.stats[user]['projects'] = set()
        self.stats[user]['no_of_commits'] = 0
        self.stats[user]['pr_open'] = 0
        self.stats[user]['pr_closed'] = 0
        self.stats[user]['languages'] = set()
        self.stats[user]['lines_added'] = 0
        self.stats[user]['lines_removed'] = 0
        self.stats[user]['commits'] = list()
    # user's data based on commits merged
    def fetch_all_pages(self,query, params=None, headers=None):
        """
        If the query returns paginated results,
        this function recursively fetchs all the results, concatenate and return.
        """
        r = requests.get(query, params=params, headers=headers)
        if not r.ok:
            raise(Exception("Error in fetch_all_pages", "query : ", query, "r.json() ", r.json()))
        link = r.headers.get('link', None)
        if link is None:
            return r.json()

        if 'rel="next"' not in link:
            return r.json()
        else:
            next_url = None
            for url in link.split(','):
                if 'rel="next"' in url:
                    next_url = url.split(';')[0][1:-1]

            return r.json() + self.fetch_all_pages(next_url, params=params, headers=headers)
    

    def fetch_all_pull_requests(self,query, since=None, headers=None):
        query = query.lstrip('<')
        r = requests.get(query, headers=headers)
        link = r.headers.get('link', None)
        if link is None:
            return r.json()

        if 'rel="next"' not in link:
            return r.json()
        else:
            if r.json()[-1]["created_at"] < since:
                return r.json()
            else:
                next_url = None
                for url in link.split(','):
                    if 'rel="next"' in url:
                        next_url = url.split(';')[0][1:-1]

                return r.json() + self.fetch_all_pull_requests(next_url, since=since, headers=headers)

        


    def run(self,since,until):
        for project in self.projects:
            print("Working on project : ", project)
            query = "https://api.github.com/repos/{}/commits".format(project)
            params = {
                'since': since,
                'until': until
            }

            commits = self.fetch_all_pages(query, params=params, headers=headers)

            for commit in commits:
                if commit['author'] is None:
                    continue
                author = commit['author']['login'].lower()
                avatar_url = commit['author']['avatar_url']
                if author in self.usernames:
                    print(author, " working on ", project)
                    html_url = commit['html_url']
                    message = commit['commit']['message']

                    _api_url_commit = commit['url']
                    r = requests.get(_api_url_commit, headers=headers)
                    if not r.ok:
                        raise(Exception("Error in fetching commit info", "query : ", _api_url_commit, "r.json() ", r.json()))
                    _commit_info = r.json()

                    try:
                        lines_added = _commit_info['stats']['additions']
                        lines_removed = _commit_info['stats']['deletions']
                    except KeyError:
                        lines_added = lines_removed = 0

                    languages_used = set()
                    files = _commit_info.get('files', None)
                    _files_modified = set()
                    if files is not None:
                        for f in _commit_info['files']:
                            _files_modified.add(f['filename'])

                    for f in _files_modified:
                        file_ext = '.' + f.split('/')[-1].split('.')[-1]
                        lang = languages_json.get(file_ext, None)
                        if lang is not None:
                            languages_used.add(lang)

                    commit_record = {
                        'html_url': html_url,
                        'message': message,
                        'project': project,
                        'lines_added': lines_added,
                        'lines_removed': lines_removed,
                    }

                    self.stats[author]['commits'].append(commit_record)
                    self.stats[author]['projects'].add(project)
                    self.stats[author]['no_of_commits'] += 1
                    self.stats[author]['languages'] = self.stats[author]['languages'].union(languages_used)
                    self.stats[author]['lines_added'] += lines_added
                    self.stats[author]['lines_removed'] += lines_removed
                    if self.stats[author]['avatar_url'] == '':
                        self.stats[author]['avatar_url'] = avatar_url

            # Students' data based on Pull Requests
            query = "https://api.github.com/repos/{}/pulls?state=all".format(project)
            prs = self.fetch_all_pull_requests(query, since=since, headers=headers)

            # Trim out of date pull requests
            while(True):
                if len(prs) == 0:
                    break
                if prs[-1]['created_at'] < since:
                    prs.pop()
                else:
                    break

            for pr in prs:
                author = pr['user']['login'].lower()
                if author in self.usernames:
                    if pr['state'] == 'open':
                        self.stats[author]['pr_open'] += 1
                    elif pr['state'] == 'closed':
                        self.stats[author]['pr_closed'] += 1

        # Update stats.json
        copy_stats = copy.deepcopy(self.stats)
        # set is not JSON serializable
        for user in copy_stats:
            copy_stats[user]['projects'] = list(copy_stats[user]['projects'])
            copy_stats[user]['languages'] = list(copy_stats[user]['languages'])

        with open('stats.json', 'w') as f:
            f.write(json.dumps(copy_stats))
        print("Done.")
    def get_stats(self,user):
        with open('stats.json', 'r') as f:
            stats = json.load(f)
            return stats[user]

org_name = 'KRSSG'
projects = ['robocup-stp']
since = '2017-11-21T00:00:00Z'
until = '2019-01-01T00:00:00Z'
user ='mulx10'
name = "Mehul Kumar Nirala"

ghs = GHScrape(org_name = org_name)
ghs.add_project(project = projects)
ghs.add_user(user = user,name = name)
ghs.run(since,until)

print(ghs.get_stats(user))
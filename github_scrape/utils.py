from models import GithubUser

from django.db import IntegrityError

import urllib2
import json
import operator

def getGithubUsers(keyword, page):
    keyword_lower = keyword.lower()
    url_base = 'https://api.github.com/legacy/user/search/%s?start_page=%d'
    url = url_base % (keyword, page)
    fp = urllib2.urlopen(url)
    users = json.load(fp)['users']
    fields = map(operator.attrgetter('name'), GithubUser._meta._fields())
    github_users = []
    for u in users:
        if keyword_lower in u['location'].lower():
            u['github_id'] = u['id']
            del u['id']
            github_users.append(GithubUser(**dict(filter(lambda x: x[0] in fields, u.iteritems()))))
        
    return github_users
                 
def scrape(keyword):
    page = 1
    users = getGithubUsers(keyword, page)
    while users:
        print 'page %d, gonna save %d users' % (page, len(users))
        for u in users:
            try:
                u.save()
            except IntegrityError:
                pass
        page += 1
        users = getGithubUsers(keyword, page)
    
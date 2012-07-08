#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.db import IntegrityError
from django.utils.encoding import smart_str

from models import GithubUser
import json
import operator
import urllib2

def get_github_users(keyword, page):
    keyword_lower = smart_str(keyword.lower())
    url_base = smart_str(u'https://api.github.com/legacy/user/search/%s?start_page=%d')
    url = url_base % (keyword, page)
    fp = urllib2.urlopen(url)
    users = json.load(fp)['users']
    fields = map(operator.attrgetter('name'), GithubUser._meta._fields())
    github_users = []
    for u in users:
        if keyword_lower in smart_str(u['location'].lower()):
            u['github_id'] = u['id']
            del u['id']
            github_users.append(GithubUser(**dict(filter(lambda x: x[0] in fields, u.iteritems()))))
        
    return github_users
                 
def scrape_location(keyword):
    page = 1
    users = get_github_users(keyword, page)
    while users:
        print 'page %d, gonna save %d users' % (page, len(users))
        for u in users:
            if GithubUser.objects.filter(github_id=u.github_id).count() == 0:
                try:
                    u.save()
                except IntegrityError:
                    pass
        page += 1
        users = get_github_users(keyword, page)
    
def scrape_sweden():
    keywords = map(smart_str, [u'Göteborg', 'Sverige', 'Sweden', 'Stockholm', u'Göteborg', 'Gothenburg',
    u'Malmö', 'Malmo', 'Uppsala', u'Västerås', u'Örebro', u'Linköping', 'Helsingborg', 
    u'Norrköping', u'Jönköping', 'Lund', u'Umeå', u'Gävle', u'Borås', u'Södertälje', u'Täby',
    'Eskilstuna', 'Karlstad', 'Halmstad', u'Växjö'])
    
    for k in keywords:
        print "Trying for ", k
        scrape_location(k)
        
        
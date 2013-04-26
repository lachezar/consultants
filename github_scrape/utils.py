#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.db import IntegrityError, transaction
from django.utils.encoding import smart_str

from models import GithubUser
import json
import operator
import urllib2

def get_github_users(keyword, page, access_token):
    keyword_lower = smart_str(keyword).lower()
    url_base = smart_str(u'https://api.github.com/legacy/user/search/%s?start_page=%d&access_token=%s')
    url = url_base % (keyword, page, access_token)
    fp = urllib2.urlopen(url)
    users = json.load(fp)['users']
    fields = map(operator.attrgetter('name'), GithubUser._meta._fields())
    github_users = []
    for u in users:
        if u['location'] and keyword_lower in smart_str(u['location']).lower():
            u['github_id'] = u['id']
            del u['id']
            github_users.append(GithubUser(**dict(filter(lambda x: x[0] in fields, u.iteritems()))))
        
    return github_users


@transaction.autocommit                 
def scrape_location(keyword, access_token):
    page = 1
    users = get_github_users(keyword, page, access_token)
    while users:
        print 'page %d, gonna save %d users' % (page, len(users))
        for u in users:
            if GithubUser.objects.filter(github_id=smart_str(u.github_id)).count() == 0:
                try:
                    u.save()
                except IntegrityError:
                    pass
        page += 1
        users = get_github_users(keyword, page, access_token)
    
    
def scrape_sweden(access_token = ''):
    ''' 
    After the last change in the Github API you need to have an oauth access token
    to perform more than 60 requests per hour.
    '''

    keywords = map(smart_str, [u'Göteborg', 'Sverige', 'Sweden', 'Stockholm', u'Göteborg', 'Gothenburg',
    u'Malmö', 'Malmo', 'Uppsala', u'Västerås', u'Örebro', u'Linköping', 'Helsingborg', 
    u'Norrköping', u'Jönköping', 'Lund', u'Umeå', u'Gävle', u'Borås', u'Södertälje', u'Täby',
    'Eskilstuna', 'Karlstad', 'Halmstad', u'Växjö'])
    
    for k in keywords:
        print "Trying for ", k
        scrape_location(k, access_token)
        
        

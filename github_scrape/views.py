# Create your views here.

from django.shortcuts import render_to_response
from django.template import RequestContext
from models import GithubUser

import operator

def index(request, language=None):
    if language is None:
        users = GithubUser.objects.all()
    else:
        users = GithubUser.objects.filter(language__iexact=language)
    users = users.order_by('-public_repo_count')
    languages = GithubUser.objects.values_list('language').exclude(language='').distinct().order_by('language')
    languages = map(operator.itemgetter(0), languages)
    
    return render_to_response('list.html', 
                              {'users': users, 
                               'languages': languages, 
                               'selected_language': language
                              }, context_instance=RequestContext(request))
    
    
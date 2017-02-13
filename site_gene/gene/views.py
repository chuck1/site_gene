from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http.response import HttpResponseRedirect
from django.contrib.auth import authenticate
import django.contrib.auth
from django.conf import settings

import os
import json
import urllib2
import urllib
import graphviz

from .models import *
from .forms import *


class Graph(object):
    def __init__(self):
        self.parent_pairs = []

    def check_parent_pair(self, m, f):

        m_pk = None
        f_pk = None

        if m: m_pk = m.pk
        if f: f_pk = f.pk

        if (m_pk, f_pk) in self.parent_pairs: return "pp_{}_{}".format(m_pk, f_pk)

        self.g.node("pp_{}_{}".format(m_pk, f_pk), "")
        
        if m:
            self.g.edge("person_{}".format(m_pk), "pp_{}_{}".format(m_pk, f_pk))
        
        if f:
            self.g.edge("person_{}".format(f_pk), "pp_{}_{}".format(m_pk, f_pk))
        
        self.parent_pairs.append((m_pk, f_pk))
        
        return "pp_{}_{}".format(m_pk, f_pk)

    def connect_parents(self, p):

        if p.mother or p.father:

            pp = self.check_parent_pair(p.mother, p.father)
        
            self.g.edge(pp, "person_{}".format(p.pk))

    def render(self):       
    	self.g.render(os.path.join(
                settings.STATIC_ROOT, 
                'gene/graph.gv'))

 
@login_required
def relation(request, pk1, pk2):

    p1 = get_object_or_404(Person, pk=pk1)
    p2 = get_object_or_404(Person, pk=pk2)
    
    an1 = p1.ancestors_distance(0)
    an2 = p2.ancestors_distance(0)


    def f1(a1):
        for a2 in an2:
            if a1[0]==a2[0]: return True
        return False
    
    def f2(a2):
        for a1 in an1:
            if a1[0]==a2[0]: return True
        return False

    an1 = filter(f1, an1)
    an2 = filter(f2, an2)

    md1 = 10000
    md2 = 10000

    #print "an1"
    for a in an1:
        md1 = min(md1, a[1])
        #print "  {:32}{:6}".format(a[0],a[1])

    #print "an2"
    for a in an2:
        md2 = min(md2, a[1])
        #print "  {:32}{:6}".format(a[0],a[1])

    def f1a(a):
        return a[1] <= md1
    
    def f2a(a):
        return a[1] <= md2
    
    an1 = filter(f1a, an1)
    an2 = filter(f2a, an2)
 
    #print "an1"
    for a in an1:
        #print "  {:32}{:6}".format(a[0],a[1])
        pass

    #print "an2"
    for a in an2:
        #print "  {:32}{:6}".format(a[0],a[1])
        pass
    
    
    x = min(md1, md2)
    y = abs(md1 - md2)
    
    print "{} and {} are {} cousins {} times removed".format(p1, p2, x, y)


@login_required
def ancestors(request, person_pk):
    
    person = get_object_or_404(Person, pk=person_pk)
 
    an = person.ancestors() + [person]

    g = Graph() 
    g.g = graphviz.Digraph(format='png')
   
    for p in an:
        
        g.g.node("person_{}".format(p.pk), str(p))
        
        if p.mother:
            g.g.edge("person_{}".format(p.mother.pk), "person_{}".format(p.pk))
        
        if p.father:
            g.g.edge("person_{}".format(p.father.pk), "person_{}".format(p.pk))

    g.render()

    context = {}
    return render(request, "gene/index.html", context)    

@login_required
def descendents(request, person_pk):
    
    person = get_object_or_404(Person, pk=person_pk)
    
    g = graphviz.Digraph(format='png')
 
    de = person.descendents() + [person]

    for p in de:
        g.node("person_{}".format(p.pk), str(p))
        
        for d in p.person_mother.all():
            g.edge("person_{}".format(p.pk), "person_{}".format(d.pk))

        for d in p.person_father.all():
            g.edge("person_{}".format(p.pk), "person_{}".format(d.pk))

    g.render(os.path.join(settings.BSAE_DIR, 'gene/static/gene/graph.gv'))

    context = {}
    return render(request, "gene/index.html", context)    

@login_required
def index(request):

    # test
    relation(request, 5, 20)

    

    g = Graph()
    g.g = graphviz.Digraph(format='png')

    print
    for p in Person.objects.all():
        print str(p)
        
        p.graph_node(g.g)
        #g.g.node("person_{}".format(p.pk), str(p))
        
        g.connect_parents(p)

    print


    #print g.g.source

    g.render()

    context = {'user':request.user}
    return render(request, "gene/index.html", context)    


def send_post_to_google(response, remoteip):

    print "SECRET SETTINGS",settings.SECRET_SETTINGS

    post_data = [
            ('secret', settings.SECRET_SETTINGS['recaptcha_secret_key']),
            ('response', response),
            ('remoteip', remoteip),
            ]

    result = urllib2.urlopen('https://www.google.com/recaptcha/api/siteverify', urllib.urlencode(post_data))
    content = result.read()

    content = json.loads(content)

    print "respnose from google", content

    return content['success']

def captcha(request):
    
    return send_post_to_google(request.POST['g-recaptcha-response'], request.META['REMOTE_ADDR'])

def register(request):
    
    # if this is a POST request we need to process the form data
    if request.method == 'POST':


        # create a form instance and populate it with data from the request:
        form = RegisterForm(request.POST)

        form.captcha = captcha(request)

        # check whether it's valid:
        if form.is_valid():
            # redirect to a new URL:
            return HttpResponseRedirect('/gene/')
    
    # if a GET (or any other method) we'll create a blank form
    else:
        form = RegisterForm()
    
    return render(request, 'gene/register.html', {'form': form})

def login(request):
    
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:

        form = LoginForm(request.POST)

        form.captcha = captcha(request)
        
        if form.is_valid():
            django.contrib.auth.login(request, form.user_cache)

            return HttpResponseRedirect('/gene/')

        else:
            print 'login not valid'

    # if a GET (or any other method) we'll create a blank form
    else:
        form = LoginForm()


    return render(request, 'gene/login.html', {'form': form})





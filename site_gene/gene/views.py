from django.shortcuts import render, get_object_or_404

# Create your views here.

import graphviz

from .models import *

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

    print "an1"
    for a in an1:
        md1 = min(md1, a[1])
        print "  {:32}{:6}".format(a[0],a[1])

    print "an2"
    for a in an2:
        md2 = min(md2, a[1])
        print "  {:32}{:6}".format(a[0],a[1])

    def f1a(a):
        return a[1] <= md1
    
    def f2a(a):
        return a[1] <= md2
    
    an1 = filter(f1a, an1)
    an2 = filter(f2a, an2)
 
    print "an1"
    for a in an1:
        md1 = min(md1, a[1])
        print "  {:32}{:6}".format(a[0],a[1])

    print "an2"
    for a in an2:
        md1 = min(md1, a[1])
        print "  {:32}{:6}".format(a[0],a[1])
    
    
    x = min(md1, md2)
    y = abs(md1 - md2)
    
    print "{} and {} are {} cousins {} times removed".format(p1, p2, x, y)


def ancestors(request, person_pk):
    
    person = get_object_or_404(Person, pk=person_pk)
 
    an = person.ancestors() + [person]
 
    g = graphviz.Digraph(format='png')
   
    for p in an:
        
        g.node("person_{}".format(p.pk), str(p))
        
        if p.mother:
            g.edge("person_{}".format(p.mother.pk), "person_{}".format(p.pk))
        
        if p.father:
            g.edge("person_{}".format(p.father.pk), "person_{}".format(p.pk))

    g.render('gene/static/gene/graph.gv')

    context = {}
    return render(request, "gene/index.html", context)    

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

    g.render('gene/static/gene/graph.gv')

    context = {}
    return render(request, "gene/index.html", context)    


def index(request):

    # test
    relation(None, 5, 20)

    g = Graph()
    g.g = graphviz.Digraph(format='png')

    print
    for p in Person.objects.all():
        print str(p)
        
        g.g.node("person_{}".format(p.pk), str(p))
        
        g.connect_parents(p)

    print


    #print g.g.source

    g.g.render('gene/static/gene/graph.gv')

    context = {}
    return render(request, "gene/index.html", context)    












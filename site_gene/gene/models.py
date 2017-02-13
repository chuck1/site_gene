from django.db import models
import django.urls


class Location(models.Model):
    name = models.CharField(max_length=256)

    def __unicode__(self):
        return self.name

class Person(models.Model):
    name = models.CharField(max_length=256)
    mother = models.ForeignKey(
        'Person', 
        related_name='person_mother', 
        blank=True, null=True)
    father = models.ForeignKey(
        'Person', 
        related_name='person_father', 
        blank=True, null=True)
    birth_year     = models.IntegerField(blank=True, null=True)
    birth_month    = models.IntegerField(blank=True, null=True)
    birth_day      = models.IntegerField(blank=True, null=True)
    birth_location = models.ForeignKey(
        Location,
        related_name = 'location_birth',
        blank=True,
        null=True)
    death_year     = models.IntegerField(blank=True, null=True)
    death_month    = models.IntegerField(blank=True, null=True)
    death_day      = models.IntegerField(blank=True, null=True)
    death_location = models.ForeignKey(
        Location,
        related_name = 'location_death',
        blank=True,
        null=True)

    def ancestors_distance(self, d):

        an = []

        if self.mother:
            an.append((self.mother, d + 1))
            an += self.mother.ancestors_distance(d + 1)
        
        if self.father:
            an.append((self.father, d + 1))
            an += self.father.ancestors_distance(d + 1)
        
        return an
  
    def ancestors(self):

        an = []
        if self.mother:
            an.append(self.mother)
            an += self.mother.ancestors()
        if self.father:
            an.append(self.father)
            an += self.father.ancestors()


        return an

    def children(self):
        return list(self.person_mother.all()) + list(self.person_father.all())

    def descendents(self):
        
        de1 = list(self.person_mother.all()) + list(self.person_father.all())
        de2 = []
        
        for d in de1:
            de2 += d.descendents()

        return de1 + de2

    def graph_node(self, g):
        if self.birth_year is not None:
            label = "{}\n{}".format(self.name, self.birth_year)
        else:
            label = "{}".format(self.name)

        url = django.urls.reverse('person', args=[self.pk])

        g.node("person_{}".format(self.pk), label, URL=url)
            


    def __unicode__(self):
        return "{} {}-{}".format(self.name, self.birth_year, self.death_year)





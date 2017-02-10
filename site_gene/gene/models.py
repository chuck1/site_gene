from django.db import models

# Create your models here.

class Person(models.Model):
    name = models.CharField(max_length=256)
    mother = models.ForeignKey('Person', related_name='person_mother', blank=True, null=True)
    father = models.ForeignKey('Person', related_name='person_father', blank=True, null=True)
 
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

    def descendents(self):
        
        de1 = list(self.person_mother.all()) + list(self.person_father.all())
        de2 = []
        
        for d in de1:
            de2 += d.descendents()

        return de1 + de2

    def __unicode__(self):
        return self.name

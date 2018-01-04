from django.db import models
from django.core.urlresolvers import reverse

class Software(models.Model):
    name = models.CharField(max_length=200)

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('software_edit', kwargs={'pk': self.pk})


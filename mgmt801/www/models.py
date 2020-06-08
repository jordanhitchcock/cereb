from django.db import models


class Visitors(models.Model):
    session_id = models.CharField(max_length=100)
    template_name = models.CharField(max_length=100)
    visit_dt = models.DateTimeField()
    ip = models.CharField(max_length=100)
    signup_email = models.EmailField()
    contact_name = models.CharField(max_length=100)
    contact_email = models.EmailField()
    contact_content = models.CharField(max_length=1000)


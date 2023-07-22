from django.db import models
from django.contrib.auth.models import User


class CompanyProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    username = models.CharField( max_length=50 , default='not added' )
    company_name = models.CharField(max_length=255)
    company_description = models.TextField()
    location = models.CharField(max_length=255)
    website = models.URLField(blank=True)


class Job(models.Model):
    company = models.ForeignKey(CompanyProfile, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=255, )
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=255)
    job_type = models.CharField(max_length=50)
    industry = models.CharField(max_length=100)
    category = models.CharField(max_length=50)
    skill = models.CharField(max_length=200)
    resume = models.FileField(upload_to='resumes/', default='path/to/default_resume.pdf')

    def _str_(self) -> str:
        return self.title
    





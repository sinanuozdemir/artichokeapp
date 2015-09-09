from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin
from django.contrib.auth.models import AbstractBaseUser
import boto
from datetime import datetime



class Industry(models.Model):
    name = models.CharField(max_length = 200)
    def __unicode__(self):
        return self.name

class User(AbstractBaseUser):
    email = models.EmailField('email address', db_index=True)
    username = models.CharField(max_length=100)
    joined = models.DateTimeField(auto_now_add=True, )
    is_active = models.BooleanField(default=True) #right now True means that they actively signed up, False otherwise
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    max_leads_per_month = models.IntegerField(default = 600)
    USERNAME_FIELD = 'email'
    def get_full_name(self):
        return self.email

    def get_short_name(self):
          return self.email
    
    @property
    def is_superuser(self):
          return self.is_admin
      
    @property
    def is_staff(self):
          return self.is_admin

    def has_perm(self, perm, obj=None):
          return self.is_admin
      
    def has_module_perms(self, app_label):
        return self.is_admin
    
    def __unicode__(self):
            return self.email

class UserPermissions(models.Model):
    user = models.ForeignKey('User')
    person = models.ForeignKey('Person', null=True, blank=True)
    organization = models.ForeignKey('Organization', null=True)
    linkedin_secret_code = models.CharField(max_length=100, null=True, blank=True)
    linkedin_access_token = models.CharField(max_length=100, null=True, blank=True)
    linkedin_code_expires_in = models.DateTimeField(default=datetime.now(), null=True, blank=True)
    is_team_leader = models.BooleanField(default = False)
    max_leads_per_month = models.IntegerField(default = 500)
    profile_picture = models.FileField(upload_to = 'user_photos/', default = 'user_photos/no-img.jpg', null=True, blank=True)

class Person(models.Model):
    personal_crunchbase                 = models.CharField(max_length = 100, null=True, default = None, unique = True)
    personal_linkedin                   = models.CharField(max_length = 100, null=True, default = None, unique = True)
    personal_google_plus                = models.CharField(max_length = 100, null=True, default = None, unique = True)
    personal_angellist                  = models.CharField(max_length = 100, null=True, default = None, unique = True)
    personal_facebook                   = models.CharField(max_length = 100, null=True, default = None, unique = True)
    personal_github                     = models.CharField(max_length = 100, null=True, blank=True, default = None, unique = True)
    personal_twitter                    = models.CharField(max_length = 100, null=True, default = None, unique = True)
    personal_home_page                  = models.CharField(max_length = 100, null=True, default = None)
    personal_wikipedia                  = models.CharField(max_length = 100, null=True, default = None)
    
    interests                           = models.ManyToManyField('Industry')
    name                                = models.CharField(max_length = 100)
    location                            = models.CharField(max_length = 100, null = True, default = None)
    country                             = models.CharField(max_length = 50, null=True, default = None)
    state                             = models.CharField(max_length = 50, null=True, default = None)
    city                                = models.CharField(max_length = 50, null=True, default = None)
    industry                            = models.CharField(max_length = 100, null = True, default = None)
    gender                              = models.CharField(max_length = 100, null = True, default = None)
    linkedin_bio                        = models.TextField(null = True, default = None)
    twitter_bio                         = models.TextField(null = True, default = None)
    photo                               = models.CharField(max_length = 1000, null = True, default = None)
    date_added                          = models.DateTimeField(default=datetime.now())
    birth_date                          = models.DateTimeField(null = True, blank = True)
    age                                 = models.IntegerField(default = None, null = True, blank = True)
    klout_score                         = models.IntegerField(default = 0)
    twitter_verified                    = models.BooleanField(default = False)
    times_analyzed                      = models.IntegerField(default = 0)
    twitter_followers                   = models.IntegerField(default = -1)
    is_analyzed                         = models.BooleanField(default = True)
    last_analyzed                       = models.DateTimeField(null = True, blank = True)
    saved_photo                         = models.FileField(upload_to='person_photos/')
    def __unicode__(self):
        return self.name

class EmailAddress(models.Model):
    types = (
        ('personal', 'Personal'),
        ('business', 'Business'),
    )
    type_of_email              = models.CharField(max_length=25, choices=types)
    email_pattern              = models.CharField(max_length=50, null = True, blank = True)
    person                     = models.ForeignKey('Person', null=True, blank=True)
    last_updated               = models.DateTimeField(default=datetime.now(), null = True, blank = True)
    address                    = models.CharField(default = None, null=True, blank=True, max_length = 100, unique = True, db_index = True)
    company                    = models.ForeignKey('Company', null=True, blank=True)
    is_current                 = models.BooleanField(default = False)
    is_deliverable             = models.CharField(default = None, null=True, blank=True, max_length = 100)
    score                      = models.IntegerField(default = 100)
    sources                    = models.ManyToManyField('Website')

class Website(models.Model):
    type_of_website                     = models.CharField(max_length=25)
    url                                 = models.CharField(max_length=200, null = True)
    last_updated                        = models.DateTimeField(default=datetime.now(), null = True, blank = True)
    html                                = models.TextField(null = True, default = None)


class PersonAdmin(admin.ModelAdmin):
    search_fields = ('name')
    
# 5 == phd
# 4 == masters
# 3 == ba
# 2 == high school
# 1 == other
# 0 == unknown
class Education(models.Model):
    person = models.ForeignKey('Person')
    date_started = models.DateTimeField(null = True, blank = True)
    date_ended = models.DateTimeField(null = True, blank = True)
    is_active = models.BooleanField(default = True)
    education_level = models.IntegerField(default = 0)
    school_name = models.CharField(max_length = 200)
    fields_of_study = models.ManyToManyField('Industry', blank=True)

class Job(models.Model):
    person = models.ForeignKey('Person')
    company = models.ForeignKey('Company')
    date_started = models.DateTimeField(null = True, blank = True)
    date_ended = models.DateTimeField(null = True, blank = True)
    is_active = models.BooleanField(default = True)
    months = models.IntegerField(default = 0)
    title = models.CharField(max_length = 200)
    def __unicode__(self):
        return self.title + " at " + self.company.name
    
class Company(models.Model):
    name                                = models.CharField(max_length = 200, blank=True)
    company_crunchbase                  = models.CharField(max_length = 200, blank=True)
    company_linkedin                    = models.CharField(max_length = 200, blank=True)
    industries                          = models.ManyToManyField('Industry', blank=True)
    email_pattern                       = models.CharField(max_length = 200, blank=True)
    company_angellist                   = models.CharField(max_length = 200, blank=True)
    company_facebook                    = models.CharField(max_length = 200, blank=True)
    company_twitter                     = models.CharField(max_length = 200, blank=True)
    company_wikipedia                   = models.CharField(max_length = 200, blank=True)
    country                             = models.CharField(max_length = 50, null=True, default = None)
    city                                = models.CharField(max_length = 50, null=True, default = None)
    state                               = models.CharField(max_length = 50, null=True, default = None)
    company_home_page                   = models.CharField(max_length = 200, blank=True)
    date_founded                        = models.DateTimeField(null = True, blank=True)
    date_aquired                        = models.DateTimeField(null = True, blank=True)
    email_host                          = models.CharField(max_length = 100, blank=True)
    funding                             = models.IntegerField(default = 0, blank=True)
    linkedin_bio                        = models.TextField(null = True, default = None)
    twitter_bio                         = models.TextField(null = True, default = None)
    revenue                             = models.IntegerField(default = 0, blank=True)
    times_analyzed                      = models.IntegerField(default = 0, blank=True)
    last_analyzed                       = models.DateTimeField(null = True, blank=True, default=datetime.now())
    number_of_employees                 = models.IntegerField(default = 0, blank=True)
    location                            = models.CharField(max_length = 200, blank=True)
    def __unicode__(self):
        return self.name
    
class techComp(models.Model):
    company  = models.ForeignKey('Company')
    technology  = models.ForeignKey('Technology')
    date_found = models.DateTimeField(default=datetime.now(), null = True, blank=True)
    date_stopped = models.DateTimeField(null = True, blank=True)

class script(models.Model):
    company  = models.ForeignKey('Company')
    type_of_script = models.CharField(max_length = 100, null=True, blank = True)
    text = models.TextField(null = True, default = None)
    src = models.TextField(null = True, default = None)

class Technology(models.Model):
    name                               = models.CharField(max_length = 200, blank = True, null = True)
    type_of_tech                       = models.CharField(max_length = 200, blank = True, null = True)
    script_alias                       = models.CharField(max_length = 1000, blank = True, null = True)
    company                            = models.ManyToManyField('Company', through = 'techComp')


class Organization(models.Model):
    name_of_organization = models.CharField(max_length = 100)
    def __unicode__(self):
        return self.name_of_organization

class Lead(models.Model):
    person = models.ForeignKey('Person')
    user = models.ForeignKey('User')
    new = models.BooleanField(default = True)
    date_matched = models.DateTimeField(default=datetime.now())
    organization = models.ForeignKey('Organization', null=True)
    imported = models.BooleanField(default = False)
    discovered = models.BooleanField(default = False)

class LeadNote(models.Model):
    lead = models.ForeignKey("Lead")
    note = models.CharField(max_length = 10000, null=True)
    date = models.DateTimeField(default=datetime.now())
    author = models.ForeignKey('User', null=True)

class Query(models.Model):
    user = models.ForeignKey('User')
    people = models.ManyToManyField('Person')
    date_made = models.DateTimeField(default=datetime.now())
    people_generated = models.IntegerField(default = 0)
    email_counter = models.IntegerField(default = 0)
    twitter_counter = models.IntegerField(default = 0)
    linkedin_counter = models.IntegerField(default = 0)
    leads_produced = models.IntegerField(default = 0)
    people_produced = models.IntegerField(default = 0)
    emails_produced = models.IntegerField(default = 0)
    title = models.CharField(max_length = 200,blank=True, null=True)
    needs_attention = models.BooleanField(default=False)
    needs_emails = models.BooleanField(default=False)
    needs_people = models.BooleanField(default=False)
    organization = models.ForeignKey('Organization', null=True)
    class Meta:
        ordering = ['-date_made']


        

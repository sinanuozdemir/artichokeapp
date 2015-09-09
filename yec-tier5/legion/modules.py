import Legion
import json
from urlparse import urlparse
import re
import string
import random
from datetime import timedelta, datetime
import requests
import operator
from celery import shared_task
from django.db.models import Q
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage as storage
import os
from django.core.files import File
from legion.models import Person, Company, Education, Industry, Job, User, Query, Lead, EmailAddress, Website
import master


def getCompanyDict(company):
    to_return = {}
    to_return['web_presence'] = {}
    to_return['name'] = company.name
    to_return['id'] = company.id
    for p in ['company_linkedin', 'company_twitter', 'company_home_page']:
        if company.__dict__[p]:
            to_return['web_presence'][p] = {'url':company.__dict__[p]}
    for p in ['email_host']:
        if company.__dict__[p]:
            to_return[p] = company.__dict__[p]
    location_dict = {}
    for i in ['location', 'country', 'city']:
        if company.__dict__[i]:
            location_dict[i] = company.__dict__[i]
    if location_dict:
        to_return['location'] = location_dict
    return to_return

def getPersonDict(person):
    to_return = {}
    to_return['web_presence'] = {}
    to_return['id'] = person.id
    for p in ['personal_linkedin', 'personal_home_page', 'personal_twitter', 'personal_crunchbase', 'personal_github', 'personal_angellist']:
        if person.__dict__[p]:
            to_return['web_presence'][p] = {'url':person.__dict__[p]}
    for p in ['age', 'name']:
        if person.__dict__[p]:
            to_return[p] = person.__dict__[p]
    location_dict = {}
    for i in ['location', 'country', 'city', 'state']:
        if person.__dict__[i]:
            location_dict[i] = person.__dict__[i]
    if location_dict:
        to_return['location'] = location_dict
    jobs = Job.objects.filter(person = person).order_by("-date_started")
    emails = person.emailaddress_set.all()
    emails = [{'address':email.address, 'is_deliverable':email.is_deliverable }for email in emails]
    if emails:
        to_return['emails'] = emails
    to_return['positions'] = [{'position_title':j.title,'is_active':j.is_active, 'company_dict':getCompanyDict(j.company)} for j in jobs]
    to_return['positions'] = [{k:v for k, v in ed.iteritems() if v} for ed in to_return['positions']]
    schools = Education.objects.filter(person = person).order_by("-date_started")
    to_return['education'] = [{'education_level':e.education_level, 'school_name':e.school_name, 'fields_of_study':e.fields_of_study.values_list('name', flat = True)} for e in schools]
    to_return['education'] = [{k:v for k, v in ed.iteritems() if v} for ed in to_return['education']]
    try:
        to_return['photo'] = person.photo
    except:
        to_return['photo'] = 'https://tier5.s3.amazonaws.com/person_photos/no-img.jpg'
    interests = [p.name for p in person.interests.all()]
    to_return['interests'] = interests
    to_return['linkedin_bio'] = person.linkedin_bio
    to_return['twitter_bio'] = person.twitter_bio
    return to_return

def getSearchResults(query_dict):
    if not len(query_dict['person']) and not len(query_dict['company']):
        return []
    if len(query_dict['company'].keys()):
        tags = Q()
        try:
            funding_filter = reduce(operator.and_, [Q(**{k: v}) for k, v in query_dict['company'].items() if 'funding' in k])
        except:
            funding_filter = Q()
        try:
            revenue_filter = reduce(operator.and_, [Q(**{k: v}) for k, v in query_dict['company'].items() if 'revenue' in k ])
        except:
            revenue_filter = Q()
        try:
            tags = reduce(operator.and_, [Q(**{k: v}) for k, v in query_dict['company'].items() if 'revenue' not in k and 'funding' not in k])
        except:
            tags = Q()
        jobs = Job.objects.filter(tags & (funding_filter | revenue_filter))
        people = Person.objects.filter(pk__in=jobs.values_list('person', flat = True))
        return people
    return []

def getCompany(company_dict):
    filter_ = [Q(**{k+'__iexact': v['url']}) for (k, v) in company_dict.get('web_presence',{}).iteritems()]
    items = ['name', 'email_host']
    email_filter = [Q(**{e+'__iexact': company_dict[e]}) for e in items if company_dict.get(e, None)]
    try:
        return Company.objects.filter(reduce(operator.or_, filter_+email_filter))[0]
    except Exception as e:
        return None

@shared_task
def makeCompany(user_dict, override = False):
    already_there = getCompany(user_dict)
    to_return = already_there is None
    if already_there and not override:
        return already_there, False
    elif already_there and override:
        new_company = already_there
    else:
        new_company = Company()
    for value in ['email_host', 'linkedin_bio', 'twitter_bio', 'email_pattern', 'name', 'number_of_employees', 'revenue', 'funding']:
        if user_dict.get(value, None):
            new_company.__dict__[value] = user_dict.get(value, None)
    if 'location' in user_dict and user_dict['location']:
        for key, value in user_dict['location'].items():
            try:
                new_company.__dict__[key] =  value
            except:
                pass
    new_company.save()
    for interest in user_dict.get('industries', []):
        interst_obj = Industry.objects.filter(name__iexact = interest)
        if len(interst_obj):
            interst_obj = interst_obj[0]
        else:
            interst_obj = Industry(name=interest.lower())
            interst_obj.save()
        new_company.industries.add(interst_obj)
    for value in user_dict.get('web_presence', []):
        if not new_company.__dict__[value]:
            new_company.__dict__[value] = user_dict['web_presence'][value]['url'].lower()
    new_company.save()
    return new_company, to_return

def getPerson(user_dict):
    email_filter = [Q(**{'emailaddress__address__iexact':email['address']}) for email in user_dict.get('emails', [])]
    filter_ = [Q(**{k+'__iexact': v['url']}) for (k, v) in user_dict.get('web_presence',{}).iteritems() if 'personal_home_page' != k and 'personal_facebook' != k]
    try:
        people = Person.objects.filter(reduce(operator.or_, filter_+email_filter)).distinct('pk')
        if people.count() == 1:
            return people.first()
    except Exception as e:
        print e
        pass
    return None


@shared_task
def completeCompany(company_dict):
    completed_company = master.completeEntity(Legion.legion(company_dict, scrapers = {}, type_of_entity = 'company'), use_the_hounds = True).information
    makeCompany(completed_company, override = True)
    return True


@shared_task
def makePerson(user_dict, override = False, complete_companies = False):
    person = getPerson(user_dict)
    created = False
    if person and not override:
        return person, False
    elif not person:
        created = True
        person = Person()
        person.save()
    for type_of_media, media_dict in user_dict.get('web_presence', {}).items():
        if not person.__dict__[type_of_media]:
            person.__dict__[type_of_media] = media_dict['url'].lower()
    person.save()
    for field in ['photo', 'klout_score', 'industry', 'name', 'twitter_followers', 'twitter_verified', 'age', 'linkedin_bio', 'twitter_bio']:
        if user_dict.get(field, None):
            person.__dict__[field] =  user_dict[field]
    if 'location' in user_dict:
        for key, value in user_dict['location'].items():
            try:
                person.__dict__[key] =  value
            except:
                pass
    person.save()
    if user_dict.get('photo', None):
        img_filename = urlparse(user_dict['photo']).path.split('/')[-1]
        image_content = ContentFile(requests.get(user_dict['photo']).content)
        person.saved_photo.save(img_filename, image_content)
    education = user_dict.get('education', [])
    if override and len(Education.objects.filter(person=person)):
        education = []
    for ed in education:
        educ = Education(person = person)
        educ.save()
        try:
            educ.date_started = datetime.strptime(ed.get("start_month", "January") +' '+ed.get("start_year", str(datetime.today().year)), "%B %Y")
        except Exception as e:
            pass
        try:
            if not ed.get('is_active', False) and ('end_month' in ed or 'end_year' in  ed):
                educ.date_ended = datetime.strptime(ed.get("end_month", "January") +' '+ed.get("end_year", str(datetime.today().year)), "%B %Y")
        except Exception as e:
            pass
        for ed_info in ['school_name', 'is_active']:
            educ.__dict__[ed_info] = ed.get(ed_info, '')
        if 'fields_of_study' in user_dict.keys():
            for interest in ed['fields_of_study']:
                interst_obj = Industry.objects.get_or_create(name = interest.lower())
                educ.fields_of_study.add(interst_obj)
        if 'degree' in ed.keys():
            degree = ed['degree'].lower()
            if 'ph' in degree:
                educ.education_level = 5
            elif 'ma' in degree or 'ms' in degree or 'm.' in degree:
                educ.education_level = 4
            elif 'ba' in degree or 'bs' in degree or 'b.' in degree:
                educ.education_level = 3
        educ.save()
    positions = user_dict.get('positions',[])
    for pos in positions:
        company, company_created = makeCompany(pos['company_dict'], override = False)
        if complete_companies and company_created:
            print "completing", company.id
            completeCompany.delay(pos['company_dict'])
        j, created = Job.objects.get_or_create(person = person, company = company, title = pos.get('position_title', '').lower())
        j.is_active = pos.get('is_active', False)
        try:
            j.date_started = datetime.strptime(pos.get("start_month", "January") +' '+pos.get("start_year", str(datetime.today().year)), "%B %Y")
        except Exception as e:
            pass
        try:
            if not pos.get('is_active', False) and ('end_month' in pos or 'end_year' in  pos):
                j.date_ended = datetime.strptime(pos.get("end_month", "January") +' '+pos.get("end_year", str(datetime.today().year)), "%B %Y")
        except Exception as e:
            pass
        if j.date_ended and j.date_started:
            try:
                j.months = (j.date_ended - j.date_started).days/30
            except:
                pass
        elif j.date_started and j.is_active:
            try:
                j.months = (datetime.now() - j.date_started).days/30
            except:
                pass
        if j.date_ended == None:
            j.is_active = True
        j.save()
    for email in user_dict.get('emails', []):
        email_ob, created = EmailAddress.objects.get_or_create(address = email['address'], defaults = {'person':person, 'is_deliverable':email.get('is_deliverable'), 'type_of_email':email.get('type_of_email', ''), 'is_current':True})
        for source in email.get('sources', []):
            email_ob.sources.add(Website.objects.get_or_create(url = source['url'].lower(), defaults = {'html':source.get('html', '')})[0])
        email_ob.save()
    interests = user_dict.get('interests', [])
    try:
        person.interests.add(*[Industry.objects.get_or_create(name = name.lower().strip())[0] for name in interests])
    except Exception as e:
        pass
    person.save()
    return person, created


def string_to_dt(t):
    t = re.sub(re.compile("\([\s\w\d]+\)"), "", t)
    if 'present' in t.lower():
        return datetime.now()
    try:
        return datetime.strptime(t, "%B %Y")
    except:
        pass
    try:
        return datetime.strptime(t, "%Y")
    except:
        pass

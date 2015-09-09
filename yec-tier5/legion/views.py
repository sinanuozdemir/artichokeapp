if True:
    from django.shortcuts import render
    from django.template import RequestContext
    from django.shortcuts import render_to_response, redirect, HttpResponseRedirect, HttpResponse
    import unicodecsv
    from django.contrib.auth import authenticate, login, logout, get_user
    from django.core.context_processors import csrf
    from legion.models import Person, Company, EmailAddress, Education, Job, Lead, Query, User, Organization, Industry, UserPermissions
    from legion.forms import DocumentForm, ImageUploadForm
    import json
    import random
    import hound
    from django.views.decorators.csrf import csrf_exempt
    import datetime
    from django.db.models import Count
    import modules
    import os
    import operator
    import time
    import csv
    import operator
    import string
    from fuzzywuzzy import fuzz
    from urlparse import urlparse
    import requests
    import scrapers
    import urllib2
    from django.core.files.base import ContentFile
    import paramiko
    import re
    import Legion
    from django.db.models import Q, F
    from django.contrib.auth.decorators import login_required
    from djqscsv import render_to_csv_response

WEB_REGEX = re.compile("(http[s]?://)?(www\.)?([^/]*)/?(.*)")

def return_url_end(url, middle = False):
    if url == '':
        return ''
    match = re.match(WEB_REGEX, url)
    if match:
        middle_ = match.group(3)
        if len(middle_) and middle_[-1] == '/':
            middle_ = middle_[:-1]
        end_ = match.group(4)
        if len(end_) and end_[-1] == '/':
            end_ = end_[:-1]
        if not middle:
            return end_
        else:
            if len(end_):
                return middle_+'/'+end_
            return middle_
    else:
        return ''

def signup(request):
    david ={'emails': [{'address':'dp@dperry.com'}], 'interests': ['video games', 'cloud gaming', 'Game Development', 'Game Design', 'MMO', 'Flash', 'Film', 'MMORPG', 'Streaming Media', 'Advertising', 'Facebook', 'Licensing', 'Consulting', 'Video Games', 'Cloud Computing', 'Entrepreneurship', 'Gambling', 'Game'], 'name': 'David Perry', 'positions': [{'start_month': 'August', 'start_year': '2012', 'is_active': True, 'company_dict': {'web_presence': {'company_linkedin': {'url': 'company/1254'}}, 'name': 'Sony Computer Entertainment America LLC'}, 'company_name': 'Sony Computer Entertainment America LLC', 'position_title': 'CEO - Gaikai'}, {'start_month': 'March', 'start_year': '2009', 'end_year': '2012', 'is_active': False, 'end_month': 'August', 'company_dict': {'web_presence': {'company_linkedin': {'url': 'company/859051'}}, 'name': 'Gaikai, Inc.'}, 'company_name': 'Gaikai, Inc.', 'position_title': 'CEO &amp; Co-Founder'}, {'start_month': 'March', 'start_year': '2006', 'end_year': '2009', 'is_active': False, 'end_month': 'December', 'company_dict': {'web_presence': {'company_linkedin': {'url': 'company/676087'}}, 'name': 'Acclaim Games Inc.'}, 'company_name': 'Acclaim Games Inc.', 'position_title': 'CCO (Chief Creative Officer)'}, {'start_month': 'October', 'start_year': '1993', 'end_year': '2006', 'is_active': False, 'end_month': 'February', 'company_dict': {'web_presence': {'company_linkedin': {'url': 'company/13479'}}, 'name': 'Shiny Entertainment Inc.'}, 'company_name': 'Shiny Entertainment Inc.', 'position_title': 'President and Founder / Programmer / Game Designer'}, {'start_year': '1991', 'end_year': '1993', 'is_active': False, 'company_dict': {'web_presence': {'company_linkedin': {'url': 'company/26334'}}, 'name': 'VIRGIN GAMES INC.'}, 'company_name': 'VIRGIN GAMES INC.', 'position_title': 'Team Leader / Lead Programmer / Game Designer'}, {'start_year': '1990', 'end_year': '1991', 'is_active': False, 'company_dict': {'name': 'Dave Perry / Nick Bruty Team'}, 'company_name': 'Dave Perry / Nick Bruty Team', 'position_title': 'Lead Programmer / Game Designer'}, {'start_year': '1987', 'end_year': '1990', 'is_active': False, 'company_dict': {'name': 'PROBE SOFTWARE'}, 'company_name': 'PROBE SOFTWARE', 'position_title': 'Lead Programmer / Game Designer'}, {'start_year': '1986', 'end_year': '1987', 'is_active': False, 'company_dict': {'name': 'UK Team'}, 'company_name': 'UK Team', 'position_title': 'Team Leader / Lead Programmer / Game Designer'}, {'start_year': '1984', 'end_year': '1986', 'is_active': False, 'company_dict': {'name': 'Mikro-Gen'}, 'company_name': 'Mikro-Gen', 'position_title': 'Lead Programmer / Game Designer'}, {'start_year': '1982', 'end_year': '1984', 'is_active': False, 'company_dict': {'name': 'Freelance Writer'}, 'company_name': 'Freelance Writer', 'position_title': 'Game Programmer / Game Designer'}], 'age': 30, 'web_presence': {'personal_linkedin': {'url': 'in/dperry'}}, 'location': 'Orange County, California Area', 'photo': 'https://media.licdn.com/mpr/mpr/shrink_200_200/p/1/000/11c/269/375621e.jpg', 'education': [{'fields_of_study': ['Video Game Industry'], 'end_year': '2006', 'start_year': '2006', 'school_name': 'Queen&#39;s University Belfast', 'degree': 'Visiting Fellow in the Creative Industries'}], 'industry': 'Computer Games'}
    p = modules.getPerson(david)
    print p, p.id, p.saved_photo.url
    return
    return render_to_response('signup.html', {}, context_instance=RequestContext(request))

def waitlistform(request):
    return render_to_response('waitlistform.html', {}, context_instance=RequestContext(request))

def splash(request):
    return render_to_response('index.html', {}, context_instance=RequestContext(request))

def member(request):
    return render_to_response('member.html', member_info, context_instance=RequestContext(request))

def all_members(request):
    if request.user.is_anonymous():
        return HttpResponseRedirect('/login')
    all_members_info = {}
    all_members_info.update(csrf(request))
    org = UserPermissions.objects.get(user = get_user(request)).organization
    users_in_organization = UserPermissions.objects.filter(organization = org)
    year = datetime.datetime.now().year
    month = datetime.datetime.now().month
    all_members_info['users_in_organization'] = []
    total_leads = []
    rows = len(users_in_organization )/ 3 + 1
    for userperm in users_in_organization:
        user = userperm.user
        querys = Query.objects.filter(user = user,
                              date_made__year=year,
                              date_made__month=month)
        leads = Lead.objects.filter(user = user,
                              date_matched__year=year,
                              date_matched__month=month)
        p = [{'person':l.person, 'date_added':l.date_matched, 'added_by':user.first_name} for l in leads]
        total_leads += p
        leads_this_month = sum([q.leads_produced for q in querys])
        all_members_info['users_in_organization'].append({'user':user, 'user_perm':userperm, 'leads_this_month':leads_this_month})
    all_members_info['rows'] = ['a']*rows
    return render_to_response('all_members.html', all_members_info, context_instance=RequestContext(request))

@csrf_exempt
def lead_management(request):
    if request.user.is_anonymous():
        return HttpResponseRedirect('/login')
    lead_management_info = {}
    lead_management_info.update(csrf(request))
    org = UserPermissions.objects.get(user = get_user(request)).organization
    users_in_organization = UserPermissions.objects.filter(organization = org)
    year = datetime.datetime.now().year
    month = datetime.datetime.now().month
    lead_management_info['users_in_organization'] = []
    total_leads = Lead.objects.filter(organization = org)
    print total_leads.count()
    if request.method == 'POST':
        print request.POST
        if 'export_new'in request.POST.keys():
            new_leads = Lead.objects.filter(organization = org, new=True)
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="new_leads.csv"'
            writer = csv.writer(response)
            writer.writerow(['Name', 'Age','Email','Twitter','Linkedin','Website','Location'])    
            for lead in new_leads:
                p = lead.person
                lead.new = False
                lead.save()
                try:
                    writer.writerow([p.name, p.age, p.email, p.personal_twitter, p.personal_linkedin, p.personal_home_page, p.location])
                except:
                    pass
            return response
        elif 'post_note' in request.POST.keys():
            if len(request.POST['post_note']):
                l = Lead.objects.get(id=request.POST['lead_id'])
                n = LeadNote(lead=l, note=request.POST['post_note'], author=request.user)
                n.save()
        elif 'delete_selected' in request.POST.keys():  
            leads_to_output = request.POST.getlist('leadsToExport')
            for lead in leads_to_output:
                Lead.objects.get(id=lead).delete()
            return HttpResponseRedirect('lead_management')
        elif "export_selected" in request.POST.keys():
            leads_to_output = request.POST.getlist('leadsToExport')
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="leads.csv"'
            writer = csv.writer(response)
            writer.writerow(['Name', 'Age','Email','Twitter','Linkedin','Website','Location'])    
            for l in Lead.objects.filter(pk__in=leads_to_output):
                p = l.person
                try:
                    writer.writerow([p.name, p.age, p.email, p.personal_twitter, p.personal_linkedin, p.personal_home_page, p.location])
                except Exception as e:
                    print e
                    pass
            return response
        elif "requesting" in request.POST.keys():
            l = Lead.objects.get(id=request.POST['requesting'])
            l.new = False
            l.save()
            n = LeadNote.objects.filter(lead=l)
            p = l.person
            return HttpResponse(response, mimetype="application/json")
        elif 'autofill' in request.POST.keys() or 'add_lead' in request.POST.keys():
            d = dict((k, v) for k, v in request.POST.iteritems() if v)
            del d['csrfmiddlewaretoken']
            person = {}
            person['web_presence'] = {}
            for key in d.keys():
                if key == 'email':
                    person['emails'] = [{'address':d['email']}]
                elif 'company_' in key:
                    if 'http' in d[key]:
                        d[key] = return_url_end(d[key], middle=('home_page' in key))
                    person['web_presence'][key] = {'url':d[key]}
            print person
            person_in_db = modules.getPerson(person)
            if person_in_db is not None:
                print "in database!"
                lead = Lead.objects.filter(person=person_in_db, organization = org)
                if len(lead) == 0:
                    q = Query(organization = org, user = request.user, leads_produced = 1)
                    q.save()
                    lead = Lead(person=person_in_db, organization = org, user=request.user)
                    lead.save()
            else:
                print "not in db!"
                legion = Legion3.findAPerson2(person)
                legion.getAllSocialMedias()
                legion.getAllBasicInfo()
                if 'name' in legion.information.keys():
                    p = modules.makePerson(legion.information)
                    q = Query(organization = org, user = request.user, leads_produced = 1)
                    q.save()
                    lead = Lead(person=p, organization = org, user=request.user)
                    lead.save()
    lead_management_info['total_leads'] = total_leads
    return render_to_response('lead_management.html', lead_management_info, context_instance=RequestContext(request))

@csrf_exempt
def account(request):
    if request.user.is_anonymous():
        return HttpResponseRedirect('/login')
    account_info = {}
    account_info.update(csrf(request))
    current_perm = UserPermissions.objects.get(user = get_user(request))
    account_info['current_user_permission'] = current_perm
    if request.method == 'POST':
        print request.POST
        if 'newName' in request.POST.keys():
            if request.POST['newPassword'] == request.POST['newPasswordAgain']:
                try:
                    u = User(
                        first_name=request.POST['newName'].split(' ')[0], 
                        last_name=request.POST['newName'].split(' ')[1],
                        password = request.POST['newPassword'],
                        max_leads_per_month = int(request.POST['leadThreshold']),
                        email = request.POST['newEmail']
                    )
                    u.save()
                    up = UserPermissions(
                        user = u,
                        organization = current_perm.organization
                        )
                    up.is_team_leader = 'squaredFour' in request.POST.keys()
                    up.save()
                except Exception as e:
                    pass
            return HttpResponseRedirect('/account')
        elif 'deleteselect' in request.POST.keys():
            for e in request.POST.getlist('deleteselect'):
                u = User.objects.get(email = e)
                up = UserPermissions.objects.get(user = u)
                u.password = ''
                u.is_active = False
                u.organization = None
                up.delete()
                u.save()
        elif 'modifyselect' in request.POST.keys():
            for e in request.POST.getlist('modifyselect'):
                u = User.objects.get(email = e, is_active=True)
                up = UserPermissions.objects.get(user = u)
                if "promote" in request.POST.keys():
                    up.is_team_leader = True
                    up.save()
                if "demote" in request.POST.keys():
                    up.is_team_leader = False
                    up.save()
        elif 'ProfilePicture' in request.FILES.keys():
            try:
                current_perm.profile_picture = request.FILES['ProfilePicture']
                current_perm.save()
            except:
                pass
        elif 'logout' in request.POST.keys():
            return HttpResponseRedirect('/logout/')
        elif "Password" in request.POST.keys() or 'EmailAddress' in request.POST.keys():
            if len(request.POST['Password']) > 0:
                request.user.password = request.POST['Password']
            if len(request.POST['EmailAddress']):
                request.user.email = request.POST['EmailAddress']
            request.user.save()
        return HttpResponseRedirect('/account')
    return render_to_response('account.html', account_info, context_instance=RequestContext(request))

@csrf_exempt
def supsecimport(request):
    s_info = {}
    s_info.update(csrf(request))
    if request.method == 'POST':
        if request.POST['type'] == 'person':
            try:
                modules.makePerson.delay(json.loads(request.POST['data']))
            except Exception as e:
                print "error in making person", e
                pass
        elif request.POST['type'] == 'company':
            try:
                modules.makeCompany(json.loads(request.POST['data']))
            except Exception as e:
                print "error in making company", e
                pass
        elif request.POST['type'] == 'company_find':
            in_db = modules.getCompany(json.loads(request.POST['data'])) != None
            return HttpResponse(json.dumps({'in_db':in_db}), content_type="application/json")
        elif request.POST['type'] == 'person_find':
            in_db = modules.getPerson(json.loads(request.POST['data'])) != None
            return HttpResponse(json.dumps({'in_db':in_db}), content_type="application/json")
        elif request.POST['type'] == 'email':
            results = json.loads(request.POST['data'])
            for r in results:
                p = Person.objects.get(id=r['id'])
                if r.get('email', None):
                    p.email = r.get('email', None).lower()
                p.is_analyzed = True
                p.last_analyzed = datetime.datetime.now()
                p.save()
    elif 'num' in request.GET.keys():
        num = request.GET.get('num', 1) 
        to_return = {}
        search_results = Person.objects.filter(is_analyzed = False)
        print search_results.count(), "people left"
        response_data = [modules.getPersonDict(p) for p in  search_results.order_by('?')[:num]]
        return HttpResponse(json.dumps(response_data), content_type="application/json")
    return render_to_response('blank.html', s_info, context_instance=RequestContext(request))
 
def lead_generation(request):
    if request.user.is_anonymous():
        return HttpResponseRedirect('/login')
    lead_generation_info = {}
    lead_generation_info.update(csrf(request))
    if request.method == 'POST':
        print request.POST
        lead_generation_info.update(csrf(request))
        if "company_funding" in request.POST.keys():                            #SEARCHING
            lead_generation_info['current_leads'] = []
            query_dict =  modules.createQueryDict(request.POST)
            query_title = ', '.join([k.replace('__icontains',':').replace('__gte', ' > ').replace('__lte',' < ')+" "+v for k, v in request.POST.iteritems() if len(v) and v != 'No Preference' and k != 'csrfmiddlewaretoken'])
            search_results = modules.getSearchResults(query_dict)
            if len(query_dict['company']):
                q = Query(user = request.user, title=query_title, extra_info = json.dumps(query_dict), organization = current_perm.organization)
                q.save()
            if search_results.count():
                q.people = search_results
                lead_generation_info['email_counter'] = search_results.exclude(emailaddress__address=None).count()
                lead_generation_info['twitter_counter'] = search_results.exclude(personal_twitter=None).count()
                lead_generation_info['linkedin_counter'] = search_results.exclude(personal_linkedin=None).count()
                lead_generation_info['lead_counter'] = search_results.count()
                q.people_generated = lead_generation_info['lead_counter']
                q.email_counter = lead_generation_info['email_counter']
                q.twitter_counter = lead_generation_info['twitter_counter']
                q.linkedin_counter = lead_generation_info['linkedin_counter']
                if float(lead_generation_info['email_counter']) / lead_generation_info['lead_counter'] < .6:
                    q.needs_emails = True
                if lead_generation_info['lead_counter'] < 1000:
                    q.needs_people = True
                q.save()
            else:
                q.needs_people = True
                q.save()
        elif 'import' in request.POST.keys(): #import leading
            all_leads = request.POST.getlist('totalLeads')
            twitter = request.POST.getlist('totalTwitter')
            email = request.POST.getlist('totalEmails')
            linkedin = request.POST.getlist('totalLinkedin')
            for a in email:
                q = Query.objects.get(id=a)
                for person in q.people.exclude(emailaddress__address=None):
                    l = Lead.objects.get_or_create(organization = current_perm.organization, person = person, defaults={'user': get_user(request)})
            for a in linkedin:
                q = Query.objects.get(id=a)
                for person in q.people.exclude(personal_linkedin=None):
                    l = Lead.objects.get_or_create(organization = current_perm.organization, person = person, defaults={'user': get_user(request)})
            for a in twitter:
                q = Query.objects.get(id=a)
                for person in q.people.exclude(personal_twitter=None):
                    l = Lead.objects.get_or_create(organization = current_perm.organization, person = person, defaults={'user': get_user(request)})
            for a in all_leads:
                q = Query.objects.get(id=a)
                for person in q.people.all():
                    l = Lead.objects.get_or_create(organization = current_perm.organization, person = person, defaults={'user': get_user(request)})
            return HttpResponseRedirect('lead_generation')
    return render_to_response('lead_generation.html', lead_generation_info, context_instance=RequestContext(request))
    
def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/login/')

def linkedin_authenticate(request):
    c = {}
    code = request.GET.get('code')
    if code is not None:
        s = modules.LinkedinLogin(code = code)
        print s.getExpirationDate()
        #either we have their linkedin or we dont or we are updating their token
        if request.user.is_anonymous():
            # instead of making a user, try to find first
            u = User()
            up = UserPermissions(user = u)
            #u.save()
            #up.save()
        info = UserPermissions.objects.get(user=get_user(request))
        p = info.person
        if not p:
            print "making new person"
            p = Person()
        print s.getPublicProfile()
        #ADDD check if this is already an authenticated linekdin
        print info.linkedin_access_token, "access token", s.getAccessToken()
        print info.linkedin_secret_code, "linkedin_secret_code", code
    return HttpResponseRedirect('/lead_generation/')

def login_view(request):
    login_info = {}
    #state = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(30))
    #login_info['linkedin_link'] = 'https://www.linkedin.com/uas/oauth2/authorization?response_type=code&scope=r_network%20r_fullprofile&client_id=7725swte4bh3q8&state='+state+'&redirect_uri=http://127.0.0.1:8080/linkedin_authenticate'
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(email=email, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/lead_generation/')
            else:
                pass
        else:
            pass
    return render_to_response('login.html', login_info, context_instance=RequestContext(request))

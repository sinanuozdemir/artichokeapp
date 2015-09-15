import string
from django.utils.timezone import utc
from textblob import TextBlob
from datetime import datetime, timedelta
import requests
from djqscsv import render_to_csv_response
import json, decimal
from django.template import RequestContext
from django.shortcuts import render_to_response, HttpResponseRedirect, HttpResponse
from legion.models import Person, Company, Industry, Job, EmailAddress
from dashboard.models import ICP, statsSnapshot, User, Document, Website, marketEvent, Connection, twitterSentiment, Competitor, keyWord, Tweet, apiCredentials, Scraper, targetMarket, Proxy
from register import RegistrationForm, AuthenticationForm, RegistrationFormTier5
from django.contrib.auth import login as django_login, authenticate
from django.contrib import auth
from legion import modules as legion_modules
import modules
from django.db.models import Q, Avg, Count
from django.contrib.auth.decorators import login_required
import random, string, re
import sendgrid
import tweepy
from django.views.decorators.csrf import csrf_exempt
import itertools



MAILCHIMP_CLIENT = '826106052845'
MAILCHIMP_SECRET = '96a792812b88918b335cd00846a3922c'
MAILCHIMP_REDIRECT_URI = 'http://legionanalytics.com/mailchimp/success/'
mailchimp_auth_url = 'https://login.mailchimp.com/oauth2/authorize?response_type=code&client_id=826106052845&redirect_uri=http://legionanalytics.com/mailchimp/success/'

sg = sendgrid.SendGridClient('sinan.u.ozdemir', 'tier5beta')
# stripe.api_key = "sk_live_Vl3d20R5NvvLUo3I7G55nDcg"

# plans = {'Free Plan': (50, 50), 'Pro Plan': (5000, 5000), 'Small Business Plan': (50000, 50000), 'Enterprise Plan': (100000, 100000)}
# stripe_plan_dict = {'0': 'Free Plan', '4900': 'Pro Plan', '35000':'Small Business Plan', '100000': 'Enterprise Plan'}

def twitterLogin(request):
    return

def mailchimpAuth(request):
    code = request.GET.get('code', None)
    if code:
        payload = {
        'grant_type':'authorization_code',
        'client_id': MAILCHIMP_CLIENT,
        'client_secret':MAILCHIMP_SECRET,
        'redirect_uri': MAILCHIMP_REDIRECT_URI,
        'code': code
        }
        request_ = requests.post('https://login.mailchimp.com/oauth2/token', data = payload)
        request.user.mailchimp_access_token = request_.json()['access_token']
        dc = requests.get('https://login.mailchimp.com/oauth2/metadata', headers = {'Authorization': 'OAuth '+str(request_.json()['access_token'])}).json()['dc']
        request.user.mailchimp_access_token = request.user.mailchimp_access_token + '-'+ dc
        request.user.save()
    return HttpResponseRedirect('/legion/my_account')

@login_required
def googleAuth(request):
    if request.GET.get('code', ''):
        r = requests.post('https://www.googleapis.com/oauth2/v3/token', data = {
            'redirect_uri': 'http://legionanalytics.com/google/success',
            'client_secret': 'VQ2sIQGhXH-ue6olCgUY9L3g',
            'client_id': '994895035422-bes5cqbhmf140j906598j1q91pvcnn08.apps.googleusercontent.com',
            'code': request.GET.get('code'),
            'grant_type': 'authorization_code'
            })
        response = r.json()
        request.user.google_refresh_token = response['refresh_token']
        request.user.id_token             = response['id_token']
        request.user.google_access_token  = response['access_token']
        r = requests.get('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'%response['access_token'])
        request.user.google_auth_email = r.json()['email']
        request.user.save()
        return HttpResponseRedirect('/legion/lead_stream')

# this one handles login and and auth
def linkedinAuth(request):
    state = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(30))
    linkedin_login_link = 'https://www.linkedin.com/uas/oauth2/authorization?response_type=code&scope=r_emailaddress%20r_basicprofile&client_id=750cvasmd47qgf&state='+state+'&redirect_uri=http://legionanalytics.com/linkedin/success'
    c = {}
    code = request.GET.get('code')
    if code is not None:
        s = modules.LinkedinLogin(code = code)
        e =  s.getEmail()
        user, user_created = User.objects.get_or_create(email = e)
        if user_created or user.linkedin_access_token == '' or datetime.utcnow().replace(tzinfo=utc) > user.linkedin_access_token_expires: # new user or expired linkedin token!!!
            user.linkedin_access_token = s.getAccessToken()
            user.linkedin_secret_code = code
            user.linkedin_access_token_expires = s.getExpirationDate()
            user.linkedin_public_profile = s.getPublicProfile()
            person = user.person
            if not person:
                pe, pe_c = Person.objects.get_or_create(personal_linkedin = user.linkedin_public_profile)
                modules.completePerson.delay(pe.id)
                user.person = pe
            else:
                user.person.personal_linkedin = user.linkedin_public_profile
                user.person.save()
                modules.completePerson.delay(user.person.id)
            user.save()
            modules.getInterestsOfUser.delay(user.id)
            if user_created:
                modules.makeDemographicStats.delay(user.id, period = 1)
        user = authenticate(email = e, social = True)
        django_login(request, user)
        return HttpResponseRedirect('/legion/dashboard')

@login_required
def twitterAuth(request):
    if request.GET.get('denied', None):
        return HttpResponseRedirect('/legion/lead_stream')
    verifier = request.GET.get('oauth_verifier')
    auth = tweepy.OAuthHandler('3IVlaNBLG2G0AVdfzhZxOleVA', 'pgE7QEoWd8RDAhpYVpDXgoHjqRsA6wjG8a7fbhijRXQ2oMoivO')
    auth.request_token = request.session['oauth_token']
    auth.get_access_token(verifier)
    user = request.user
    user.twitter_access_token_key = auth.access_token
    user.twitter_access_token_secret = auth.access_token_secret
    user.save()
    modules.getTwitterStats(user.id)
    modules.getSentimentStatsForUser(user.id)
    modules.analyzeFollowers.delay(user.id)
    auth.set_access_token(user.twitter_access_token_key, user.twitter_access_token_secret)
    api = tweepy.API(auth)
    me = api.me()
    user.twitter_id = me.id
    user.twitter_handle = me.screen_name.lower()
    user.twitter_picture = me.profile_image_url.replace('_normal','')
    person = user.person
    if not person:
        pe, pe_c = Person.objects.get_or_create(personal_twitter = me.screen_name.lower())
        modules.completePerson.delay(pe.id)
        user.person = pe
    else:
        user.person.personal_twitter = me.screen_name.lower()
        user.person.save()
        modules.completePerson.delay(user.person.id)
    user.save()
    k = keyWord.objects.get_or_create(text='@'+user.twitter_handle, defaults={'reference': 'twitter', 'active': True})[0]
    k.user.add(user)
    return HttpResponseRedirect('/legion/dashboard')


@login_required
def my_account(request):
    my_account_info = {}
    if request.method == "POST":
        if 'twitter' in request.POST:
            auth = tweepy.OAuthHandler('3IVlaNBLG2G0AVdfzhZxOleVA', 'pgE7QEoWd8RDAhpYVpDXgoHjqRsA6wjG8a7fbhijRXQ2oMoivO')
            redirect_url = auth.get_authorization_url()
            request.session['oauth_token'] = auth.request_token
            return HttpResponseRedirect(redirect_url)
        if request.POST.get('new-email', False):
            request.user.email = request.POST['new-email']
            request.user.save()
        if request.POST.get('new-password', False):
            request.user.set_password(request.POST['new-password'])
            request.user.save()
        return HttpResponseRedirect('/legion/my_account')
    return render_to_response('my_account.html', my_account_info, context_instance=RequestContext(request))

def forgot_password(request):
    if request.method == 'POST':
        if request.POST.get('token', None):
            user = User.objects.get(password_token=request.POST['token'].strip())
            user.set_password(request.POST['password'])
            user.save()
            user = authenticate(password_token = request.POST['token'].strip())
            django_login(request, user)
            return HttpResponseRedirect('/legion/lead_stream')
        else:
            try:
                user = User.objects.get(email=request.POST['email'])
                email = request.POST['email'].lower().strip()
                chars = string.ascii_letters + string.digits + '!@#$%^&*()'
                random_code = ''.join(random.choice(chars) for i in range(20))
                user.password_token = random_code
                user.save()
                message = sendgrid.Mail()
                message.set_from('yourfriends@legionanalytics.com')
                message.add_to(email)
                message.set_subject('Forgot Your Password?')
                message.set_html('Body')
                message.add_substitution(':Code:', random_code)
                message.set_text('Body')
                message.add_filter('templates', 'enable', '1')
                message.add_filter('templates', 'template_id', 'ba9b5dea-4de1-44f6-ac37-ba7c254e7a1e')
                status, msg = sg.send(message)
            except Exception as e:
                pass

    return render_to_response('forgot-pw.html', {}, context_instance=RequestContext(request))

def splash(request):
    return render_to_response('home.html', context_instance=RequestContext(request))

def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/legion/login')

def login(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/legion/my_account')
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = authenticate(email=request.POST['email'], password=request.POST['password'])
            if user is not None:
                if user.is_active:
                    django_login(request, user)
                    return HttpResponseRedirect('/legion/lead_stream')
    else:
        form = AuthenticationForm()
    return render_to_response('dash_login.html', {
        'form': form,
    }, context_instance=RequestContext(request))

def error404(request):
    return render_to_response('404page.html', {}, context_instance=RequestContext(request))

@csrf_exempt
@login_required
def lead_stream(request, view_id):
    tms = targetMarket.objects.filter(user=request.user)
    if tms.count() > 0:
        try:
            tm = targetMarket.objects.get(pk=view_id, user = request.user)
        except:
            tm = tms.first()
        connections = Connection.objects.filter(target_market = tm).values('new_lead', 'message','message__opened','message__subject', 'job__company__funding', 'job__company__industries__name', 'job__company__number_of_employees', 'job__company__revenue', 'job__company__company_home_page', 'job__company__company_linkedin', 'job__company__location', 'job__company__name', 'job__company__company_facebook', 'job__company__company_twitter', 'person__personal_facebook', 'person__personal_twitter', 'person__personal_linkedin', 'person__personal_home_page', 'job__title', 'person__id', 'person__name', 'person__saved_photo', 'person__twitter_bio', 'person__age', 'person__klout_score', 'person__location', 'person__emailaddress__address').distinct('person__id')
        new_con = len([c for c in connections if c['new_lead']])
        people = {c['person__id']: c for c in connections}
        tms = targetMarket.objects.filter(user=request.user).exclude(pk=tm.id)
    else:
        people = {}
        new_con = 0
        tm = None
    if request.method == 'POST':
        if "DELETE" in request.POST:
            try:
                tm.delete()
            except:
                pass
            return HttpResponseRedirect('/legion/lead_stream')
        elif 'export_leads' in request.POST:
            connections = Connection.objects.filter(target_market = tm).values('new_lead', 'job__title', 'job__company__funding', 'job__company__revenue', 'job__company__company_home_page', 'job__company__company_linkedin', 'job__company__company_twitter', 'job__company__company_facebook', 'job__company__location', 'job__company__name', 'person__personal_facebook', 'person__personal_twitter', 'person__personal_linkedin', 'person__personal_home_page', 'job__title', 'person__id', 'person__name', 'person__saved_photo', 'person__twitter_bio', 'person__age', 'person__klout_score', 'person__location', 'person__emailaddress__address').distinct('person__id')
            return render_to_csv_response(connections)
        elif "clicked_new" in request.POST:
            Connection.objects.filter(target_market = tm).update(new_lead = False)
        elif 'name' in request.POST:
            query = request.POST.copy()
            query = {k: v for k, v in query.items() if len(v)}
            if 'industries' in query:
                industries = [l.strip() for l in request.POST.getlist('industries')]
            else:
                industries = ['']
            name = query['name']
            query['industries'] = ', '.join(industries)
            try:
                del query['name']
                del query['csrfmiddlewaretoken']
            except:
                pass
            description = ''
            if 'job_title' in query:
                description += query['job_title'].title()+' | '
            if 'location' in query:
                description += query['location'].title()+' | '
            if "revenue_max" in query or "revenue_min" in query:
                revenue = ''
                if "revenue_min" in query:
                    revenue += str(query['revenue_min'])+" <"
                revenue += " Revenue "
                if "revenue_max" in query:
                    revenue += " < "+str(query['revenue_max'])
                description += revenue +' | '
            if "funding_min" in query or "funding_max" in query:
                revenue = ''
                if "funding_min" in query:
                    revenue += str(query['funding_min'])+" <"
                revenue += " Funding "
                if "funding_max" in query:
                    revenue += " < "+str(query['funding_max'])
                description += revenue +' | '
            if "age_min" in query or "age_max" in query:
                revenue = ''
                if "age_min" in query:
                    revenue += str(query['age_min'])+" <"
                revenue += " Age "
                if "age_max" in query:
                    revenue += " < "+str(query['age_max'])
                description += revenue +' | '
            shortened_name = ''.join([n[0] for n in name.split(' ')]).upper()
            t = targetMarket(user = request.user, name = name, short_name = shortened_name, query = json.dumps(query), description = description, star_limit = 2.)
            t.save()
            try:
                modules.findUsersForTargetMarket.delay(t.id, 5)
            except Exception as ee:
                pass
            if 'job_title' in query:
                positions = [l.strip() for l in request.POST.get('job_title').split((','))]
            else:
                positions = ['']
            if 'location' in query:
                locations = [l.strip() for l in request.POST.get('location').split((','))]
            else:
                locations = ['']
            for keyword, location, industry in list(itertools.product(*[positions, locations, industries])):
                Scraper.objects.get_or_create(keywords = keyword.lower(), industry = industry, location = location.lower(), website='google_linkedin', defaults={'current_index':0})
            for keyword, location in list(itertools.product(*[positions, locations])):
                Scraper.objects.get_or_create(keywords = keyword.lower(), location = location.lower(), website='twitter_scan', defaults={'current_index':51, 'last_run': None, 'targetmarket':t})
        elif 'tweeting' in request.POST:
            modules.tweetAtSomeone.delay(request.user.id, request.POST['tweeting'])
        elif 'emailFrom' in request.POST:
            modules.sendEmailAsUser.delay(request.user.id, request.POST['emailTo'], request.POST['emailBody'], request.POST['emailSubject'])
    is_google_authenticated = request.user.google_auth_email is not None
    return render_to_response('lead_stream.html', {'tms':tms, 'is_google_authenticated':is_google_authenticated, 'people':people, 'new_con':new_con, 'people_json':json.dumps(people), 'tm': tm}, context_instance=RequestContext(request))

@login_required
@csrf_exempt
def getUpdatedLeadStream(request):
    if request.method == 'POST':
        tm_id = request.POST['target_market_id']
        try:
            tm = targetMarket.objects.get(pk=tm_id, user = request.user)
        except:
            return HttpResponse(json.dumps({}),content_type="application/json")
        connections = Connection.objects.filter(Q(target_market = tm)&Q(new_lead=True)).values('new_lead', 'message','message__opened','message__subject', 'job__title', 'job__company__funding', 'job__company__industries__name', 'job__company__number_of_employees', 'job__company__revenue', 'job__company__company_home_page', 'job__company__company_linkedin', 'job__company__location', 'job__company__name', 'job__company__company_facebook', 'job__company__company_twitter', 'person__personal_facebook', 'person__personal_twitter', 'person__personal_linkedin', 'person__personal_home_page', 'job__title', 'person__id', 'person__name', 'person__saved_photo', 'person__twitter_bio', 'person__age', 'person__klout_score', 'person__location', 'person__emailaddress__address').distinct('person__id')
        new_con = len([c for c in connections if c['new_lead']])
        people = {c['person__id']: c for c in connections}
        to_return = {'people':people, 'new_con':new_con, 'people_json':json.dumps(people)}
        return HttpResponse(json.dumps(to_return),content_type="application/json")
    return HttpResponse(json.dumps({}),content_type="application/json")



def decimal_default(obj):
    if isinstance(obj, decimal.Decimal):
        return float(obj)
    raise TypeError

def average(l):
    try:
        l = [float(a) for a in l]
        return round(sum(l) / float(len(l)), 2)
    except Exception as e:
        return 0


@csrf_exempt
def getInboundInfo(request, page_num, per_page = 10):   
    people = []
    pks = set()
    user_id = request.user.id
    if not page_num:
        page_num = 1
    page_num = int(page_num)
    if request.method == 'POST':
        query = request.POST.copy()
        try:
            del query['csrfmiddlewaretoken']
        except:
            pass
        if request.session.get('last_inbound_query', '') != json.dumps(query):
            print "making the query", query
            now = datetime.now()
            request.session['last_inbound_query'] = json.dumps(query)
            people_q = Q()
            tweets, tweet_ids = None, None
            if 'competitor_id' in query:
                keywords = keyWord.objects.filter(competitor__id=query['competitor_id'])
                if "positive" in query or "negative" in query:
                    if "positive" in query:
                        if pks:
                            pks &= set(Person.objects.filter(Q(twittersentiment__time_taken__gte=datetime.now() - timedelta(days=30)) & Q(twittersentiment__keyWord__in=keywords)).annotate(avg = Avg('twittersentiment__sentiment')).filter(avg__gt = 0).values_list('id', flat = True))
                        else:
                            pks = set(Person.objects.filter(Q(twittersentiment__time_taken__gte=datetime.now() - timedelta(days=30)) & Q(twittersentiment__keyWord__in=keywords)).annotate(avg = Avg('twittersentiment__sentiment')).filter(avg__gt = 0).values_list('id', flat = True))
                    if "negative" in query:
                        if pks:
                            pks &= set(Person.objects.filter(Q(twittersentiment__time_taken__gte=datetime.now() - timedelta(days=30)) & Q(twittersentiment__keyWord__in=keywords)).annotate(avg = Avg('twittersentiment__sentiment')).filter(avg__lt  = 0).values_list('id', flat = True))
                        else:
                            pks = set(Person.objects.filter(Q(twittersentiment__time_taken__gte=datetime.now() - timedelta(days=30)) & Q(twittersentiment__keyWord__in=keywords)).annotate(avg = Avg('twittersentiment__sentiment')).filter(avg__lt = 0).values_list('id', flat = True))
                else:
                    pks = set(twitterSentiment.objects.filter(~Q(person=None) &Q(time_taken__gte=datetime.now() - timedelta(days=7)) & Q(keyWord__in=keywords)).distinct('person').values_list('person__pk', flat = True))
            elif 'competitor_id' not in query:
                competitors = Competitor.objects.filter(user__id = user_id)
                keywords = keyWord.objects.filter(Q(user__id=user_id)).exclude(id__in=competitors.values_list('keywords__id', flat = True))
                c_q = Q(user_id = user_id)
                if 'all' in query:
                    pks = set(Connection.objects.filter(c_q).values_list('person__pk', flat = True))
                elif 'followers' in query or 'subscriber' in query or 'top_ten' in query:
                    if 'top_ten' in query:
                        pks = set(list(Connection.objects.filter(Q(user_id = user_id) & ~Q(person__klout_score = None)).order_by('-person__klout_score').values_list('person__pk', flat = True))[:10])
                    if 'followers' in query:
                        c_q &= Q(followed_by = True)
                    if 'subscriber' in query:
                        c_q &= Q(from_site = True)
                    if pks:
                        pks &= set(Connection.objects.filter(c_q).values_list('person__pk', flat = True))
                    else:
                        pks = set(Connection.objects.filter(c_q).values_list('person__pk', flat = True))
                if 'positive' in query or 'negative' in query:
                    sentiment_pk = set()
                    if "positive" in query:
                        if sentiment_pk:
                            sentiment_pk |= set(Person.objects.filter(Q(twittersentiment__time_taken__gte=datetime.now() - timedelta(days=30)) & Q(twittersentiment__keyWord__in=keywords)).annotate(avg = Avg('twittersentiment__sentiment')).filter(Q(avg__gt = 0)).values_list('id', flat = True))
                        else:
                            sentiment_pk = set(Person.objects.filter(Q(twittersentiment__time_taken__gte=datetime.now() - timedelta(days=30))  & Q(twittersentiment__keyWord__in=keywords)).annotate(a = Avg('twittersentiment__sentiment')).filter(a__gt = 0).values_list('id', flat = True))
                    if "negative" in query:
                        if sentiment_pk:
                            sentiment_pk |= set(Person.objects.filter(Q(twittersentiment__time_taken__gte=datetime.now() - timedelta(days=30)) & Q(twittersentiment__keyWord__in=keywords)).annotate(a = Avg('twittersentiment__sentiment')).filter(a__lt = 0).values_list('id', flat = True))
                        else:
                            sentiment_pk = set(Person.objects.filter(Q(twittersentiment__time_taken__gte=datetime.now() - timedelta(days=30)) & Q(twittersentiment__keyWord__in=keywords)).annotate(a = Avg('twittersentiment__sentiment')).filter(a__lt = 0).values_list('id', flat = True))
                    if pks:
                        pks &= sentiment_pk
                    else:
                        pks = sentiment_pk
            keywords_text = map(str, keywords.values_list('text', flat = True))
            pks = list(pks)[:200]
            request.session['keywords_text'] = keywords_text
            request.session['last_inbound_query_people'] = pks
            request.session.save()
            pks = pks[(page_num - 1) * per_page:((page_num - 1) * per_page) + per_page]
            twitter_q = Q(person__pk__in=pks) & Q(keywords__in=keywords)
            tweets = Tweet.objects.filter(twitter_q).extra(select={'datestr':"to_char(date, 'YYYY-MM-DD HH24:MI')"})
            people = Person.objects.filter(pk__in=pks).values('personal_facebook', 'personal_twitter', 'personal_linkedin', 'personal_home_page', 'id', 'name', 'saved_photo', 'twitter_bio', 'age', 'klout_score', 'location', 'emailaddress__address').distinct('id')
            for person in people:
                person['num_tweets'] = 0
                person['tweets'] = []
                person['sentiment'] = 'No Sentiment'
                try:
                    person['tweets'] = list(tweets.filter(person__pk = person['id']).values('text', 'status_id', 'datestr', 'textblob_sentiment', 'person__pk')) 
                    person['num_tweets'] = len(person['tweets'])
                    sent = average([float(a['textblob_sentiment']) for a in person['tweets']])
                    if sent > 0:
                        person['sentiment'] = 'Positive Sentiment'
                    elif sent < 0:
                        person['sentiment'] = 'Negative Sentiment'
                    else:
                        person['sentiment'] = 'Neutral Sentiment'
                except Exception as e:
                    pass
                person = dict(person)
            people = list(people) 
        else:
            print "same query"
            tweets = None
            keywords = keyWord.objects.filter(text__in=request.session['keywords_text'])
            pks =  request.session['last_inbound_query_people'][(page_num - 1) * per_page:((page_num - 1) * per_page) + per_page]
            twitter_q = Q(person__pk__in=pks) & Q(keywords__in=keywords)
            tweets = Tweet.objects.filter(twitter_q).extra(select={'datestr':"to_char(date, 'YYYY-MM-DD HH24:MI')"})
            people = Person.objects.filter(pk__in=pks).values('personal_facebook', 'personal_twitter', 'personal_linkedin', 'personal_home_page', 'id', 'name', 'saved_photo', 'twitter_bio', 'age', 'klout_score', 'location', 'emailaddress__address').distinct('id')
            people = list(people)
            for person in people:
                person['num_tweets'] = 0
                person['tweets'] = []
                person['sentiment'] = 'No Sentiment'
                try:
                    person['tweets'] = list(tweets.filter(person__pk = person['id']).values('text', 'id', 'datestr', 'textblob_sentiment', 'person__pk')) 
                    person['num_tweets'] = len(person['tweets'])
                    sent = average([float(a['textblob_sentiment']) for a in person['tweets']])
                    if sent > 0:
                        person['sentiment'] = 'Positive Sentiment'
                    elif sent < 0:
                        person['sentiment'] = 'Negative Sentiment'
                    else:
                        person['sentiment'] = 'Neutral Sentiment'
                except Exception as e:
                    pass
                person = dict(person)
            people = list(people) 
    return HttpResponse(json.dumps(people, default = decimal_default),content_type="application/json")


@login_required
@csrf_exempt
def email_dashboard2(request):
    dashboard_info = {'settings':json.loads(request.user.settings_json)}
    if request.method == 'POST':
        print request.POST
        if 'event_name' in request.POST:
            modules.makeMarketEvent(request.POST, request.user.id)
            return HttpResponseRedirect('/legion/dashboard')
        elif 'deleteMarketEvent' in request.POST:
            marketEvent.objects.get(id = request.POST['deleteMarketEvent']).delete()
            modules.getSentimentStatsForUser.delay(request.user.id)
        elif 'deleteCompetitor' in request.POST:
            print "delete comp"
            c = Competitor.objects.get(id = request.POST['deleteCompetitor'])
            keys = c.keywords.all()
            for key in keys:
                print key.text
                key.user.remove(request.user)
            c.delete()
            return HttpResponseRedirect('/legion/dashboard')
        elif 'replyTweetId' in request.POST and 'tweetTextArea' in request.POST:
            person = Person.objects.get_or_create(personal_twitter = request.user.twitter_handle.lower())[0]
            t = Tweet(text=request.POST['tweetTextArea'], reply_to = request.POST['replyTweetId'], person = person, textblob_sentiment = TextBlob(request.POST['tweetTextArea']).sentiment.polarity)
            t.save()
            tweet = modules.tweetAtSomeone(request.user.id, message = request.POST['tweetTextArea'], reply_to = request.POST['replyTweetId'])
            t.status_id = tweet.id_str
            t.save()
        elif 'new_kpi' in request.POST:
            settings = json.loads(request.user.settings_json)
            settings['inbound_settings']['toolbar'][int(request.POST['kid'][-1])-1] = request.POST['new_kpi']
            request.user.settings_json = json.dumps(settings)
            request.user.save()
            dashboard_info = {'settings':json.loads(request.user.settings_json)}
        elif 'company_name' in request.POST:
            company = {}
            company['web_presence'] = {}
            for item in ['company_linkedin', 'company_twitter', 'company_facebook']:
                if request.POST[item]:
                    cleaned_company_link = re.search('(@)?(https?://)?(www.)?(\w+\.com?/?)?([\w\/]+)?', request.POST[item]).group(5).lower()
                    company['web_presence'][item] = {"url":cleaned_company_link}
            c, c_created = legion_modules.makeCompany(company, override = False)
            if request.POST['company_website']: 
                c.company_home_page = re.search('(@)?(https?://)?(www.)?([\w\.]+\.[cogovm]{2,})/?([\w\/]+)?', request.POST['company_website']).group(4).lower()
                c.save()
            modules.getTwitterStatsForCompany.delay(request.user.id, c.id)
            comp, c_c = Competitor.objects.get_or_create(company=c, user=request.user, defaults = {'name':request.POST['company_name']})

            keywords = [s.strip() for s in request.POST['company_keywords'].lower().split(',')]
            keywords.append('@'+company['web_presence']['company_twitter']['url'].lower())
            keywords = [k for k in keywords if k]
            comp.keywords.add(*[keyWord.objects.get_or_create(text = tag.lower(), defaults={'reference':'twitter', 'active': True})[0] for tag in keywords])
            modules.makeDemographicStatsForCompetitor.delay(comp.id, period = 1)
            modules.getSentimentStatsForCompetitor.delay(comp.id)
            for word in keywords:
                k, k_c = keyWord.objects.get_or_create(text=word.lower(), defaults={'reference': 'twitter', 'active': True})
                k.user.add(request.user)
                modules.gatherTweetsFromKeyword2.delay(k.id)
        return HttpResponseRedirect('/legion/dashboard')
    return render_to_response('email_dashboard.html', dashboard_info, context_instance=RequestContext(request))

def onboarding(request):
    user = request.user
    try:
        first_name = user.name.split(' ')[0]
    except:
        first_name = user.name
    request.session['first_name'] = first_name
    if request.method == 'POST':
        file_ = request.FILES['uploaded_csv']
        d = Document(belongs_to = request.user, docfile = file_)
        d.save()
        user.uploaded_a_csv = True
        user.save()
        request.session['doc_stats'] = modules.getDocumentStats(d.id)
        modules.submitDocument.delay(d.id, user.id)
        return HttpResponseRedirect('/legion/onboarding/almostthere')
    return render_to_response('onboarding1.html', {}, context_instance=RequestContext(request)) 


def signup(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/legion/lead_stream')
    signup_info = {}
    if request.method == 'POST':
        password = request.POST['password']
        stored_user, user_created = User.objects.get_or_create(email = request.POST['email'].strip().lower())
        if user_created:
            stored_user.set_password(request.POST['password'])
            stored_user.company_name = request.POST['company_name'].lower()
            stored_user.phone = request.POST['phone'].lower()
            stored_user.name = request.POST['name'].lower()
            stored_user.save()
            modules.makeDemographicStats.delay(stored_user.id, period = 1)
            w = Website(address=request.POST['website'].lower(), user = stored_user)
            w.save()
            user = authenticate(email=stored_user.email, password=password)
            
            return HttpResponse(json.dumps({'status':'success'}), content_type="application/json")
        else:
            signup_info['error'] = 'A user with this email already exists!!!'
            return HttpResponse(json.dumps({'status':'failed'}), content_type="application/json")
    return render_to_response('signup.html', signup_info, context_instance=RequestContext(request))


def getRandomAPICredentials(request):
    return HttpResponse(json.dumps(apiCredentials.objects.filter(social_media = request.GET['social_media']).order_by('?').values('api_key', 'api_secret', 'access_token', 'access_secret').first()), content_type="application/json")

def getRandomAPIProxies(request):
    return HttpResponse(json.dumps(list(Proxy.objects.order_by('?').values('port', 'ip', 'type_of_proxy')[0:int(request.GET.get('limit', 10))])), content_type="application/json")


def messageView(request, message_id):
    modules.makeMessageView(request, message_id)
    return HttpResponse(json.dumps({}),content_type="application/json") 

@csrf_exempt
def getEntityFromDB(request):
    if request.POST.get('type') == 'company':
        company = legion_modules.getCompany(json.loads(request.POST.get('dict')))
        if company:
            return HttpResponse(json.dumps(legion_modules.getCompanyDict(company)),content_type="application/json") 
    elif request.POST.get('type') == 'person':
        person = legion_modules.getPerson(json.loads(request.POST.get('dict')))
        if person:
            return HttpResponse(json.dumps(legion_modules.getPersonDict(person)),content_type="application/json") 
    return HttpResponse(json.dumps({}),content_type="application/json") 

@csrf_exempt
def putEntityInDB(request):
    override = request.POST.get('override', 'true').lower() == 'true'
    if request.POST.get('type') == 'company':
        legion_modules.makeCompany.delay(json.loads(request.POST.get('dict')), override = override)
    elif request.POST.get('type') == 'person':
        legion_modules.makePerson.delay(json.loads(request.POST.get('dict')), override = override)
    else:
        person, person_created = -1, False
    return HttpResponse(json.dumps({'put in queue': True}),content_type="application/json") 





def check(request):
    people = modules.getInfoForTM(191)
    return HttpResponse(json.dumps(people),content_type="application/json")
    # print
    # print
    # modules.findUsersForTargetMarket(186, 5)
    # modules.completePerson(311904, with_email = False)
    

    # print modules.getTweetsforAllTMs()



    # import experiments
    # import pandas as pd
    # df = pd.read_csv('/Users/sinanozdemir/Downloads/YEC.csv')
    # emails = map(lambda x: str(x.lower()), list(df['Email'].dropna()))
    # print len(emails)
    # for email in emails[100:200]:
    #     print email
    #     experiments.connectEmailToUser.delay(email = email, user_id = 129, validate_first = True, lead = True)
    
    

    # for i in range(10, 11):
    #     print modules.importConspireProfile(i)
    return None









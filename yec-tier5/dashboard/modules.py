from fuzzywuzzy import fuzz
from django.utils.timezone import utc
from klout import *
from BeautifulSoup import BeautifulSoup
import urllib
import pickle
from textblob import TextBlob
import string
import requests
import random
import datetime
import json
from legion.modules import makePerson, getPerson, makeCompany, getPersonDict, getCompanyDict, getCompany
import legion.growth_scrapers as growth_scrapers
import legion.master as master
from legion.models import EmailAddress, Person, Job, Company, Technology, techComp, script, Industry, Website
from celery import task
from dashboard.models import Connection, User, Document, statsSnapshot, Competitor, twitterSentiment, marketEvent, twitterStats, targetMarket, Message, keyWord, Tweet, Scraper, MessageView
from legion import scrapers
from legion import Legion
from collections import defaultdict, Counter
from django.db.models import Q, Count, Avg, Max, Min, Sum, F
from operator import itemgetter, and_, or_, mul
import sendgrid
import re
import itertools
from celery.schedules import crontab
import tweepy
from celery.decorators import periodic_task
import time
import base64
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import cgi


k = Klout('3ezgcrc4urzfexjpuh7qbjvu')
sg = sendgrid.SendGridClient('sinan.u.ozdemir', 'tier5beta')

def average(l):
	if len(l) == 0:
		return 0
	try:
		l = [float(a) for a in l]
		return round(sum(l) / float(len(l)), 2)
	except Exception as e:
		return 0

############################################
##### DEMOGRAPHICS AND CONSUMER STATS ######
############################################

def getDemographicStats(people_pk, keywords = None, period = 1):
	people = Person.objects.filter(pk__in=people_pk)
	stats = {}
	
	all_cities = people.exclude(city=None).values_list('city', flat = True)
	stats['all_of_the_cites'] = Counter(all_cities)
	stats['all_cities'] = [a for a in stats['all_of_the_cites'].most_common(11)]
	if keywords:
		avg_cities = average([a[1] for a in stats['all_of_the_cites'].iteritems()])
		twitter_query = ~Q(textblob_sentiment = 0) & Q(keywords__in=keywords) & Q(date__gte = datetime.datetime.now() - datetime.timedelta(days = period))
		tweets = Tweet.objects.filter(twitter_query).values_list('person__pk', 'textblob_sentiment')
		tweets = [(key, sum(float(item[1]) for item in subiter))  for key, subiter in itertools.groupby(tweets, itemgetter(0))]
		positive_sentiments = [a[0] for a in tweets if a[1] > 0]
		negative_sentiments = [a[0] for a in tweets if a[1] < 0]
		positive_people = people.filter(pk__in=positive_sentiments)
		negative_people = people.filter(pk__in=negative_sentiments)
		positive_cities = positive_people.exclude(city=None).filter(country='US').values_list('city', flat = True)
		positive_states = list(positive_people.exclude(state=None).filter(country='US').values_list('state', flat = True))
		stats['positive_cities'] = Counter(positive_cities).iteritems()
		stats['positive_cities'] = sorted([(a[0], float(a[1]) / stats['all_of_the_cites'][a[0]]) for a in stats['positive_cities'] if a[0] and stats['all_of_the_cites'][a[0]] > avg_cities], key = lambda x:x[1], reverse = True)[:11]
		negative_cities = negative_people.exclude(city=None).filter(country='US').values_list('city', flat = True)
		negative_states = list(negative_people.exclude(state=None).filter(country='US').values_list('state', flat = True))
		stats['negative_cities'] = Counter(negative_cities).iteritems()
		stats['negative_cities'] = sorted([(a[0], float(a[1]) / stats['all_of_the_cites'][a[0]]) for a in stats['negative_cities'] if a[0] and stats['all_of_the_cites'][a[0]] > avg_cities], key = lambda x:x[1], reverse = True)[:11]
		states = defaultdict(int)
		for state in list(set(positive_states + negative_states)):
			if state and len(state) == 2:
				try:
					states[str(state)] += positive_states.count(state)
					states[str(state)] -= negative_states.count(state)
				except:
					pass
		stats['negative_states'] = [str(k) for k, v in states.iteritems() if v < 0 and v]
		stats['positive_states'] = [str(k) for k, v in states.iteritems() if v > 0 and v]
		del stats['all_of_the_cites']
	A = dict(Counter([a.title() for a in people.values_list('industry', flat = True) if a]))
	stats['industries'] = dict(sorted(A.iteritems(), key=itemgetter(1), reverse=True)[:10])
	total_ = float(sum(stats['industries'].values()))
	if total_ > 0:
		for k, v in stats['industries'].iteritems():
			stats['industries'][k] = int(100 * float(v) / total_)
	stats['industries'] = sorted([(k, v) for k, v in stats['industries'].iteritems()], key=lambda x:x[1], reverse = True)
	sm = {}
	sm['Github'] = people.filter(personal_github__isnull=False).count()
	sm['Crunchbase'] = people.filter(personal_crunchbase__isnull=False).count()
	sm['Facebook'] = people.filter(personal_facebook__isnull=False).count()
	sm['Angellist'] = people.filter(personal_angellist__isnull=False).count()
	sm['Twitter'] = people.filter(personal_twitter__isnull=False).count()
	sm['Linkedin'] = people.filter(personal_linkedin__isnull=False).count()
	stats['social_medias'] = sm
	ages = people.values_list('age', flat=True)
	age_dict = {}
	for i in range(20, 65, 5):
		age_dict[str(i)] = 0
	age_dict['61'] = 0
	for age in [a for a in ages if a]:
		if age <= 20:
			age_dict['20'] += 1
		elif age <= 25:
			age_dict['25'] += 1
		elif age <=30:
			age_dict['30'] += 1
		elif age <=35:
			age_dict['35'] += 1
		elif age <=40:
			age_dict['40'] += 1
		elif age <=45:
			age_dict['45'] += 1
		elif age <=50:
			age_dict['50'] += 1
		elif age <=55:
			age_dict['55'] += 1
		elif age <=60:
			age_dict['60'] += 1
		else:
			age_dict['61'] += 1
	tmp = max(age_dict.iteritems(), key=itemgetter(1))[0]
	age_dict = dict(age_dict)
	stats['ages'] = age_dict
	return stats






												#####################
												##### TWITTER #######
												#####################

@task(queue='send_emails')
def makeDemographicStatsForCompetitor(competitor_id, period = 1):
	competitor_object = Competitor.objects.get(id = competitor_id)
	keywords = competitor_object.keywords.all()
	people_pk = Tweet.objects.filter(Q(keywords__in=keywords)).values_list('person__pk').distinct('person__pk')
	if people_pk.count() == 0:
		return False
	stats = getDemographicStats(people_pk, keywords, period = period)
	stats = {str(k): v for k, v in stats.iteritems() if v}
	s = statsSnapshot(
						stats = json.dumps(stats), 
						competitor_id = competitor_id, 
						period = period,
						type_of_stats = 'demographic_stats',
						generated = datetime.datetime.now(), 
						number_of_connections_used = people_pk.count()
					)
	s.save()
	return s



@task(queue='send_emails')
def makeDemographicStats(user_id, period = 1):
	user = User.objects.get(pk=user_id)
	competitors = Competitor.objects.filter(user__id = user_id)
	keywords = keyWord.objects.filter(Q(user__id=user_id)).exclude(id__in=competitors.values_list('keywords__id', flat = True))
	people_pk = Tweet.objects.filter(Q(keywords__in=keywords)).values_list('person__pk').distinct('person__pk')
	if people_pk.count() == 0:
		return
	stats = getDemographicStats(people_pk, keywords, period = period)
	
	stats = {str(k): v for k, v in stats.iteritems() if v}
	s = statsSnapshot(
						stats = json.dumps(stats), 
						user = user, 
						period = period,
						type_of_stats = 'demographic_stats',
						generated = datetime.datetime.now(), 
						number_of_connections_used = people_pk.count()
					)
	s.save()
	return s

@periodic_task(run_every=crontab(hour='*/12', minute = '0'))
def makeDemographicStatsSnapShots():
	for user in User.objects.all():
		makeDemographicStats.delay(user.id, period = 1)
	for competitor in Competitor.objects.all():
		makeDemographicStatsForCompetitor.delay(competitor.id, period = 1)


#######################
##### GET TWEETS ######
#######################

@periodic_task(run_every=crontab(hour='*/12', minute = '0'))
def getTweetsforAllUsersTMs():
	for user in User.objects.annotate(tms = Count('targetmarket')).filter(tms__gt = 0):
		getTweetsForUsersTM(user.id)

def getTweetsForUsersTM(user_id):
	tms = targetMarket.objects.filter(Q(user_id = user_id) & Q(archived = False))
	for tm in tms:
		for connection in tm.connection_set.all():
			getTweetsByEntity.delay(type_ = 'person', id_ = connection.person.id, user_id = user_id)
			getTweetsByEntity.delay(type_ = 'company', id_ = connection.job.company.id, user_id = user_id)



@task(queue='for_twitter')
def getTweetsByEntity(type_ = 'person', id_ = -1, user_id = -1):
	if id_ == -1 or user_id == -1:
		return False
	if type_ == 'company':
		entity = Company.objects.get(id = id_)
		last_seen = Tweet.objects.filter(company_id = id_).order_by('date').last()
		handle = entity.company_twitter
	elif type_ == 'person':
		entity = Person.objects.get(id = id_)
		last_seen = Tweet.objects.filter(person_id = id_).order_by('date').last()
		handle = entity.personal_twitter
	if not handle:
		return False
	api = getUserTwitterAPI(User.objects.get(id = user_id))
	if not api:
		return False
	if last_seen:
		tweets = tweepy.Cursor(api.user_timeline, screen_name=handle, since_id=last_seen.status_id).items()
	else:
		tweets = tweepy.Cursor(api.user_timeline, screen_name=handle).items()
	i = 0
	for tweet_ in tweets:
		i += 1
		if i > 30:
			return True
		d = {
			'text': tweet_.text,
			'date': tweet_.created_at,
			'textblob_sentiment': TextBlob(tweet_.text).sentiment.polarity,
			'favorite_count': tweet_.favorite_count,
			'retweet_count': tweet_.retweet_count,
			}
		if type_ == 'person':
			d['person'] = entity
		elif type_ == 'company':
			d['company'] = entity
		tw, cr = Tweet.objects.get_or_create(status_id = tweet_.id_str, defaults = d)
		if 'retweeted_status' in tweet_.__dict__:
			tw.retweet = tweet_.retweeted_status.id_str
		if 'in_reply_to_status_id_str' in tweet_.__dict__:
			tw.reply_to = tweet_.in_reply_to_status_id_str
		tw.save()
	return True



@task(queue='for_twitter')
def gatherTweetsFromKeyword2(keyword_id):
	keyword_in_question = keyWord.objects.get(id=keyword_id)
	users_of_keyword = keyword_in_question.user.all()
	if users_of_keyword.count() == 0:
		return False
	last_seen = keyword_in_question.last_seen
	never_seen = last_seen is None
	random_user = random.choice(users_of_keyword)
	api = getUserTwitterAPI(random_user)
	if not api:
		return False
	if last_seen:
		tweets = tweepy.Cursor(api.search, q=keyword_in_question.text, since_id=last_seen.status_id).items()
	else:
		tweets = tweepy.Cursor(api.search, q=keyword_in_question.text).items()
	keywords = keyWord.objects.all()
	for tweet_ in tweets:
		try:
			personal_home_page = scrapers.return_url_end(tweet_.author.entities['url']['urls'][0]['expanded_url'], middle=True)
		except:
			personal_home_page = None
		p, p_c = Person.objects.get_or_create(personal_twitter = tweet_.author.screen_name.lower(), defaults={
			'photo':tweet_.author.profile_image_url_https.replace("_normal",''),
			'twitter_followers': tweet_.author.followers_count,
			'twitter_bio': tweet_.author.description,
			'twitter_verified': tweet_.author.verified,
			'name':tweet_.author.name,
			'personal_home_page': personal_home_page,
			'is_analyzed': False})
		tw, cr = Tweet.objects.get_or_create(status_id = tweet_.id_str, defaults = {
			'text': tweet_.text,
			'person': p,
			'date': tweet_.created_at,
			'textblob_sentiment': TextBlob(tweet_.text).sentiment.polarity,
			'favorite_count': tweet_.favorite_count,
			'retweet_count': tweet_.retweet_count,
			})
		if p_c and (tw.textblob_sentiment < -.2 or tw.textblob_sentiment > .2):
			completePerson.delay(p.id, with_email = False)
		if 'retweeted_status' in tweet_.__dict__:
			tw.retweet = tweet_.retweeted_status.id_str
		if 'in_reply_to_status_id_str' in tweet_.__dict__:
			tw.reply_to = tweet_.in_reply_to_status_id_str
		tw.save()
		[tw.keywords.add(keyword) for keyword in keywords if keyword.text.lower() in tw.text.lower()]
		if tweets.num_tweets == 1:
			tw.save()
			keyword_in_question.last_seen = tw
			keyword_in_question.save()
	if never_seen:
		backlogTwitterSentimentsByKeyword.delay(keyword_id)
	return None


@periodic_task(run_every=crontab(hour='*', minute = '*/18'))
def gatherTweets():
	for keyword in keyWord.objects.filter(Q(reference = 'twitter') & Q(active = True)):
		gatherTweetsFromKeyword2.delay(keyword.id)


#####################################
##### COMMUNICATE WITH TWITTER ######
#####################################

@task(queue='for_twitter')
def tweetAtSomeone(user_id, message, reply_to = None):
	user = User.objects.get(pk=user_id)
	api = getUserTwitterAPI(user)
	if not api:
		return False
	return api.update_status(status = message, in_reply_to_status_id = reply_to)



#####################################
###### SENTIMENT WITH TWITTER #######
#####################################



@task(queue='send_emails')
def computeTwitterSentimentsForKeyword(keyword_id, hours_ago = 1, now_meow = None):
	if not now_meow:
		now_meow = datetime.datetime.now()
	else:
		now_meow = datetime.datetime.strptime(now_meow, "%m/%d/%Y %H:%M")
	word = keyWord.objects.get(id=keyword_id)
	tweets_in_question = word.tweet_set.all().filter(Q(date__gte=now_meow - datetime.timedelta(hours=hours_ago)) & Q(date__lte=now_meow))
	if tweets_in_question.count() > 0:
		t = twitterSentiment(sentiment = float(average(tweets_in_question.values_list('textblob_sentiment', flat = True))), keyWord=word, hours_looked_back=hours_ago, time_taken = now_meow)
	else:
		return
	t.save()
	t.tweets = tweets_in_question
	t.save()
	people = tweets_in_question.values_list('person__id', flat = True).distinct('person__id')
	for person in people:
		specific_tweets = tweets_in_question.filter(person__id=person)
		if specific_tweets.count():
			if tweets_in_question.count():
				t = twitterSentiment(sentiment = float(average(specific_tweets.values_list('textblob_sentiment', flat = True))), keyWord=word, hours_looked_back=hours_ago, person_id = person, time_taken = now_meow)
			else:
				t = twitterSentiment(sentiment = 0, keyWord=word, hours_looked_back=hours_ago, person_id = person, time_taken = now_meow)
			t.save()
			t.tweets = specific_tweets
			t.save()


@periodic_task(run_every=crontab(hour='*', minute='0'))
def computeTwitterSentiments(hours_ago = 1):
	keywords = keyWord.objects.filter(reference='twitter')
	for word in keywords:
		computeTwitterSentimentsForKeyword.delay(word.id, hours_ago = hours_ago)

def date_range(b, e, by = 'hour'):
	if by == 'hour':
		while b <= e:
			b += datetime.timedelta(hours=1)
			yield b



@task(queue='send_emails')
def backlogTwitterSentimentsByKeyword(word_id, notify_users = False):
	word = keyWord.objects.get(pk=word_id)
	tweets = word.tweet_set.all().order_by('date')
	first_datetime = tweets.first().date
	first_datetime_truncated = datetime.datetime(first_datetime.year, first_datetime.month, first_datetime.day, first_datetime.hour)
	last_datetime = tweets.last().date
	last_datetime_truncated = datetime.datetime(last_datetime.year, last_datetime.month, last_datetime.day, last_datetime.hour)
	for da in date_range(first_datetime_truncated, last_datetime_truncated):
		computeTwitterSentimentsForKeyword(word.id, hours_ago = 1, now_meow = datetime.datetime.strftime(da, "%m/%d/%Y %H:%M"))
	for competitor in Competitor.objects.filter(keywords = word):
		getSentimentStatsForCompetitor(competitor.id)
		makeDemographicStatsForCompetitor(competitor.id, period = 1)
	return


#####################################
######## STATS WITH TWITTER #########
#####################################


@task(queue='send_emails')
def getTwitterStats(user_id):
	user = User.objects.get(pk=user_id)
	api = getUserTwitterAPI(user)
	if not api:
		return False
	me = api.me()
	num_followers = me.followers_count
	num_following = me.friends_count
	t = twitterStats(num_followers=num_followers, num_following=num_following, user=user, time_taken=datetime.datetime.now())
	try:
		last_stats = twitterStats.objects.filter(user=user).last()
	except:
		last_stats = None
	if not last_stats:
		t.save()
		return True
	if last_stats.num_following != num_following or last_stats.num_followers != num_followers:
		t.save()
	return True

@task(queue='send_emails')
def getTwitterStatsForCompany(user_id, company_id):
	user = User.objects.get(pk=user_id)
	company = Company.objects.get(pk=company_id)
	api = getUserTwitterAPI(user)
	if not api:
		return False
	try:
		them = api.get_user(company.company_twitter)
	except:
		t = twitterStats(num_followers=0, num_following=0, company=company, time_taken=datetime.datetime.now())
		t.save()
		return
	num_followers = them.followers_count
	num_following = them.friends_count
	t = twitterStats(num_followers=num_followers, num_following=num_following, company=company, time_taken=datetime.datetime.now())
	try:
		last_stats = twitterStats.objects.filter(company=company).last()
	except:
		last_stats = None
	if not last_stats:
		t.save()
	elif last_stats and last_stats.num_following != num_following or last_stats.num_followers != num_followers:
		t.save()
	return True

@periodic_task(run_every=crontab(hour='*', minute='0'))
def makeAllTwitterStats():
	for user in User.objects.exclude(twitter_access_token_key=None):
		try:
			getTwitterStats.delay(user.id)
		except:
			pass
		try:
			getSentimentStatsForUser.delay(user.id)
		except:
			pass
		for compet in user.competitors.all():
			try:
				getTwitterStatsForCompany.delay(user.id, compet.id)
			except Exception as e:
				pass
	for competitor in Competitor.objects.all():
		getSentimentStatsForCompetitor.delay(competitor.id)

@periodic_task(run_every=crontab(minute='*/5'))
def getAllFollowers():
	users_with_twitter = User.objects.exclude(twitter_access_token_key=None)
	for user in users_with_twitter:
		analyzeFollowers.delay(user.id)

@task(queue='for_twitter')
def analyzeFollowers(user_id):
	user = User.objects.get(pk=user_id)
	api = getUserTwitterAPI(user)
	followers = tweepy.Cursor(api.followers).items()
	most_recent_follower = followers.next() # the most recent follower
	stop_id = user.most_recent_follower_id # last person i saw from this user
	most_recent_id = most_recent_follower.id # most recent person right meow
	if str(most_recent_id) == str(stop_id): # if they are the same, no need to continue
		return
	user.most_recent_follower_id = most_recent_id
	user.save()
	convertTwitterToConnection2.delay(most_recent_follower.screen_name, user_id)
	while True:
		try:
			follower = followers.next()
			if str(follower.id) == str(stop_id): # DONE
				return
			convertTwitterToConnection2.delay(follower.screen_name, user_id)
			i += 1
		except tweepy.TweepError:
			time.sleep(60 * 1)
		except StopIteration:
			break

def getUserTwitterAPI(user):
	try:
		# ADDDD change these twitter creds
		auth = tweepy.OAuthHandler('Ftp4IDSOcPJaCdTlxblRMPW05', '6AIiTKoVC3hChn81o1pRgOlokS0sN8NsQS39TZvLyig8QE1G4k')
		if not user.twitter_access_token_key:
			return None
		auth.set_access_token(user.twitter_access_token_key, user.twitter_access_token_secret)
		api = tweepy.API(auth, wait_on_rate_limit = True, wait_on_rate_limit_notify = True)
		return api
	except:
		return None

@task(queue='default')
def convertTwitterToConnection2(handle, user_id):
	handle = handle.lower().strip()
	try:
		p = Person.objects.get(Q(personal_twitter__iexact = handle)) # person already in db
		c, d = Connection.objects.get_or_create(user_id = user_id, person = p)
		c.followed_by = True
		c.followed_on = datetime.datetime.now()
		c.last_date   = datetime.datetime.now()
		c.save()
		if not p.is_analyzed:
			completePerson.delay(p.id, with_email = True)
		return c, d
	except Exception as e:
		pass # person not in database
	try:
		l = Legion.legion({'web_presence':{'personal_twitter':{'url':handle}}}, scrapers = {}, type_of_entity = 'person')
		final_form = master.getEmail(l, complete = True, use_the_hounds = True).information
	except Exception as e:
		final_form = {'web_presence':{'personal_twitter':{'url': handle}}}
	person_in_db, created = makePerson(final_form, override = True)
	c, d = Connection.objects.get_or_create(user_id = user_id, person = person_in_db)
	c.followed_by = True
	c.followed_on = datetime.datetime.now()
	c.last_date   = datetime.datetime.now()
	c.save()
	return c, d



@task(queue="default")
def makeConnection2(email, user_id):
	try:
		email = email.lower().strip().decode('utf-8')
	except:
		return None
	try: # if the email is already in the db
		e = EmailAddress.objects.get(address=email)
		c = Connection.objects.get_or_create(user_id = user_id, person = e.person)[0]
		if not c.from_site:
			c.from_site = True
			c.save()
		return c
	except:
		pass
	try:
		legion_standard_form = master.completeEmail(email, use_the_hounds = True).information
	except Exception as e:
		print e
		legion_standard_form = {'emails':[{'address':email, 'is_deliverable':'Unknown'}]}
	person, created = makePerson(legion_standard_form, override = True)
	c = Connection.objects.get_or_create(user_id = user_id, person = person)[0]
	if not c.from_site:
		c.from_site = True
		c.save()
	return c


SIMPLE_EMAIL_REGEX = re.compile('(([a-zA-Z0-9][\w\.-]+)@([a-z-_A-Z0-9\.]+)\.(net|com|co|edu|gov|org))', re.IGNORECASE)

def g(x):
	try:
		return x.lower().strip().decode('utf-8')
	except:
		return None

def getDocumentStats(d_id):
	d = Document.objects.get(id=d_id)
	emails = list(set([g(m[0]) for m in re.findall(SIMPLE_EMAIL_REGEX, d.docfile.read())]))
	return {'num_emails': len(emails),'first_few': emails[:10], 'name': d.__unicode__()}

@task(queue="default")
def submitDocument(d_id, u_id):
	d = Document.objects.get(id=d_id)
	emails = list(set([g(m[0]) for m in re.findall(SIMPLE_EMAIL_REGEX, d.docfile.read())]))
	d.emails_on_csv = len(emails) # emails_on_csv is the total number
	c = Connection.objects.filter(Q(user__pk=u_id) & Q(person__emailaddress__address__in=emails)).values_list('person__emailaddress__address', flat = True)
	emails = list(set(emails) - set(c))
	d.emails_new_to_user = len(emails)
	d.save()
	for email in emails:
		makeConnection2.delay(email = email, user_id = u_id, document_id = d_id)

def _stripOutFillers(stringIn):
	stringIn = stringIn.lower()
	for word in ['manager', 'head', 'director', 'vp ', 'vice president', 'of']:
		stringIn = stringIn.replace(word, '')
	return "".join(l for l in stringIn if l not in string.punctuation).strip().replace('  ',' ')

def filterLeads(query, u_id = None, limit = -1):
	personal_stuff = 0
	company_stuff = 0
	if limit == 0:
		return []
	if u_id:
		try:
			leads = Connection.objects.filter(Q(user__organization__id=User.objects.get(id=u_id).organization.id) & Q(lead = True)).values_list('person__pk', flat = True).distinct('person__pk')
		except Exception as filterleadserror:
			leads = Connection.objects.filter(Q(user=User.objects.get(id=u_id)) & Q(lead = True)).values_list('person__pk', flat = True).distinct('person__pk')
		q = ~Q(person__pk__in=leads)
	else:
		q = Q()
	# web presences
	presences =['personal_twitter', 'personal_google_plus', 'personal_angellist', 'personal_github', 'personal_facebook', 'personal_linkedin', 'personal_crunchbase']
	try:
		personal_stuff += len([presence for presence in presences if presence in query])
		q &= reduce(and_, [~Q(**{'person__'+presence:None}) for presence in presences if presence in query])
	except Exception as e:
		pass
	# job title

	if len(query.get('industries', '')):
		company_stuff += 1
		industries = [i.lower().strip() for i in query['industries'].split(',')]
		q &= reduce(or_, [Q(company__industries__name__icontains=i) for i in industries])

	if len(query.get('job_title', '')):
		company_stuff += 1
		titles = [s.strip().lower() for s in query['job_title'].split(',')]
		new_titles = []
		other_jobs = {'coo': ['chief operating officer'], 'cfo':['chief financial officer'], 'ceo': ['chief executive officer'], 'cmo': ['chief marketing officer'], 'cto': ['chief technical officer', 'chief technology officer']}
		for title in titles:
			if title.lower() in other_jobs:
				new_titles.extend(other_jobs[title])
		titles.extend(new_titles)
		job_query = reduce(or_, [Q(title__iregex = r'([^\w]|\A)'+title+'([^\w]|\Z)') for title in titles if len(title) > 2])
		q &= job_query

	q &= Q(is_active = query.get('is_active', True))
	if query.get('job_months', False):
		q &= Q(months__gte=int(query['job_months']))
	if query.get('company_website', False):
		company_stuff += 1
		q &= ~Q(company__company_home_page=None)


	if 'revenue_min' in query or 'revenue_max' in query or 'funding_max' in query or 'funding_min' in query:
		if 'revenue_min' in query or 'revenue_max' in query:
			company_stuff += 1
			revenue_query = (Q(company__revenue__gte=int(query.get('revenue_min', 0))) & Q(company__revenue__lte=int(query.get('revenue_max', 99999999999))))
		else:
			revenue_query = Q()
		if 'funding_min' in query or 'funding_max' in query:
			company_stuff += 1
			funding_query = (Q(company__funding__gte=int(query.get('funding_min', 0))) & Q(company__funding__lte=int(query.get('funding_max', 99999999999)))) 
		else:
			funding_query = Q()
		q &= (funding_query | revenue_query)


	if query.get('company_name',False):
		company_stuff += 1
		q &= Q(company__name__iexact = True)

	# name
	if query.get('name', False):
		personal_stuff += 1
		q &= Q(person__name__icontains=query['name'])
	# klout
	if query.get('klout', False):
		personal_stuff += 1
		q &= Q(person__klout_score__gte=query['klout'])
	# age
	if 'age_min' in  query or 'age_max' in query:
		personal_stuff += 1
		q &= ~Q(person__age=None)
		if 'age_min' in query:
			q &= Q(person__age__gte=int(query['age_min']))
		if'age_max' in query:
			q &= Q(person__age__lte=int(query['age_max']))


	# location
	if len(query.get('location', '')):
		personal_stuff += 1
		locations = [s.strip() for s in query['location'].split('|')]
		l = [Q(person__location__icontains = location) for location in locations]
		location_q = reduce(or_, l)
		refined = map(scrapers.locationToJson, locations)
		for r in refined:
			city = r['city']
			state = r['state']
			if city or state:
				if state and city:
					locat_q = Q(person__state__exact = state) & Q(person__city__exact = city)
				elif state:
					locat_q = Q(person__state__exact = state)
				elif city:
					locat_q = Q(person__city__exact = city)
				location_q |= locat_q
		q &= location_q
			
	


	# followers
	# q &= Q(person__twitter_followers__gte=query.get('twitter_followers_min', -1))
	# q &= Q(person__twitter_followers__lte=query.get('twitter_followers_max', 100000000))
	# verified
	# if query.get('verified', False):
	# 	q &= Q(person__twitter_verified = True)

	
	jobs = Job.objects.filter(q).distinct('person__id')
	if query.get('email', False):
		personal_stuff += 1
		jobs = jobs.filter(~Q(person__emailaddress__address=None) & ~Q(person__emailaddress__is_deliverable='Invalid'))
	jobs_list = jobs.values_list('pk', flat=True)
	jobs = Job.objects.filter(pk__in=jobs_list).order_by('?')
	print jobs.count(), "jobs", personal_stuff, company_stuff
	if limit > -1:
		jobs = jobs[:limit]
	return jobs


def filterLeads2(query, u_id = None, limit = -1, star_limit = 5, icp_dict = None):
	personal_stuff = 0
	company_stuff = 0
	jobs_list = []
	user = User.objects.get(id=u_id)
	# changable_jobs = []
	overall_q = Q(is_active = query.get('is_active', True))
	if limit == 0:
		return []
	try:
		leads = Connection.objects.filter(Q(user__organization__id=user.organization.id) & Q(lead = True)).values_list('person__pk', flat = True).distinct('person__pk')
	except Exception as filterleadserror:
		leads = Connection.objects.filter(Q(user=user) & Q(lead = True)).values_list('person__pk', flat = True).distinct('person__pk')
	overall_q &= ~Q(person__pk__in=leads)
	
	# location
	if len(query.get('location', '')):
		locations = [s.strip() for s in query['location'].split('|')]
		l = [Q(person__location__icontains = location) for location in locations]
		location_q = reduce(or_, l)
		refined = map(scrapers.locationToJson, locations)
		for r in refined:
			city = r['city']
			state = r['state']
			if city or state:
				if state and city:
					locat_q = Q(person__state__exact = state) & Q(person__city__exact = city)
				elif state:
					locat_q = Q(person__state__exact = state)
				elif city:
					locat_q = Q(person__city__exact = city)
				location_q |= locat_q
		# jobs_list += list(Job.objects.filter(overall_q & location_q).distinct('person__id').values_list('id', flat = True))
		overall_q &= location_q

	if len(query.get('industries', '')):
		industries = [i.lower().strip() for i in query['industries'].split(',')]
		overall_q &= reduce(or_, [Q(company__industries__name__icontains=i) for i in industries])
		# jobs_list += list(Job.objects.filter(q).distinct('person__id').values_list('id', flat = True))

	# web presences
	presences =['personal_twitter', 'personal_google_plus', 'personal_angellist', 'personal_github', 'personal_facebook', 'personal_linkedin', 'personal_crunchbase']
	try:
		personal_stuff += len([presence for presence in presences if presence in query])
		q = overall_q & reduce(and_, [~Q(**{'person__'+presence:None}) for presence in presences if presence in query])
		jobs_list += list(Job.objects.filter(q).distinct('person__id').values_list('id', flat = True))
	except Exception as e:
		pass
	# job title

	

	if len(query.get('job_title', '')):
		company_stuff += 1
		titles = [s.strip().lower() for s in query['job_title'].split(',')]
		new_titles = []
		other_jobs = {'coo': ['chief operating officer'], 'cfo':['chief financial officer'], 'ceo': ['chief executive officer'], 'cmo': ['chief marketing officer'], 'cto': ['chief technical officer', 'chief technology officer']}
		for title in titles:
			if title.lower() in other_jobs:
				new_titles.extend(other_jobs[title])
		titles.extend(new_titles)
		job_query = overall_q & reduce(or_, [Q(title__iregex = r'([^\w]|\A)'+title+'([^\w]|\Z)') for title in titles if len(title) > 2])
		# changable_jobs += list(Job.objects.filter(job_query).values_list('id', flat = True).distinct('person__id'))
		jobs_list += list(Job.objects.filter(job_query).values_list('id', flat = True))*2  # ADDD figure out if this is the best idea for weight, hint: it's not
		
	if query.get('job_months', False):
		q &= Q(months__gte=int(query['job_months']))
	if query.get('company_website', False):
		company_stuff += 1
		q = overall_q & ~Q(company__company_home_page=None)
		jobs_list += list(Job.objects.filter(q).distinct('person__id').values_list('id', flat = True))


	if 'revenue_min' in query or 'revenue_max' in query or 'funding_max' in query or 'funding_min' in query:
		if 'revenue_min' in query or 'revenue_max' in query:
			company_stuff += 1
			revenue_query = (Q(company__revenue__gte=int(query.get('revenue_min', 0))) & Q(company__revenue__lte=int(query.get('revenue_max', 99999999999))))
		else:
			revenue_query = Q()
		if 'funding_min' in query or 'funding_max' in query:
			company_stuff += 1
			funding_query = (Q(company__funding__gte=int(query.get('funding_min', 0))) & Q(company__funding__lte=int(query.get('funding_max', 99999999999)))) 
		else:
			funding_query = Q() 
		jobs_list += list(Job.objects.filter(overall_q & (funding_query | revenue_query)).distinct('person__id').values_list('id', flat = True))


	if query.get('company_name',False):
		company_stuff += 1
		q = overall_q & Q(company__name__iexact = True)
		jobs_list += list(Job.objects.filter(q).distinct('person__id').values_list('id', flat = True))

	# name
	if query.get('name', False):
		personal_stuff += 1
		q = overall_q & Q(person__name__icontains=query['name'])
		jobs_list += list(Job.objects.filter(q).distinct('person__id').values_list('id', flat = True))
	# klout
	if query.get('klout', False):
		personal_stuff += 1
		q = overall_q & Q(person__klout_score__gte=query['klout'])
		jobs_list += list(Job.objects.filter(q).distinct('person__id').values_list('id', flat = True))
	# age
	if 'age_min' in  query or 'age_max' in query:
		personal_stuff += 1
		q = overall_q & ~Q(person__age=None)
		if 'age_min' in query:
			q &= Q(person__age__gte=int(query['age_min']))
		if'age_max' in query:
			q &= Q(person__age__lte=int(query['age_max']))
		jobs_list += list(Job.objects.filter(q).distinct('person__id').values_list('id', flat = True))


	

	if query.get('email', False):
		personal_stuff += 1
		email_q = overall_q & ~Q(person__emailaddress__address=None) & ~Q(person__emailaddress__is_deliverable='Invalid')
		jobs_list += list(Job.objects.filter(email_q).distinct('person__id').values_list('id', flat = True))
	

	counter = Counter(jobs_list)
	counter = {n: min(5, round(5 * (counter[n]/ float(personal_stuff + company_stuff)), 2) ) for n in counter.keys()}


	refined_counter = sorted(counter.iteritems(), key = lambda x:x[1], reverse = True)
	print len(refined_counter), "jobs"
	refined_counter = [r for r in refined_counter if r[1] > star_limit / 2.]


	# needs_attention = set([c[0] for c in counter.iteritems() if c[1] < star_limit]) & set(changable_jobs)
	# print len(needs_attention), "needs_attention", list(needs_attention)[:20]

	print len(refined_counter), "jobs"


	to_return = []
	if user.person:
		user_dict = getPersonDict(user.person)
	else:
		user_dict = None

	for job_id, tm_close in refined_counter:
		person = Job.objects.get(id=job_id).person
		person_dict = {'person_id':person.id, 'job_id':job_id}
		closeness = {'tm_close':tm_close}
		if icp_dict:
			try:
				closeness['icp_close'] = (personCloseToICP(person.id, icp_dict))
			except Exception as icp_e:
				print icp_e, "icp_e"
				pass
		if user_dict:
			try:
				closeness_to_user = personDictSimilarity(user_dict, getPersonDict(person))
				closeness['user_close'] = closeness_to_user['star_rating']
			except Exception as person_closeness_e:
				print person_closeness_e, "person_closeness_e"
				pass
		if len(closeness.keys()) == 1:
			star_rating = closeness['tm_close']
		else:
			other_factors = len(closeness.keys()) - 1
			star_rating = 0
			for key, value in closeness.iteritems():
				if key == 'tm_close':
					star_rating += .7 * closeness[key]
				else:
					star_rating += .3 / other_factors * closeness[key]
		print person_dict, star_rating, closeness
		if star_rating >= star_limit:
			person_dict['star_rating'] = star_rating
			try:
				person_dict.update(closeness)
				person_dict['person_closeness'] = closeness_to_user
			except:
				pass
			to_return.append(person_dict)
			if len(to_return) >= limit:
				return to_return
	return to_return


def _cleanSchool(st):
    st = st.strip().lower()
    for repl in ['university', 'the', 'college', 'school', 'academy']:
        st = st.replace(repl,'')
    st = st.strip()
    return st

def personDictSimilarity(p1_dict, p2_dict):
    similarity = {}
    for key in set(p1_dict.keys()) & set(p2_dict.keys()):
        if not (p1_dict[key] and p2_dict[key]):
            continue
        if key == 'interests':
            same_interests = set([a.lower() for a in p1_dict[key]]) & set([a.lower() for a in p2_dict[key]])
            if len(same_interests):
            	# similarity['interests'] = ', '.join(same_interests)
            	similarity['num_interests'] = len(same_interests)
        if key == 'education':
            same_schools = set([_cleanSchool(a['school_name']) for a in p1_dict[key]]) & set([_cleanSchool(a['school_name']) for a in p2_dict[key]])
            if len(same_schools):
            	# similarity['schools'] = ', '.join(same_schools)
            	similarity['num_schools'] = len(same_schools)
        if key == 'positions':
            same_titles = set([a['position_title'] for a in p1_dict[key]]) & set([a['position_title'] for a in p2_dict[key]])
            if len(same_titles):
            	# similarity['titles'] = ', '.join(same_titles)
            	similarity['num_titles'] = len(same_titles)
            same_companies = set([a['company_dict']['name'] for a in p1_dict[key]]) & set([a['company_dict']['name'] for a in p2_dict[key]])
            if len(same_companies):
            	# similarity['companies'] = ', '.join(same_companies)
            	similarity['num_companies'] = len(same_companies)
        if key == 'location':
            for i in ['city', 'state']:
                if (i in p1_dict[key] and i in p2_dict[key]) and fuzz.ratio(p1_dict[key].get(i, '').lower(), p2_dict[key].get(i, '').lower()):
                    similarity['num_locations'] = 1
                    # similarity[i] = p1_dict[key][i]
    similarity['star_rating'] = round(5 * float(len(similarity.keys())) / len(set(p1_dict.keys()) & set(p2_dict.keys())), 2)
    return similarity

@task(queue="send_emails")
def findUsersForTargetMarket(target_id, limit):
	t = targetMarket.objects.get(id=target_id)
	query = json.loads(t.query)
	user = t.user
	try:
		icp_dict = json.loads(t.icp_set.first().icp_dict)
	except:
		icp_dict = None
	jobs = filterLeads2(query, user.id, limit = limit, star_limit = float(t.star_limit), icp_dict = icp_dict)
	for job in jobs: 
		connection, connection_created = Connection.objects.get_or_create(user = user, person_id = job['person_id'])
		connection.target_market.add(t)
		connection.job_id = job['job_id']
		connection.new_lead = True
		connection.lead = True
		connection.lead_on   = datetime.datetime.now()
		connection.last_date = datetime.datetime.now()
		for key in job.get('person_closeness', {}).keys():
			try:
				connection.__dict__[key] = job['person_closeness'][key]
			except:
				pass
		connection.star_rating = job['star_rating']
		for rating in ['tm_close', 'user_close', 'icp_close']:
			try:
				connection.__dict__[rating] = job[rating]
			except Exception as ee:
				pass
		connection.save()

@task(queue="send_emails")
def findUsersForTargetMarkets(user_id):
	user = User.objects.get(id=user_id)
	target_markets = targetMarket.objects.filter(Q(user = user) & Q(archived = False))
	if target_markets.count() == 0:
		return False
	leads_for_each_market = int(user.daily_leads / float(target_markets.count()))
	for t in target_markets:
		findUsersForTargetMarket(t.id, leads_for_each_market)

@task(queue='default')
def bringInCompanyLinkedin(company_dict):
	if not getCompany(company_dict):
		completed_company = master.completeEntity(Legion.legion(company_dict, type_of_entity = 'company', scrapers = {}), use_the_hounds = True)
		company, created = makeCompany(completed_company.information, override = True)
		id_ = completed_company.scrapers['company_linkedin'].getCompanyId()
		if id_ and len(id_):
			company.company_linkedin = 'company/' + id_
			company.save()
		return True
	else:
		pass
	return False

@task(queue='default')
def _bringinTwitterPerson(twitter_person):
	person, person_created = makePerson(twitter_person, override = True, complete_companies = True)
	if person_created:
		completePerson.delay(person.id, with_email = True)

@periodic_task(run_every=crontab(hour='*/2', minute='0'))
def scanForLeads():
	for scraper in Scraper.objects.exclude(current_index = -1).order_by('?'):
		scraper_dict = {k:v for k, v in scraper.__dict__.items() if v is not None}
		if scraper.website == 'google_linkedin':
			results = growth_scrapers.scanGoogleForLinkedin(scraper_dict)
			scraper.current_index = scraper.current_index + 10
			scraper.save()
			if len(results) == 0:
				scraper.current_index = -1
				scraper.save()
			for result in results:
				insertPersonLinkedinProfile.delay(result)
			scraper.last_run = datetime.datetime.now()
			scraper.save()
		elif scraper.website == 'twitter_scan':
			api = getUserTwitterAPI(scraper.targetmarket.user)
			if not api:
				continue
			scraper.last_run = datetime.datetime.now()
			scraper.save()
			for result in growth_scrapers.scanTwitter(scraper_dict, api = api):
				print result
				_bringinTwitterPerson.delay(result)
		elif scraper.website == 'google_company_linkedin':
			results = growth_scrapers.scanGoogleForCompanyLinkedin(scraper_dict)
			scraper.current_index = scraper.current_index + 10
			scraper.save()
			if len(results) == 0:
				scraper.current_index = -1
				scraper.save()
			for result in results:
				bringInCompanyLinkedin.delay(result)
			scraper.last_run = datetime.datetime.now()
			scraper.save()

@periodic_task(run_every=crontab(hour='8', minute='0'))
def addLeads():
	for user in User.objects.annotate(num_tm=Count('targetmarket')).filter(num_tm__gt=0):
		findUsersForTargetMarkets.delay(user.id)


@task(queue="default")
def completePerson(p_id, with_email = False):
	person = Person.objects.get(id=p_id)
	p_dict = Legion.legion(getPersonDict(person), scrapers = {})
	if with_email:
		completed_person = master.getEmail(p_dict, complete = True, use_the_hounds = True).information
	else:
		completed_person = master.completeEntity(p_dict).information
	if completed_person != p_dict:
		person, person_made = makePerson(completed_person, override = True)
		person.is_analyzed = True
		person.last_analyzed = datetime.datetime.now()
		person.save()
		return True
	person.is_analyzed = True
	person.last_analyzed = datetime.datetime.now()
	person.save()
	return False

@task(queue="default")
def fixPersonLocation(person_id):
	person = Person.objects.get(id=person_id)
	locationjson = scrapers.locationToJson(person.location)
	person.country = locationjson['country']
	person.city = locationjson['city']
	person.state = locationjson['state']
	person.save()

@task(queue="default")
def completeCompany(p_id, with_hounds = False):
	company = Company.objects.get(id=p_id)
	c = getCompanyDict(company)
	completed_person = master.completeEntity(Legion.legion(c, scrapers = {}, type_of_entity = 'company'), use_the_hounds = with_hounds)
	a, b = makeCompany(completed_person.information, override = True)
	if a.id != p_id:
		Job.objects.filter(company=company).update(company=a)
	try:
		c_id = completed_person.scrapers['company_linkedin'].getCompanyId()
		if c_id:
			a.company_linkedin = 'company/'+c_id
	except:
		pass
	scanCompanyForTech(company.id)
	a.last_analyzed = datetime.datetime.now()
	a.save()
	return a.id

@task(queue='default')
def importConspireProfile(conspire_id):
	c = scrapers.conspireScraper(conspire_id)
	per = c.getPerson()
	if per['web_presence'] != {}:
		person = getPerson(per)
		if person:
			db_person = getPersonDict(person)
			if db_person['web_presence'] == per['web_presence']: # same social medias, no need to do anything
				return None
			for key, value in db_person.iteritems():
				if key != 'web_presence':
					per[key] = db_person[key]
				else:
					per['web_presence'].update(db_person['web_presence'])
		if 'emails' not in per:
			per = master.getEmail(Legion.legion(per, scrapers = {}), complete = True).information
		makePerson(per, override = True)
	else:
		print "I can't import", per
	return

@task(queue='default')
def insertPersonLinkedinProfile(linkedin_url, want = ['company']):
	p = Person.objects.filter(personal_linkedin=linkedin_url.lower())
	if len(p):
		return False
	l = Legion.legion({'web_presence':{'personal_linkedin':{'url':linkedin_url}}}, scrapers = {}, type_of_entity = 'person')
	final_form = master.getEmail(l, complete = True, use_the_hounds = True, want = want).information
	person, person_created = makePerson(final_form, override = True, complete_companies = True)
	if person.name == '':
		person.is_analyzed = False
		person.save()
	return True

@task(queue='default')
def insertPersonLinkedinProfileWithoutEmail(linkedin_url):
	p = Person.objects.filter(personal_linkedin=linkedin_url)
	if len(p):
		return False
	l = Legion.legion({'web_presence':{'personal_linkedin':{'url':linkedin_url}}}, scrapers = {}, type_of_entity = 'person')
	final_form = master.completeEntity(l, use_the_hounds = False).information
	makePerson(final_form, override = True)
	return True


@task(queue='default')
def findEmployeesOfCompany(company_id, keywords = None, pages = 1, auth = False):
	try:
		company = Company.objects.get(id=company_id)
	except:
		return False
	if auth:
		cookie_url = 'https://s3-us-west-2.amazonaws.com/tier5/linkedin_cookies/jamasen'
		f = urllib.urlopen(cookie_url)
		cookies = requests.utils.cookiejar_from_dict(pickle.load(f))
		cl = company.company_linkedin
		cl = cl.replace('company/','')
		r = requests.get("https://www.linkedin.com/vsearch/p?f_CC="+cl, cookies = cookies)
		soup = BeautifulSoup(r.text)
		pages =  r.text.count('/vsearch/p?f_CC='+cl+'&page_num=')
		people = list(set( re.findall('profile/view\?id=\d+&authType=[a-zA-Z\_]+&authToken=[a-zA-Z0-9]+&locale=en_US', r.text)))
		for page in range(2,pages):
			r = requests.get("https://www.linkedin.com/vsearch/p?f_CC="+cl+'&page_num='+str(page), cookies = cookies)
			soup = BeautifulSoup(r.text)
			people += list(set( re.findall('profile/view\?id=\d+&authType=[a-zA-Z\_]+&authToken=[a-zA-Z0-9]+&locale=en_US', r.text)))
		for person in people:
			insertPersonLinkedinProfile.delay(person)
	else:
		query = '"' + company.name + '"'
		if keywords:
			query += ' '+keywords
		g = scrapers.googleScraper()
		for page in range(pages):
			query += ' site:www.linkedin.com/in OR site:www.linkedin.com/pub -site:www.linkedin.com/pub/dir'
			results = g.search(query, current_index = page * 10)
			for r in results['results']:
				if 'linkedin.com' not in r['link'].lower():
					continue
				personal_linkedin = r['link'].split('linkedin.com/')[1].lower()
				for char in ['?', '%', '&']:
					personal_linkedin = personal_linkedin.split(char)[0]
				insertPersonLinkedinProfile.delay(personal_linkedin)
	return True

def fixEmail(email_id):
	e = EmailAddress.objects.get(id=email_id)
	domain = e.address.split('@')[1]
	try:
		company = Company.objects.get(Q(company_home_page__iexact=domain) | Q(email_host__iexact='@'+domain))
		e.company = company
	except Exception as ee:
		pass
	try:
		e.email_pattern = getPatternOfEmail(e.person.name, e.address.split('@')[0])
	except:
		pass
	e.save()



def mergeCompanies(old_, new_):
	if old_ == new_:
		return None
	o = Company.objects.get(id=old_)
	n = Company.objects.get(id=new_)
	Job.objects.filter(company = o).update(company=n)
	EmailAddress.objects.filter(company=o).update(company=n)
	for item in ['revenue', 'funding', 'location', 'country', 'city', 'number_of_employees', 'company_linkedin', 'company_twitter', 'company_home_page']:
		if o.__dict__[item] and not n.__dict__[item]:
			n.__dict__[item] = o.__dict__[item]
	n.save()
	o.delete()

def getPatternOfEmail(name, handle):
	name = name.lower()
	handle = handle.lower()
	fname, lname = name.split(' ')[0], name.split(' ')[-1]
	finitial, linitial = fname[0], lname[0]
	patterns = {'fname':fname, 
				'finitiallname':finitial+lname, 
				'fname.lname':fname+'.'+lname, 
				'fname.linitial':fname+'.'+linitial,
				'lname':lname,
				'fnamelname':fname+lname,
				'fnamelinitial':fname+linitial,
				'fname-lname':fname+'-'+lname
				}
	for pattern, potent in patterns.items():
		if handle == potent:
			return pattern
	return None

@task(queue='default')
def getEmailofPersonID(person_id, want = ['company', 'personal']):
	person_dict = getPersonDict(Person.objects.get(id=person_id))
	l = Legion.legion(person_dict, scrapers = {})
	ema = master.getEmail(l, want = want)
	emails = ema.information.get('emails', [])
	for email_ in emails:
		email, created = EmailAddress.objects.get_or_create(address = email_['address'], defaults = {'person_id':person_id, 'is_deliverable':email_.get('is_deliverable'), 'type_of_email':email_.get('type_of_email', ''), 'is_current':True})
		email.person = Person.objects.get(id=person_id)
		email.email_pattern = getPatternOfEmail(person_dict.get('name', ''), email_['address'].split('@')[0])
		email.save()
		domain = email_['address'].split('@')[1]
		try:
			if email_.get('type_of_email', '') == 'company':
				company = Company.objects.get(Q(company_home_page__iexact=domain) | Q(email_host__iexact='@'+domain))
				email.company = company
				company.email_host = '@'+domain
				email.save()
				company.save()
		except Exception as w:
			pass




########################################
###### SCANNING FOR TECHNOLOGIES #######
########################################



@task(queue='default')
def scanCompanyForTech(company_id):
	try:
		company_ = Company.objects.get(Q(id=company_id) & ~Q(company_home_page=''))
		company_web_page = 'http://'+company_.company_home_page
	except:
		return False
	all_links = [company_web_page]
	seen = [company_web_page]
	checked = 0
	while len(all_links):
		link = all_links.pop(0)
		checked +=1 
		if checked >= 5:
			return False
		try:
			r = requests.get(link, timeout = 10)
		except:
			continue
		soup = BeautifulSoup(r.text)
		scripts_text = [a.get('src', '')+' '+a.text for a in soup.findAll('script')]
		scripts_src = [{'company':company_, 'src':a.get('src'), 'text':a.text} for a in soup.findAll('script')]
		for sc in scripts_src:
			script.objects.get_or_create(**sc)
		for tech in Technology.objects.all():
			if sum([s.lower().count(tech.script_alias.lower()) for s in scripts_text]) > 0:
				techComp.objects.get_or_create(company=company_, technology=tech)
		for a in soup.findAll('a'):
			if 'href' in a and a['href'] not in seen:
				new_link = a['href']
				if company_web_page in new_link:
					all_links.append( new_link)
				elif new_link[0] == '/':
					new_link = company_web_page+new_link
					all_links.append( new_link)
				seen.append(a['href'])


def webpageContainsTextInHeader(url, alias):
	if 'http://' not in url:
		url  = 'http://'+url
	try:
		r = requests.get(url)
		soup = BeautifulSoup(r.text)
		scripts = [a.get('src', '')+' '+a.text for a in soup.findAll('script')]
		return sum([s.count(alias) for s in scripts]) > 0
	except:
		return False



########################################
############# LINKEDIN #################
########################################


@task(queue="send_emails")
def getInterestsOfUser(user_id):
	user = User.objects.get(id = user_id)
	try:
		l = scrapers.privatePersonalLinkedinScraper(user.linkedin_public_profile)
		user.interests.add(*[Industry.objects.get_or_create(name = name.lower().strip())[0] for name in l.getInterests()])
	except:
		pass
	return None


LINKEDIN_SECRET_KEY = 'dpDaS1DIAanBKIBY'
LINKEDIN_API_KEY = '750cvasmd47qgf'
LINKEDIN_REDIRECT_URI = 'http://127.0.0.1:8000/linkedin/success'



class LinkedinLogin():
    def __init__(self, code = '', access_token = ''):
        self.code = code
        self.access_token = access_token
        if len(code):
            link = 'https://www.linkedin.com/uas/oauth2/accessToken?grant_type=authorization_code&code=%s&redirect_uri=%s&client_id=%s&client_secret=%s' % (self.code, LINKEDIN_REDIRECT_URI, LINKEDIN_API_KEY, LINKEDIN_SECRET_KEY)
            self.authorization_json = requests.get(link).json()
            self.access_token = self.authorization_json['access_token']
            self.expires_in = datetime.datetime.now() + datetime.timedelta(seconds=self.authorization_json['expires_in'])
    def getAccessToken(self):
        return self.access_token
    def getExpirationDate(self):
        return self.expires_in.isoformat() 
    def getEmail(self):
        r2 = requests.get('https://api.linkedin.com/v1/people/~:(email-address)?format=json&oauth2_access_token='+self.access_token).json()['emailAddress'].lower()
        return r2
    def getPublicProfile(self, info = ''):
        r2 = requests.get('https://api.linkedin.com/v1/people/~:(public-profile-url)?format=json&oauth2_access_token='+self.access_token).json()['publicProfileUrl'].replace('https://www.linkedin.com/', '')
        return r2
    def getProfileInfo(self):
        r2 = requests.get('https://api.linkedin.com/v1/people/~:?format=json&oauth2_access_token='+self.access_token).json()
        return r2
    def getSelf(self):
        r2 = requests.get('https://api.linkedin.com/v1/people/~:(id,public-profile-url,headline,first-name,last-name,picture-url,positions:(title,company),educations:(school-name,degree))?format=json&oauth2_access_token='+self.access_token).json()
        #convert to standard dictionary
        to_return = self.convertToStandard(r2)
        to_return['positions'] = self.getPositions()
        to_return['education'] = self.getEducation()
        return to_return
    def getPositions(self):
        r2 = requests.get('https://api.linkedin.com/v1/people/~:(positions)?format=json&oauth2_access_token='+self.access_token).json()
        #convert to standard dictionary
        return self.convertToStandard(r2)
    def getFirstConnections(self):
        connections = []
        r2 = requests.get('https://api.linkedin.com/v1/people/~:(id,public-profile-url,headline,first-name,last-name,picture-url,positions:(title,company),educations:(school-name,degree))?format=json', headers = {'Authorization': 'Bearer '+str(self.access_token)}).json()
        print r2
        return
        #convert to standard dictionary
        for r in r2:
            connections.append(self.convertToStandard(r))
        return connections
    def getEducation(self):
        r2 = requests.get('https://api.linkedin.com/v1/people/~:(educations)?format=json&oauth2_access_token='+self.access_token).json()
        #convert to standard dictionary
        return self.convertToStandard(r2)
    def getName():
        pass
    def convertToStandard(self, linkedin_dict):
        to_return = {}
        try:
            to_return['name'] = linkedin_dict['firstName']+' '+linkedin_dict['lastName']
        except:
            pass
        try:
            to_return['photo'] = linkedin_dict['pictureUrl']
        except:
            pass
        try:
            to_return['web_presence'] = {}
            to_return['web_presence']['personal_linkedin'] = {}
            to_return['web_presence']['personal_linkedin']['url']= linkedin_dict['publicProfileUrl']
            to_return['web_presence']['personal_linkedin']['id'] = linkedin_dict['id']
        except:
            pass
        if linkedin_dict.has_key('positions'):
            if linkedin_dict.has_key('positions') and linkedin_dict['positions'].has_key('values'):
                positions = []
                for p in linkedin_dict['positions']['values']:
                    company = {}
                    if p.has_key('company'):
                        try:
                            company['company_name'] = p['company']['name']
                        except:
                            pass
                        try:
                            company['industry'] = p['company']['industry']
                        except:
                            pass
                        try:
                            company['position'] = p['company']['title']
                        except:
                            pass
                    if p.has_key('endDate') and p['endDate'].has_key('year'):
                        company['end_year'] = p['endDate']['year']
                    if p.has_key('startDate') and p['startDate'].has_key('year'):
                        company['start_year'] = p['startDate']['year']
                    if p.has_key('isCurrent'):
                        company['active'] = p['isCurrent']
                    positions.append(company)
                to_return['positions'] = positions
        if linkedin_dict.has_key('educations') and linkedin_dict['educations'].has_key('values'):
            educations = []
            for p in linkedin_dict['educations']['values']:
                school = {}
                if p.has_key('schoolName'):
                   school['name'] = p['schoolName']
                if p.has_key('degree'):
                   school['degree'] = p['degree']
                if p.has_key('fieldOfStudy'):
                   school['fields_of_study'] = p['fieldOfStudy'].split(', ')
                if p.has_key('endDate') and p['endDate'].has_key('year'):
                   school['end_year'] = p['endDate']['year']
                if p.has_key('startDate') and p['startDate'].has_key('year'):
                   school['start_year'] = p['startDate']['year']
                educations.append(school)
            to_return['educations'] = educations
        return to_return







########################################
##### GOOGLE API / SENDING EMAILS ######
########################################


'''
INPUT : google auth token
OUTPUT: bool
	T -> auth token is good to go
	F -> auth token is not good to go
'''
def goodGoogleAuth(token):
	try:
		r = requests.get('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'%token)
		return 'error' not in r.json()
	except:
		return False

def getGoogleAccessToken(refresh_token):
	r = requests.post('https://www.googleapis.com/oauth2/v3/token', data = {
            'client_secret': 'VQ2sIQGhXH-ue6olCgUY9L3g',
            'client_id': '994895035422-bes5cqbhmf140j906598j1q91pvcnn08.apps.googleusercontent.com',
            'refresh_token': refresh_token,
            'grant_type': 'refresh_token'
            })
        response = r.json()
        return response['access_token']

def useGoogleAPI(user_id):
	u = User.objects.get(id=user_id)
	token = u.google_access_token
	if not goodGoogleAuth(token):
		u.google_access_token = getGoogleAccessToken(u.google_refresh_token)
		u.save()
		token = u.google_access_token
	else:
		pass
	return u.google_access_token

@task(queue="send_emails")
def sendEmailAsUser(user_id, to, body, subject):
	try:	
		person = Person.objects.get(emailaddress__address__iexact=to)
	except:
		person = None
	u = User.objects.get(id=user_id)
	try:
		conn = Connection.objects.get(person = person, user = u)
	except:
		conn = None
	access_token = useGoogleAPI(user_id)
	url = 'https://www.googleapis.com/gmail/v1/users/me/messages/send'
	headers = {}
	headers['content-type'] = 'application/json'
	headers['authorization'] = 'Bearer ' + access_token
	headers['content-length'] = 101
	unique = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(70))
	body = cgi.escape(body, True)
	body = body.replace("\n","<br />")
	message = MIMEMultipart('alternative')
	message['to'] = to
	message['from'] = User.objects.get(id=user_id).google_auth_email
	pixel_tracker_link = 'http://legionanalytics.com/msg/i_seens_it/shh/'+unique
	pixel_tracker = '<img src="%s" style="height: 1px; width:1px; display: none !important;"/>' % pixel_tracker_link
	message['subject'] = subject
	part1 = MIMEText(body, 'plain')
	html = """\
	<html>
	  <head></head>
	  <body>
	    <p>
	    %s
	    </p>
	  </body>
	</html>
	""" % body + pixel_tracker
	part2 = MIMEText(html, 'html')
	message.attach(part1)
	message.attach(part2)
	data = json.dumps({'raw': base64.urlsafe_b64encode(message.as_string())})
	try:
		r = requests.post(url, data=data, headers = headers)
		Message(user = u, person = person, subject = subject, connection = conn, body = body, type_of_message = 'email', unique_id = unique).save()
		return True
	except Exception as e:
		return False


def makeMessageView(request, message_id):
	m =  Message.objects.get(unique_id=message_id)
	try:
		if m.user == request.user:
			return False
	except Exception as e:
		pass
	MessageView(message = m).save()
	m.opened = True
	m.save()
	return False














########################################
####### INBOUND MARKETING INFO #########
########################################


def makeMarketEvent(market_info, user_id):
	m = marketEvent(name=market_info['event_name'], type_of_event = market_info['event_type'], user_id=user_id)
	date = datetime.datetime.strptime(market_info['event_date'], "%Y-%m-%d")
	m.date_started = date
	user = User.objects.get(pk=user_id)
	try:
		m.followers_at_the_time = twitterStats.objects.filter(Q(user=user) & Q(time_taken__lte=date)).last().num_followers
	except:
		api = getUserTwitterAPI(user)
		me = api.me()
		m.followers_at_the_time = me.followers_count 
	competitors = Competitor.objects.filter(user__id = user_id)
	keywords = keyWord.objects.filter(Q(user__id=user_id)).exclude(id__in=competitors.values_list('keywords__id', flat = True))
	sentiments = []
	for k in keywords:
		closest_sentiment = twitterSentiment.objects.filter(Q(keyWord=k) & Q(person=None) & Q(time_taken__lte=date)).last()
		if closest_sentiment:
			sentiments.append(float(closest_sentiment.sentiment))
	if len(sentiments):
		m.sentiment_at_the_time = sum(sentiments) / float(len(sentiments))
	else:
		m.sentiment_at_the_time = 0
	m.save()
	return True

def _cleanNumber(num):
	num = int(num)
	if num >= 1000000000:
		return str(round(num / 1000000000., 1))+'B'
	elif num >= 1000000:
		return str(round(num / 1000000., 1))+'M'
	elif num >= 10000:
		return str(round(num / 1000., 1))+'K'
	return str(num)

def competitorInfo(comp_id, period = 2):
	inbound_info = {}
	
	compet = Competitor.objects.get(id=comp_id)
	company = compet.company
	inbound_info['company_name']   = compet.name
	inbound_info['competitor_id']   = compet.id
	inbound_info['company_cleaned_name']   = inbound_info['company_name'].lower().replace(' ','_')
	inbound_info['company_logo']   = "http://logo.clearbit.com/"+company.company_home_page
	inbound_info['keywords']       = compet.keywords.all()
	end_date                       = datetime.datetime.now()
	beginning_date                 = end_date - datetime.timedelta(days=period)
	two_ago_date                   = beginning_date - datetime.timedelta(days=period)    
	try:
		inbound_info['most_recent_followers']          = twitterStats.objects.filter(company__id=company.id).last().num_followers
	except:
		inbound_info['most_recent_followers'] 		   = '0'
	stats = twitterStats.objects.filter(company__id=company.id)
	if stats.count():
		try:
			inbound_info['last_followers']                 = twitterStats.objects.filter(company__id=company.id).filter(time_taken__lte=beginning_date).last().num_followers
		except:
			inbound_info['last_followers']                 = twitterStats.objects.filter(company__id=company.id).first().num_followers
	else:
		inbound_info['last_followers'] = 0
	try:
		inbound_info['percent_change_followers'] = round(100. * (float(inbound_info['most_recent_followers']) - inbound_info['last_followers']) / inbound_info['last_followers'], 2)
	except:
		inbound_info['percent_change_followers'] = '0'
	inbound_info['change_followers'] = _cleanNumber(int(inbound_info['most_recent_followers']) - int(inbound_info['last_followers']))
	inbound_info['most_recent_followers'] = _cleanNumber(inbound_info['most_recent_followers'])
	inbound_info['last_followers'] = _cleanNumber(inbound_info['last_followers'])
	twitter_query                  = Q(date__gte=beginning_date) & Q(date__lte=end_date)
	if len(inbound_info['keywords']):
		twitter_query                  &= Q(keywords__in=inbound_info['keywords'])
	tweets                         = Tweet.objects.filter(twitter_query)
	if period == 30:
		inbound_info['sentiments']     = tweets.filter(~Q(textblob_sentiment=0)).values('date', 'textblob_sentiment')
		sentiments     = [(datetime.datetime.strftime(t['date'], '%D'), float(t['textblob_sentiment'])) for t in inbound_info['sentiments']]
		inbound_info['sentiments'] = []
		for date in set([a[0] for a in sentiments]):
			sents = [float(a[1]) for a in sentiments if date == a[0]]
			avg_sent = sum(sents) / len(sents)
			inbound_info['sentiments'].append((date, round(avg_sent, 2)))
		days_ago_30 = datetime.datetime.today() - datetime.timedelta(days = 31)
		for day in (days_ago_30 + datetime.timedelta(n) for n in range(32)):
			if datetime.datetime.strftime(day, '%D') not in [a[0] for a in inbound_info['sentiments']]:
				inbound_info['sentiments'].append((datetime.datetime.strftime(day, '%D'), 0.0))
		inbound_info['sentiments'] = sorted(inbound_info['sentiments'])
	inbound_info['positive_count'] = _cleanNumber(tweets.filter(textblob_sentiment__gt=0).count())
	if not inbound_info['positive_count']:
		inbound_info['positive_count'] = '0'
	inbound_info['negative_count'] = _cleanNumber(tweets.filter(textblob_sentiment__lt=0).count())
	if not inbound_info['negative_count']:
		inbound_info['negative_count'] = '0'
	inbound_info['sentiment']      = 100*float(average(tweets.values_list('textblob_sentiment', flat = True)))
	if not inbound_info['sentiment']:
		inbound_info['sentiment'] = '0'
	twitter_query                  = Q(date__gte=two_ago_date) & Q(date__lte=beginning_date)
	if len(inbound_info['keywords']):
		twitter_query              &= Q(keywords__in=inbound_info['keywords'])
	else:
		twitter_query = Q(id=-1)
	older_tweets = Tweet.objects.filter(twitter_query)
	inbound_info['older_sentiment']   = 100*float(average(older_tweets.values_list('textblob_sentiment', flat = True)))
	if not inbound_info['older_sentiment']:
		inbound_info['older_sentiment'] = '0'
	try:
		inbound_info['pop_change']     = 100.*(float(inbound_info['sentiment']) - float(inbound_info['older_sentiment'])) / inbound_info['older_sentiment']
	except:
		inbound_info['pop_change'] = 'N/A'
	if not inbound_info['pop_change']:
		inbound_info['pop_change'] = 'N/A'
	inbound_info['keywords'] = list(map(str, inbound_info['keywords'].values_list('text', flat = True)))
	inbound_info = {k: v for k, v in inbound_info.iteritems() if v}
	return inbound_info


def inboundInfo(user_id, period = 1):
	inbound_info = {}
	competitors                    = Competitor.objects.filter(user__id = user_id)
	end_date                       = datetime.datetime.now()
	beginning_date                 = end_date - datetime.timedelta(days=period)
	two_ago_date                   = beginning_date - datetime.timedelta(days=period)
	inbound_info['company_name']      = User.objects.get(pk=user_id).company_name
	inbound_info['keywords']       = keyWord.objects.filter(Q(user__id=user_id)).exclude(id__in=competitors.values_list('keywords__id', flat = True))
	try:
		inbound_info['most_recent_followers']           = twitterStats.objects.filter(user__id=user_id).last().num_followers
	except:
		inbound_info['most_recent_followers'] = 0
	last_stats = twitterStats.objects.filter(user__id=user_id).filter(time_taken__lte=beginning_date).last()
	inbound_info['last_followers'] = 0
	if last_stats:
		inbound_info['last_followers']                  = last_stats.num_followers
	else:
		last_stats = twitterStats.objects.filter(user__id=user_id).first()
		if last_stats:
			inbound_info['last_followers']                  = last_stats.num_followers
	if inbound_info['last_followers']:
		inbound_info['percent_change_followers']            = round(100. * (float(inbound_info['most_recent_followers']) - inbound_info['last_followers'] ) / inbound_info['last_followers'] , 2)
		inbound_info['change_followers'] = _cleanNumber(inbound_info['most_recent_followers'] - inbound_info['last_followers'] )
	else:
		inbound_info['percent_change_followers'], inbound_info['change_followers'] = '0', '0'
	inbound_info['most_recent_followers'] = _cleanNumber(inbound_info['most_recent_followers'])
	inbound_info['last_followers'] = _cleanNumber(inbound_info['last_followers'])
	twitter_query                  = Q(date__gte=beginning_date) & Q(date__lte=end_date)
	if len(inbound_info['keywords']):
		twitter_query                  &= Q(keywords__in=inbound_info['keywords'])
	else:
		twitter_query = Q(id = -1)
	tweets                         = Tweet.objects.filter(twitter_query)
	if period == 30:
		inbound_info['sentiments']     = tweets.filter(~Q(textblob_sentiment=0)).values('date', 'textblob_sentiment')
		sentiments                     = [(datetime.datetime.strftime(t['date'], '%D'), float(t['textblob_sentiment'])) for t in inbound_info['sentiments']]
		inbound_info['sentiments'] = []
		for date in set([a[0] for a in sentiments]):
			sents = [float(a[1]) for a in sentiments if date == a[0]]
			avg_sent = sum(sents) / len(sents)
			inbound_info['sentiments'] .append((date, round(avg_sent, 2)))
		days_ago_30 = datetime.datetime.today() - datetime.timedelta(days = 31)
		for day in (days_ago_30 + datetime.timedelta(n) for n in range(32)):
			if datetime.datetime.strftime(day, '%D') not in [a[0] for a in inbound_info['sentiments']]:
				inbound_info['sentiments'].append((datetime.datetime.strftime(day, '%D'), 0.0))
		inbound_info['sentiments'] = sorted(inbound_info['sentiments'])
	inbound_info['positive_count'] = _cleanNumber(tweets.filter(textblob_sentiment__gt=0).count())
	if not inbound_info['positive_count']:
		inbound_info['positive_count'] = '0'
	inbound_info['negative_count'] = _cleanNumber(tweets.filter(textblob_sentiment__lt=0).count())
	if not inbound_info['negative_count']:
		inbound_info['negative_count'] = '0'
	try:
		inbound_info['sentiment']      = 100*float(average(tweets.values_list('textblob_sentiment', flat = True)))
		if not inbound_info['sentiment']:
			inbound_info['sentiment'] = '0'	
	except:
		inbound_info['sentiment'] = '0'
	twitter_query                  = Q(date__gte=two_ago_date) & Q(date__lte=beginning_date)
	if len(inbound_info['keywords']):
		twitter_query              &= Q(keywords__in=inbound_info['keywords'])
	else:
		twitter_query = Q(id=-1)
	older_tweets = Tweet.objects.filter(twitter_query)
	inbound_info['older_sentiment']   = 100*float(average(older_tweets.values_list('textblob_sentiment', flat = True)))
	if not inbound_info['older_sentiment']:
		inbound_info['older_sentiment'] = '0'
	try:
		inbound_info['pop_change']     = int(100.*(inbound_info['sentiment'] - inbound_info['older_sentiment']) / inbound_info['older_sentiment'])
	except:
		inbound_info['pop_change'] = 'N/A'
	if not inbound_info['pop_change']:
		inbound_info['pop_change'] = 'N/A'
	inbound_info['keywords'] = list(map(str, inbound_info['keywords'].values_list('text', flat = True)))
	inbound_info = {k: v for k, v in inbound_info.iteritems() if v}
	return inbound_info


@task(queue='send_emails')
def getSentimentStatsForCompetitor(competitor_id):
	for days_ago in [30]:
		try:
			last_one = statsSnapshot.objects.filter(competitor_id=competitor_id, type_of_stats = 'sentiment_stats', period = days_ago).order_by('-generated').first()
			to_compare = last_one.stats
		except:
			to_compare = ''
		stats = json.dumps(competitorInfo(competitor_id, period = days_ago))
		if to_compare != stats:
			s = statsSnapshot(
								stats = stats,
								competitor_id = competitor_id, 
								period = days_ago,
								type_of_stats = 'sentiment_stats',
								generated = datetime.datetime.now()
							)
			s.save()
			return s
	return None



@task(queue='send_emails')
def getSentimentStatsForUser(user_id):
	for days_ago in [30]:
		try:
			last_one = statsSnapshot.objects.filter(user_id=user_id, type_of_stats = 'sentiment_stats', period = days_ago).order_by('-generated').first()
			to_compare = last_one.stats
		except:
			to_compare = ''
		dashboard_info = {}
		dashboard_info['me'] = inboundInfo(user_id, period = days_ago)
		people_pk = Connection.objects.exclude(followed_on=None).filter(Q(user__id = user_id) & Q(followed_on__gte=datetime.datetime.now() - datetime.timedelta(days=days_ago)) & (Q(followed_by=True) | Q(from_site = True))).order_by('-last_date').values_list('person__pk', flat = True)[:10]
		dashboard_info['most_recent_people'] = Person.objects.filter(pk__in=people_pk).values('personal_facebook', 'personal_twitter', 'personal_linkedin', 'personal_home_page', 'id', 'name', 'saved_photo', 'twitter_bio', 'age', 'klout_score', 'location', 'emailaddress__address')
		dashboard_info['most_recent_people'] = [dict(a) for a in dashboard_info['most_recent_people']]
		if to_compare != json.dumps(dashboard_info):
			s = statsSnapshot(
								stats = json.dumps(dashboard_info), 
								user_id = user_id, 
								period = days_ago,
								type_of_stats = 'sentiment_stats',
								generated = datetime.datetime.now()
							)
			s.save()
	return None


@task(queue='default')
def getSourceForEmail(email_id):
	e = EmailAddress.objects.get(id = email_id)
	g = scrapers.googleScraper()
	query = '"'+e.address+'"'
	results = g.search(query, current_index = 0)
	for r in results['results']:
		try:	
			text = requests.get(r['link'], timeout = 10).text
		except:
			continue
		e.sources.add(Website.objects.get_or_create(url = r['link'].lower()[:199], defaults = {'html':text})[0])






#############################
######## MAILCHIMP ##########
#############################


def getMailchimpAPI(user_id):
	access_token = User.objects.get(id = user_id).mailchimp_access_token
	api_key, shard = access_token.split('-')
	endpoint = "https://" + shard + ".api.mailchimp.com/3.0/"
	print requests.post(endpoint+'lists', headers = {'Authorization':'apikey '+str(access_token)}).json()
	return




#############################
########### ICP #############
#############################


def normalizeIt(counters):
    if counters == []: 
        return counters
    avg = max(1.0, float(average(c[1] for c in counters)) / 2.)
    return dict([(c[0], (c[1] / avg)) for c in counters if c[1] / avg > 1])




def makeICP(people, user_id = None):

    icp_dict = {}
    emails = EmailAddress.objects.filter(~Q(is_deliverable='Invalid') &Q(pk__in=people.values_list('emailaddress', flat = True)))
    sources = [scrapers._cleanURL(u).replace('http://','').split('/')[0] for u in emails.values_list('sources__url', flat = True) if u]
    sources = [s for s in sources if s]
    top_sources = Counter(sources).most_common(20)
    icp_dict['email_sources'] = normalizeIt(top_sources)

    interests = Counter(people.exclude(interests=None).values_list('interests', flat = True)).most_common(20)
    top_interests = zip(Industry.objects.filter(pk__in = [a[0] for a in interests]).values_list('name', flat = True), [a[1] for a in interests])
    icp_dict['interests'] =  normalizeIt(top_interests)
    job_titles = list(people.exclude(job=None).values_list('job', flat = True))
    active_job_title = Counter(Job.objects.filter(Q(pk__in = job_titles) & Q(is_active = True)).values_list('title', flat = True)).most_common(20)
    previous_job_title = Counter(Job.objects.filter(Q(pk__in = job_titles) & Q(is_active = False)).values_list('title', flat = True)).most_common(20)
    icp_dict['active_jobs'] = normalizeIt(active_job_title)
    icp_dict['previous_jobs'] = normalizeIt(previous_job_title)

    stopwords = set(['has', 'am', 'just', 'http', 'co', 'who', 'all', 'be', 'new', 'best', 'about', 'it', 'his', 'he', 'as', 'her', 'im', 'we', 'been', 'have', 'from', 'was', 'from', 'or', 'by', 'over', 'i', 'an', 'and', 'of', 'the', 'a', 'to', 'in', 'for', 'my', 'at', 'is', 'you', 'that', 'your', '', 'these', 'those', 'are', 'me', 'on', 'with', 'what', 'where', 'there', 'their', "they're"])
    exclude = set(string.punctuation) | set(['\n'])
    twitter_bios = list(people.filter(~Q(twitter_bio=None)).values_list('twitter_bio', flat = True))
    t_bios = [list(set(''.join(ch for ch in t.lower() if ch not in exclude).split(' '))) for t in twitter_bios]
    if len(t_bios): 
        twitter_top_words = [a for a in Counter(reduce(lambda x, y: x+y, t_bios)).most_common() if a[0] not in stopwords and not re.match(r'\d+', a[0])][:20] 
    else: 
        twitter_top_words = []
    icp_dict['twitter_keywords'] = normalizeIt(twitter_top_words)

   

    linkedin_bios = list(people.filter(~Q(linkedin_bio=None)).values_list('linkedin_bio', flat = True))
    l_bios = [list(set(''.join(ch for ch in t.lower() if ch not in exclude).split(' '))) for t in linkedin_bios]
    if len(l_bios): 
        linkedin_top_words = [a for a in Counter(reduce(lambda x, y: x+y, l_bios)).most_common() if a[0] not in stopwords][:20] 
    else: 
        linkedin_top_words = []
    icp_dict['linkedin_keywords'] = normalizeIt(linkedin_top_words)
    ICP(user_id = user_id, icp_dict = json.dumps(icp_dict), people = people).save()
    
def personCloseToICP(person_id, icp_dict):
    person = Person.objects.get(id = person_id)
    strength = 0
    for key, value in icp_dict.iteritems():
        if key == 'interests':
            try:
                interest_strength = min(5., reduce(lambda x, y:x*y, [value.get(i, 1.) for i in person.interests.values_list('name', flat = True)]))
            except:
                interest_strength = 0
            strength += interest_strength
        elif key == 'twitter_keywords':
            try:
                twitter_strength = min(5., reduce(lambda x, y:x*y, [value.get(i, 1.) for i in (''.join(ch for ch in person.twitter_bio.lower()).split(' '))]))
            except Exception as e:
                twitter_strength = 0
            strength += twitter_strength
        elif key == 'linkedin_keywords':
            try:
                linkedin_strength = min(5., reduce(lambda x, y:x*y, [value.get(i, 1.) for i in (''.join(ch for ch in person.linkedin_bio.lower()).split(' '))]))
            except:
                linkedin_strength = 0
            strength += linkedin_strength
        elif key == 'email_sources':
            sources = [scrapers._cleanURL(u).replace('http://','').split('/')[0] for u in person.emailaddress_set.all().values_list('sources__url', flat = True) if u]
            try:
                email_strength = min(5., reduce(lambda x, y:x*y, [value.get(s, 1.) for s in sources]))
            except:
                email_strength = 0
            strength += email_strength
        elif key == 'active_jobs':
            try:
                active_job_strength = min(5., reduce(lambda x, y:x*y, [value.get(i, 1.) for i in map(lambda x:x.lower(), person.job_set.all().filter(is_active = True).values_list('title', flat = True))]))
            except:
                active_job_strength = 0
            strength += active_job_strength
        elif key == 'previous_jobs':
            try:
                previous_job_strength = min(5., reduce(lambda x, y:x*y, [value.get(i, 1.) for i in map(lambda x:x.lower(), person.job_set.all().filter(is_active = False).values_list('title', flat = True))]))
            except:
                previous_job_strength = 0
            strength *= previous_job_strength
    return min(5., round(strength / 25., 1))



def getInfoForTM(targetmarket_id):
    people = list(targetMarket.objects.get(id = targetmarket_id).connection_set.values('person__personal_linkedin', 'person__personal_twitter', 'person__personal_facebook', 'person__personal_home_page', 'star_rating', 'person__age', 'num_interests', 'num_schools', 'num_titles', 'num_locations', 'person__name', 'person__pk', 'job__pk', 'job__company__pk', 'job__company__name', 'job__title', 'pk'))
    # return
    for person in people:
        person['star_rating'] = float(person['star_rating'])
        p = Person.objects.get(id = person['person__pk'])
        c = Company.objects.get(id = person['job__company__pk'])
        intersts = list(p.interests.all().values_list('name', flat = True))
        person['intersts'] = intersts
        emails = list(p.emailaddress_set.all().values_list('address', flat = True ))
        person['emails'] = emails
        educations = list(p.education_set.all().values_list('school_name', flat = True ))
        person['educations'] = [e for e in educations if len(e)]
        tweets_from_person = list(p.tweet_set.all().extra(select={'datestr':"to_char(date, 'YYYY-MM-DD HH24:MI')"}).values('text', 'datestr'))
        person['tweets_from_person'] = tweets_from_person
        tweets_from_company = list(c.tweet_set.all().extra(select={'datestr':"to_char(date, 'YYYY-MM-DD HH24:MI')"}).values('text', 'datestr'))
        person['tweets_from_company'] = tweets_from_company
        # person = {k: v for k, v in person.iteritems() if v}
    return people




import time
from collections import Counter
import json
import sys
import scrapers
import requests
import re
import HTMLParser
import web_analytics
from fuzzywuzzy import process, fuzz
h = HTMLParser.HTMLParser()

name_regex = re.compile('([A-Z]\w+ [A-Z]\w+)')


personal = ['gmail.com', '.edu', 'yahoo.com', 'hotmail.com', 'aol.com', 'comcast.net']

known_bad = ['balanced', 'policies', 'domainiq', 'domainiq_com', 'group.php', 'whattookyousolong', 'app_scoped_user_id', 'notes',\
 'inbox', 'notes', 'websitevaluecheck', 'fluidicon.png', 'l.php', 'r.php', 'login.php', 'pinned-octocat.svg', \
 'favicon.ico', 'signup', 'sessions', 'forum', 'forums', 'docs', 'home', 'share', 'people', 'public', 'plugins', \
 'widgets', 'pages', 'widgets.js', 'collection', 'oct.js', 'intent', 'share.php', 'sharer.php', 'shareArticle', \
 'techcrunch', 'login', 'about', '_private', 'private', 'fluidicon', 'security', 'pinned', 'recover', 'help', \
 'sharer', 'assets', 'favicon', 'dialog', 'contact', 'lead411', 'campaign', 'images', 'site', 'articles', 'blog']

class Scanner():
	def __init__(self, **kwargs):

		self.email_to_find = kwargs['email_to_find'].lower()
		self.seen = {v:set() for k, v in web_analytics.regex_dict.items()}
		self.confirmed = {}
		self.host = self.email_to_find.split('@')[0] 												# the part before the @
		self.domain, self.ending = self.email_to_find.split('@')[1].split('.')[0], '.'.join(self.email_to_find.split('@')[1].split('.')[1:])
		self.verbose = kwargs.get('verbose', False)
		self.names = []
		if sum([b in self.email_to_find for b in personal]) > 0:
			self.type = 'personal'
			self.keywords = []
		else:
			self.type = 'other'
			self.keywords = [self.domain]
		self.scrapers = {}
	def _getScraper(self, social_media, handle):
		if social_media == 'personal_twitter':
			return scrapers.personalTwitterScraper(handle, data = None)
		elif social_media == 'personal_linkedin':
			return scrapers.privatePersonalLinkedinScraper(handle)
		elif social_media == 'personal_github':
			return scrapers.personalGithubScraper(handle)
		elif social_media == 'personal_crunchbase':
			return scrapers.personalCrunchbaseScraper(handle)
		elif social_media == 'personal_facebook':
			return scrapers.personalFacebookScraper(handle)
		elif social_media == 'personal_angellist':
			return scrapers.personalAngellistScraper(handle)
		elif social_media == 'personal_google_plus':
			return scrapers.personalGooglePlusScraper(handle)
		return None

	def _averageMatch(self, s1, s2):
		return sum([fuzz.token_sort_ratio(s1, s2), fuzz.partial_ratio(s1, s2), fuzz.ratio(s1, s2)]) / 300.0

	def _confidence(self, sm, handle):
		scraper = self._getScraper(sm, handle)
		if scraper is None:
			return 0
		try:
			name = scraper.getInfo('name').lower()
		except:
			name = ''
		try:
			shortened_name = name.split(' ')[0]+ ' ' + name.split(' ')[-1]
		except:
			shortened_name = name
		try:
			first_name = name.split(' ')[0]
		except:
			shortened_name = name
		name_confidence = max(fuzz.ratio(name, self.host) / 100., fuzz.ratio(shortened_name, self.host) / 100., fuzz.ratio(first_name, self.host) / 100.)
		if self.type == 'personal':
			handle_confidence = fuzz.ratio(handle, self.host) / 100. # personal emails are more likely to have unique handles
		else:
			handle_confidence = fuzz.ratio(handle, self.host) / 200.
		try:
			if len(self.keywords):
				keyword_counts = [(k, json.dumps(scraper.getInfo('positions')).lower().count(k)+scraper.getInfo('name').lower().count(k)) for k in self.keywords]
				keyword_confidence = min(1., sum([k[1] for k in keyword_counts]) / float(len(self.keywords)))
				if name_confidence < .4:   # could be a company social media
					keyword_confidence = 0
			else:
				keyword_confidence = 0
				confidence = string_confidence
		except Exception as e:
			keyword_confidence = 0
		if self.verbose:
			print sm, handle, handle_confidence, keyword_confidence, name_confidence
		return {
				'keyword_confidence': keyword_confidence,
				'name_confidence': name_confidence,
				'handle_confidence': handle_confidence,
				'scraper':scraper
				}, name, shortened_name

	def isCorrectHandle(self, handle, social_media, threshold = {'keyword_confidence':.95, 'name_confidence':.95, 'handle_confidence':.95}):
		if re.match('^\d+$', handle) or handle in [a[0] for a in self.seen.get(social_media, [])] or social_media in self.confirmed.keys() or handle in known_bad or len(handle) < 3:
			return False, ''
		confidence_dict, name, shortened_name = self._confidence(social_media, handle)
		if self.type == 'other' and confidence_dict['keyword_confidence'] >= .95 and confidence_dict['name_confidence'] >= .95:
			print "confirmed because other"
			self.confirmed[social_media] = (handle.lower(), name.lower(), shortened_name.lower(), .95)
			self.scrapers[social_media] = confidence_dict['scraper']
			if self.verbose:
				print "CONFIRMED!", handle, social_media
			return True, name.lower()
		for confidence, confidence_threshhold in threshold.items():
			if confidence_dict[confidence] >= confidence_threshhold:
				self.confirmed[social_media] = (handle.lower(), name.lower(), shortened_name.lower(), confidence_dict[confidence])
				self.scrapers[social_media] = confidence_dict['scraper']
				if self.verbose:
					print "CONFIRMED!", handle, social_media
				return True, name.lower()
		self.seen[social_media].add((handle.lower(), name.lower(), shortened_name.lower(), confidence_dict[confidence], confidence_dict['scraper']))
		return False, ''


	def ScanForSocialMedias(self, only_confirmed = False, validate_email = False):

		if validate_email:
			validator = scrapers.emailVerifier(self.email_to_find)
			if validator.getKBMetrics()[1] == 'Invalid':
				return {'emails':[{'address':self.email_to_find, 'is_deliverable':'Invalid', 'type_of_email':self.type}]}, {} 
		# whenever I get the html of a site, grab all name regex and store ina  list
		# do a counter and get top 1-3 names
		# at the very end, loop through already_seen and compare names and shortened names to matching name regexs
		likely_name = ''
		if 'gmail.com' in self.email_to_find: #do the googel plus thing
			try:
				j = json.loads(scrapers.getHTMLForUrl('https://plus.google.com/complete/search?client=es-main-search&hl=en-US&gs_rn=18&gs_ri=es-main-search&cp=25&gs_id=6e&q='+self.email_to_find+'&xhr=t'))
				id_ = j[1][0][3]['a']
				personal_plus_scraper = self._getScraper('personal_google_plus', id_)
				self.scrapers['personal_google_plus'] = personal_plus_scraper
				self.confirmed['personal_google_plus'] = (id_, j[1][0][0].lower(), j[1][0][0].lower(), 1.0)
				likely_name = j[1][0][0]
				print "likely name is", likely_name
			except Exception as e:
				print e, "gmail error"
				pass


		lenient_threshold = {'keyword_confidence':.5, 'name_confidence':.6, 'handle_confidence':.6}
		g = scrapers.googleScraper()
		results = g.search(query='"'+self.email_to_find+'"')['results']						# 
		self.names += [m.group(1).lower() for m in re.finditer(name_regex, json.dumps(results))]				# 					# 
		for result in results:
			if sum([a in result['link'] for a in ['.php', '.pdf', '.txt', '.py', '.xml']]) > 0:						# ignore pdfs for now
				continue
			if self.verbose:
				print result['link']
			for regex, social_media in web_analytics.regex_dict.iteritems():
				m = re.search(regex, result['link'])
				if not m:
					continue
				correct, name = self.isCorrectHandle(m.group(1).lower(), social_media, threshold = lenient_threshold) # very low becuase its on the same page as their email
				if correct and not likely_name:
					likely_name = name
					print "name is", likely_name
					break
			try:	
				html = h.unescape(requests.get(result['link'], timeout = 10).text)
			except Exception as e:
				continue
			self.names += [m.group(1).lower() for m in re.finditer(name_regex, html)]
			len_html, emails_found = len(html), [m.start(0) for m in re.finditer(self.email_to_find, html)]
			for regex, social_media in web_analytics.regex_dict.iteritems():						# for each sm i havent seen
				if regex in self.confirmed.keys():
					continue
				handles_on_page = [(m.start(0), m.group(1).lower()) for m in list(set([r for r in re.finditer(regex, html)])) if m.group(1).lower() not in self.seen]
				if not len(handles_on_page):
					continue
				for distance, handle in handles_on_page:							# Sorted by distance to instance of email
					correct, name = self.isCorrectHandle(handle.lower(), social_media, threshold = lenient_threshold)
					if m and correct and not likely_name: # very low becuase its on the same page as their email
						likely_name = name
						print "name is", likely_name
						break

		if (len(self.confirmed.keys()) > 0 and only_confirmed) or not only_confirmed: # if theres even a chance	
			time.sleep(5)	
			if self.type == 'personal':
				if self.verbose:
					print "now its personal"
				results = g.search(query=self.host)['results']	
			else:
				if self.verbose:
					print "its just business"	
				results = g.search(query=self.host+' '+self.domain)['results']	
			new_thresholds = {'keyword_confidence':1.1, 'name_confidence':1.1, 'handle_confidence':1.1} # impossible 
			self.names += [m.group(1).lower() for m in re.finditer(name_regex, json.dumps(results))]				# 
			for result in results:
				if sum([a in result['link'] for a in ['.php', '.pdf', '.txt', '.py', '.xml']]) > 0:						# ignore pdfs for now
					continue
				if self.verbose:
					print result['link']
				for regex, social_media in web_analytics.regex_dict.iteritems():
					m = re.search(regex, result['link'])
					if not m:
						continue
					correct, name = self.isCorrectHandle(m.group(1).lower(), social_media, threshold = new_thresholds)
					if correct and not likely_name:
						likely_name = name
						print "name is", likely_name
						break
					elif social_media == 'personal_angellist':
						print "is an angellist"
						angel = scrapers.companyAngellistScraper(m.group(1).lower())
						for employee in angel.getFounders():
							print employee
							correct, name = self.isCorrectHandle(employee['web_presence']['personal_angellist']['url'], 'personal_angellist', threshold = new_thresholds)
							self.names +=[name.lower()]*2
							print "self.names", self.names
							if correct and not likely_name:
								print "found on angellsit"
								likely_name = name
								print "name is", likely_name
								break
		
		if not len(likely_name):
			most_common = Counter(self.names).most_common()
			likely_names = [(count[0], count[1] / float(most_common[0][1]) * fuzz.partial_ratio(self.host, count[0])) for count in most_common[:5] if fuzz.partial_ratio(self.host, count[0]) > .7]
			try:
				likely_name = sorted(likely_names, key = lambda x:x[1])[-1][0]
			except:
				likely_name = ''


		almost_confirmed = {}
		for social_media, already_seen in self.seen.iteritems():
			if social_media in self.confirmed.keys() or social_media in almost_confirmed.keys():
				continue
			for handle, name, short_name, conf, scraper in sorted(already_seen, key = lambda x:x[3], reverse = True):
				if social_media in self.confirmed.keys() or social_media in almost_confirmed.keys():
					break
				for confirmed_social_media, confirmed_information in self.confirmed.iteritems():
					confirmed_handle, confirmed_name, confirmed_short_name, confi = confirmed_information
					name_confidence = max(
							fuzz.ratio(short_name, confirmed_short_name) / 100., 
							fuzz.ratio(name, confirmed_name) / 100.)
					if social_media == 'personal_linkedin' and 'in/' in handle: # need to clean this up a bit
						handle = handle.replace('in/','')
					handle_confidence = int(handle == confirmed_handle)
					if self.verbose:
						print handle, handle_confidence, name_confidence
					if name_confidence >= .8 or handle_confidence >= .9:
						new_confidence = max(name_confidence, handle_confidence)
						if social_media == 'personal_linkedin' and 'pub/' not in handle:
							handle = 'in/'+handle
						if self.verbose:
							print "BASED ON OTHER SOCIAL MEDIA", handle, " is the ", social_media, new_confidence
						almost_confirmed[social_media] = (handle, new_confidence)
						self.scrapers[social_media] = scraper
						break
		

		fuzzy_string_matches = {}
		if not only_confirmed:	
			if len(self.confirmed.keys()) + len(almost_confirmed.keys()) <= 1 and len(likely_name):
				if self.verbose:
					print "The name is likely ::   ", likely_name.title()
				for social_media, already_seen in self.seen.iteritems():
					for handle, name, short_name, conf, scraper in already_seen:
						if social_media in self.confirmed.keys() or social_media in almost_confirmed.keys():
							break
						print short_name, likely_name, name
						name_confidence = max(fuzz.ratio(short_name, likely_name) / 100., fuzz.ratio(name, likely_name) / 100.)
						print name_confidence, fuzz.ratio(self.host, handle)/100., handle, social_media
						if name_confidence >= .9 or fuzz.ratio(self.host, handle)/100. >=.9:
							print "FUZZY MATCH", handle, " is the ", social_media, name_confidence, fuzz.ratio(self.host, handle)/100.
							fuzzy_string_matches[social_media] = (handle, name_confidence)
							self.scrapers[social_media] = scraper
							break

		
		to_return = self.confirmed
		to_return.update(almost_confirmed)
		if not only_confirmed:
			to_return.update(fuzzy_string_matches)
		return {'web_presence':{k:{'url':v[0]} for k, v in to_return.items()}, 'emails':[{'address':self.email_to_find, 'is_deliverable':'Valid', 'type_of_email':self.type}]}, self.scrapers

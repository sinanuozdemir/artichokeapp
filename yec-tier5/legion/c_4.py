import kb_lounge
import time
from collections import Counter, defaultdict
import json
import sys
import scrapers
import requests
import re
import Legion
import elves
import HTMLParser
import web_analytics
from fuzzywuzzy import process, fuzz
h = HTMLParser.HTMLParser()

name_regex = re.compile('([A-Z]\w+ [A-Z]\w+)')

known_bad = ['search', 'businessinsider', 'iwebsiteworth', 'simplyhired', 'dnshistory', 'domainbigdata', 'pub/domain-bigdata/b9/a90/959', 'flickr', 'askfmpage', \
 'iconosquare', 'profile.php', 'ohiomeansjobs.omj', 'speechpathologycom', 'opfsn', 'tr', 'reddit', 'profile', 'slideshare', \
 'privacy', 'ratemyprofessor', 'peekyou', 'profile/edit', '2008', 'balanced', 'policies', 'permalink.php', 'domainiq', \
 'domainiq_com', 'group.php', 'whattookyousolong', 'app_scoped_user_id', 'notes',\
 'inbox', 'notes', 'websitevaluecheck', 'fluidicon.png', 'l.php', 'r.php', 'login.php', 'pinned-octocat.svg', \
 'favicon.ico', 'signup', 'sessions', 'forum', 'forums', 'docs', 'home', 'share', 'people', 'public', 'plugins', \
 'widgets', 'pages', 'widgets.js', 'collection', 'oct.js', 'intent', 'share.php', 'sharer.php', 'shareArticle', \
 'techcrunch', 'login', 'about', '_private', 'private', 'fluidicon', 'security', 'pinned', 'recover', 'help', \
 'sharer', 'assets', 'favicon', 'search.json', 'zoominformation', 'supercompressor', 'dialog', 'contact', 'lead411', 'campaign', 'images', 'site', 'articles', 'blog']

personal = ['gmail.com', '.ed', 'yahoo.com', 'hotmail.com', 'aol.com', 'comcast.net']

class Scanner():
	def __init__(self, **kwargs):
		self.email_to_find = kwargs['email_to_find'].lower().strip()
		self.seen = defaultdict(list)
		self.confirmed = {}
		self.verbose = kwargs.get('verbose', False)
		self.status = kwargs.get('status', 'Unknown')
		validity = 'Valid'
		if kwargs['validate_first']:
			kb = kb_lounge.validateEmail(self.email_to_find, vrfy_hard = True)
			self.status = kb['validity']
		self.email_list = [{'address':self.email_to_find, 'is_deliverable':self.status}]
		self.fuzzy = kwargs.get('fuzzy', True)
		self.host, self.domain, self.ending = self.email_to_find.split('@')[0], self.email_to_find.split('@')[1].split('.')[0], '.'.join(self.email_to_find.split('@')[1].split('.')[1:])
		if sum([b in self.email_to_find for b in personal]) > 0:
			self.type = 'personal'
			self.keywords = []
		else:
			self.type = 'other'
			self.keywords = [self.domain]
		self.scrapers = {}
	def getInfoFromGmail(self):
		j = json.loads(scrapers.getHTMLForUrl('https://plus.google.com/complete/search?client=es-main-search&hl=en-US&gs_rn=18&gs_ri=es-main-search&cp=25&gs_id=6e&q='+self.email_to_find+'&xhr=t'))
		id_ = j[1][0][3]['a']
		personal_plus_scraper = self._getScraper('personal_google_plus', id_)
		self.scrapers['personal_google_plus'] = personal_plus_scraper
		self.confirmed['personal_google_plus'] = {'url':id_}
		self.known_name = j[1][0][0]
	def getRegexFromSite(self, url):
		seen = {}
		timeout = 5
		if 'emailsherlock' in url.lower():
			timeout = 15
		try:
			h = HTMLParser.HTMLParser()
			html = h.unescape(requests.get(url, timeout = timeout, allow_redirects = True).text)
		except Exception as e:
			return {}, ''
		for regex, social_media in web_analytics.regex_dict.items():
			found_sm = list(set([r.lower() for r in re.findall(regex, html) if r.lower() not in known_bad]))
			if found_sm:
				seen[social_media] =  found_sm
		return seen, html
	def _getScraper(self, social_media, handle):
		if social_media == 'personal_twitter':
			return scrapers.personalTwitterScraper(handle)
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
	def isASocialMediaLink(self, link):
		for regex, social_media in web_analytics.regex_dict.items():
			if re.search(regex, link) and re.search(regex, link).group(1).lower() not in known_bad and '/dir/' not in link and '/title/' not in link:
				return social_media, re.search(regex, link).group(1).lower()
	def _confidence(self, handle, sm):
		if handle in known_bad or sm in self.scrapers or sm in self.confirmed: # don't look at these st all
			return {}
		if handle in self.seen[sm]: #  I already have it
			sm_scraper = self.seen[sm][handle]['scraper']
		else:
			sm_scraper 			= self._getScraper(sm, handle)
		name_on_sm 				= sm_scraper.getInfo('name').lower()
		bio_on_sm 				= sm_scraper.getInfo('bio').lower().replace(' ', '')
		positions_on_sm 		= json.dumps(sm_scraper.getInfo('positions')).lower().replace(' ', '')
		try:
			first, last = name_on_sm.split(' ')[0], name_on_sm.split(' ')[-1]
		except:
			first, last = 'q','q'
		if not len(first) or not len(last):
			first, last = 'q', 'q'
		name_matches_host = max(fuzz.ratio(self.host, name_on_sm), fuzz.ratio(self.host, first), fuzz.ratio(self.host, first[0]+last), fuzz.ratio(self.host, first+' '+last))
		handle_matches_host = fuzz.ratio(handle.replace('in/',''), self.host)  #replace in clase its a linkedin
		keywords = int(100*(sum([k in bio_on_sm+positions_on_sm for k in self.keywords]) / max(float(len(self.keywords)), 1.0)))
		to_return = {'scraper': sm_scraper, 'name':name_on_sm, 'name_conf': name_matches_host, 'handle_conf': handle_matches_host, 'keyword_conf': keywords, 'exact_result':self.exact_result, 'handle': handle}
		return to_return
	def isCorrectHandle(self, handle, sm, already_confidence = None):
		if already_confidence:
			confidence = already_confidence
		else:
			confidence = self._confidence(handle, sm)
		if not confidence or sm in self.confirmed:
			return False
		
		l2 = Legion.legion({'web_presence':{sm:{'url':handle}}}, scrapers = {sm:confidence['scraper']})
		for known_sm, scraper in self.scrapers.items():    # compare against previously found social medias
			l1 = Legion.legion({'web_presence':{known_sm:self.confirmed[known_sm]}}, scrapers = {known_sm:scraper})
			if self.exact_result:
				result = elves._legionsAreTheSame(l1, l2, enough = [['name']])['result']
			else:
				result = elves._legionsAreTheSame(l1, l2)['result']
			if result: 
				self.scrapers[sm] = confidence['scraper']
				self.confirmed[sm] = {'url': handle}
				return True

		if self.fuzzy:
			if confidence['handle_conf'] == 100 or confidence['keyword_conf'] == 100: 
				self.scrapers[sm] = confidence['scraper']
				self.confirmed[sm] = {'url': handle}
				return True
		if self.exact_result:
			if confidence['name_conf'] >= 80: 
				self.scrapers[sm] = confidence['scraper']
				self.confirmed[sm] = {'url': handle}
				return True
			if confidence['handle_conf'] >= 95: 
				self.scrapers[sm] = confidence['scraper']
				self.confirmed[sm] = {'url': handle}
				return True
		if not already_confidence:
			self.seen[sm].append(confidence)
		return False
	def ScanForSocialMedias(self, validate_first = False):
		if self.status == 'Invalid':
			return Legion.legion({'emails':self.email_list}, scrapers = {})

		g = scrapers.googleScraper()

		self.exact_result = True
		self.exact_results_to_output = []
		exact_results = g.search('"'+self.email_to_find+'" -filetype:pdf')['results']
		social_links = [self.isASocialMediaLink(result['link']) for result in exact_results]
		social_links = [s for s in social_links if s]

		for sm, handle in social_links:
			if self.isCorrectHandle(handle, sm):
				if self.verbose:
					print "*****CONFIRMED", handle.upper(), sm.upper(), "CONFIRMED*****"

		for result in exact_results:
			link = result['link'].lower()
			link_dict = {'url':link}
			
			if sum([a in link for a in ['.pdf']]) > 0 or self.isASocialMediaLink(link):
				self.exact_results_to_output.append(link_dict)
				continue
			if self.verbose:
				print link
			regexes, html = self.getRegexFromSite(link)
			link_dict['html'] = html
			self.exact_results_to_output.append(link_dict)
			for sm, list_o_handles in regexes.iteritems():
				for handle in list_o_handles:
					if self.isCorrectHandle(handle, sm):
						if self.verbose:
							print "*****CONFIRMED", handle.upper(), sm.upper(), "CONFIRMED*****"

		self.email_list[0]['sources'] = self.exact_results_to_output
		# try to bring in ones that ahven't been matched yet
		for not_yet_got_sm in set(self.seen.keys()) - set(self.confirmed.keys()):
			for confidence in self.seen[not_yet_got_sm]:
				if self.isCorrectHandle(confidence['handle'], not_yet_got_sm, already_confidence = confidence):
					if self.verbose:
						print "*****CONFIRMED", confidence['handle'].upper(), not_yet_got_sm.upper(), "CONFIRMED*****"

		if self.fuzzy or self.scrapers:
			self.exact_result = False
			if self.type == 'personal':
				fuzzy_query = '"'+self.host+'"'
			else:
				fuzzy_query = '"'+self.host + '" ' + self.domain
			unexact_results = g.search(fuzzy_query + ' -filetype:pdf', include_fuzzy = True)['results']
			social_links = [self.isASocialMediaLink(result['link']) for result in unexact_results if self.isASocialMediaLink(result['link'])]
			for sm, handle in social_links:
				if self.isCorrectHandle(handle, sm):
					if self.verbose:
						print "*****CONFIRMED", handle.upper(), sm.upper(), "CONFIRMED*****"
			for result in unexact_results:
				link = result['link'].lower()
				if sum([a in link for a in ['.pdf']]) > 0 or self.isASocialMediaLink(link):
					continue
				for sm, list_o_handles in self.getRegexFromSite(link)[0].iteritems():
					for handle in list_o_handles:
						if self.isCorrectHandle(handle, sm):
							if self.verbose:
								print "*****CONFIRMED", handle.upper(), sm.upper(), "CONFIRMED*****"

		if '@gmail.com' in self.email_to_find:
			try:
				self.getInfoFromGmail()
				self.email_list[0]['is_deliverable'] = 'Valid'
			except:
				self.email_list[0]['is_deliverable'] = 'Unknown'
		
		# try to bring in ones that ahven't been matched yet
		for not_yet_got_sm in set(self.seen.keys()) - set(self.confirmed.keys()):
			for confidence in self.seen[not_yet_got_sm]:
				if self.isCorrectHandle(confidence['handle'], not_yet_got_sm, already_confidence = confidence):
					if self.verbose:
						print "*****CONFIRMED", confidence['handle'].upper(), not_yet_got_sm.upper(), "CONFIRMED*****"

		info = {'web_presence': self.confirmed, 'emails': self.email_list}
		l = Legion.legion(info, scrapers = self.scrapers)
		if self.verbose:
			print info['web_presence']
		return l.complete()
		


if __name__ == "__main__":
	s = Scanner(email_to_find = 'romano.nh@gmail.com', validate_first = False, verbose = True)
	complete = s.ScanForSocialMedias()
	print complete.information['web_presence']


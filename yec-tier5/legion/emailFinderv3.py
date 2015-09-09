import HTMLParser
import elves
import Legion
import c_4
import scrapers
import requests
import json
import re
from fuzzywuzzy import process, fuzz
from BeautifulSoup import BeautifulSoup
import web_analytics

name_dict = {'nicholas':'nick', 'jonathan': 'jon', 'johnathan': 'john', 'thomas':'tom', 'michael':'mike', 'samuel':'sam', 'samantha':'sam'}
important = ['founder', 'ceo', 'cmo', 'cto', 'owner']

class Emailgorithm():
	def __init__(self, legion_object, want = ['personal', 'company']):
		self.legion_object = legion_object
		self.scrapers = legion_object.scrapers
		self.person = legion_object.information
		self.want = want
	def isValidEmail(self, email):
		return scrapers.emailVerifier(email).validate()
	def match(self, email):
		if not self.isValidEmail(email):
			return False
		potential_person = c_4.Scanner(email_to_find = email, validate_first = False, verbose = False).ScanForSocialMedias()
		cor = elves._legionsAreTheSame(self.legion_object, potential_person)
		if cor['result']:
			try:
				self.legion_object.scrapers.update(potential_person.scrapers)
				self.legion_object.information['web_presence'].update(potential_person.information['web_presence'])
				self.legion_object.information['emails'] = [{'address':email, 'is_deliverable':'Valid'}]
			except Exception as e:
				pass
			return True
		try:
			requests.post('http://legionanalytics.com/putEntityInDB/', data={'type':'person', 'override': 'false', 'dict':json.dumps(potential_person.information)})
		except Exception as e:
			print e, "posting error"
		return False

	def fuzzyStringMatch(self, email):
		email = email.lower()
		name = self.legion_object.getInfo('name')
		host, domain = email.split('@')
		return fuzz.partial_ratio(name, host) >= 70 or fuzz.partial_ratio(name, domain) >= 60

	def _getPermutationsOfEmail(self, first, last, company_host): #assume the per determiend patter has the @ symbol
		return [f+company_host for f in [first, first+'.'+last, first+last, first+'-'+last, first[0]+last, first+last[0], first+'.'+last[0]]]


	def mainSearch(self):
		tried = set([])
		potential_emails = []
		handles_of_person = elves.getAllHandles(self.person)


		try:
			home_page = re.match('(\w+\.[^/]+)', self.person.get('web_presence', {}).get('personal_home_page', {}).get('url', '')).group(1)
		except:
			home_page  = ''

		if sum([a in home_page for a in ['medium.com', 'blogspot', 'twitter.com', 'instagram', 't.co', 'about.me', 'facebook', 'linkedin']]) > 0 or 'personal' not in self.want:
			home_page = ''


		# check if its anywhere in their legion dict
		m = re.findall(web_analytics.SIMPLE_EMAIL_REGEX, json.dumps(self.person))
		if m:
			self.legion_object.information['emails'] = [{'address':m[0][0].lower(), 'is_active':True, 'is_deliverable':'Valid'}]
			return self.legion_object



		if home_page:
			# check whois of their website
			w = scrapers.WhoisGenerator(home_page)
			for email in w.getEmails():
				if email in tried: continue
				tried.add(email)
				if self.fuzzyStringMatch(email):
					self.legion_object.information['emails'] = [{'address':email, 'is_active':True, 'is_deliverable':'Valid'}]
					return self.legion_object
				correct = self.match(email)
				if correct:
					return self.legion_object
			# scan their website
			for email in web_analytics.findRegexFromRoot(home_page, contact_only = True):
				if email in tried: continue
				tried.add(email)
				if self.fuzzyStringMatch(email):
					self.legion_object.information['emails'] = [{'address':email, 'is_active':True, 'is_deliverable':'Valid'}]
					return self.legion_object
				correct = self.match(email)
				if correct:
					return self.legion_object
			# try combinations of their name with their home page
			try:
				first_name, last_name = self.legion_object.getInfo('name').lower().split(' ')
				for email in self._getPermutationsOfEmail(first_name, last_name, '@'+home_page):
					if self.isValidEmail(email): # if its a real email, good enough
						self.legion_object.information['emails'] = [{'address':email, 'is_active':True, 'is_deliverable':'Valid'}]
						return self.legion_object
			except Exception as e:
				pass


		# check their linkedin
		if self.person.get('web_presence', {}).get('self.personal_linkedin', {}).get('url', ''):
			linkedin_link = self.person.get('web_presence', {}).get('self.personal_linkedin', {}).get('url', '')
			linkedin = scrapers.privateself.personalLinkedinScraper(linkedin_link)
			for email in linkedin.getEmailsOnSite():
				if email in tried: continue
				tried.add(email)
				if self.fuzzyStringMatch(email):
					self.legion_object.information['emails'] = [{'address':email, 'is_active':True, 'is_deliverable':'Valid'}]
					return self.legion_object
				correct = self.match(email)
				if correct:
					return self.legion_object

		# Try handles at @gmail, @yahoo
		try:
			hosts = reduce(lambda x, y: x+y, [[handle + host for host in ['@gmail.com', '@yahoo.com']] for handle in handles_of_person])
		except:
			hosts = []
		if home_page:
			hosts.extend([handle+'@'+home_page for handle in handles_of_person])
		if 'personal' not in self.want:
			hosts = []	
		for email in hosts:
			tried.add(email)
			correct = self.match(email)
			if correct:
				return self.legion_object



		if 'company' in self.want:
			# ok now try random combinations with known email hosts
			#start with combinations and email hosts
			try:
				first_name, last_name = self.legion_object.getInfo('name').lower().split(' ')[0], self.legion_object.getInfo('name').lower().split(' ')[-1]
			except:
				first_name, last_name = '', ''
			tried_times = 0
			for position in self.legion_object.getInfo('positions', alt = []):
				if not position.get('is_active', False):
					continue
				# complete the company information
				tried_times += 1
				if tried_times >= 2:
					break
				print position, "could be a source for email"
				company_legion = Legion.legion(position['company_dict'], type_of_entity = 'company', scrapers = {})
				if 'email_host' not in position['company_dict'] and 'company_home_page' not in position['company_dict'].get('web_presence', {}):
					completed_company = company_legion.complete().information
					position['company_dict'] = completed_company
				if position['company_dict'].get('email_host', None):
					emails = self._getPermutationsOfEmail(first_name, last_name, position['company_dict']['email_host'])
				elif position['company_dict'].get('web_presence', {}).get('company_home_page', None):
					emails = self._getPermutationsOfEmail(first_name, last_name, '@'+position['company_dict']['web_presence']['company_home_page']['url'])
				else:
					emails = []
				for email in emails:
					print email, "email"
					if self.isValidEmail(email): # if its a real email, good enough
						self.legion_object.information['emails'] = [{'address':email, 'type_of_email':"company", 'is_deliverable':'Valid'}]
						return self.legion_object

		
		# at this point do the internet scraper for each current job
		# but ONLY FOR THE FIRST 2!!
		
			found_emails = []
			y = scrapers.googleScraper()
			for position in self.legion_object.getInfo('positions', alt = []):
				if not position.get('is_active', False):
					continue
				try:
					company_name = position['company_dict']['name']
				except:
					continue
				print "searching: " + '"'+self.legion_object.getInfo('name', alt = '')+'" email ' + company_name
				results = y.search('"'+self.legion_object.getInfo('name', alt = '')+'" email ' + company_name)
				found_emails += [a[0] for a in re.findall(web_analytics.SIMPLE_EMAIL_REGEX, json.dumps(results))]
			found_emails = process.extract(self.legion_object.getInfo('name', alt = ''), list(set(found_emails)), limit=10) #order by closest match to self.persons name
			for email in found_emails:
				if str(email[0]) in tried: continue
				tried.add(email[0])
				if self.fuzzyStringMatch(email[0]):
					self.legion_object.information['emails'] = [{'address':email[0], 'is_active':True, 'is_deliverable':'Valid'}]
					return self.legion_object
				correct = self.match(email[0])
				if correct:
					return self.legion_object


		return self.legion_object





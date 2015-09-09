from fuzzywuzzy import process, fuzz
import scrapers
import elves
import Legion

'''
try passing in a list of things to check and the confidence is the % of those that matched
'''


media_dict = {
	'personal_linkedin': 'linkedin.com/pub OR site:linkedin.com/in -site:linkedin.com/pub/dir -site:linkedin.com/title -site:linkedin.com/company -site:linkedin.com/pulse',
	'personal_twitter': 'twitter.com/',
	'personal_github': 'github.com/',
	'personal_crunchbase': 'crunchbase.com/person/',
	'personal_angellist': 'angel.co/',
	'personal_facebook': 'facebook.com/'
}

company_media_dict = {
	'company_linkedin': 'linkedin.com/company/',
	'company_twitter': 'twitter.com/',
	'company_crunchbase': 'crunchbase.com/organization/',
	'company_angellist': 'angel.co/',
	'company_home_page': '',
	'company_facebook': 'facebook.com/'
}

def getCompanysSocialMedia(company_legion, type_of_media, verbose = False):
	g = scrapers.googleScraper()
	company_dict = company_legion.information
	current_web = company_legion.current_web_presences
	if type_of_media == 'company_home_page':
		results = g.search(query=company_legion.getInfo('name'))
	else:
		results = g.search(query=company_legion.getInfo('name')+' site:'+company_media_dict[type_of_media])
	for r in results['results'][:5]:
		try:
			handle = elves.return_url_end(r['link'])
		except:
			continue
		if handle.count('/')> 1:
			continue
		if type_of_media == 'company_home_page':
			if fuzz.partial_ratio(company_dict.get('name', ''), handle) >= 80:
				current_web['company_home_page'] = {'url': handle}
				company_dict = Legion.legion(company_dict, type_of_entity = 'company').complete()
				return Legion.legion(company_dict, type_of_entity = 'company', scrapers = {}).complete()
		complete = Legion.legion({'web_presence':{type_of_media:{'url':handle}}}, type_of_entity = 'company', scrapers = {}).complete()
		if elves._companiesAreTheSame(company_dict, complete.information):
			current_web.update(complete.current_web_presences)
			company_dict.update(complete.information)
			company_dict['web_presence'] = current_web
			return Legion.legion(company_dict, type_of_entity = 'company', scrapers = {}).complete()
	return Legion.legion(company_dict, type_of_entity = 'company', scrapers = {}).complete()


def getPersonsSocialMedia(this_legion, type_of_media, verbose = True, enough = []):
	queries = []
	query = this_legion.getInfo('name')
	if not query:
		query = ''
	tried = 0
	positions = this_legion.getInfo('positions')
	if not positions:
		positions = []
	for position in positions:
		if not position.get('is_active', False):
			continue
		tried += 1		
		if tried > 2:
			break

		queries.append(query + ' ' + position['position_title'] + ' "' + position['company_dict']['name']+'"')
	for query1 in queries:
		handles = []
		l = scrapers.googleScraper()
		if verbose:
			print "Searching", query1+' site:'+media_dict[type_of_media]
		try:
			handles += [elves.return_url_end(a) for a in l.search(query1+' site:'+media_dict[type_of_media])['social_medias'].get(type_of_media) if len(elves.return_url_end(a))]
			handles = [h.replace('person/', '') for h in handles] # clean them up
			handles = process.extract(this_legion.getInfo('name'), list(set(handles)), limit=5)
		except Exception as e:
			pass
		for handle in handles:
			if verbose:
				print "looking at", handle
			l = Legion.legion({'web_presence':{type_of_media:{'url':handle[0]}}}, scrapers = {})
			result = elves._legionsAreTheSame(this_legion, l, enough = enough)
			if result['result']:
				return result['updated_legion']
	return None

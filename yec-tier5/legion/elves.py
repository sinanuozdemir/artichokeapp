import io
import re
from fuzzywuzzy import process, fuzz
import math
import json
import urllib2 as urllib
import Legion
try:
	from PIL import Image
	import numpy as np
	from skimage.measure import structural_similarity as ssim
except:
	pass

def cleanCompanyName(stri):
	stri = stri.lower()
	for ending in ['.com', 'inc.', ' llc', ' management']:
		stri = stri.replace(ending, '')
	return stri.strip()

def getAllHandles(person):
    if not person or 'web_presence' not in person.keys():
        return []
    we = []
    for media, web_dict in person.get('web_presence', {}).iteritems():
        if media in ['personal_home_page', 'personal_crunchbase', 'personal_angellist', 'personal_google_plus']:
            continue
        handle = web_dict['url']
        if media == 'personal_linkedin':
            if 'in/' in handle:
                handle = handle[3:]
            else:
                continue    
        we.append(handle)
    return list(set(we))

def return_url_end(url, middle = False):
    WEB_REGEX = re.compile("(http[s]?://)?(www\.)?([^/]*)/?([^\?]*)(\?.*)?")
    to_return = ''
    if url == '':
        return ''
    match = re.match(WEB_REGEX, url)
    if not match:
    	return ''
    if middle:
    	to_return +=match.group(3)+'/'
    to_return += match.group(4)
    while to_return[-1] == '/':
		to_return = to_return[:-1]
    return to_return

def _companiesAreTheSame(c1, c2):
	first_name  =  cleanCompanyName(c1.get('name', '').lower())
	second_name =  cleanCompanyName(c2.get('name','').lower())
	for media, value in c1.get('web_presence', {}).iteritems():
		c1_url = value['url']
		c2_url = c2.get('web_presence', {}).get(media, {}).get('url', '')
		if c2_url.lower() == c1_url.lower():
			return True
	if first_name and second_name and fuzz.ratio(first_name, second_name) >= 70:
		return True
	return False

def imageSimilarity(url1, url2):
	try:
		fd = urllib.urlopen(url1)
		image_file = io.BytesIO(fd.read())
		img = Image.open(image_file).convert('L')
		img.thumbnail( (50,50) )
		fd2 = urllib.urlopen(url2)
		image_file2 = io.BytesIO(fd2.read())
		img2 = Image.open(image_file2).convert('L')
		img2.thumbnail( (50,50) )	
		return ssim(np.array(img2), np.array(img))
	except Exception as e:
		print e, "image error"
	return 0

def _peopleConfidence(p1, p2):
	reasons = []
	w1, w2 = p1.get('web_presence', {}).items(), p2.get('web_presence', {}).items()
	w1 = [(w[0], w[1]['url']) for w in w1]
	w2 = [(w[0], w[1]['url']) for w in w2]
	reasons += [a[0] for a in set(w1) & set(w2)]
	w1 = [w[1].replace('in/','') for w in w1]
	w2 = [w[1].replace('in/','') for w in w2]
	if len(set(w1)&set(w2)):
		reasons.append('same_handle')
	

	if p1.get('photo') and p2.get('photo'):
		if imageSimilarity(p1['photo'], p2['photo']) >= .8:
			reasons.append('photo')

	if p1.get('name') and p2.get('name'):
		if fuzz.partial_ratio(p1['name'], p2['name']) >= 80:
			reasons.append('name')

	if p1.get('location') and p2.get('location'):
		if fuzz.partial_ratio(p1['location'], p2['location']) >= 80:
			reasons.append('location')

	w1, w2 = p1.get('positions', []), p2.get('positions', [])
	for pos in w1:
		for pos2 in w2:
			if _companiesAreTheSame(pos.get('company_dict', {}), pos2.get('company_dict', {})):
				reasons.append('company')
				if fuzz.partial_ratio(pos.get('position_title', '').lower(), pos2.get('position_title', '').lower()) >= 80:
					print pos['position_title'].lower(), pos2['position_title'].lower(), fuzz.partial_ratio(pos.get('position_title', '').lower(), pos2.get('position_title', '').lower()) 
					reasons.append('position company')


	return reasons

def _peopleAreTheSame2(p1, p2, enough = [['photo'], ['name', 'same_handle'], ['name', 'position'], ['name', 'company'], ['personal_facebook'], ['personal_linkedin'], ['personal_angellist'], ['name', 'personal_home_page'], ['personal_twitter']]):
	conf = _peopleConfidence(p1, p2)
	for e in enough:
		if len(e) == len(set(e) & set(conf)):
			print "matched becuase of ", conf
			return True
	return False



def _legionsAreTheSame(l1, l2, enough = []):
	emails = l1.information.get('emails',[]) + l2.information.get('emails',[])
	enough.extend([['photo'], ['name', 'position company'], ['name', 'company'], ['position company'], ['name', 'same_handle'], ['name', 'personal_home_page'], ['personal_linkedin'], ['personal_angellist'], ['personal_crunchbase'], ['personal_twitter']])
	if _peopleAreTheSame2(l1.information, l2.information, enough = enough):
		l1.scrapers.update(l2.scrapers)
		l1.current_web_presences.update(l2.current_web_presences)
		return {'result': True, 'updated_legion': Legion.legion(information = {'emails':emails, 'web_presence':l1.current_web_presences}, scrapers = l1.scrapers).complete()}
	for sm, sm_dict in l1.information.get('web_presence', {}).items():
		if sm in l1.scrapers:
			p2 = Legion.legion(information = {'web_presence':{sm:sm_dict}}, scrapers = {sm: l1.scrapers[sm]})
		else:
			p2 = Legion.legion(information = {'web_presence':{sm:sm_dict}}, scrapers = {})
		p2.getAllBasicInfo()
		p2.getAllAdvancedInfo()
		p2.getAllSocialMedias()
		if _peopleAreTheSame2(l2.information, p2.information, enough = enough):
			l1.scrapers.update(p2.scrapers)
			l1.current_web_presences.update(p2.current_web_presences)
			return {'result': True, 'updated_legion': Legion.legion(information = {'emails':emails, 'web_presence':l1.current_web_presences}, scrapers = l1.scrapers).complete()}
	for sm, sm_dict in l2.information.get('web_presence', {}).items():
		if sm in l2.scrapers:
			p2 = Legion.legion(information = {'web_presence':{sm:sm_dict}}, scrapers = {sm: l2.scrapers[sm]})
		else:
			p2 = Legion.legion(information = {'web_presence':{sm:sm_dict}}, scrapers = {})
		p2.getAllBasicInfo()
		p2.getAllAdvancedInfo()
		p2.getAllSocialMedias()
		if _peopleAreTheSame2(l1.information, p2.information, enough = enough):
			l1.scrapers.update(p2.scrapers)
			l1.current_web_presences.update(p2.current_web_presences)
			return {'result': True, 'updated_legion': Legion.legion(information = {'emails':emails, 'web_presence':l1.current_web_presences}, scrapers = l1.scrapers).complete()}
	for sm, sm_dict in l1.information.get('web_presence', {}).items():
		if sm in l1.scrapers:
			p1 = Legion.legion(information = {'web_presence':{sm:sm_dict}}, scrapers = {sm: l1.scrapers[sm]})
		else:
			p1 = Legion.legion(information = {'web_presence':{sm:sm_dict}}, scrapers = {})
		for sm2, sm_dict2 in l2.information.get('web_presence', {}).items():
			if sm2 in l2.scrapers:
				p2 = Legion.legion(information = {'web_presence':{sm2:sm_dict2}}, scrapers = {sm2: l2.scrapers[sm2]})
			else:
				p2 = Legion.legion(information = {'web_presence':{sm2:sm_dict2}}, scrapers = {})
			p1.getAllBasicInfo()
			p1.getAllAdvancedInfo()
			p1.getAllSocialMedias()
			p2.getAllBasicInfo()
			p2.getAllAdvancedInfo()
			p2.getAllSocialMedias()
			if _peopleAreTheSame2(p1.information, p2.information, enough = enough):
				l1.current_web_presences.update(l2.current_web_presences)
				l1.scrapers.update(l2.scrapers)
				return {'result':True,  'updated_legion': Legion.legion(information = {'emails':emails, 'web_presence':l1.current_web_presences}, scrapers = l1.scrapers).complete()}
	return {'result': False, 'updated_legion': None}






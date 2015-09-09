import HTMLParser
import re
import requests
from BeautifulSoup import BeautifulSoup
from pyPdf import PdfFileWriter, PdfFileReader
import os


regex_dict = {
	'twitter.com/([\w\.\-]+)':'personal_twitter',
	'facebook.com/([\w\.\-]+)':'personal_facebook',
	'linkedin.com/([pubin]+/[\/\w\-]+)':'personal_linkedin',
	'github.com/([\w\.\-]+)':'personal_github',
	'angel.co/([\w\.\-]+)':'personal_angellist',
	'crunchbase.com/person/([\w\.\-]+)':'personal_crunchbase',
	'producthunt.com/([\w\.\-]+)':'personal_twitter',
	'watchonperiscope.com/([\w\.\-]+)':'personal_twitter',
	'tweettunnel.com/([\w\.\-]+)':'personal_twitter',
	'twitteraccountsdetails.com/([\w\.\-]+)':'personal_twitter'	,
	'plus.google.com/(\d+)': 'personal_google_plus'
}


def _extractEmailsFromPdf(url):
	file_name = 'pdf/'+''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(10))+'.pdf'
	r = requests.get(url)
	with open(file_name, "wb") as file_pdf:
		file_pdf.write(r.content)
	pdfDoc = PdfFileReader(file(file_name, "rb"))
	content = ""
	for i in range(0, min(pdfDoc.getNumPages(), 2)):		
		content += (pdfDoc.getPage(i).extractText() + "\n").encode('ascii', 'ignore').lower()
	emails = list(set([a[0] for a in re.findall(SIMPLE_EMAIL_REGEX, content)]))
	os.remove(file_name)
	return emails


def getRegexGroupFromSite(url, rege = ''):
	url = _cleanURL(url)
	try:
		h = HTMLParser.HTMLParser()
		html = h.unescape(requests.get(url, timeout = 3, allow_redirects = True).text)
	except Exception as e:
		return []
	return list(set([r.lower() for r in re.findall(rege, html)]))



SIMPLE_EMAIL_REGEX = re.compile('(([a-zA-Z0-9][\w\.-]+)@([a-z-_A-Z0-9\.]+)\.(\w\w\w?))', re.IGNORECASE)
website_regex = re.compile('((https?://)?(www.)?([\w\.]+)(\.[etorgcovmn]+)(/.+)?)', re.IGNORECASE)
EMAIL_REGEX = re.compile('(([a-zA-Z0-9][\w.-]+)(\s+)?\(?(@|at)\)?(\s+)?([a-z-_A-Z0-9]+)(\s+)?(\.|dot)(\s+)?(net|com|co|edu|gov|org))', re.IGNORECASE)
important = ['founder', 'owner', 'vice', 'president', 'ceo', 'coo', 'cto', 'chief', 'investor', 'cmo']

bad_emails = ['info@', 'contactus@', 'contact@', 'admin@', '@contactprivacy.com', 'customerservice@', 'gandi', 'domains@', 'domain@', 'careers@', 'speakers@', 'sales@', 'pr@','dnsmaster@', 'marketing@', 'legal@', 'support@', 'press@', 'abusecomplaints@', 'hostmaster@', 'whois', 'abuse@', '@domainsbyproxy']
static = ['.png', '.css', '.js', '.jpg', '.jpeg', 'rss', '.svg', '.pdf', '.ico', ':void', 'mailto:', '.xml', 'googleapis', '/feed', 'google.com', 'itunes', 'apps.microsoft']
contact = ['info', 'contact', 'about', 'team', 'bio', 'biography']
news = ['techcrunch', 'prweb', 'gigaom', 'fastco', 'indiegogo', 'digitaltrends', 'forbes', 'inc.' 'kickstarter', 'cnn.']
sm = ['twitter', 'reddit', 'facebook', 'linkedin', 'instagram', 'youtube', 'vimeo', 'article', 'blog', 'plus.google', 'pinterest', 'crunchbase', 'angellist', 'tumblr', 'wordpress']


def _extractEmailsFromPdf(url):
	#random file name
	file_name = 'pdf/'+''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(10))+'.pdf'
	r = requests.get(url, allow_redirects=False)
	with open(file_name, "wb") as file_pdf:
		file_pdf.write(r.content)
	pdfDoc = PdfFileReader(file(file_name, "rb"))
	content = ""
	for i in range(0, pdfDoc.getNumPages()):		
		content += (pdfDoc.getPage(i).extractText() + "\n").encode('ascii', 'ignore').lower()
	emails = list(set([a[0] for a in re.findall(SIMPLE_EMAIL_REGEX, content)]))
	os.remove(file_name)
	return emails

def _cleanURL(url):
	if sum([bad in url for bad in static]) > 0:
		return ''
	url = url.lower()
	match = re.match(website_regex, url) # create a regular expression object
	if match: # if the website matches the regex
		return 'http://www.'+ ''.join([a for a in match.groups()[3:] if a]).replace('.html','')
	return ''


def getInternalLinksFromSite(url, host = ''):
    url = _cleanURL(url)
    try:
        h = HTMLParser.HTMLParser()
        html = h.unescape(requests.get(url, timeout = 3, allow_redirects = False).text)
    except Exception as e:
        return []
    soup = BeautifulSoup(html)
    unfiltered = [a['href'] for a in soup.findAll('a') if a.get('href')]
    filtered = set()
    for site in unfiltered:
        if '/' == site[0]:
            site = host+site
        if '#' in site:
            site = site[:site.find('#')]
        site = _cleanURL(site)
        if site and url in site:
            filtered.add(_cleanURL(site))
    return list(filtered)


def getRegexFromSite(url, rege = SIMPLE_EMAIL_REGEX):
	url = _cleanURL(url)
	try:
		h = HTMLParser.HTMLParser()
		html = h.unescape(requests.get(url, timeout = 3, allow_redirects = True).text)
	except Exception as e:
		return []
	return list(set([r[0].lower() for r in re.findall(rege, html)]))


def breadthFirstSearch(url, rege = SIMPLE_EMAIL_REGEX, contact_only = False):
	url = _cleanURL(url)
	to_see = [url]
	seen = set()
	while len(to_see):
		looking_at = to_see.pop(0)
		if looking_at == url or (looking_at not in seen and (not contact_only or sum([c in looking_at.lower() for c in contact]) > 0)):
			seen.add(looking_at)
			yield getRegexFromSite(looking_at, rege)
			to_see += set(getInternalLinksFromSite(looking_at, url)) - seen

def findRegexFromRoot(url, n = 5, rege = SIMPLE_EMAIL_REGEX, contact_only = False):
	b = breadthFirstSearch(url, rege, contact_only)
	i, emails  = 0, []
	while i < n and not len(emails):
		try:
			emails = b.next()
		except:
			return emails
		i+=1
	return emails

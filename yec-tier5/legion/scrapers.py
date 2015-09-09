import geocoder
import pickle
import Legion
import string
import requests
from BeautifulSoup import BeautifulSoup
import json
import oauth2 as oauth
import urllib
import re
from klout import *
import time
import tweepy
import json
import HTMLParser
from fuzzywuzzy import fuzz
from collections import defaultdict
import random
import clearbit
from datetime import datetime, date
import kb_lounge

bad_emails = ['info@', 'privateregistration', '@emails.com', 'protecteddomainservices.com', 'domainreg@', 'domains-tech@', 'nocontactsfound', 'compliance@', 'jobs@', 'hello@', 'proxy', 'accounts', 'advertising', 'domainholdings.com', 'system@', 'investor', 'businessdevelopment', '@domaindiscreet', 'contact@', 'admin@', 'customerservice@', 'gandi', 'domains@', 'careers@', 'speakers@', 'sales@', 'pr@','dnsmaster@', 'marketing@', 'legal@', 'support@', 'domain@', 'press@', 'abusecomplaints@', 'hostmaster@', 'whois', 'abuse@', '@domainsbyproxy']
bad_site_contains = ['.xml', '.js']
bad_sites = ['lead411']


# client   = kickbox.Client('a1edfc79c80d401eb4fd95c9664c8d8446dfce4cda5cddfea561a6c1d03bae0a')
# kickbox  = client.kickbox()


sinans = '4568c46b5c97886c88b28f311616ed62'
cb_api_key = sinans


k = Klout('3ezgcrc4urzfexjpuh7qbjvu')


website_regex = re.compile('(https?://)?(www.)?([\w\.]+)(\.[etorigcovmn]+)(/.+)?', re.IGNORECASE)
SIMPLE_EMAIL_REGEX = re.compile('(([a-zA-Z0-9][\w\.-]+)@([a-z-_A-Z0-9\.]+)\.(net|com|co|edu|gov|org))', re.IGNORECASE)

fullcontact_api_key = '3ef6f45fcad16ea2'

clearbit.key = '78dc26c13571840076621e1cb9b42707' # bobs
# clearbit.key='298d03011c74dfb18a55a30cc42304e7' # sinans
media_dict = {
    'personal_linkedin': ['linkedin.com/in/', 'linkedin.com/pub/'],
    'personal_twitter': ['twitter.com/'],
    'personal_github': ['github.com/'],
    'personal_crunchbase': ['crunchbase.com/person/'],
    'personal_angellist': ['angel.co/']
}

USER_AGENTS = ["Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.6) Gecko/20070725 Firefox/2.0.0.6",
               "Mozilla/5.0 (X11; U; Linux i686; en-US) AppleWebKit/534.3 (KHTML, like Gecko) Chrome/6.0.472.63 Safari/534.3",
               "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)",
               "Opera/9.00 (Windows NT 5.1; U; en)",
               "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36",
               "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2226.0 Safari/537.36",
               "Mozilla/5.0 (compatible, MSIE 11, Windows NT 6.3; Trident/7.0; rv:11.0) like Gecko",
               "Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; AS; rv:11.0) like Gecko",
               "Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/6.0)",
               "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.67 Safari/537.36"
]

def _cleanURL(url):
    if sum([bad in url for bad in bad_site_contains]) > 0:
        return ''
    url = url.lower()
    match = re.match(website_regex, url) # create a regular expression object
    if match: # if the website matches the regex
        return 'http://'+ ''.join([a for a in match.groups()[2:] if a]).replace('.html','')
    return ''

def locationToJson(location):
    if not location:
        return {}
    try:
        to_return = {}
        g = geocoder.google(location)
        to_return['location'] = location
        to_return['city'] = g.city
        to_return['country'] =  g.country
        to_return['state'] =  g.state
    except Exception as e:
        to_return = {'location':'IDK', 'country':'IDK', 'city':'IDK'}
    return to_return

def locationToCountry(location):
    if not location:
        return 'IDK'
    if 'united states' in location.lower():
        return 'US'
    try:
        location = location.lower()
        location = location.replace('greater', '').replace('area', '')
        location = location.strip()
        return requests.get('http://api.openweathermap.org/data/2.5/weather?id=80575a3090bddc3ce9f363d40cee36c2&q='+location).json()['sys']['country']
    except Exception as e:
        return 'IDK'
    return 'IDK'


def getProxies(test = False, max_time = '2000', anon = '34', king_only = False, cookies = None):
    if test:
        PROXY_LIST = [a['type_of_proxy']+a['ip']+':'+a['port'] for a in  requests.get('http://legionanalytics.com/getRandomAPIProxies?limit=10').json()]
        return PROXY_LIST
    for i in range(5):
        PROXY_LIST = []
        try:
            response = requests.get('https://kingproxies.com/api/v2/proxies.txt?key=1df2713cbc434caaa8bca8cddc014f&type=anonymous', timeout=3)
            if '<!DOCTYPE html>' in response.text:
                king_only = False
            else:
                PROXY_LIST += ['http://'+a for a in response.text.split('\n') if len(a) > 2]
        except Exception as e:
            pass
        if not king_only:
            try:
                PROXY_LIST += ['http://'+a for a in requests.get('http://incloak.com/api/proxylist.php?country=CNUS&maxtime='+max_time+'&type=h&anon=' + anon + '&out=plain&lang=en&code=1122019427', timeout=3).text.split('\r\n') if len(a) > 2]
            except Exception as e:
                pass
        if len(PROXY_LIST):
            return PROXY_LIST
    return []


linkedin_cookies = ['sinan', 'jamasen']
def getHTMLForUrl(url, timeout = 6, attempts_to_make = 10, max_time = '2000', anon = '34', king_only = False, cookies = None):
    # print "for", url
    PROXY_LIST = getProxies(test = False, king_only = king_only, max_time = max_time, anon = anon)
    h = HTMLParser.HTMLParser()
    attempts = 0
    if cookies:
        if 'linkedin' in cookies:
            cookie_url = 'https://s3-us-west-2.amazonaws.com/tier5/linkedin_cookies/'+random.choice(linkedin_cookies)
            f = urllib.urlopen(cookie_url)
            cookies = requests.utils.cookiejar_from_dict(pickle.load(f))
    if len(PROXY_LIST) == 0:
        return ''
    while attempts < attempts_to_make:
        headers = {
        'User-Agent': random.choice(USER_AGENTS),
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding': 'deflate',
        'Connection': 'close'
        }
        rand = random.choice(PROXY_LIST)
        proxies = {'http':rand}
        PROXY_LIST.remove(rand)
        try:            
            r = requests.get(url, proxies = proxies, headers = headers, cookies = cookies, timeout=timeout)
            time.sleep(random.choice(range(3)))
            status = r.status_code
        except Exception as e:
            time.sleep(random.choice(range(3)))
            status = -1
        attempts +=1
        if status == 200 and 'META NAME="ROBOTS"' not in r.text and 'https://www.linkedin.com/lite/ua/error' not in r.text and '<title>Bot or Human</title>' not in r.text:
            time.sleep(random.choice(range(3)))
            return h.unescape(r.text)
        elif status == 404:
            return ''
    return ''

def return_url_end(url, middle = False):
    WEB_REGEX = re.compile("(http[s]?://)?(www\.)?([^/]*)/?(.*)")
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
            if end_.find('?') > 0:
                return end_[:end_.find('?')].lower()
            else:
                return end_
        else:
            if len(end_):
                if (middle_+'/'+end_).find('?') > 0:
                    return middle_+'/'+end_[:(middle_+'/'+end_).find('?')].lower()
                return middle_+'/'+end_
            if (middle_+'/'+end_).find("?")>0:
                return middle_+'/'+end_[:(middle_+'/'+end_).find('?')]
            return middle_.lower()
    else:
        return ''

class personalGooglePlusScraper():
    def __init__(self, handle = ''):
        self.handle = handle
        try:
            self.soup = BeautifulSoup(getHTMLForUrl('https://plus.google.com/'+handle+'/about', anon='4', king_only = True))
        except:
            self.soup = BeautifulSoup('')
    def getName(self):
        try:
            return self.soup.find('div', {'guidedhelpid':'profile_name'}).text
        except:
            return ''
    def getPhoto(self):
        try:
            if 'AAAAAAAAAAI/AAAAAAAAAAA' not in self.soup.find('div', {'guidedhelpid':'profile_photo'}).findChild('img')['src']:
                return 'http:'+self.soup.find('div', {'guidedhelpid':'profile_photo'}).findChild('img')['src']
        except:
            pass
        return ''
    def getInterests(self):
        try:
            to_scan = self.soup.find('div', {'id':'8'})
            for i, d in enumerate(to_scan.findChildren('div')):
                if d.text == 'Skills':
                    return to_scan.findChildren('div')[i+1].text.split(',')
        except:
            return []
    def getPositions(self):
        positions = []
        to_scan = self.soup.find('div', {'id':'8'})
        if to_scan is None:
            return []
        for u in to_scan.findChildren('li', {'class':'UZa'}):
            pos = {}
            company_name = u.findAll('div')[0].text
            position_title, dates = ''.join(u.findAll('div')[1].text.split(',')[:-1]), u.findAll('div')[1].text.split(',')[-1]
            pos['position_title'] = position_title
            company_name = company_name.strip()
            if 'present' == u.findAll('div')[1].text.lower():
                pos['is_active'] = True
            else:
                try:
                    position_title, dates = ''.join(u.findAll('div')[1].text.split(',')[:-1]), u.findAll('div')[1].text.split(',')[-1]
                    pos['start_year'] = int(dates.split(' - ')[0])
                    if 'present' != dates.split(' - ')[1].lower():
                        pos['end_year'] = int(dates.split(' - ')[1])
                        pos['is_active'] = False
                    else:
                        pos['is_active'] = True
                except Exception as ree:
                    print ree, "POSITION START TIME ERROR 1", self.handle
            pos['company_dict'] = {'name':company_name}
            positions.append(pos)
        return positions
    def getEducation(self):
        positions = []
        to_scan = self.soup.find('div', {'id':'9'})
        if to_scan is None:
            return []
        for u in to_scan.findChildren('li', {'class':'UZa'}):
            pos = {}
            school_name = u.findAll('div')[0].text
            degree, dates = ''.join(u.findAll('div')[1].text.split(',')[:-1]), u.findAll('div')[1].text.split(',')[-1]
            pos['degree'] = degree.strip()
            if '-' in dates:
                try:
                    pos['start_year'] = int(dates.split(' - ')[0])
                    if 'present' != dates.split(' - ')[1].lower():
                        pos['end_year'] = int(dates.split(' - ')[1])
                        pos['is_active'] = False
                    else:
                        pos['is_active'] = True
                except Exception as ree:
                    pass
            else:
                pos['end_year'] = dates.strip()
                pos['is_active'] = False
            pos['school_name'] = school_name.strip()
            positions.append(pos)
        return positions
    def getAge(self):
        educations = self.getEducation()
        for e in educations:
            try:
                if 'ba' in e['degree'].lower() or 'bs' in e['degree'].lower() or 'b.s' in e['degree'].lower() or 'b.a' in e['degree'].lower() or "bachelor" in e['degree'].lower():
                    return datetime.now().year-int(e['end_year']) + 21
            except:
                continue
        if len(educations) > 0: #couldn't find the right degree, just using first one
            try:
                return datetime.now().year-int(educations[0]['end_year']) + 21
            except:
                return 0
        return ''
    def getLocation(self):
        try:
            return locationToJson(self.soup.find('div', {'class':'adr y4'}).text)
        except:
            pass
    def getCountry(self):
        return locationToCountry(self.getLocation())
    def getPersonalLinkedin(self):
        try:
            return return_url_end([a['href'] for a in self.soup.findAll('a', {'class':'OLa url Xvc'}) if 'linkedin' in a['href'].lower()][0])
        except:
            return ''
    def getPersonalTwitter(self):
        try:
            return return_url_end([a['href'] for a in self.soup.findAll('a', {'class':'OLa url Xvc'}) if 'twitter' in a['href'].lower()][0])
        except:
            return ''
    def getPersonalHomePage(self):
        try:
            d = self.soup.find('div', {'class':'wna fa-TCa Ala'})
            return return_url_end(d.findChildren('a', {'class':'OLa url Xvc'})[0]['href'], middle = True).lower()
        except Exception as e:
            pass
        try:
            d = self.soup.find('div', {'class':'wna fa-UCa Ala'})
            return return_url_end(d.findChildren('a', {'class':'OLa url Xvc'})[0]['href'], middle = True).lower()
        except Exception as e:
            pass
        return ''
    def getInfo(self, type_of_info = ''):
        if type_of_info == 'name':
            return self.getName()
        if type_of_info == 'positions':
            return self.getPositions()
        elif type_of_info == 'photo':
            return self.getPhoto()
        elif type_of_info == 'education':
            return self.getEducation()
        elif type_of_info == 'location':
            return self.getLocation()
        elif type_of_info == 'country':
            return self.getCountry()
        elif type_of_info == 'interests':
            return self.getInterests()
        else:
            return ''
    def getMedia(self, type_of_media = ''):
        if type_of_media == 'personal_twitter':
            return self.getPersonalTwitter()
        elif type_of_media == 'personal_linkedin':
            return self.getPersonalLinkedin()
        elif type_of_media == 'personal_home_page':
            return self.getPersonalHomePage()
        else:
            return ''

def createAPI():
    credentials = requests.get('http://legionanalytics.com/getRandomAPICredentials?social_media=twitter').json()
    consumer_key = credentials['api_key']
    consumer_secret = credentials['api_secret']
    access_token = credentials['access_token']
    access_token_secret = credentials['access_secret']
    # OAuth process, using the keys and tokens
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth, wait_on_rate_limit = True, wait_on_rate_limit_notify = True)
    return api


class personalTwitterScraper():
    def __init__(self, handle='', data = None):
        self.handle = handle
        if data:
            self.data = data
        else:
            api = createAPI()
            self.data = api.get_user(handle)
    def getFollowerCount(self):
        try:
            return self.data.followers_count
        except:
            return -1
    def getFollowingCount(self):
        try:
            return self.data.friends_count
        except:
            return -1
    def getPositions(self):
        pos = []
        try:
            string_ = self.getBio()
            for thing in [':']:
                string_.replace(thing, '')
            position_re = re.compile('(([a-z]?[A-Z][\w\-\:]+ ?)+)((: )|(at )|(at the )|(of )|(of the ))?@([\w\-]+)')
            for a in re.finditer(position_re, string_):
                pos.append({'position_title':a.group(1).strip(),'is_active':True, 'company_dict':{'web_presence':{'company_twitter':{'url':a.group(9).strip().lower()}}}})
            position_re = re.compile('(([a-z]?[A-Z][\w\-]+ ?)+)((: )|(at )|(at the )|(of )|(of the ))(([a-z]?[A-Z][\w\-]+ ?)+)')
            for a in re.finditer(position_re, string_):
                pos.append({'position_title':a.group(1).strip(),'is_active':True, 'company_dict':{'name':a.group(9).strip()}})
        except:
            pass
        return pos
    def getVerified(self):
        try:
            return self.data.verified
        except:
            return False
    def getName(self):
        try:
            return self.data.name
        except:
            return ''
    def getLocation(self):
        try:
            return locationToJson(self.data.location)
        except:
            pass
        return None
    def getCountry(self):
        return locationToCountry(self.getLocation())
    def getBio(self):
        try:
            return self.data.description
        except:
            return ''
    def getPhoto(self):
        try:
            ph = self.data.profile_image_url_https
            ph = ph.replace("_normal",'')
            return ph
        except:
            pass
    def getKloutScore(self):
        try:
            kloutId = k.identity.klout(screenName=self.handle).get('id')
            return int(k.user.score(kloutId = kloutId, timeout=10).get('score'))
        except Exception as e:
            return None
    def getPersonalHomePage(self):
        try:
            return return_url_end(self.data.entities['url']['urls'][0]['expanded_url'], middle=True)
        except:
            pass
        try:
            return return_url_end(self.data.url, middle=True)
        except:
            pass
    def getMedia(self, type_of_media = ''):
        if type_of_media == 'personal_home_page':
            return self.getPersonalHomePage()
        elif type_of_media == 'company_home_page':
            return self.getPersonalHomePage()
        else:
            return ''
    def getInfo(self, type_of_info = ''):
        if type_of_info == 'name':
            return self.getName()
        elif type_of_info == 'photo':
            return self.getPhoto()
        elif type_of_info == 'location':
            return self.getLocation()
        elif type_of_info == 'country':
            return self.getCountry()
        elif type_of_info == 'klout_score':
            return self.getKloutScore()
        elif type_of_info == 'twitter_verified':
            return self.getVerified()
        elif type_of_info == 'twitter_followers':
            return self.getFollowerCount()
        elif type_of_info == 'bio':
            return self.getBio()
        elif type_of_info == 'twitter_bio':
            return self.getBio()
        elif type_of_info == 'positions':
            return self.getPositions()
        else:
            return ''

class companyAngellistScraper():
    def __init__(self, handle):
        self.handle = handle
        self.soup = BeautifulSoup(getHTMLForUrl('https://angel.co/'+handle))
    def getName(self):
        try:
            return self.soup.find('h1', {'class':'name'}).text
        except:
            return ''
    def getFounders(self):
        try:
            founders =  [return_url_end(a['href']) for a in self.soup.find('div', {'class':'founders section'}).findChildren('a',{'class':'profile-link'})][0::2]
            positions = [a.text for a in self.soup.find('div', {'class':'founders section'}).findChildren('div',{'class':'role_title'})]
            names = [a.text for a in self.soup.find('div', {'class':'founders section'}).findChildren('a',{'class':'profile-link'})][1::2]
            return [{'name':n, 'positions':[{'position_title':p, 'company_dict':{'web_presence':{'company_angellist':{'url':self.handle}}}}], 'web_presence':{'personal_angellist':{'url':f}}} for f, p, n in zip(founders, positions, names)]
        except:
            return []
    def getLocation(self):
        try:
            return locationToJson([a.text for a in self.soup.find('div', {'class':"tags"}).findChildren()][0])
        except:
            pass
    def getCountry(self):
        return locationToCountry(self.getLocation())
    def getIndustries(self):
        try:
            return [a.text for a in self.soup.find('div', {'class':"tags"}).findChildren()][1:]
        except:
            return []
    def getCompanyTwitter(self):
        try:
            return return_url_end(self.soup.find('a', {'class':re.compile('twitter')})['href'])
        except:
            return ''
    def getCompanyHomePage(self):
        try:
            return return_url_end(self.soup.find('a', {'class':re.compile('company_url')})['href'], middle=True)
        except:
            return ''
    def getCompanyCrunchbase(self):
        try:
            return return_url_end(self.soup.find('a', {'class':re.compile('crunchbase')})['href'])
        except:
            return ''
    def getCompanyLinkedin(self):
        try:
            return return_url_end(self.soup.find('a', {'class':re.compile('linkedin')})['href'])
        except:
            return ''
    def getCompanyFacebook(self):
        try:
            return return_url_end(self.soup.find('a', {'class':re.compile('facebook')})['href'])
        except:
            return ''
    def getFunding(self):
        try:
            return sum([float(a.text.replace('$','').replace(',','')) for a in self.soup.findAll('div', {'class':'raised'})])
        except Exception as e:
            return 0
    def getMedia(self, type_of_media = ''):
        if type_of_media == 'company_facebook':
            return self.getCompanyFacebook()
        elif type_of_media == 'company_twitter':
            return self.getCompanyTwitter()
        elif type_of_media == 'company_facebook':
            return self.getCompanyFacebook()
        elif type_of_media == 'company_linkedin':
            return self.getCompanyLinkedin()
        elif type_of_media == 'company_crunchbase':
            return self.getCompanyCrunchbase()
        elif type_of_media == 'company_home_page':
            return self.getCompanyHomePage()
        else:
            return ''
    def getInfo(self, type_of_info = ''):
        if type_of_info == 'name':
            return self.getName()
        elif type_of_info == 'location':
            return self.getLocation()
        elif type_of_info == 'country':
            return self.getCountry()
        elif type_of_info == 'industries':
            return self.getIndustries()
        elif type_of_info == 'funding':
            return self.getFunding()
        else:
            return ''


class conspireScraper():
    def __init__(self, conspire_id):
        self.soup = BeautifulSoup(getHTMLForUrl('https://www.conspire.com/profiles/'+str(conspire_id)))
    def getPerson(self):
        profiles = [l.findChild('a')['href'].lower() for l in self.soup.findAll('li', {'class':'c_social_profile'})]
        person = {'web_presence':{}}
        for p in profiles:
            if 'twitter' in p.lower():
                person['web_presence']['personal_twitter'] = {'url':p.split('/')[-1].lower()}
            elif 'facebook' in p.lower():
                person['web_presence']['personal_facebook'] = {'url':p.split('/')[-1].lower()}
            elif 'angel' in p.lower():
                person['web_presence']['personal_angellist'] = {'url':p.split('/')[-1].lower()}
            elif 'linkedin' in p.lower():
                person['web_presence']['personal_linkedin'] = {'url':p.split('linkedin.com/')[-1].lower()}
                if 'pub/' not in person['web_presence']['personal_linkedin']['url'] and 'in/' not in person['web_presence']['personal_linkedin']['url']:
                    person['web_presence']['personal_linkedin']['url'] = 'in/'+person['web_presence']['personal_linkedin']['url']
        return person


class personalAngellistScraper():
    def __init__(self, handle):
        self.soup = BeautifulSoup(getHTMLForUrl('https://angel.co/'+handle))
    def getName(self):
        try:
            return self.soup.find('span', {'itemprop':'name'}).text
        except:
            return ''
    def getPersonalFacebook(self):
        try:
            return return_url_end(self.soup.find('a', {'class':re.compile('facebook')})['href'])
        except:
            return ''
    def getPhoto(self):
        try:
            return self.soup.find('img', {'class':'avatar_img'})['src']
        except:
            pass
    def getLocation(self):
        try:
            return locationToJson(self.soup.find('span', {'itemprop':'locality'}).text)
        except:
            pass
    def getCountry(self):
        return locationToCountry(self.getLocation())
    def getInterests(self):
        try:
            return [a.text for a in self.soup.findAll('span', {'class':'tag'})][1:]
        except:
            return []
    def getPersonalCrunchbase(self):
        try:
            return return_url_end(self.soup.find('a', {'class':re.compile('crunchbase')})['href'])
        except:
            return ''
    def getPersonalTwitter(self):
        try:
            return return_url_end(self.soup.find('a', {'class':re.compile('twitter')})['href']).replace('#!/','').replace('@','')
        except:
            return ''
    def getPersonalGithub(self):
        try:
            return return_url_end(self.soup.find('a', {'class':re.compile('github')})['href'])
        except:
            return ''
    def getPersonalHomePage(self):
        try:
            return return_url_end(self.soup.find('a', {'class':'link_el'})['href'], middle=True)
        except:
            return ''
    def getPersonalLinkedin(self):
        try:
            return return_url_end(self.soup.find('a', {'class':re.compile('linkedin')})['href'])
        except:
            return ''
    def getPositions(self):
        positions = []
        for div in self.soup.findAll('div', {'data-_tn':'startup_roles/experience'}):
            try:
                positions.append({'position_title':div.findChild('div', {'class':'role_title'}).text, 'company_dict':{'name':div.findChild('a', {'class':'startup-link'})['title'], 'web_presence':{'company_angellist':{'url':div.findChild('a', {'class':'startup-link'})['href'].replace('https://','')}}}})
            except:
                pass
        return positions
    def getMedia(self, type_of_media = ''):
        if type_of_media == 'personal_facebook':
            return self.getPersonalFacebook()
        elif type_of_media == 'personal_twitter':
            return self.getPersonalTwitter()
        elif type_of_media == 'personal_crunchbase':
            return self.getPersonalCrunchbase()
        elif type_of_media == 'personal_linkedin':
            return self.getPersonalLinkedin()
        elif type_of_media == 'personal_github':
            return self.getPersonalGithub()
        elif type_of_media == 'personal_home_page':
            return self.getPersonalHomePage()
        else:
            return ''
    def getInfo(self, type_of_info = ''):
        if type_of_info == 'name':
            return self.getName()
        elif type_of_info == 'photo':
            return self.getPhoto()
        elif type_of_info == 'location':
            return self.getLocation()
        elif type_of_info == 'country':
            return self.getCountry()
        elif type_of_info == 'interests':
            return self.getInterests()
        elif type_of_info == 'positions':
            return self.getPositions()
        else:
            return ''
  
class personalFacebookScraper():
    def __init__(self, url):
        self.soup = BeautifulSoup(getHTMLForUrl('https://facebook.com/'+url))
    def getPersonalTwitter(self):
        try:
            return link
        except:
            return ''
    def getPersonalHomePage(self):
        try:
            return re.search(re.compile('id="u_0_[p|q|n]"&gt;http://(www.)?(.*)/&lt;'), self.soup.prettify()).group(2)
        except Exception as e:
            return ''
    def getPersonalLinkedin(self):
        try:
            return link
        except:
            return ''
    def getVerified(self):
        try:
            return '"__html":"Verified Page"' in self.soup.prettify()
        except:
            return False
    def getPersonalAngelList(self):
        try:
            return link
        except:
            return ''
    def getPersonalWikipedia(self):
        try:
            return link
        except:
            return ''
    def getName(self):
        try:
            return self.soup.title.text.split(' | ')[0]
        except Exception as e:
            return ''
    def getPersonalCrunchbase(self):
        try:
            return link
        except:
            return ''
    def getMedia(self, type_of_media = ''):
        if type_of_media == 'personal_facebook':
            return self.getPersonalFacebook()
        elif type_of_media == 'personal_twitter':
            return self.getPersonalTwitter()
        elif type_of_media == 'personal_angellist':
            return self.getPersonalAngelList()
        elif type_of_media == 'personal_home_page':
            return self.getPersonalHomePage()
        elif type_of_media == 'company_home_page':
            return self.getPersonalHomePage()
        elif type_of_media == 'personal_crunchbase':
            return self.getPersonalCrunchbase()
        elif type_of_media == 'personal_wikipedia':
            return self.getPersonalWikipedia()
        elif type_of_media == 'personal_linkedin':
            return self.getPersonalLinkedin()
        else:
            return ''
    def getInfo(self, type_of_info = ''):
        if type_of_info == 'name':
            return self.getName()
        elif type_of_info == 'facebook_verified':
            return self.getVerified()
        return ''


class companyCrunchbaseScraper():
    def __init__(self, handle):
        try:
            self.handle = handle
            self.soup = BeautifulSoup(getHTMLForUrl('http://crunchbase.com/organization/'+handle, anon='4', king_only = True))
        except Exception as e:
            self.soup = BeautifulSoup('')
    def getIndustry(self):
        try:
            for d in self.soup.findAll('dd'):
                if  d.findChild('a') and 'category' in d.findChild('a').get('href', ''):
                    return d.text.split(',')
        except Exception as e:
            return []
    def getHostOfEmail(self): #the part including and the @
        try:
            to_return = self.soup.find('span', {'class':'email'}).text.split('@')[1]
        except Exception as e:
            to_return = ''
        return to_return
    def getEmployees(self):
        people = []
        try:
            employees = self.soup.findAll('div', {'class':'info-block'})
            for e in employees:
                try:
                    if 'person' in e.findChild('a')['href']:
                        person_dict = {'name':e.findChild('a').text, 'positions':[{'is_active':True, 'position_title':e.findChild('h5').text, 'company_dict':{'web_presence':{'company_crunchbase':{'url':self.handle}}, 'name':self.getName()}}], 'web_presence':{'personal_crunchbase':{'url':e.findChild('a')['href'][8:]}}}
                        if '@' not in e.findChild('h5').text and '#' not in e.findChild('h5').text and e.findChild('a').text not in [p['name'] for p in people]:
                            people.append(person_dict)
                except Exception as q:
                    pass
        except Exception as e:
            print e
        return people
    def getNumEmployees(self):
        try:
            min_, max_ = self.soup.findAll('dd')[-1].text.replace('k','000').replace(' ','').split('|')[0].split('-')
            return int((float(min_)+float(max_))/2.)
        except Exception as e:
            return 0
    def getName(self):
        try:
            return self.soup.title.text.split(' | ')[0]
        except:
            return ''
    def getCompanyHomePage(self):
        try:
            return _cleanURL(self.soup.find('a', {'title':'homepage'})['href']).replace('http://','')
        except Exception as e:
            print e
        return ''
    def getCompanyFacebook(self):
        try:
            return self.soup.find('a', {'title':'facebook'})['href'].split('/')[-1]
        except Exception as e:
            return ''
    def getCompanyTwitter(self):
        try:
            return self.soup.find('a', {'title':'twitter'})['href'].split('/')[-1]
        except Exception as e:
            print e
            return ''
    def getCompanyLinkedin(self):
        try:
            return re.match(website_regex, self.soup.find('a', {'title':'linkedin'})['href']).group(5)[1:]
        except:
            return ''
    def getCompanyAngelList(self):
        try:
            return self.soup.find('a', {'title':'angellist'})['href'].split('/')[-1]
        except:
            return ''
    #return the total money raised from the crunchbase page
    def getFunding(self):
        total_money_raised = 0
        try:
            mult = 1
            money = self.soup.find('span', {'class':'funding_amount'}).text.replace('$','').replace(' ','')
            if "Thousand" in money:
                mult = 1000.
                money = money.replace('Thousand','')
            elif "Million" in money:
                mult = 1000000.
                money = money.replace('Million','')
            elif "Billion" in money:
                mult = 1000000000.
                money = money.replace('Billion','')
            return float(money)*mult
        except:
            return 0
    def getRevenue(self):
        try:
            return self.getNumEmployees() * 50000
        except:
            return 0
    def getLocation(self):
        try:
            for d in self.soup.findAll('dd'):
                if  d.findChild('a') and 'location' in d.findChild('a').get('href', ''):
                    return locationToJson(d.text)
        except:
            pass
    def getCountry(self):
        return locationToCountry(self.getLocation())
    def getInfo(self, type_of_info = ''):
        if type_of_info == 'name':
            return self.getName()
        elif type_of_info == 'email_host':
            return self.getHostOfEmail()
        elif type_of_info == 'location':
            return self.getLocation()
        elif type_of_info == 'country':
            return self.getCountry()
        elif type_of_info == 'industries':
            return self.getIndustry()
        elif type_of_info == 'number_of_employees':
            return self.getNumEmployees()
        elif type_of_info == 'funding':
            return self.getFunding()
        elif type_of_info == 'revenue':
            return self.getRevenue()
        else:
            return ''
    def getMedia(self, type_of_media = ''):
        if type_of_media == 'company_facebook':
            return self.getCompanyFacebook()
        elif type_of_media == 'company_twitter':
            return self.getCompanyTwitter()
        elif type_of_media == 'company_angellist':
            return self.getCompanyAngelList()
        elif type_of_media == 'company_home_page':
            return self.getCompanyHomePage()
        elif type_of_media == 'company_linkedin':
            return self.getCompanyLinkedin()
        else:
            return ''

# MUST TEST
class personalCrunchbaseScraper():
    def __init__(self, handle):
        self.handle = handle
        try:
            self.soup = BeautifulSoup(getHTMLForUrl('http://www.crunchbase.com/person/'+handle, anon='4', king_only = True))
        except Exception as e:
            self.soup = BeautifulSoup('')
    def getIndustry(self):
        try:
            for d in self.soup.findAll('dd'):
                if  d.findChild('a') and 'category' in d.findChild('a').get('href', ''):
                    return d.text.split(',')
        except Exception as e:
            return []
    def getHostOfEmail(self): #the part including and the @
        try:
            to_return = self.soup.find('span', {'class':'email'}).text.split('@')[1]
        except Exception as e:
            to_return = ''
        return to_return
    def getPhoto(self):
        try:
            return self.soup.find('img', {'class':'entity-info-card-primary-image'})['src']
        except:
            return ''
    def getName(self):
        try:
            return self.soup.find('a', {'href':'/person/'+self.handle}).text
        except:
            return ''
    def getPersonalHomePage(self):
        try:
            return _cleanURL(self.soup.find('a', {'title':'homepage'})['href']).replace('http://','')
        except Exception as e:
            pass
        return ''
    def getPersonalFacebook(self):
        try:
            return self.soup.find('a', {'title':'facebook'})['href'].split('/')[-1]
        except Exception as e:
            return ''
    def getPersonalTwitter(self):
        try:
            return self.soup.find('a', {'title':'twitter'})['href'].split('/')[-1]
        except:
            return ''
    def getPersonalLinkedin(self):
        try:
            return re.match(website_regex, self.soup.find('a', {'title':'linkedin'})['href']).group(5)[1:]
        except:
            return ''
    def getPersonalAngelList(self):
        try:
            return self.soup.find('a', {'title':'angellist'})['href'].split('/')[-1]
        except:
            return ''
    def getPositions(self):
        pos = []
        for d in self.soup.findAll('div', {'class':'current_job'}):
            p = {}
            c = d.findChild('div', {'class':'info-block'})
            p['position_title'] = c.findChild('h4').text
            p['company_dict'] = {'name': c.findChild('a').text, 'is_active':True, 'web_presence':{'company_crunchbase':{'url':c.findChild('a')['href'][1:]}}}
            pos.append(p)
        return locationToJson(pos)
    def getInfo(self, type_of_info = ''):
        if type_of_info == 'name':
            return self.getName()
        elif type_of_info == 'industries':
            return self.getIndustry()
        elif type_of_info == 'photo':
            return self.getPhoto()
        elif type_of_info == 'positions':
            return self.getPositions()
        else:
            return ''
    def getMedia(self, type_of_media = ''):
        if type_of_media == 'personal_facebook':
            return self.getPersonalFacebook()
        elif type_of_media == 'personal_twitter':
            return self.getPersonalTwitter()
        elif type_of_media == 'personal_angellist':
            return self.getPersonalAngelList()
        elif type_of_media == 'personal_home_page':
            return self.getPersonalHomePage()
        elif type_of_media == 'personal_linkedin':
            return self.getPersonalLinkedin()
        else:
            return ''
      
class personalGithubScraper():
    def __init__(self, handle = ''):
        self.soup = BeautifulSoup(getHTMLForUrl('http://github.com/'+handle))
    def getPhoto(self):
        try:
            return self.soup.find('img', {'class':'avatar'})['src']
        except:
            return ''
    def getLocation(self):
        try:
            return locationToJson(self.soup.find('li', {'itemprop':'homeLocation'}).text)
        except:
            pass
    def getCountry(self):
        return locationToCountry(self.getLocation())
    def getAffiliation(self):
        try:
            return self.soup.find('li', {'itemprop':'worksFor'}).text
        except:
            return ''
    def getName(self):
        try:
            return self.soup.find('span', {'class':'vcard-fullname'}).text
        except:
            return ''
    def getEmail(self):
        try:
            return self.soup.find('a', {'class':'email'})['href'].replace('mailto:','')
        except:
            return ''
    def getPersonalHomePage(self):
        try:
            return return_url_end(self.soup.find('a', {'class':'url'}).text, middle  = True)
        except:
            return ''
    def getInfo(self, type_of_info = ''):
        if type_of_info == 'name':
            return self.getName()
        elif type_of_info == 'location':
            return self.getLocation()
        elif type_of_info == 'country':
            return self.getCountry()
        elif type_of_info == 'photo':
            return self.getPhoto()
        elif type_of_info == 'personal_email':
            return self.getEmail()
        else:
            return ''
    def getMedia(self, type_of_media):
        if type_of_media == 'personal_home_page':
            return self.getPersonalHomePage()
        else:
            return ''


class privatePersonalLinkedinScraper():
    def __init__(self, handle = '', cookies = None):
        self.handle = handle
        if cookies or "profile/view" in handle:
            cookies = 'linkedin'
        if '/dir/' in handle:
            self.soup = BeautifulSoup('')
        else:
            self.soup = BeautifulSoup(getHTMLForUrl("http://www.linkedin.com/"+handle, cookies = cookies))
    def getPublicHandle(self):
        try:
            return return_url_end(self.soup.find('a', {'class':"view-public-profile"})['href'])
        except Exception as e:
            pass
        return ''
    def getPhoto(self):
        photo = ''
        try:
            photo = self.soup.find('div', attrs={'id':'profile-picture'}).findChildren()[0]['src']
        except:
            pass
        try:
            photo = self.soup.find('div', attrs={'class':'profile-picture'}).find('img')['src']
        except:
            pass
        return photo
    def getPositions(self):
        positions = []
        for p in self.soup.findAll('div'):
            if p.has_key('class') and 'position' in p['class'] and 'experience' in p['class']:
                position  = {}
                try:
                    company_url = p.find('a', attrs={'class':"company-profile-public"})['href'][:-15]
                    position['company_dict'] =  {'name':p.findAll('span')[1].text}
                    if 'company/' in company_url:
                        position['company_dict']['web_presence'] = {'company_linkedin':{'url':company_url}}
                except Exception as e:
                    pass
                try:
                    position['position_title'] = p.find('span').text
                except:
                    pass
                try:
                    text =  p.find('p').text
                    m = re.search(re.compile('(.*) industry'), text)
                    position['company_dict']['industries'] = [m.group(1)]
                except Exception as e:
                    pass
                try:
                    text =  p.findAll('p')[-1].text
                    text = text.replace("'", "")
                    text = text.replace('"', '')
                    text = text.replace(",", "")
                    #position['summary'] = text
                except Exception as e:
                    pass
                try:
                    position['start_month'], position['start_year'] = p.find('abbr').text.split(' ')
                except Exception as e:
                    pass
                try:
                    position['start_month'], position['start_year'] = p.find('abbr').text.split(' ')
                except Exception as e:
                    pass
                try:
                    end = p.findAll('abbr')[1].text
                    if end.lower() == 'present':
                        position['is_active'] = True
                    else:
                        position['is_active'] = False
                        position['end_month'], position['end_year'] = p.findAll('abbr')[1].text.split(' ')
                except Exception as e:
                    pass
                if len(position.keys()):
                    positions.append(position)
            elif p.has_key("id") and 'experience' in p['id'] and "container" not in p['id']:
                position = {}
                if re.match(re.compile('experience-[\d]+-view'), p['id']):
                    try:
                        a = p.findChild('a', href=re.compile('company/\w+'))
                        company_url = 'company/'+return_url_end(a['href'])
                    except:
                        company_url = ''
                    try:
                        position['position_title'] = p.find('h4').text
                        for pot in p.findAll('h5'):
                            if pot.text != '':
                                c_name = pot.text
                    except Exception as e:
                        pass
                    position['company_dict'] =  {'name':c_name}
                    if len(company_url) and 'company/' in company_url:
                        position['company_dict']['web_presence'] = {'company_linkedin':{'url': return_url_end(company_url)}}
                    elif 'company/' in p.findChild('a')['href']:
                        position['company_dict']['web_presence'] = {'company_linkedin':{'url': return_url_end(p.findChild('a')['href'])}}
                    times = p.findAll('time')
                    try:
                        if len(times) <= 1:
                            position['is_active'] = True
                            if len(times[0].text.split(' '))>1:
                                position['start_month'], position['start_year'] =times[0].text.split(' ')
                            else:
                                position['start_year'] = times[0].text
                        else:
                            if len(times[0].text.split(' '))>1:
                                position['start_month'], position['start_year'] =times[0].text.split(' ')
                            else:
                                position['start_year'] = times[0].text
                            position['is_active'] = False
                            if len(times[1].text.split(' '))>1:
                                position['end_month'], position['end_year'] =times[1].text.split(' ')
                            else:
                                position['end_year'] = times[1].text
                    except:
                        pass
                if len(position.keys()):
                    positions.append(position)
        return positions
    def getName(self):
        name = ''
        #returns firstname lastname
        try:
            name = self.soup.find('span', attrs={'class':'given-name'}).text + ' ' + self.soup.find('span', attrs={'class':'family-name'}).text
        except:
            pass
        if len(name):
            return name
        try:
            name = self.soup.find('span', attrs={'class':'full-name'}).text
        except:
            pass
        return name
        return ''
    def getLocation(self):
        try:
            return locationToJson(self.soup.find('span', attrs={'class':'locality'}).text)
        except:
            pass
        return ''
    def getCountry(self):
        return locationToCountry(self.getLocation())
    def getEmailsOnSite(self):
        #returns location of person
        try:
            emails = [a[1]+'@'+a[5]+'.'+a[9] for a in re.findall(SIMPLE_EMAIL_REGEX, self.soup.prettify())]
            return [e.lower() for e in emails]
        except Exception as e:
            pass
        return ''
    def getIndustries(self):
        #returns industry
        industry = ''
        try:
            industry = self.soup.find('dd', attrs={'class':'industry'}).text
        except:
            pass
        return industry
    def getPersonalTwitter(self):
        #returns url of twitter
        pass
    def getEducation(self):
        #returns [{schoo_name]
        educations = []
        for e in self.soup.findAll('div'):
            if e.has_key('class') and 'position' in e['class'] and 'education' in e['class']:
                education = {}
                try:
                    education['school_name'] = e.find('a').text
                except:
                    pass
                try:
                    education['start_year'] = e.find('abbr').text
                    education['end_year'] = e.findAll('abbr')[1].text
                except:
                    pass
                try:
                    education['fields_of_study'] = e.find('span', attrs={'class':"major"}).text.split(', ')
                except:
                    pass
                try:
                    education['degree'] = e.find('span', attrs={'class':"degree"}).text
                except:
                    pass
                if len(education.keys()):
                    educations.append(education)
            elif e.has_key('id') and re.match(re.compile('education-[\d]+-view'), e['id']):
                education = {}
                try:
                    education['school_name'] = e.findAll('a')[1].text
                except:
                    pass
                try:
                    education['degree'] = e.find('span', attrs={'class':'degree'}).text[:-1]
                except:
                    pass
                try:
                    field = e.find('span', attrs={'class':'major'})
                    education['fields_of_study'] = [f.text for f in field.findAll('a')]
                except:
                    pass
                times = e.findAll('time')
                try:
                    if len(times) == 1:
                        education['start_year'] =times[0].text.split(' ')[1]
                    else:
                        education['start_year'], education['end_year'] =  times[0].text.split(' ')[0], times[1].text.split(' ')[1]
                    if len(education.keys()):
                        educations.append(education)
                except Exception as e:
                    pass
        return educations
    def getAge(self):
        #returns int of age
        educations = self.getEducation()
        for e in educations:
            try:
                if 'ba' in e['degree'].lower() or 'bs' in e['degree'].lower() or 'b.s' in e['degree'].lower() or 'b.a' in e['degree'].lower() or "bachelor" in e['degree'].lower():
                    return datetime.now().year-int(e['end_year']) + 21
            except:
                continue
        if len(educations) > 0: #couldn't find the right degree, just using first one
            try:
                return datetime.now().year-int(educations[0]['end_year']) + 21
            except:
                return 0
        return ''
    def getPersonalHomePage(self):
        #returns link of home page
        try:
            link = self.soup.find('dd', attrs={'class':'websites'}).find('a')['href']
            m = re.search(re.compile('\/redir\/redirect\?url=(.*)\&urlhash='), link)
            link = m.group(1)
            link = link.replace('%3A', ':')
            link = link.replace('%2F', '/')
            link = link.replace('%2E', '.')
            return link
        except:
            pass
        return ''
    def getNumConnections(self):
        #returns number of connections
        try:
            text = self.soup.find('dd', attrs={'class':'overview-connections'}).text
            return text[0:text.find('connections')]
        except:
            pass
        return ''
    def getInterests(self):
        #returns names of all endorsements
        industries = []
        try:
            industries +=[s.text for s in self.soup.findAll('span', attrs={'class':'jellybean'})]
        except:
            pass
        try:
            industries += [a.text for a in self.soup.findAll('span', attrs={'class':'endorse-item-name-text'})]
        except:
            pass
        try:
            industries += [a.text for a in self.soup.findAll('span', attrs={'class':'endorse-item-name'})]
        except:
            pass
        return list(set([i.replace('...','') for i in industries]))
    def getBio(self):
        try:
            return self.soup.find('p', {"class":"description"}).text
        except:
            return ''
    def getMedia(self, type_of_media = ''):
        if type_of_media == 'personal_twitter':
            return self.getPersonalTwitter()
        elif type_of_media == 'personal_home_page':
            return self.getPersonalHomePage()
        else:
            return ''
    def getInfo(self, type_of_info = ''):
        if type_of_info == 'name':
            return self.getName()
        elif type_of_info == 'photo':
            return self.getPhoto()
        elif type_of_info == 'age':
            return self.getAge()
        elif type_of_info == 'personal_email':
            return self.getEmail()
        elif type_of_info == 'education':
            return self.getEducation()
        elif type_of_info == 'positions':
            return self.getPositions()
        elif type_of_info == 'location':
            return self.getLocation()
        elif type_of_info == 'country':
            return self.getCountry()
        elif type_of_info == 'interests':
            return self.getInterests()
        elif type_of_info == 'industry':
            return self.getIndustries()
        elif type_of_info == 'bio':
            return self.getBio()
        elif type_of_info == 'linkedin_bio':
            return self.getBio()
        else:
            return ''

class emailVerifier():
    def __init__(self, email):
        self.email = email.lower()
        self.kick_box_response = {}
    def getKBMetrics(self):   
        metrics = kb_lounge.validateEmail(self.email, vrfy_hard = True)
        return metrics, metrics['validity']
    def agreesWithKickbox(self):
        return self.getKBMetrics()[1] == 'Valid'
    def _emailAgreesWithBing(self):
        b = bingScraper()
        results = b.search(query = '"'+self.email+'"')
        for result in results:
            if self.email.lower() in result['summary'].lower() and sum([a in result['link'] for a in bad_sites]) == 0:
                return True
        return False
    def _emailAgreesWithYahooBoss(self):
        y = YahooBoss()
        results = y.search(q = '"'+self.email+'"')
        for result in results:

            if self.email.lower() in result['summary'].lower() and sum([a in result['link'] for a in bad_sites]) == 0:
                return True
        return False
    def _emailAgreesWithGoogle(self):
        g = googleScraper()
        results = g.search(query = '"'+self.email+'"').get('results', [])
        for result in results:
            if sum([b in result['link'].lower() for b in bad_sites]) > 0:
                continue
            if self.email in result['summary'].lower():
                return True
        return False
    def validate(self):
        if not self.email:
            return False
        kb_response = self.getKBMetrics()[1]
        if kb_response == 'Invalid':
            return False
        elif kb_response == 'Valid':
            return True
        #otherwise it is unknown
        return self._emailAgreesWithGoogle() # or self._emailAgreesWithYahooBoss() or self._emailAgreesWithBing()

class personalClearbitScraper():
    def __init__(self, email):
        try:
            self.profile = clearbit.Person.find(email=email)
        except:
            self.profile = {}
    def isValid(self):
        try:
            if self.profile is not None and 'pending' not in self.profile.keys():
                return True
        except:
            return False
        return False
    def getName(self):
        try:
            return self.profile['name']['fullName']
        except:
            return ''
    def getPersonalTwitter(self):
        try:
            return self.profile['twitter']['handle'].replace('@','').lower()
        except:
            return ''
    def getPersonalGithub(self):
        try:
            return self.profile['github']['handle'].lower()
        except:
            return ''
    def getPersonalFacebook(self):
        try:
            return self.profile['facebook']['handle'].lower()
        except:
            return ''
    def getPersonalLinkedin(self):
        try:
            return self.profile['linkedin']['handle'].lower()
        except:
            return ''
    def getPersonalAngelList(self):
        try:
            return self.profile['angellist']['handle'].lower()
        except:
            return ''
    def getPersonalHomePage(self):
        try:
            return return_url_end(self.profile['site'], middle=True).lower()
        except:
            return ''
    def getLocation(self):
        try:
            return locationToJson(self.profile['location'])
        except:
            return ''
    def getPhoto(self):
        try:
            return self.profile['avatar']
        except:
            return ''
    def getInfo(self, type_of_info = ''):
        if type_of_info == 'name':
            return self.getName()
        elif type_of_info == 'personal_email':
            return self.email
        elif type_of_info == 'photo':
            return self.getPhoto()
        elif type_of_info == 'location':
            return self.getLocation()
        else:
            return ''
    def getMedia(self, type_of_media = ''):
        if type_of_media == 'personal_facebook':
            return self.getPersonalFacebook()
        elif type_of_media == 'personal_twitter':
            return self.getPersonalTwitter()
        elif type_of_media == 'personal_github':
            return self.getPersonalGithub()
        elif type_of_media == 'personal_angellist':
            return self.getPersonalAngelList()
        elif type_of_media == 'personal_home_page':
            return self.getPersonalHomePage()
        elif type_of_media == 'personal_linkedin':
            return self.getPersonalLinkedin()
        else:
            return ''
            
# must input company website
class companyClearbitScraper():
    def __init__(self, email):
        self.profile = clearbit.Company.find(domain=email)
    def isValid(self):
        try:
            return self.profile['status'] == 200
        except:
            return False
    def getName(self):
        try:
            return self.profile['name']['fullName']
        except:
            return ''
    def getCompanyTwitter(self):
        try:
            return self.profile['twitter']['handle']
        except:
            return ''
    def getCompanyFacebook(self):
        try:
            return self.profile['facebook']['handle']
        except:
            return ''
    def getCompanyLinkedin(self):
        try:
            return self.profile['linkedin']['handle']
        except:
            return ''
    def getCompanyAngelList(self):
        try:
            return self.profile['angellist']['handle']
        except:
            return ''
    def getCompanyHomePage(self):
        try:
            return return_url_end(self.profile['site'], middle=True)
        except:
            return ''
    def getComapnyCrunchbase(self):
        try:
            return self.profile['crunchbase']['handle']
        except:
            return ''
    def getLocation(self):
        try:
            return locationToJson(self.profile['location'])
        except:
            return ''
    def getIndustry(self):
        try:
            return self.profile['categories']
        except:
            return []
    def getInfo(self, type_of_info = ''):
        if type_of_info == 'name':
            return self.getName()
        elif type_of_info == 'location':
            return self.getLocation()
        elif type_of_info == 'industries':
            return self.getIndustry()
        else:
            return ''
    def getMedia(self, type_of_media = ''):
        if type_of_media == 'company_facebook':
            return self.getCompanyFacebook()
        elif type_of_media == 'company_twitter':
            return self.getCompanyTwitter()
        elif type_of_media == 'company)crunchbase':
            return self.getCompanyCrunchbase()
        elif type_of_media == 'company_angellist':
            return self.getCompanyAngelList()
        elif type_of_media == 'company_home_page':
            return self.getCompanyHomePage()
        elif type_of_media == 'company_linkedin':
            return self.getCompanyLinkedin()
        else:
            return ''

class fullContactScraper():
    def __init__(self, email):
        self.email = email.strip().lower()
        try:
            r = requests.get("https://api.fullcontact.com/v2/person.json?email="+self.email+"&apiKey="+fullcontact_api_key)
            self.profile = r.json()
        except Exception as e:
            self.profile = {}
    def isValid(self):
        try:
            return self.profile['status'] == 200
        except:
            return False
    def getName(self):
        try:
            return self.profile['contactInfo']['fullName']
        except Exception as e:
            return ''
    def getLocation(self):
        try:
            return locationToJson(self.profile['demographics']['deducedLocation'])
        except Exception as e:
            return ''
    def getAge(self):
        try:
            return self.profile['demographics']['age']
        except Exception as e:
            return ''
    def getPersonalFacebook(self):
        try:
            return return_url_end([a['url'] for a in self.profile['socialProfiles'] if a['type'] == "facebook"][0])
        except Exception as e:
            return ''
    def getPersonalGithub(self):
        try:
            return [a['username'] for a in self.profile['socialProfiles'] if a['type'] == "github"][0]
        except Exception as e:
            return ''
    def getPersonalWikipedia(self):
        try:
            return [a['username'] for a in self.profile['socialProfiles'] if a['type'] == "wikipedia"][0]
        except Exception as e:
            return ''
    def getPersonalCrunchbase(self):
        try:
            return [a['username'] for a in self.profile['socialProfiles'] if a['type'] == "crunchbase"][0]
        except Exception as e:
            return ''
    def getPersonalLinkedin(self):
        try:
            return return_url_end([a['url'] for a in self.profile['socialProfiles'] if a['type'] == "linkedin"][0])
        except Exception as e:
            return ''
    def getPersonalTwitter(self):
        try:
            return [a['username'] for a in self.profile['socialProfiles'] if a['type'] == "twitter"][0].replace('@','')
        except Exception as e:
            return ''
    def getPersonalAngelList(self):
        try:
            return [a['username'] for a in self.profile['socialProfiles'] if a['type'] == "angellist"][0]
        except Exception as e:
            return ''
    def getPersonalHomePage(self):
        try:
            return return_url_end(self.profile['contactInfo']['websites'][0]['url'], middle=True)
        except Exception as e:
            return ''
    def getInfo(self, type_of_info = ''):
        if type_of_info == 'name':
            return self.getName()
        elif type_of_info == 'personal_email':
            return self.email
        elif type_of_info == 'location':
            return self.getLocation()
        elif type_of_info == 'age':
            return self.getAge()
        else:
            return ''
    def getMedia(self, type_of_media = ''):
        if type_of_media == 'personal_facebook':
            return self.getPersonalFacebook()
        elif type_of_media == 'personal_twitter':
            return self.getPersonalTwitter()
        elif type_of_media == 'personal_github':
            return self.getPersonalGithub()
        elif type_of_media == 'personal_angellist':
            return self.getPersonalAngelList()
        elif type_of_media == 'personal_home_page':
            return self.getPersonalHomePage()
        elif type_of_media == 'personal_crunchbase':
            return self.getPersonalCrunchbase()
        elif type_of_media == 'personal_wikipedia':
            return self.getPersonalWikipedia()
        elif type_of_media == 'personal_linkedin':
            return self.getPersonalLinkedin()
        else:
            return ''

class YahooBoss():
    def __init__(self):
        self.url = 'https://yboss.yahooapis.com/ysearch/web'
        self.key = 'dj0yJmk9QzIyMWxxaGVmSlZyJmQ9WVdrOVdXODNUVEkxTnpnbWNHbzlNQS0tJnM9Y29uc3VtZXJzZWNyZXQmeD0xYw--'
        self.secret = 'f2fc23925c67c2c2aed0d26b7228dbb2b8ca467f'
        self.params = {
            'oauth_version': "1.0",
            'format': 'json',
            'count':5
        }
        
    def search(self, q, site = ''):
        new_params = {
            'oauth_nonce': oauth.generate_nonce(),
            'oauth_timestamp': int(time.time()),
            'q' : urllib.quote_plus(q.strip())
        }
        if site:
            new_params['sites'] = site
        self.consumer = oauth.Consumer(key=self.key,secret=self.secret)
        self.signature_method = oauth.SignatureMethod_HMAC_SHA1()
        r_params = dict( self.params.items() + new_params.items())
        req = oauth.Request(method="GET",url=self.url,parameters=r_params)
        req.sign_request(self.signature_method, self.consumer, None)
        f = requests.get(req.to_url()).json()
        to_return = []
        if 'results' not in f['bossresponse']['web']:
            return []
        for result in f['bossresponse']['web']['results']:
            to_return.append({
                'link': result['url'],
                'name_of_link': result['title'],
                'summary': result['abstract']
                })
        return to_return

class googleScraper():
    def __init__(self):
        pass
    def search(self, query, include_fuzzy = False, current_index = 0):
        html = getHTMLForUrl('https://www.google.com/search?q='+'+'.join(query.split(' '))+'&start='+str(current_index), anon = '4', attempts_to_make = 20, king_only = True)
        time.sleep(random.choice(range(15)))
        if html and ('No results found for' not in html or include_fuzzy):
            self.soup = BeautifulSoup(html)
            try:
                return self.parseResults()
            except Exception as e:
                print "google search error", e
        return {'results':[]}
    def parseResults(self):
        results = []
        social_medias = defaultdict(list)
        for l in self.soup.findAll('li', attrs={'class':'g'})+self.soup.findAll('div', attrs={'class':'g'}):
            summary = l.text
            a = l.find('a')
            name_of_link = a.text.encode('ascii','ignore')
            link = a['href'].encode('ascii','ignore')
            link = link.replace('/url?q=','')
            if '&sa=U&' in link:
                link = link[:link.find('&sa=U&')]
            for media, list_of_potential in media_dict.iteritems():
                for value in list_of_potential:
                    if value in link and 'pub/dir' not in link and '/status/' not in link:
                        social_medias[media].append(link)
            results.append({'name_of_link':name_of_link, 'link':link, 'summary':summary})
        return {'results':results, 'social_medias': social_medias}
                    
class bingScraper():
    def __init__(self):
        pass
    def search(self, query):
        self.soup = BeautifulSoup(getHTMLForUrl('http://bing.com/search?q='+'+'.join(query.split(' '))))
        try:
            return {'results':self.parseResults()}
        except:
            return []
    def parseResults(self):
        to_return = []
        results = self.soup.findAll('li', attrs={'class':'b_algo'})
        if not len(results):
            return to_return
        for d in results:
            try:
                new_dict = {}
                new_dict['link'] = d.find('a')['href']
                new_dict['title'] = d.find('a').text.encode('ascii', 'ignore')
                new_dict['summary'] = d.find('p').text.encode('ascii', 'ignore')
                to_return.append(new_dict)
            except:
                pass
        return to_return        

class companyLinkedinScraper():
    def __init__(self, url = ''):
        try:
            self.soup = BeautifulSoup(getHTMLForUrl('http://www.linkedin.com/'+url, anon = '34', king_only = False))
        except:
            self.soup = BeautifulSoup('')
    def getIndustries(self): 
        try:
            return self.soup.find('li', attrs={'class':'industry'}).findChild('p').text.split(',')
        except:
            return []
    def getCompanyId(self):
        try:
            return re.findall('companyId=(\d+)', self.soup.prettify())[0]
        except Exception as e:
            return ''
    def getLocation(self):
        try:
            return locationToJson(' '.join([a.text for a in self.soup.find('li', attrs={'class':'vcard hq'}).findChild('p').findChildren()]))
        except:
            return {}
    def getCountry(self):
        return locationToCountry(self.getLocation())
    def getName(self):
        try:
            return self.soup.find('span', attrs={'itemprop':'name'}).text.split('|')[0].strip()
        except:
            return ''
    def getCompanyHomePage(self):
        try:
            return _cleanURL(self.soup.find('li', attrs={'class':'website'}).text.replace('Website','')).replace('http://','').split('/')[0]
        except Exception as e:
            return ''
    def getNumEmployees(self):
        try:
            employees = self.soup.find('li', attrs={'class':'company-size'}).findChild('p').text.replace('employees', '').replace('k','000').replace(' ','').replace(',','').split('|')[0].split('-')
            if '+' in employees[0]:
                return int(employees[0][:-1])
            min_, max_ = employees
            return int((float(min_)+float(max_))/2.)
        except Exception as e:
            return ''
    def getRevenue(self):
        try:
            return self.getNumEmployees() * 50000
        except:
            return 0
    def getBio(self):
        try:
            return self.soup.find('div', {'class':'basic-info-description'}).text
        except:
            return ''
    def getInfo(self, type_of_info = ''):
        if type_of_info == 'industries':
            return self.getIndustries()
        elif type_of_info == 'location':
            return self.getLocation()
        elif type_of_info == 'linkedin_bio':
            return self.getBio()
        elif type_of_info == 'country':
            return self.getCountry()
        elif type_of_info == 'name':
            return self.getName()
        elif type_of_info == 'number_of_employees':
            return self.getNumEmployees()
        elif type_of_info == 'revenue':
            return self.getRevenue()
    def getMedia(self, type_of_media = ''):
        if type_of_media == 'company_home_page':
            return self.getCompanyHomePage()

class WhoisGenerator():
    def __init__(self, url):
        self.url = _cleanURL(url).replace('http://', '')
    def networkSolutions(self, remove_bad = True):
        if self.url == '':
            return []
        try:
            html = getHTMLForUrl('http://www.networksolutions.com/whois/results.jsp?domain='+self.url, timeout = 8)
        except Exception as e:
            return []
        emails = list(set([a[0].lower() for a in re.findall(SIMPLE_EMAIL_REGEX, html)]))
        if remove_bad:
            emails = [e.lower() for e in emails if sum([b in e for b in bad_emails]) == 0]
        return emails
    def whoIsSearch(self, remove_bad = True):
        if self.url == '':
            return []
        try:
            html = getHTMLForUrl('http://www.whois-search.com/whois/'+self.url, timeout = 8)
        except:
            return []
        emails = list(set([a[0].lower() for a in re.findall(SIMPLE_EMAIL_REGEX, html)]))
        if remove_bad:
            emails = [e.lower() for e in emails if sum([b in e for b in bad_emails]) == 0]
        return emails
    def getEmails(self):
        found_emails = self.networkSolutions()
        if len(found_emails):
            return found_emails
        found_emails = self.whoIsSearch()
        if len(found_emails):
            return found_emails
        return []


def getLatestCrunchbase():
    soup = BeautifulSoup(getHTMLForUrl('http://www.crunchbase.com/funding-rounds', anon='4', king_only = True, timeout = 5, attempts_to_make = 20))
    companies = soup.findAll('div', {'class':'info-block'})
    c = []
    for e in companies:
        c.append({'web_presence':{'company_crunchbase':{'url':e.findChild('a')['href'][14:]}}, 'name':e.findChild('a')['title']})
    return c




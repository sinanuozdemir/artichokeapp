import master
import json
import datetime
import re
import tweepy
import unicodedata
from Legion import legion
import collections
import requests
from BeautifulSoup import BeautifulSoup
import scrapers
import urllib
from modules import getPerson

website_regex = re.compile('((https?://)?(www.)?([\w\.]+)(\.[etorgcovmn]+)(/.+)?)', re.IGNORECASE)
static = ['.png', '.css', '.js', '.jpg', '.jpeg', 'rss', '.svg', '.pdf', '.ico', ':void', 'mailto:', '.xml', 'googleapis', '/feed', 'google.com', 'itunes', 'apps.microsoft']

def _cleanURL(url):
    if sum([bad in url for bad in static]) > 0:
        return ''
    url = url.lower()
    match = re.match(website_regex, url) # create a regular expression object
    if match: # if the website matches the regex
        return 'http://www.'+ ''.join([a for a in match.groups()[3:] if a]).replace('.html','')
    return ''



def scanGoogleForCompanyLinkedin(search_dict):
    results = []
    query = ''
    g = scrapers.googleScraper()
    query += '"'+search_dict.get('keywords','')+'" '
    query += '"'+search_dict.get('location', '')+'" '
    query += '"'+search_dict.get('industry', '')+'" '
    for ending in [' site:www.linkedin.com/company']:
        google_query = urllib.quote_plus(query+ending)
        results += g.search(google_query, current_index = search_dict['current_index'])['results']
    return [{'web_presence':{'company_linkedin':{'url':r['link'].split('linkedin.com/')[1]}}, 'name':r['name_of_link'].split(' | ')[0]} for r in results]



def scanGoogleForLinkedin(search_dict):
    results = []
    g = scrapers.googleScraper()
    position = search_dict.get('keywords','')
    if not position: position = ''
    location = search_dict.get('location', '')
    if not location: location = ''
    query = '"'+position+'"'+' '+location
    if 'industry' in search_dict and search_dict['industry']:
        query += '"' + search_dict.get('industry', '') + '"'
    for ending in [' site:www.linkedin.com/in', ' site:www.linkedin.com/pub -site:www.linkedin.com/pub/dir']:
        google_query = urllib.quote_plus(query+ending)
        results += g.search(google_query, current_index = search_dict.get('current_index', 0))['results']
    links = [r['link'].split('linkedin.com/')[1].replace('?trk=pub-pbmap', '').lower() for r in results]
    return links

def scanTwitter(scraper_dict, limit = 51, api = None):
    if not api:
        api = scrapers.createAPI()
    keyword = scraper_dict.get('keywords', '').lower()
    location = scraper_dict.get('location', '').lower()
    query = keyword + ' ' + location
    handle_set = set()
    users_list = []
    for users in tweepy.Cursor(api.search_users, q=query).pages(int(scraper_dict.get('current_index', 1))) :
        for user in users:
            if user.screen_name.lower() not in handle_set and not getPerson({'web_presence':{'personal_twitter':{'url':user.screen_name.lower()}}}):
                handle_set.add(user.screen_name.lower())      
                t = scrapers.personalTwitterScraper(data = user)
                l = {'web_presence':{'personal_twitter':{'url':user.screen_name.lower()}}}
                l = legion({'web_presence':{'personal_twitter':{'url':user.screen_name.lower()}}}, scrapers = {'personal_twitter':t}).complete().information
                yield l



def scrape_indeed(keyword, location, item_num, limit):
    people = []
    keyword = '?q="'+keyword+'"'
    item_num = "&start=" + str(item_num)
    if not location:
        webpage = "http://www.indeed.com/resumes" + keyword + item_num
    else :
        location = location.replace(",","")
        webpage = "http://www.indeed.com/resumes" + keyword + "&l=" + location + item_num 
    webpage += '&sort=date'
    html_content = requests.get(webpage).text
    soup = BeautifulSoup(html_content)
    
    count = 0
    for link in soup.findAll('div', "app_name") [:limit] :
        link = link.find('a').get('href')
        link = "http://www.indeed.com" + str(link)
        person = scrape_resume(link)
        people.append(person)
        count += 1 
    return people [:limit]
    
# helper function for scraping each resume returns a person's information that is listed in a resume
def scrape_resume(url) :
    html_content = requests.get(url).text
    soup = BeautifulSoup(html_content)
    person = {}
    item = ['name','job_title','location', 'education', 'webpage', 'work_experience']
    
    # name
    person['name'] = soup.find(id="resume-contact").text
    

    
    # location
    try :
        person['location'] = soup.find(id = "headline_location").text
    except Exception as e :
        pass
    
    # education
    educations = []
    try :    
        edu = soup.find("div", "section-item education-content")
        edus = edu.findAll("div", "data_display")
        edu_info = ["degree", "school_name","school_location", "edu_dates"]
        for i in edus :
            education = {}
            try :
                education['degree'] = i.find("p", "edu_title").text
                if ' in ' in education['degree']:
                    education['degree'], education['fields_of_study'] = education['degree'].split(' in ')
                    education['fields_of_study'] = education['fields_of_study'].split(',')
            except Exception as e :
                pass
            try :
                education['school_name'] = i.find("span", itemprop="name").text
            except Exception as e :
                pass
            try :
                times = i.find("p", "edu_dates").text
                if 'Present' in times:
                    education['is_active'] = True
                elif ' ' not in times:
                    education['end_year'] = times
                else:
                    end_time = times.split(' to ')[1]
                    if ' ' in end_time:
                        education['end_month'], education['end_year'] = end_time.split(' ')
                    else:
                        education['end_year'] = end_time
                    start_time = times.split(' to ')[0]
                    if ' ' in start_time:
                        education['start_month'], education['start_year'] = start_time.split(' ')
                    else:
                        education['start_year'] = start_time

                if "ba" == education['degree'].lower() or 'b.a' in education['degree'].lower() or 'bachelor' in education['degree'].lower() :
                    person['age'] = datetime.datetime.now().year - int(education['end_year']) + 22
                if 'high school' in education['degree'].lower() :
                    person['age'] = datetime.datetime.now().year - int(education['end_year']) + 18
            except Exception as e :
                pass
            educations.append(education)
        person['education'] = educations
    except Exception as e :
        pass
    
    # webpages
    person['web_presence'] = {}
    try :
        webpage = soup.find("div", "section-item links-content")
        urls = webpage.findAll("p", "link_url")
        for i in urls :
            url = _cleanURL(i.findChild('a').text).replace('http://www.', '').lower()
            if "drive.google" in url or len(url) == 0:
                continue
            elif 'linkedin' in url:
                person['web_presence']['personal_linkedin'] = {'url':url.replace('linkedin.com/','')}
            elif 'twitter' in url:
                person['web_presence']['personal_twitter'] = {'url':url.replace('twitter.com/','')}
            elif 'github' in url:
                person['web_presence']['personal_github'] = {'url':url.replace('github.com/','')}
            else:
                person['web_presence']['personal_home_page'] = {'url':url}
    except Exception as e :
        pass
    
    # work_experiences
    works = []
    try :
        w = soup.find("div", "section-item workExperience-content") # html for work expeirnce item section
        work_experiences = w.findAll("div", "data_display") # find all work expeirnces
        work_info = ["work_title","company_name","company_location","work_dates"] # create a list of info for work-exp
        for i in work_experiences :
            work = {}
            # work title
            try :
                work['position_title'] = i.find("p", "work_title title").text
            except Exception as e :
                pass
            # company name
            work['company_dict'] = {}
            try :
                work['company_dict']['name'] = i.find("div", "work_company").find("span", "bold").text
            except Exception as e :
                pass
            # company location
            try :
                work['company_dict']['location'] = i.find("div", "inline-block").text
            except Exception as e :
                pass
            # work dates
            try :
                times = i.find("p", "work_dates").text
                if 'Present' in times:
                    work['is_active'] = True
                else:
                    end_time = times.split(' to ')[1]
                    if ' ' in end_time:
                        work['end_month'], work['end_year'] = end_time.split(' ')
                    else:
                        work['end_year'] = end_time
                start_time = times.split(' to ')[0]
                if ' ' in start_time:
                    work['start_month'], work['start_year'] = start_time.split(' ')
                else:
                    work['start_year'] = start_time
            except Exception as e :
                pass
            works.append(work)
        person['positions'] = works # add work-exps to person dictionary
    except Exception as e :
        pass
    
    return person





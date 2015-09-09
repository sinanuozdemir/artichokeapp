import re
import web_analytics
import scrapers

personal_preferred_order = {
    'name':['personal_twitter', 'personal_angellist', 'personal_github', 'personal_google_plus', 'personal_linkedin', 'personal_facebook'],
    'photo': ['personal_twitter', 'personal_linkedin', 'personal_facebook', 'personal_github', 'personal_angellist', 'personal_google_plus', 'personal_crunchbase'],
    'age': ['personal_linkedin', 'personal_google_plus'],
    'positions': ['personal_linkedin', 'personal_angellist', 'personal_crunchbase', 'personal_google_plus', 'personal_twitter'],
    'education': ['personal_linkedin', 'personal_google_plus'],
    'twitter_bio': ['personal_twitter'],
    'linkedin_bio': ['personal_linkedin'],
    'facebook_verified':['personal_facebook'],
    'twitter_bio':['personal_twitter'],
    'industry': ['personal_linkedin'],
    'interests': ['personal_linkedin', 'personal_angellist', 'personal_google_plus'],
    'location': ['personal_linkedin', 'personal_twitter', 'personal_github', 'personal_angellist', 'personal_google_plus'],
    'klout_score': ['personal_twitter'],
    'twitter_verified': ['personal_twitter'],
    'twitter_followers': ['personal_twitter'],
    'personal_home_page': ['personal_twitter', 'personal_angellist', 'personal_google_plus'],
    'personal_twitter':['personal_crunchbase', 'personal_angellist', 'personal_google_plus'],
    'personal_crunchbase':[],
    'personal_linkedin':['personal_angellist', 'personal_crunchbase', 'personal_google_plus'],
    'personal_facebook':['personal_angellist', 'personal_crunchbase'],
    'personal_github':['personal_angellist'],
    'personal_angellist':[]
}
company_preferred_order = {
    'name':['company_linkedin', 'company_twitter', 'company_facebook', 'company_github', 'company_google_plus'],
    'revenue': ['company_linkedin', 'company_crunchbase'],
    'funding': ['company_crunchbase', 'company_angellist'],
    'facebook_verified':['company_facebook'],
    'twitter_bio':['company_twitter'],
    'industries': ['company_linkedin'],
    'number_of_employees': ['company_linkedin', 'company_angellist'],
    'location': ['company_linkedin', 'company_twitter', 'company_angellist'],
    'email_host': ['company_crunchbase'],
    'company_home_page': ['company_twitter', 'company_linkedin', 'company_angellist', 'company_facebook'],
    'company_twitter':['company_crunchbase', 'company_angellist'],
    'company_crunchbase':[],
    'company_linkedin':['company_angellist', 'company_crunchbase'],
    'company_facebook':['company_angellist', 'company_crunchbase'],
    'company_github':['company_angellist'],
    'company_angellist':[],
    'linkedin_bio': ['company_linkedin'],
    'twitter_bio':['company_twitter']
}


PERSONAL_WEB_PRESENCES = ['personal_linkedin', 'personal_angellist', 'personal_facebook', 'personal_twitter', 'personal_github', 'personal_crunchbase', 'personal_home_page', 'personal_google_plus']
PERSONAL_BASIC_INFO = ['name', 'age', 'education', 'positions', 'location', 'interests', 'photo', 'industry']
ADVANCED_BASIC_INFO = ['klout_score', 'twitter_bio', 'twitter_followers', 'twitter_verified', 'linkedin_bio']
COMPANY_WEB_PRESENCES = ['company_crunchbase', 'company_linkedin', 'company_facebook', 'company_twitter', 'company_angellist', 'company_home_page']
COMPANY_BASIC_INFO = ['name', 'location', 'industries', 'email_host', 'number_of_employees', 'funding', 'revenue']
ADVANCED_COMPANY_INFO = ['facebook_verified', 'twitter_verified', 'linkedin_bio', 'twitter_bio']


class legion():
    def __init__(self, information = {}, type_of_entity = 'person', scrapers = {}):
        self.type_of_entity = type_of_entity
        if type_of_entity == 'person':
            self.basic_info, self.advanced_info, self.web_presences, self.pref = PERSONAL_BASIC_INFO, ADVANCED_BASIC_INFO, PERSONAL_WEB_PRESENCES, personal_preferred_order
        elif type_of_entity == 'company':
            self.basic_info, self.advanced_info, self.web_presences, self.pref = COMPANY_BASIC_INFO, ADVANCED_COMPANY_INFO, COMPANY_WEB_PRESENCES, company_preferred_order
        self.information = information
        self.checked = {}
        for social_media in self.web_presences:
            self.checked[social_media] = {}
            for info in self.basic_info + self.advanced_info+self.web_presences:
                self.checked[social_media][info] = False
        self.scrapers = scrapers
        self.current_web_presences = self.information.get('web_presence', {})
    def getAllBasicInfo(self):
        for info in self.basic_info:
            self.getInfo(type_of_info = info)
    def getAllAdvancedInfo(self):
        for info in set(self.advanced_info) - set(self.information.keys()):
            self.getInfo(type_of_info = info)
    def getInfo(self, type_of_info = '', alt = None):
        type_of_info = type_of_info.lower()
        if self.information.get(type_of_info, ''):
            return self.information.get(type_of_info)
        for media in self.pref.get(type_of_info, []):
            if media not in self.current_web_presences or self.checked[media][type_of_info]:
                continue
            self.checked[media][type_of_info] = True
            url = self.current_web_presences[media]['url']
            my_scraper = self._getScraper(media, url)
            if my_scraper:
                found_info = my_scraper.getInfo(type_of_info = type_of_info)
                if found_info:
                    self.information[type_of_info] = found_info
                    return found_info
        return alt
    def getAllSocialMedias(self):
        for media in set(self.web_presences) - set(self.current_web_presences.keys()):
            self.getSocialMedia(type_of_media = media)
    def getSocialMedia(self, type_of_media = 'personal_linkedin'):
        if type_of_media in self.current_web_presences.keys(): # already have it
            return type_of_media
        for media in self.pref.get(type_of_media, []):
            if media not in self.current_web_presences or self.checked[media][type_of_media]: # already tried it from here
                continue
            self.checked[media][type_of_media] = True
            url = self.current_web_presences[media]['url']
            my_scraper = self._getScraper(media, url)
            if not my_scraper:
                continue
            found_media = my_scraper.getMedia(type_of_media = type_of_media)
            if found_media:
                flag = 0
                if 'home_page' in type_of_media:
                    for reg, sm in web_analytics.regex_dict.iteritems():
                        m = re.search(reg, found_media)
                        if not m:
                            continue
                        flag = 1
                        self.current_web_presences[sm] = {'url':m.group(1).lower()}
                if flag == 0:
                    self.current_web_presences[type_of_media] = {'url':found_media.lower()}
                return found_media
        return None
    def complete(self):
        self.getAllSocialMedias()
        self.getAllBasicInfo()
        self.getAllAdvancedInfo()
        return self
    def _getScraper(self, type_of_media, handle):
        if self.scrapers.has_key(type_of_media):
            return self.scrapers[type_of_media]
        elif type_of_media == 'personal_linkedin':
            self.scrapers[type_of_media] = scrapers.privatePersonalLinkedinScraper(handle)
            if "profile/view" in handle:
                self.current_web_presences['personal_linkedin'] = {'url':self.scrapers[type_of_media].getPublicHandle()}
        elif type_of_media == 'personal_google_plus':
            self.scrapers[type_of_media] = scrapers.personalGooglePlusScraper(handle)
        elif type_of_media == 'personal_crunchbase':
            self.scrapers[type_of_media] = scrapers.personalCrunchbaseScraper(handle)
        elif type_of_media == 'personal_facebook':
            self.scrapers[type_of_media] = scrapers.personalFacebookScraper(handle)
        elif type_of_media == 'personal_twitter':
            self.scrapers[type_of_media] = scrapers.personalTwitterScraper(handle, data = None)
        elif type_of_media == 'personal_github':
            self.scrapers[type_of_media] = scrapers.personalGithubScraper(handle)
        elif type_of_media == 'personal_angellist':
            self.scrapers[type_of_media] = scrapers.personalAngellistScraper(handle)
        elif type_of_media == 'company_linkedin':
            self.scrapers[type_of_media] = scrapers.companyLinkedinScraper(handle)
        elif type_of_media == 'company_crunchbase':
            self.scrapers[type_of_media] = scrapers.companyCrunchbaseScraper(handle)
        elif type_of_media == 'company_home_page':
            self.scrapers[type_of_media] = scrapers.companyClearbitScraper(handle)
        elif type_of_media == 'company_twitter':
            self.scrapers[type_of_media] = scrapers.personalTwitterScraper(handle, data = None)
        elif type_of_media == 'company_angellist':
            self.scrapers[type_of_media] = scrapers.companyAngellistScraper(handle)
        elif type_of_media == 'company_facebook':
            self.scrapers[type_of_media] = scrapers.personalFacebookScraper(handle)
        else:
            return None
        return self.scrapers[type_of_media]

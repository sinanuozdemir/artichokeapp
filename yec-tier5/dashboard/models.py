from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from datetime import datetime

class twitterStats(models.Model):
    user                                 = models.ForeignKey('User', null=True, blank=True)
    person                               = models.ForeignKey('legion.Person', null=True, blank=True)
    company                              = models.ForeignKey('legion.Company', null=True, blank=True)
    competitor                           = models.ForeignKey('Competitor', null=True, blank=True)
    num_followers                        = models.IntegerField(default = 0, null = True)
    num_following                        = models.IntegerField(default = 0, null = True)
    time_taken                           = models.DateTimeField(default=datetime.now())
   
class twitterSentiment(models.Model):
    user                                 = models.ForeignKey('User', null=True, blank=True)
    person                               = models.ForeignKey('legion.Person', null=True, blank=True)
    time_taken                           = models.DateTimeField(default=datetime.now())
    hours_looked_back                    = models.IntegerField(default = 0, null = True)
    sentiment                            = models.DecimalField(default = 0, max_digits=7, decimal_places=2, null = True, blank=True)
    keyWord                              = models.ForeignKey('keyWord', null = True)
    tweets                               = models.ManyToManyField('Tweet', null=True, blank=True)



class marketEvent(models.Model):
    date_started                         = models.DateTimeField(default=datetime.today(), null = True)
    date_ended                           = models.DateTimeField(null = True)
    person                               = models.ForeignKey('legion.Person', null=True, blank=True)
    competitor                           = models.ForeignKey('Competitor', null=True, blank=True)
    user                                 = models.ForeignKey('User', null=True, blank=True)
    organization                         = models.ForeignKey('Organization', null=True, blank=True)
    followers_at_the_time                = models.IntegerField(default = 0, null = True)
    subscribers_at_the_time              = models.IntegerField(default = 0, null = True)
    sentiment_at_the_time                = models.DecimalField(default = 0, max_digits=7, decimal_places=2, null = True, blank=True)
    name                                 = models.CharField(max_length=200, null = True, db_index = True)
    type_of_event                        = models.CharField(max_length=200, null = True, db_index = True)
    description                          = models.CharField(max_length=1000, null = True, db_index = True)



class Tweet(models.Model):
    person                               = models.ForeignKey('legion.Person', null=True, blank=True)
    company                              = models.ForeignKey('legion.Company', null=True, blank=True)
    date                                 = models.DateTimeField(default=datetime.today(), null = True)
    text                                 = models.CharField(max_length=170, blank = True, null = True)
    status_id                            = models.CharField(max_length=50, null = True, db_index = True)
    textblob_sentiment                   = models.DecimalField(default = 0, max_digits=7, decimal_places=2, null = True, blank=True)
    retweet                              = models.CharField(max_length=50, null = True)
    reply_to                             = models.CharField(max_length=50, null = True)
    keywords                             = models.ManyToManyField('keyWord', null=True, blank=True)
    favorite_count                       = models.IntegerField(default = 0, null = True)
    retweet_count                        = models.IntegerField(default = 0, null = True)

class keyWord(models.Model):
    text                                 = models.CharField(max_length=170, blank = True, null = True)
    user                                 = models.ManyToManyField('User', null=True, blank=True)
    reference                            = models.CharField(max_length=170, blank = True, null = True)
    last_seen                            = models.ForeignKey('Tweet', null=True, blank=True)
    active                               = models.BooleanField(default = False)   

class Competitor(models.Model):
    company                              = models.ForeignKey('legion.Company', null=True, blank=True)
    name                                 = models.CharField(max_length=100, default = None, null = True)
    user                                 = models.ForeignKey('User', null=True, blank=True)
    keywords                             = models.ManyToManyField('keyWord', null=True, blank=True)

class Message(models.Model):
    user                                 = models.ForeignKey('User', null=True, blank=True)
    person                               = models.ForeignKey('legion.Person', null=True, blank=True)
    connection                           = models.ForeignKey('Connection', null=True, blank=True)
    subject                              = models.CharField(max_length=100, default = None, null = True)
    body                                 = models.TextField(default = '', null = True, blank = True)
    opened                               = models.BooleanField(default = False)   
    date_sent                            = models.DateTimeField(default=datetime.now())
    date_first_opened                    = models.DateTimeField(default=None, null = True)
    unique_id                            = models.CharField(max_length=100, default = None, null = True)
    type_of_message                      = models.CharField(max_length=100, default = None, null = True)

class MessageView(models.Model):
    message                              = models.ForeignKey('Message', null=True, blank=True)
    location                             = models.CharField(max_length=100, default = None, null = True)
    date                                 = models.DateTimeField(default=datetime.now())


class Proxy(models.Model):
    type_of_proxy                        = models.CharField(max_length=10, default = None, null = True)
    ip                                   = models.CharField(max_length=30, default = None, null = True)
    port                                 = models.CharField(max_length=10, default = None, null = True)
    date_updated                         = models.DateTimeField(default=datetime.now())

class Scraper(models.Model):
    website                              = models.CharField(max_length=100, default = None, null = True)
    keywords                             = models.CharField(max_length=100, default = None, null = True)
    current_index                        = models.IntegerField(default = 0, null = True) # used for snapshot
    industry                             = models.CharField(max_length=100, default = None, null = True)
    location                             = models.CharField(max_length=100, default = None, null = True)
    date_created                         = models.DateTimeField(default=datetime.now())
    last_run                             = models.DateTimeField(default=datetime.now(), null = True)
    targetmarket                         = models.ForeignKey('targetMarket', null=True, blank=True)

class apiCredentials(models.Model):
    social_media                         = models.CharField(max_length=50, default = None, null = True)
    api_key                              = models.CharField(max_length=50, default = None, null = True)
    api_secret                           = models.CharField(max_length=50, default = None, null = True)
    access_token                         = models.CharField(max_length=50, default = None, null = True)
    access_secret                        = models.CharField(max_length=50, default = None, null = True)


class targetMarket(models.Model):
    user                                 = models.ForeignKey('User', null=True, blank=True)
    name                                 = models.CharField(max_length=100, default = '', null = True)
    short_name                           = models.CharField(max_length=100, default = '', null = True)
    description                          = models.CharField(max_length=200, default = '', null = True)
    query                                = models.TextField(default = '', null = True)
    archived                             = models.BooleanField(default = False)
    star_limit                           = models.DecimalField(default = 5, max_digits=3, decimal_places=1, null = True, blank=True)


class flag(models.Model):
    flag_on                              = models.ForeignKey('legion.Person', null=True, blank=True)
    comments                             = models.TextField(default = '', null = True)
    resolved                             = models.BooleanField(default = False)
    flagLinkedin                         = models.BooleanField(default = False)
    flagTwitter                          = models.BooleanField(default = False)
    flagFacebook                         = models.BooleanField(default = False)
    flagEmail                            = models.BooleanField(default = False)
    flagPhone                            = models.BooleanField(default = False)
    flagJob                              = models.BooleanField(default = False)
    flagOther                            = models.BooleanField(default = False)

class ICP(models.Model):
    user                                 = models.ForeignKey('User', null=True, blank=True)
    people                               = models.ManyToManyField('legion.Person', null=True, blank=True)
    icp_dict                             = models.TextField(default = '', null = True)
    name                                 = models.CharField(max_length = 500, default = '', null = True)
    target_market                        = models.ForeignKey('targetMarket', null = True, blank = True)
    generated                            = models.DateTimeField(default=datetime.now(), null = True)


class Connection(models.Model):
    person                               = models.ForeignKey('legion.Person', null=True, blank=True)
    job                                  = models.ForeignKey('legion.Job', null=True, blank=True)
    user                                 = models.ForeignKey('User', null=True, blank=True)
    lead                                 = models.BooleanField(default = False)
    converted                            = models.BooleanField(default = False)
    converted_on                         = models.DateTimeField(default=None, null = True)
    conversion_time_in_months            = models.DecimalField(default = 0, max_digits=7, decimal_places=2, null = True, blank=True)
    lead_on                              = models.DateTimeField(default=None, null = True)
    following                            = models.BooleanField(default = False) # true if the user is following person
    following_on                         = models.DateTimeField(default=None, null = True)
    followed_by                          = models.BooleanField(default = False) # true if the user is followed by the person
    followed_on                          = models.DateTimeField(default=None, null = True)
    last_date                            = models.DateTimeField(default=datetime.now(), null = True)
    linkedin                             = models.BooleanField(default = False)
    facebook                             = models.BooleanField(default = False)   
    crunchbase                           = models.BooleanField(default = False)
    angellist                            = models.BooleanField(default = False)
    individual                           = models.BooleanField(default = False)
    from_site                            = models.BooleanField(default = False)
    used_for_stats                       = models.BooleanField(default = False)
    new_lead                             = models.BooleanField(default = False)
    num_interests                        = models.IntegerField(default = 0, null = True) # used for snapshot
    num_schools                          = models.IntegerField(default = 0, null = True) # used for snapshot
    num_titles                           = models.IntegerField(default = 0, null = True) # used for snapshot
    num_companies                        = models.IntegerField(default = 0, null = True) # used for snapshot
    num_locations                        = models.IntegerField(default = 0, null = True) # used for snapshot
    star_rating                          = models.DecimalField(default = 0, max_digits=6, decimal_places=4, null = True, blank=True)
    tm_close                             = models.DecimalField(default = 0, max_digits=6, decimal_places=4, null = True, blank=True)
    icp_close                            = models.DecimalField(default = 0, max_digits=6, decimal_places=4, null = True, blank=True)
    user_close                           = models.DecimalField(default = 0, max_digits=6, decimal_places=4, null = True, blank=True)
    target_market                        = models.ManyToManyField('targetMarket', null = True, blank = True)
    sourced_from                         = models.ManyToManyField('Document', null = True, blank = True)
    subscribed_to                        = models.ManyToManyField('Website', null = True, blank = True)

class statsSnapshot(models.Model):
    user                                 = models.ForeignKey('User', null=True, blank=True)
    competitor                           = models.ForeignKey('Competitor', null=True, blank=True)
    company                              = models.ForeignKey('legion.Company', null=True, blank=True)
    generated                            = models.DateTimeField(default=datetime.now())
    type_of_stats                        = models.CharField(max_length = 200, null = True, blank = True)
    stats                                = models.TextField(default = '', null = True)
    number_of_connections_used           = models.IntegerField(default = 0, null = True) # used for snapshot
    period                               = models.IntegerField(default = 0, null = True) # used for snapshot
    def __str__(self):
        return datetime.strftime(self.generated, '%D %H:%m')    

class Document(models.Model):
    docfile                             = models.FileField(upload_to='documents/')
    date_uploaded                       = models.DateTimeField(default=datetime.now())
    date_competed                       = models.DateTimeField(default=None, null = True, blank = True)
    belongs_to                          = models.ForeignKey('User', null=True, blank=True)
    is_analyzed                         = models.BooleanField(default=False)
    analyzed                            = models.IntegerField(default = 0)
    emails_on_csv                       = models.IntegerField(default = 0)
    emails_new_to_user                  = models.IntegerField(default = 0)
    exported                            = models.BooleanField(default=False)
    def __unicode__(self):
        return self.docfile.name[10:]

class Organization(models.Model):
    name                                = models.CharField(max_length = 200, null = True, blank = True)


class User(AbstractBaseUser):
    email                               = models.EmailField('email address', unique=True, db_index=True)
    joined                              = models.DateTimeField(auto_now_add=True)
    new                                 = models.BooleanField(default=True)
    organization                        = models.ForeignKey('Organization', null=True, blank=True)
    is_active                           = models.BooleanField(default=True)
    is_admin                            = models.BooleanField(default=False)
    available_for_stats                 = models.IntegerField(default = 50)
    daily_leads                         = models.IntegerField(default = 20, null = True)
    twitter_available_for_stats         = models.IntegerField(default = 50, null = True)
    password_token                      = models.CharField(max_length=25, default = None, null = True)
    company_name                        = models.CharField(max_length=100, default = None, null = True)
    USERNAME_FIELD                      = 'email'
    gender                              = models.CharField(max_length=25, default = None, null = True)
    phone                               = models.CharField(max_length=25, default = None, null = True)
    name                                = models.CharField(max_length=25, default = None, null = True)
    twitter_access_token_key            = models.CharField(max_length=100, default = None, null = True)
    mailchimp_access_token              = models.CharField(max_length=100, default = None, null = True)
    twitter_oauth_token                 = models.CharField(max_length=1000, default = None, null = True)
    twitter_id                          = models.CharField(max_length=100, default = None, null = True)
    twitter_handle                      = models.CharField(max_length=100, default = None, null = True)
    twitter_picture                     = models.CharField(max_length=500, default = None, null = True)
    twitter_access_token_secret         = models.CharField(max_length=100, default = None, null = True)
    most_recent_follower_id             = models.CharField(max_length=100, default = None, null = True)    
    # if this is None, then i've never checked for their followers
    stripe_id                           = models.CharField(max_length=255, default = None, null = True)
    type_of_entity                      = models.CharField(max_length=25, default = None, null = True)
    uploaded_a_csv                      = models.BooleanField(default=False)
    tweeted_at_someone                  = models.BooleanField(default=False)
    referred                            = models.IntegerField(default=0)
    followed_tier5                      = models.BooleanField(default=False)
    earned_onboarding_500               = models.BooleanField(default=False)
    pricing_plan                        = models.CharField(max_length=100, default = 'Free Plan', null = True)
    referral_token                      = models.CharField(max_length=25, default = None, null = True)
    referred_by                         = models.CharField(max_length=25, default = None, null = True)
    is_staff                            = models.BooleanField(default=False)
    is_admin                            = models.BooleanField(default=False)
    is_superuser                        = models.BooleanField(default=False)
    competitors                         = models.ManyToManyField('legion.Company', through='Competitor', null=True, blank=True)
    google_refresh_token                = models.TextField(default = '', null = True)
    id_token                            = models.TextField(default = '', null = True)
    linkedin_secret_code                = models.TextField(default = '', null = True)
    linkedin_public_profile             = models.TextField(default = '', null = True)
    interests                           = models.ManyToManyField('legion.Industry')
    person                              = models.ForeignKey('legion.Person', unique = True, null = True, blank = True)
    linkedin_access_token               = models.TextField(default = '', null = True)
    linkedin_access_token_expires       = models.DateTimeField(default=None, null = True)
    google_access_token                 = models.TextField(default = '', null = True)
    settings_json                       = models.TextField(default = '{"inbound_settings": {"toolbar": ["P.o.P Change","Total People","Negative Comments","Positive Comments", "Period (45 Days)"],"period": 45}}', null = True)
    default_period                      = models.CharField(default = '45', null = True, max_length = 5)
    google_auth_email                   = models.EmailField(unique=True, db_index=True, null = True, blank = True, default = None)
    def __unicode__(self):
        return self.email


class Website(models.Model):
    type_of_website                     = models.CharField(max_length=25)
    address                             = models.CharField(max_length=100, null = True)
    user                                = models.ForeignKey('User', null=True, blank=True)
    last_updated                        = models.DateTimeField(default=datetime.now(), null = True, blank = True)




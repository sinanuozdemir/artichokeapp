from datetime import datetime, timedelta
import json
from models import User, statsSnapshot, Competitor, keyWord, twitterStats, twitterSentiment, marketEvent
from django.core import serializers
from django.db.models import Q

class ImpersonateMiddleware(object):
    def process_request(self, request):
        if "__impersonate" in request.GET:
            request.user = User.objects.get(email=request.GET['__impersonate'])
            request.session['impersonate_id'] = request.user.id
            for i in ['last_checked_for_inbound', 'total_people', 'last_inbound_query', 'inbound_stats', 'last_checked_for_inbound', '30']:
                try:
                    del request.session[i]
                except:
                    pass
        elif "__unimpersonate" in request.GET:
            for i in ['impersonate_id', 'last_checked_for_inbound', 'total_people', 'last_inbound_query', 'inbound_stats', 'last_checked_for_inbound', '30']:
                try:
                    del request.session[i]
                except:
                    pass
            request.user = User.objects.get(id=request.session['saved_id'])
        elif 'impersonate_id' in request.session:
            request.user = User.objects.get(id=request.session['impersonate_id'])


def process_dt(d):
    try:
        return datetime.strptime(d, "%m/%d/%Y %H:%M")
    except:
        pass
    try:
        return datetime.strptime(d, "%m/%d/%y %H:%M")
    except:
        pass
    try:
        return datetime.strptime(d, "%D %H:%M")
    except:
        pass
    return None

class SettingsMiddleWare(object):
    def process_request(self, request):
        if request.method == 'POST' or request.user.is_anonymous() or '/legion/dashboard' not in request.META['PATH_INFO']:
            return
        if  False or 'last_checked_for_inbound' not in request.session or (datetime.now()-process_dt(request.session['last_checked_for_inbound'])).total_seconds() >= 5:
            last_demographic_snap = statsSnapshot.objects.filter(Q(user=request.user) & Q(type_of_stats = 'demographic_stats')).order_by('-pk').first()
            last_30_sentiment_snap = statsSnapshot.objects.filter(Q(user=request.user) & Q(period=30)& Q(type_of_stats = 'sentiment_stats')).order_by('-pk').first()
            try:
                request.session['total_people'] = last_demographic_snap.number_of_connections_used
                request.session['inbound_stats'] = json.loads(last_demographic_snap.stats)
            except:
                request.session['total_people'] = '??'
                request.session['inbound_stats'] = {}
            request.session['last_checked_for_inbound'] = datetime.strftime(datetime.now(), "%m/%d/%Y %H:%M")
            compet = Competitor.objects.filter(user=request.user)
            try:
                request.session['30'] = json.loads(last_30_sentiment_snap.stats)
            except Exception as e:
                request.session['30'] = {}
            request.session['30']['competitors'] = []
            for competitor in compet:
                a = statsSnapshot.objects.filter(Q(competitor = competitor) & Q(type_of_stats='sentiment_stats')).last()
                if a:
                    sen_stats = json.loads(a.stats)
                else:
                    sen_stats = {}
                a = statsSnapshot.objects.filter(Q(competitor = competitor) & Q(type_of_stats = 'demographic_stats')).last()
                if a:
                    sen_stats['demographics'] = json.loads(a.stats)
                request.session['30']['competitors'].append(sen_stats)
            try:
                most_recent_followers           = int(twitterStats.objects.filter(user=request.user).last().num_followers)
                market_events  = marketEvent.objects.filter(user=request.user).values('followers_at_the_time', 'sentiment_at_the_time', 'date_started', 'id', 'name', 'type_of_event')
                request.session['30']['me']['market_events'] = []
                keys = keyWord.objects.filter(Q(user=request.user)).exclude(id__in=compet.values_list('keywords__id', flat = True))
                for event in market_events:
                    event['date_started'] = datetime.strftime(event['date_started'], '%D')
                    event['change_in_followers'] = int(most_recent_followers - event['followers_at_the_time'])
                    try:
                        event['percent_change_in_sentiment'] = int(100.*(float(twitterSentiment.objects.filter(Q(keyWord__in=inbound_info['keywords']) & Q(person=None) & Q(time_taken__gte=beginning_date) & Q(time_taken__lte=end_date)).values('time_taken', 'sentiment').last()['sentiment']) - event['sentiment_at_the_time']) / event['sentiment_at_the_time'])
                    except:
                        event['percent_change_in_sentiment'] = 0
                    event['type_of_event'] = str(event['type_of_event'])
                    event['name'] = str(event['name'])
                    event['sentiment_at_the_time'] = float(event['sentiment_at_the_time'])
                    request.session['30']['me']['market_events'].append(event)
            except:
                pass







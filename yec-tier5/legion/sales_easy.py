from simple_salesforce import Salesforce

userName = "sinan@kovani.co"
password = "dino9119"
securityToken = "6IFr3W6z1KjU0hTpuIghGJw7"
instance = "na34"

sf = Salesforce(username=userName, password=password, security_token=securityToken)

bylines = sf.query_all("SELECT Id, Name, Email FROM Contact")
records = bylines["records"]

for record in records:
    r = dict(record)
    print r['Name'], r['Email']


import pytz
import datetime
end = datetime.datetime.now(pytz.UTC)  # we need to use UTC as salesforce API requires this!
sf.Contact.updated(end - datetime.timedelta(days=10), end)

contact = sf.Contact.get('00361000002Rq2MAAS')



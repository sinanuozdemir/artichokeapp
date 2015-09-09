import requests

def login(userName, password):
  request = """<?xml version="1.0" encoding="utf-8" ?>
  <env:Envelope xmlns:xsd="http://www.w3.org/2001/XMLSchema"
      xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
      xmlns:env="http://schemas.xmlsoap.org/soap/envelope/">
    <env:Body>
      <n1:login xmlns:n1="urn:partner.soap.sforce.com">
        <n1:username>""" + userName + """</n1:username>
        <n1:password>""" + password + """</n1:password>
      </n1:login>
    </env:Body>
  </env:Envelope>"""
   
  encoded_request = request.encode('utf-8')
  url = "https://login.salesforce.com/services/Soap/u/30.0"
   
  headers = {"Content-Type": "text/xml; charset=UTF-8",
             "SOAPAction": "login"}
                             
  response = requests.post(url=url,
                           headers = headers,
                           data = encoded_request,
                           verify=False)

  return unicode(response.text)

def addBatch(instance, sessionId, jobId, objects):

  request = u"""<?xml version="1.0" encoding="UTF-8"?>
  <sObjects xmlns="http://www.force.com/2009/06/asyncapi/dataload">
     """ + objects + """
  </sObjects>"""

  encoded_request = request.encode('utf-8')
  url = "https://" + instance + ".salesforce.com/services/async/30.0/job/" + jobId + "/batch"
   
  headers = {"X-SFDC-Session": sessionId,
             "Content-Type": "application/xml; charset=UTF-8"}
                             
  response = requests.post(url=url,
                           headers = headers,
                           data = encoded_request,
                           verify=False)

  return unicode(response.text)

def createJob(instance, sessionId, operation, object, contentType):

  request = u"""<?xml version="1.0" encoding="UTF-8"?>
  <jobInfo xmlns="http://www.force.com/2009/06/asyncapi/dataload">
      <operation>""" + operation + """</operation>
      <object>"""+ object + """</object>
      <contentType>""" + contentType + """</contentType>
  </jobInfo>"""

  encoded_request = request.encode('utf-8')
  url = "https://" + instance + ".salesforce.com/services/async/30.0/job"
   
  headers = {"X-SFDC-Session": sessionId,
             "Content-Type": "application/xml; charset=UTF-8"}
                             
  response = requests.post(url=url,
                           headers = headers,
                           data = encoded_request,
                           verify=False)

  return unicode(response.text)

from simple_salesforce import Salesforce

def createObjectXml(objectXml, userName, password, securityToken):

  sf = Salesforce(username=userName, password=password, security_token=securityToken)

  bylines = sf.query_all("SELECT Id, Name, Title__c, Published_Link__c FROM Byline__c WHERE Published_Link__c != ''")
  records = bylines["records"]

  counter = 0
  errors = ''

  for record in records:

    counter = counter + 1
    
    id = record["Id"]
    name = record["Name"]
    title = record["Title__c"]
    publishedLink = record["Published_Link__c"]
    
    twitterCount = 0
    facebookShares = 0
    linkedInCount = 0

    try:
      twitterJson = requests.get('http://cdn.api.twitter.com/1/urls/count.json?callback=?&url=' + publishedLink).json()
      facebookJson = requests.get('http://graph.facebook.com/' + publishedLink).json()
      linkedInJson = requests.get('http://www.linkedin.com/countserv/count/share?url=' + publishedLink + '&format=json').json()
    except ValueError:
      continue

    if 'count' in twitterJson:
      twitterCount = twitterJson["count"]

    if 'shares' in facebookJson:
      facebookShares = facebookJson["shares"]

    if 'count' in linkedInJson:
      linkedInCount = linkedInJson["count"]

    objectXml = objectXml + u"""<sObject>
       <Id>""" + id + """</Id>
       <Twitter_Mentions__c>""" + str(twitterCount) + """</Twitter_Mentions__c>
       <Facebook_Likes__c>""" + str(facebookShares) + """</Facebook_Likes__c>
       <LinkedIn_Shares__c>""" + str(linkedInCount) + """</LinkedIn_Shares__c>
    </sObject>"""

  return objectXml

import xml.etree.ElementTree as ET



def closeJob(instance, sessionId, jobId):

  request = u"""<?xml version="1.0" encoding="UTF-8"?>
  <jobInfo xmlns="http://www.force.com/2009/06/asyncapi/dataload">
    <state>Closed</state>
  </jobInfo>"""

  encoded_request = request.encode('utf-8')
  url = "https://" + instance + ".salesforce.com/services/async/30.0/job/" + jobId
   
  headers = {"X-SFDC-Session": sessionId,
             "Content-Type": "application/xml; charset=UTF-8"}
                             
  response = requests.post(url=url,
                           headers = headers,
                           data = encoded_request,
                           verify=False)

  return unicode(response.text)

import re
userName = "sinan@kovani.co"
password = "dino9119"
securityToken = "6IFr3W6z1KjU0hTpuIghGJw7"
instance = "na34"



print ">> Login"

loginXmlResponse = login(userName, password + securityToken)
loginXmlResponse
loginXmlRoot = ET.fromstring(loginXmlResponse)
sessionId = loginXmlRoot[0][0][0][4].text
instance = loginXmlRoot[0][0][0][3].text
print ">> Create Job"

jobXmlResponse = createJob(instance, sessionId, "update", "Byline__c", "XML")

jobXmlRoot = ET.fromstring(jobXmlResponse)
jobId = jobXmlRoot[0].text

print ">> Add Batch"

objectXml = ""
objectXml = createObjectXml(objectXml, userName, password, securityToken)

addBatch(instance, sessionId, jobId, objectXml)

print ">>> Close Job"

closeJob(instance, sessionId, jobId)


import random
import requests
import telnetlib
import time
import re
import csv
import os


# gets the list of emails and rest of the row elements from csv
def inputCSV(filename) :
    with open(filename) as csvfile:
        reader = csv.DictReader(csvfile)
        email_validity = []
        for row in reader :
            email_validity.append(row)
    return email_validity

# finds handle/id of a email
def getID(email) :
    id_regex = re.compile('(\S+)@\S+', re.IGNORECASE)
    match = re.search(id_regex, email)
    id = match.group(1)
    return id

# finds domain of a email
def getDomain(email) :
    domain_regex = re.compile('\S+@(\S+)', re.IGNORECASE)
    match = re.search(domain_regex, email)
    domain = match.group(1).lower()
    return domain

# helper funciton for validating yahoo mail, 
# finds country code
def getCountryCode(domain) :
    country_regex = re.compile('\S+(.\S+)', re.IGNORECASE)
    match = re.search(country_regex, domain)
    country_code = match.group(1).lower()
    return country_code

# get domain host from 'nslookup'
def getHost(domain) :
    query = 'nslookup -q=mx {0}'
    pattern = '\*\*\sserver\scan\'t\sfind'
    reg = re.compile('mail exchanger = \d+ (\S+)', re.IGNORECASE)
    mx_hosts = []
    connect = False
    count = 0
    try:
        command = query.format(domain)
        with os.popen(command) as response :
            result = response.readlines()
            cleaned_results = [re.search(reg, r).group(1)[:-1] for r in result if re.search(reg, r)]
            for clean_result in cleaned_results:
                try:
                    tn = telnetlib.Telnet(clean_result, 25, timeout = 5)
                    tn.close()
                    return clean_result
                except:
                    pass
    except Exception:
        pass
    return None

# validates email 
def validateEmail(address, vrfy_hard = False) :
    print "running %s" %address
    try:
        address = str(address)
    except:
        return {}
    domain = getDomain(address)
    val = {}
    val['last_comment'] = ""
    val['reason'] = ""
    # validate yahoo emails
    if "yahoo.com" in domain :
        id = getID(address)
        val['host'] = domain
        val['catch_all'] = False
        # check if the id is in valid form(more than 4 characters)
        if len(id) >= 4 :
            if domain == "yahoo.com" :
                validity, reason = validateYmail(id)
                if validity == True:
                    val['validity'] = "Valid"
                else :
                    val['validity'] = "Invalid"                    
                val['reason'] = reason
                return val
            else :
                country_code = getCountryCode(domain)
                validity, reason = validateYmail(id, country_code)
                if validity == True:
                    val['validity'] = "Valid"
                else :
                    val['validity'] = "Invalid"
                val['reason'] = reason
                return val
        else : 
            val['validity'] = "Invalid"
            val['reason'] = "ID less than 4 characters"
            return val
    else :
        # get domain host by using nslookup
        host = getHost(domain)
        val['host'] = host
        # check if the domain host exists in the server
        if host != None :
            # validate gmails
            if "gmail.com" in domain :
                validity, comment = validateGmail(host, address)
                if validity == True:
                    val['validity'] = "Valid"
                else :
                    val['validity'] = "Invalid"
                    val['reason'] = "Email does not exist"
                val['last_comment'] = comment
                val['catch_all'] = False
                return val
            # validate company emails using google domain host
            elif 'gmail-smtp' in host.lower() or 'google' in host.lower() or 'googlemail' in host.lower() :
                ret = isCatchAll_google(host, address, domain)
                if ret != True :
                    validity, comment = validateGmail(host, address)
                    if validity == True:
                        val['validity'] = "Valid"
                    else :
                        val['validity'] = "Invalid"
                        val['reason'] = "Email does not exist"
                    val['last_comment'] = comment
                    val['catch_all'] = False
                    return val
                else :
                    val['validity'] = "Unknown"
                    val['reason'] = "Catch All"
                    val['catch_all'] = True
                    return val
            # other emails. 
            # needs to be implemented(hotmail/aol/comcast/etc)
            else :
                if vrfy_hard == True :
                    ret, tn = isCatchAll_other(host, address, domain)
                    if ret == False :
                        validity, comment = validateOther(host, address, domain, tn)
                        time.sleep(30)
                        if validity == True: 
                            val['validity'] = "Valid"
                            val['reason'] = ""
                            val['last_comment'] = comment
                        elif validity == False :
                            val['validity'] = "Invalid"
                            val['reason'] = "Email does not exist"
                            val['last_comment'] = comment
                        else :
                            val['validity'] = "Unknown"
                            val['reason'] = "Other Reason"
                            val['last_comment'] = comment
                        val['catch_all'] = False
                        return val
                    else :
                        if tn != None :
                            tn.write("quit\r\n")
                        time.sleep(30)
                        if ret == True :
                            val['validity'] = "Unknown"
                            val['reason'] = "Catch All"
                            val['catch_all'] = True
                            return val
                        else :
                            val['validity'] = "Unknown"
                            val['reason'] = "Other Reason"
                            val['catch_all'] = False
                            val['last_comment'] = ret
                            return val
                else :
                    val['validity'] = "Unknown"
                    val['reason'] = "Hotmail/Other Mail"
                    val['catch_all'] = False
                    return val

        # host does not exist
        else :
            val['validity'] = "Invalid"
            val['reason'] = "No Host"
            val['catch_all'] = False
            return val

# checks if a google domain host is catch all server by trying with random ID
def isCatchAll_google(host, address, domain) :
    tn = telnetlib.Telnet(host, 25)
    time.sleep(0.5)
    tn.write("helo h\n")
    time.sleep(0.1)
    tn.write("mail from: <" + address + ">\n")
    time.sleep(0.1)
    tn.write("rcpt to: <not.a.validaddress.example@" + domain + ">\n")
    time.sleep(0.3)
    tn.write("quit\n")
    s = tn.read_very_eager()
    error_msg1 = "550-5.1.1 The email account that you tried to reach does not exist"
    error_msg2 = "550 5.2.1 The email account that you tried to reach is disabled"
    error_msg3 = "550"
    error_msg4 = "554"
    if error_msg1 not in s and error_msg2 not in s and error_msg3 not in s and error_msg4 not in s:
        return True
    else :
        return False

# checks if a non_google domain host is catch all server by trying with random ID
def isCatchAll_other(host, address, domain) :
    s = "Server Connection Failed"
    tn = None
    try:
        tn = telnetlib.Telnet(host, 25, timeout = 10)
        time.sleep(5)
        s = "1. " + tn.read_very_eager()   
        tn.write("helo h" + domain + "\r\n")
        time.sleep(3)
        s = "2. " + tn.read_very_eager()
        tn.write("mail from: <" + address + ">\r\n")
        time.sleep(3)
        s = "3. " + tn.read_very_eager()
        tn.write("rcpt to: <not.a.validaddress.e@" + domain + ">\r\n")
        time.sleep(5)
        s = "4. " + tn.read_very_eager()
        error_msg1 = "550-5.1.1 The email account that you tried to reach does not exist"
        error_msg2 = "550 5.2.1 The email account that you tried to reach is disabled"
        error_msg3 = "550"
        error_msg4 = "553"
        error_msg5 = "554"
        if "250" in s :
            return True, tn
        else :
            if "administrative prohibition" in s.lower() or "administrative lockout" in s.lower() or "spoofed message" in s.lower() :
                return s, tn
            elif error_msg1 in s or error_msg2 in s or error_msg3 in s or error_msg4 in s or error_msg5 in s :
                return False, tn
            else :
                return s, tn
    except Exception :
        return s, tn
        
# validate email that uses google domain
# Inputs smtp host and address 
def validateGmail(host, address) :
    address = str(address)
    tn = telnetlib.Telnet(host, 25)
    time.sleep(0.1)
    s = "1. " + tn.read_very_eager()

    tn.write("helo\n")
    time.sleep(0.3)
    s = "2. " + tn.read_very_eager()
    
    tn.write("mail from: <example@gmail.com>\n")
    time.sleep(0.3)
    s = "3. " + tn.read_very_eager()

    tn.write("rcpt to: <"+address+">\n")
    time.sleep(0.7)
    s = "4. " + tn.read_very_eager()

    tn.write("quit\n")
    time.sleep(0.1)

    error_msg1 = "550-5.1.1 The email account that you tried to reach does not exist"
    if error_msg1 in s :
        return False, s
    else :
        return True, s

# validate yahoo mail 
# Inputs id and Returns 'True' if email exists, and 'False' if email does not exists
# AAADDDDDD randomize this proxy!!!!!!
def validateYmail(id, country_code="us") :
    try:
        response = requests.get('https://kingproxies.com/api/v2/proxies.txt?key=1df2713cbc434caaa8bca8cddc014f&type=anonymous', timeout=3)
        PROXY_LIST += ['http://'+a for a in response.text.split('\n') if len(a) > 2]
        proxies = {'http': random.choice(PROXY_LIST)}
    except:
        proxies = {"http" : "http://54.187.52.159:3128"}
    url = "https://overview.mail.yahoo.com/u.php?u=" + id + "&intl=" + country_code
    for i in proxies :
        r = requests.get(url, proxies=proxies)
        if "false" in r.text.lower() :
            return True, ""
        else :
            return False, "Mail Not Exist"      

# validate other emails (hotmail/aol/comcast)
# currently does not work due to IP blocks 
def validateOther(host, address, domain, tn) :
    #tn = telnetlib.Telnet(host, 25)
    #time.sleep(0.5)
    #domain = getDomain(address)
    #tn.write("helo " + domain + "\r\n")
    tn.write("rset\r\n")
    time.sleep(3)
    s = tn.read_very_eager()

    tn.write("mail from: <"+address+">\r\n")
    time.sleep(2)
    s = "3. " + tn.read_very_eager()

    tn.write("rcpt to: <"+address+">\r\n")
    time.sleep(3)
    s = "4. " + tn.read_very_eager()

    tn.write("quit\r\n")
    time.sleep(0.1)

    if "250" in s :
        return True, s
    elif "450" in s :
        return None, s
    else :
        return False, s



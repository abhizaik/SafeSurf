import ipaddress
import re
from bs4 import BeautifulSoup
import requests
import whois
import urllib
import urllib.request
from datetime import datetime
import requests
import json
import csv
import time


global BASE_SCORE
global PROPERTY_SCORE_WEIGHTAGE
BASE_SCORE = 50  # default trust_ score of url out of 100
PROPERTY_SCORE_WEIGHTAGE = {
    'domain_rank': 0.6,
    'domain_age': 0.4,
    'is_url_shortened': 0.2,
    'hsts_support': 0.1,
    'ip_present': 0.8,
    'url_redirects': 0.05,
    'too_long_url': 0.05,
    'too_deep_url': 0.1,
    'content': 0.1
}



# check whether the link is active or not
def validate_link(link):
    try:
        if not link.startswith('http://') and not link.startswith('https://'):
            link = 'http://' + link

        response = requests.get(link)
        if(response.status_code == 200):
            return {'url': link}
        else:
            return False

    except requests.exceptions.RequestException:
        return False



# get domain rank if it exists in top 1M list
def get_domain_rank(domain):
    
    with open('sorted-top1million.txt') as f:
        top1million = f.read().splitlines()

    is_in_top1million = binary_search(top1million, domain)

    if is_in_top1million == 1:
        with open('domain-rank.json', 'r') as f:
            domain_rank_dict = json.load(f)
        rank = domain_rank_dict.get(domain, 0)
        return int(rank)
    else:
        return 0


# binary search
def binary_search(arr, x):
    low = 0
    high = len(arr) - 1
    while low <= high:
        mid = (low + high) // 2
        if arr[mid] == x:
            return 1
        elif arr[mid] < x:
            low = mid + 1
        else:
            high = mid - 1
    return 0

# get age of domain in years
def domain_age(domain):
    try:
        domain = whois.whois(domain)
        creation_date = domain.creation_date
        if type(creation_date) is list:
            creation_date = creation_date[0]
        age = (datetime.now() - creation_date).days / 365
        return age
    except Exception as e:
        print(f"Error: {e}")
        return False


# check for HSTS support
def hsts_support(url): # url should be http / https as prefix
    try:
        response = requests.get(url)
        headers = response.headers
        if 'Strict-Transport-Security' in headers:
            return 1
        else:
            return 0
    except:
        return 0


# check for URL shortening services
def is_url_shortened(domain): 
    try:
        with open('url-shorteners.txt') as f:
            services_arr = f.read().splitlines()
        
        for service in services_arr:
            if service in domain:
                return 1
        return 0
    except:
        return 0


# check if an IP is present in the URL
def ip_present(url):
    try:
        ipaddress.ip_address(url)
        result = 1
    except:
        result = 0
    return result


# check for website redirects
def url_redirects(url):
    try:
        response = requests.get(url)
        if len(response.history) > 1:
            # URL is redirected
            url_history = [] # returns array of redirected URLs
            for resp in response.history:
                url_history.append(resp.url)
            return url_history
        else:
            return 0
    except Exception as e:
        # print(f"Error: {e}")
        return 0


# check whether the URL is too long 
def too_long_url(url):
    if len(url) > 75:
        return 1
    else:
        return 0


# check whether the URL is too deep 
def too_deep_url(url):
    slashes = -2 # to skip first two slashes after protocol, i.e. https://
    for i in url:
        if i == '/':
            slashes += 1

    if slashes > 5:
        return 1
    else:
        return 0



# check whether the URL is having 
def content_check(url):
    try:

        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')

        result = {'onmouseover':0, 'right-click':0, 'form':0, 'iframe':0, 'login':0, 'popup':0}

        # check if onmouseover is enabled
        if soup.find(onmouseover=True):
            result['onmouseover'] = 1


        # check if right-click is disabled
        if soup.find_all('body', {'oncontextmenu': 'return false;'}):
            result['right-click'] = 1


        # check if there are any forms present
        if soup.find_all('form'):
            result['form'] = 1

        # check if there are any iframes present
        if soup.find_all('iframe'):
            result['iframe'] = 1

        # check if there are any login keyword present
        if soup.find_all(text=re.compile('password|email|forgotten|login')):
            result['login'] = 1

        # check if there are any pop-ups present
        if soup.find_all('div', {'class': 'popup'}):
            result['popup'] = 1
        
        return result

    except Exception as e:
        # print(f"Error: {e}")
        return 0



def phishtank_search(url):

    try:
        endpoint = "https://checkurl.phishtank.com/checkurl/"
        response = requests.post(endpoint, data={"url": url, "format": "json"})
        data = json.loads(response.content)
        if data['results']['valid'] == True:
            return 1
        return 0

    except Exception as e:
        # print(f"Error: {e}")
        return 0


# TEST FUNCTION TO ADD NEW URL CHECKS
def test(domain):
    
    with open('sorted-top1million.txt') as f:
        top1million = f.read().splitlines()
        

# res = content_check(url)
# print(res)


def calculate_trust_score(current_score, case, value):

    score = current_score

    if case == 'domain_rank':
        if value == 0:  # not in top 10L rank
            score = current_score - (PROPERTY_SCORE_WEIGHTAGE['domain_rank'] * BASE_SCORE * 0.5)
        elif value < 100000:  # in top 1L rank
            score = current_score + (PROPERTY_SCORE_WEIGHTAGE['domain_rank'] * BASE_SCORE)
        elif value < 500000:  # in 1L - 5L rank
            score = current_score + (PROPERTY_SCORE_WEIGHTAGE['domain_rank'] * BASE_SCORE * 0.5)
        else:  # in 5L - 10L rank
            score = current_score + (PROPERTY_SCORE_WEIGHTAGE['domain_rank'] * BASE_SCORE * 0.25)
        return score

    elif case == 'domain_age':
        if value < 5:
            score = current_score - (PROPERTY_SCORE_WEIGHTAGE['domain_age'] * BASE_SCORE)
        elif value >= 5 and value < 10:
            score = current_score
        elif value >= 10:
            score = current_score + (PROPERTY_SCORE_WEIGHTAGE['domain_age'] * BASE_SCORE)
        return score

    elif case == 'is_url_shortened':
        if value == 1:
            score = current_score - (PROPERTY_SCORE_WEIGHTAGE['is_url_shortened'] * BASE_SCORE)
        return score

    elif case == 'hsts_support':
        if value == 1:
            score = current_score + (PROPERTY_SCORE_WEIGHTAGE['hsts_support'] * BASE_SCORE)
        else:
            score = current_score - (PROPERTY_SCORE_WEIGHTAGE['hsts_support'] * BASE_SCORE)
        return score

    elif case == 'ip_present':
        if value == 1:
            score = current_score - (PROPERTY_SCORE_WEIGHTAGE['ip_present'] * BASE_SCORE)
        return score

    elif case == 'url_redirects':
        if value:
            score = current_score - (PROPERTY_SCORE_WEIGHTAGE['url_redirects'] * BASE_SCORE)
        return score

    elif case == 'too_long_url':
        if value == 1:
            score = current_score - (PROPERTY_SCORE_WEIGHTAGE['too_long_url'] * BASE_SCORE)
        return score

    elif case == 'too_deep_url':
        if value == 1:
            score = current_score - (PROPERTY_SCORE_WEIGHTAGE['too_deep_url'] * BASE_SCORE)
        return score
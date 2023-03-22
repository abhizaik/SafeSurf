from urllib.parse import urlparse, urlencode, quote, unquote
import tldextract
import model

global BASE_SCORE
BASE_SCORE = 50  # default trust_ score of url out of 100


def main(url):

    # input validattion
    url = model.include_protocol(url.lower())
    url_validation = model.validate_url(url)

    # default data
    domain = tldextract.extract(url).domain + '.' + tldextract.extract(url).suffix
    parsed_url = urlparse(url)
    print(parsed_url)
    encoded_url = quote(url, safe='')
    encoded_url = parsed_url.netloc + parsed_url.path + parsed_url.params + parsed_url.query + parsed_url.fragment
    response = {'status': 'SUCCESS', 'url': url, 'encoded_url' : encoded_url, 'msg': "URL is valid."}
    trust_score = BASE_SCORE


    # ================== starting url assessment ==================

    # phishtank check   
    phishtank_response = model.phishtank_search(url)
    if phishtank_response:
        response = {'status': 'SUCCESS', 'url': url,
                    'msg': "This is a verified phishing link."}
        return response

    if (not url_validation):
        response = {'status': 'ERROR', 'url': url, 'msg': "Link is not valid."}
        return response


    # domain_rank
    domain_rank = model.get_domain_rank(domain)
    trust_score = model.calculate_trust_score(trust_score, 'domain_rank', domain_rank)
    if domain_rank:
        response['rank'] = domain_rank
    else:
        response['rank'] = '10,00,000+'


    # domain_age
    domain_age = model.domain_age(domain)
    trust_score = model.calculate_trust_score(trust_score, 'domain_age', domain_age)
    response['age'] = str(round(domain_age,1)) + ' years old.'


    # is_url_shortened
    is_url_shortened = model.is_url_shortened(url)
    trust_score = model.calculate_trust_score(trust_score, 'is_url_shortened', is_url_shortened)
    response['is_url_shortened'] = is_url_shortened


    # hsts_support
    hsts_support = model.hsts_support(url)
    trust_score = model.calculate_trust_score(trust_score, 'hsts_support', hsts_support)
    response['hsts_support'] = hsts_support


    # ip_present
    ip_present = model.ip_present(url)
    trust_score = model.calculate_trust_score(trust_score, 'ip_present', ip_present)
    response['ip_present'] = ip_present


    # url_redirects
    url_redirects = model.url_redirects(url)
    trust_score = model.calculate_trust_score(trust_score, 'url_redirects', url_redirects)
    response['url_redirects'] = url_redirects


    # too_long_url
    too_long_url = model.too_long_url(url)
    trust_score = model.calculate_trust_score(trust_score, 'too_long_url', too_long_url)
    response['too_long_url'] = too_long_url


    # too_deep_url
    too_deep_url = model.too_deep_url(url)
    trust_score = model.calculate_trust_score(trust_score, 'too_deep_url', too_deep_url)
    response['too_deep_url'] = too_deep_url




    trust_score = int(max(min(trust_score, 100), 0))
    response['trust_score']= trust_score
    response['msg']= 'Assessment finished successfully.'


    return response
from urllib.parse import urlparse, urlencode, quote, unquote
import tldextract
import model
import time


class Controller:
    def __init__(self):
        self.BASE_SCORE = 50  # default trust score of URL out of 100
        self.model = model

    def main(self, url):
        try:
            # Input validation
            print(time.time(), "entry")
            url = self.model.include_protocol(url)
            print(time.time(), "include_protocol")
            url_validation = self.model.validate_url(url)
            print(time.time(), "validate_url")

            # Default data
            domain = tldextract.extract(url).domain + '.' + tldextract.extract(url).suffix
            print(time.time(), "extract")
            response = {'status': 'SUCCESS', 'url': url}
            trust_score = self.BASE_SCORE

            # Phishtank check
            phishtank_response = self.model.phishtank_search(url)
            print(time.time(), "phishtank_search")
            if phishtank_response:
                response['msg'] = "This is a verified phishing link."

            # Website status
            response['response_status'] = url_validation

            # Domain rank
            domain_rank = self.model.get_domain_rank(domain)
            print(time.time(), "get_domain_rank")
            trust_score = self.model.calculate_trust_score(trust_score, 'domain_rank', domain_rank)
            response['rank'] = domain_rank if domain_rank else '10,00,000+'

            # Domain age and WHOIS data
            whois_data = self.model.whois_data(domain)
            print(time.time(), "whois_data")
            trust_score = self.model.calculate_trust_score(trust_score, 'domain_age', whois_data['age'])
            response['age'] = whois_data['age'] if whois_data['age'] == 'Not Given' else f"{round(whois_data['age'], 1)} year(s)"
            response['whois'] = whois_data['data']

            # Is URL shortened
            is_url_shortened = self.model.is_url_shortened(url)
            print(time.time(), "is_url_shortened")
            trust_score = self.model.calculate_trust_score(trust_score, 'is_url_shortened', is_url_shortened)
            response['is_url_shortened'] = is_url_shortened

            # HSTS support
            hsts_support = self.model.hsts_support(url)
            print(time.time(), "hsts_support")
            trust_score = self.model.calculate_trust_score(trust_score, 'hsts_support', hsts_support)
            response['hsts_support'] = hsts_support

            # IP present
            ip_present = self.model.ip_present(url)
            print(time.time(), "ip_present")
            trust_score = self.model.calculate_trust_score(trust_score, 'ip_present', ip_present)
            response['ip_present'] = ip_present

            # URL redirects
            url_redirects = self.model.url_redirects(url)
            print(time.time(), "url_redirects")
            trust_score = self.model.calculate_trust_score(trust_score, 'url_redirects', url_redirects)
            response['url_redirects'] = url_redirects

            # Too long URL
            too_long_url = self.model.too_long_url(url)
            print(time.time(), "too_long_url")
            trust_score = self.model.calculate_trust_score(trust_score, 'too_long_url', too_long_url)
            response['too_long_url'] = too_long_url

            # Too deep URL
            too_deep_url = self.model.too_deep_url(url)
            print(time.time(), "too_deep_url")
            trust_score = self.model.calculate_trust_score(trust_score, 'too_deep_url', too_deep_url)
            response['too_deep_url'] = too_deep_url

            # Get IP address
            ip = self.model.get_ip(domain)
            print(time.time(), "get_ip")
            response['ip'] = 'Unavailable' if ip == 0 else ip

            # Get certificate details
            ssl = self.model.get_certificate_details(domain)
            print(time.time(), "get_certificate_details")
            response['ssl'] = ssl

            trust_score = int(max(min(trust_score, 100), 0))
            response['trust_score'] = trust_score
            return response

        except Exception as e:
            print(f"Error: {e}")
            response = {'status': 'ERROR', 'url': url, 'msg': "Some error occurred, please check the URL.",'emsg':e}
            return response


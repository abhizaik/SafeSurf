[Go back to SafeSurf Documentation](README.md#learn-and-contribute-to-the-project)

# Code Documentaion
## Documentation for app.py 

### Introduction
The `app.py` file serves as the entry point of the application, defining three API endpoints for interacting with the SafeSurf web application.

### API Endpoints
- `/`: Homepage of the application where users can input a URL to assess its safety.
- `/preview`: Endpoint to view a preview of the website within SafeSurf.
- `/source-code`: Endpoint to view the source code of a website.

### Dependencies
The file imports the following external libraries:
- Flask: A micro web framework for building web applications.
- requests: A library for making HTTP requests to external resources.
- BeautifulSoup: A library for parsing HTML and XML documents.
- urljoin: A function for joining relative URLs to absolute URLs.

### Functionality Overview
#### / Endpoint (Home)
- Handles GET and POST requests.
- Parses the input URL and passes it to the `controller.main` function for assessment.
- Renders the `index.html` template with the assessment result.

#### /preview Endpoint
- Handles POST requests.
- Retrieves the HTML content of the input URL using the requests library.
- Parses the HTML content with BeautifulSoup and injects external resources into the HTML.
- Renders the `preview.html` template with the prettified HTML content.

#### /source-code Endpoint
- Handles GET and POST requests.
- Retrieves the HTML content of the input URL using the requests library.
- Renders the `source_code.html` template with the prettified HTML content.


## Documentation for `controller.py`

The `controller.py` file serves as the main controller for the trustworthiness assessment of URLs. It orchestrates various checks and calculations to determine the trust score of a given URL. Below is a detailed explanation of how the code functions:

### Global Variables
- `BASE_SCORE`: This variable holds the default trust score for a URL out of 100. It is initialized to 50.

### Function: `main(url)`
This function is the entry point for URL assessment. It takes a URL as input and performs the following steps:

1. **Input Validation**:
   - The URL is validated and formatted to include the protocol (HTTP or HTTPS) using the `include_protocol()` function from the `model` module.
   
2. **Default Data Initialization**:
   - The domain of the URL is extracted using `tldextract` to determine the domain name.
   - A default response dictionary is initialized with 'SUCCESS' status and the input URL.
   - The trust score is initialized with the base score.

3. **URL Assessment**:

   - Phishtank Check: It checks if the URL is listed as a phishing link in the Phishtank database.
   - Website Status: It determines the status of the website's response using the `validate_url()` function from the `model` module.
   - Domain Rank: It retrieves the domain rank using the `get_domain_rank()` function from the `model` module. Authentic websites typically have high traffic volume, indicating popularity and reliability.
   - Domain Age: It retrieves WHOIS data to determine the domain's age and includes it in the response. The age of a domain is determined using WHOIS data. Websites less than 2 years old may raise suspicion.
   - URL Shortening: Check for the use of URL shortening services, which can obscure the original URL and potentially indicate malicious intent.
   - HSTS Support: It checks if the website supports HTTP Strict Transport Security (HSTS). Verify if the domain supports HTTPS and HSTS. Legitimate domains often prioritize security with HSTS support.
   - IP Presence: It checks for the presence of an IP address associated with the domain. Phishing links may use IP addresses instead of domain names. Authentic domains typically have dedicated domain names.
   - URL Redirects: It checks for URL redirects. Redirection to other pages can be a tactic to hide the original phishing link.
   - URL Length: It checks if the URL is too long. URLs exceeding 75 characters may indicate phishing attempts, as attackers may try to conceal suspicious parts in the address bar.
   - URL Depth: It checks if the URL depth is too deep. Excessive depth in the URL structure (number of '/') raises suspicion, as legitimate websites typically have simpler structures.


1. **IP Address and SSL Certificate**:
   - It retrieves the IP address associated with the domain and includes it in the response.
   - It retrieves SSL certificate details using the `get_certificate_details()` function from the `model` module.

2. **Trust Score Calculation**:
   - The trust score is calculated based on the results of the assessments. 

3. **Response Generation**:
   - A response JSON containing the assessment results, including the trust score, is returned.

4. **Error Handling**:
   - Any exceptions that occur during the assessment process are caught, and an error response is generated with details of the error.

This function provides a comprehensive assessment of the trustworthiness of the input URL by conducting various checks and calculations, encapsulating the results in a response dictionary.


## Documentation for `model.py`

The `model.py` file contains various functions responsible for conducting different checks and calculations to determine the trustworthiness of a URL. Below is a detailed explanation of each function's purpose and functionality:

### Global Variables
- `BASE_SCORE`: This variable holds the default trust score for a URL out of 100. It is initialized to 50.
- `PROPERTY_SCORE_WEIGHTAGE`: This dictionary holds the weightage of different properties in determining the trust score. Score is added according to the weightage given for each parameters, the value of the weightage is found out through trials and referring papers (there is no any standard value for it).

### Function: `validate_url(url)`
This function checks whether the provided URL is active by making a request to it. It returns the HTTP response status code if the URL is reachable; otherwise, it returns `False`.

### Function: `include_protocol(url)`
This function ensures that the URL provided has a protocol prefix (HTTP or HTTPS). If not, it appends 'https://' as the default protocol.

### Function: `get_domain_rank(domain)`
This function retrieves the domain rank from a precompiled list of the top 1 million domains. If the domain is found in the list, its rank is returned; otherwise, 0 is returned.

### Function: `whois_data(domain)`
This function retrieves WHOIS data for the given domain, including creation date, expiration date, and other relevant information.

### Function: `hsts_support(url)`
This function checks whether the provided URL supports HTTP Strict Transport Security (HSTS) by examining the response headers. It returns 1 if HSTS is supported; otherwise, it returns 0.

### Function: `is_url_shortened(domain)`
This function checks whether the provided domain is a URL shortening service by comparing it against a list of known URL shorteners. It returns 1 if the domain is a URL shortener; otherwise, it returns 0.

### Function: `ip_present(url)`
This function checks whether an IP address is present in the provided URL. It returns 1 if an IP address is present; otherwise, it returns 0.

### Function: `url_redirects(url)`
This function checks whether the provided URL redirects to another URL. If redirection occurs, it returns an array of redirected URLs; otherwise, it returns 0.

### Function: `too_long_url(url)`
This function checks whether the provided URL is too long by comparing its length to a predefined threshold. It returns 1 if the URL is too long; otherwise, it returns 0.

### Function: `too_deep_url(url)`
This function checks whether the provided URL has a deep hierarchy by counting the number of slashes in the URL path. If the number exceeds a predefined threshold, it returns 1; otherwise, it returns 0.

### Function: `content_check(url)`
This function analyzes the content of the provided URL's webpage for various potentially malicious elements, such as onmouseover events, right-click disabling, presence of forms, iframes, login keywords, and pop-ups. It returns a dictionary indicating the presence of each element.

### Function: `phishtank_search(url)`
This function searches the Phishtank database to determine if the provided URL is listed as a phishing link. It returns 1 if the URL is found in the database; otherwise, it returns 0.

### Function: `get_ip(domain)`
This function retrieves the IP address associated with the provided domain.

### Function: `get_certificate_details(domain)`
This function retrieves SSL certificate details for the provided domain, including issuer information, validity period, revocation status, cipher suite, and SSL/TLS version.

### Function: `calculate_trust_score(current_score, case, value)`
This function calculates the trust score based on the provided parameters. It adjusts the current score based on the specific case and value passed to it.

This module provides a comprehensive set of functions for analyzing various aspects of a URL to determine its trustworthiness.

## Documentation for `onetimescript.py`

The `onetimescript.py` file is a one-time script used to update the `sorted-top1million.txt` and `domain-rank.json` files with the latest list of top 1 million websites. The purpose of this script is to maintain an updated list of the top 1 million websites, which can be used for the URL assessment.

Below is a detailed explanation of how the script functions:

### Function: `create_sorted_arr_and_dict()`

This function is responsible for updating the two files with the latest data. It performs the following steps:

1. **Reading Data from CSV**:
   - It reads the data from the `top-1m.csv` file, which contains the list of the top 1 million websites along with their ranks.

2. **Populating Arrays and Dictionary**:
   - It populates two data structures:
     - `domain_data_array`: This list contains the domain names extracted from the CSV file.
     - `domain_data_dict`: This dictionary maps each domain name to its rank.

3. **Sorting**:
   - It sorts the `domain_data_array` alphabetically to create a sorted list of domain names.

4. **Clearing Existing Files**:
   - It clears the contents of the existing `sorted-top1million.txt` and `domain-rank.json` files.

5. **Writing Data to Files**:
   - It writes the sorted domain names to the `sorted-top1million.txt` file.
   - It writes the domain-rank dictionary to the `domain-rank.json` file in JSON format.

### If you want to update the list and JSON on your local machine, follow these steps:
1. **Download Latest Data**: Obtain the latest `top-1m.csv` file from [Tranco List](https://tranco-list.eu/). This CSV file is updated monthly.
2. **Update Local Files**: Copy the downloaded `top-1m.csv` file to the `/static/data/` directory.
3. **Execute Script**: Run the `onetimescript.py` file. The script will automatically read the `top-1m.csv` file, extract relevant data, and update the `sorted-top1million.txt` and `domain-rank.json` files. The execution time of the script varies but typically takes about 10-20 seconds to complete.

### Last Updated
The script was last executed with the latest `top-1m.csv` file on: 2024-03-04

This script provides a convenient way to update the files containing the list of top 1 million websites, facilitating the assessment of URLs based on their domain ranks.


[Go back to SafeSurf Documentation](README.md#learn-and-contribute-to-the-project)

<img src="static/safesurf-normal.png"  width="350" height="88">


# SafeSurf

A phishing domain detection tool that also allows you to safely view the website without actually visiting it. Built using Python. With SafeSurf, you can quickly identify suspicious websites and protect yourself from phishing attacks.


## Features

These are the features provided by SafeSurf to its users.
- The website is easy to use, with a simple interface that anyone can navigate.
- Users can see the preview of the website without actually visiting it.
- SafeSurf gives a trust score to the URL, which will provide the user an understanding of the trustability and authenticity of the domain.
- The URL is checked with a phish database (PhishTank) to see whether it is a reported phishing link.
- SafeSurf provides crucial details (WHOIS, SSL and general) regarding the domain, which will help the user to get a basic understanding of the URL.

## Demo

https://safesurf.vercel.app

<img src="static/safesurf-screenshot.png"  width="350" height="175">
<br>

## Local Setup
If you find this project useful or interesting, please consider starring it and putting it on your watch list.
To run the application on your system, follow these steps:

1. Clone the repository: 

```shell
git clone https://github.com/incogGod/SafeSurf.git
cd SafeSurf
```

2. Install the dependencies: 

```shell
pip install -r requirements.txt
```

3. Start the Flask app: 

```shell
python app.py
```

4. Open your web browser and go to http://localhost:5000 to use the application locally.

## Contributing

Contributions are always welcome. If you find this project useful or interesting, please consider starring it and putting it on your watch list. If you want to contribute to the project, here's how you can do it:

1. Fork the repository to your GitHub account
2. Clone the forked repository to your local machine: 

```shell
git clone https://github.com/yourusername/SafeSurf.git
```

3. Create a new branch for your changes:

```shell
git checkout -b my-feature-branch
```

4. Make your changes to the code
5. Commit your changes: 

```shell
git commit -m "Added a new feature"
```

6. Push your changes to your forked repository: 

```shell
git push origin my-feature-branch
```

7. Create a pull request from your forked repository to the main repository
8. Wait for your changes to be reviewed and merged
   

<!-- Before beginning to work on the feature, please [create an issue](https://github.com/incogGod/SafeSurf/issues) and get assigned. -->

## Feedback

If you have any feedback or suggestions, please reach out at https://abhishekkp.com/contact/ or start a discussion on [SafeSurf Discussions](https://github.com/abhizaik/SafeSurf/discussions).

Any input is highly appreciated.


<!-- ## Authors

- [@incogGod](https://www.github.com/incogGod) -->





<!-- # URL Assessment Criteria

## Traffic Volume Ranking
Most authentic websites are usually have good traffic volumne. -->
<!-- 
A Research-Oriented Top Sites Ranking Hardened Against Manipulation. This list aggregates the top 1M ranks from the lists provided by Alexa, Umbrella, Majestic, and Farsight from 16 February 2023 to 17 March 2023 (30 days). 
May be later we can integrate tranco into code instead of using the CSV to always get the latest 1M list.
[tranco website](https://tranco-list.eu/)  
-->

<!-- ## Age of Domain
Using who is get the domain age. If domain is less than 2 years old might not be a very authentic website.

## URL Shortner 
Check whether the original URL is hidden using any URL shortening services. 

## HSTS Support
Check whether the domain has HTTPS, HSTS support. Authentic domains often have HSTS support.

## Presence of IP Address Instead of Domain
Phishing links may have IP address instead of domain names. All authentic domains have dedicated domain names.

## URL Redirects to Other Page
If the URL is redirected to any other page, attacker may be trying to hide the original phishing link.

## Too Long URL
If the URL length is greater than 75, it may be a phishing website and attacker may be trying to hide the sketchy part from the address bar.

## Depth of URL
If the the depth of URL (number of /) is more than usual, chances that the URL is a phishing link is high. Legit websites don't usually keep too many sub pages. -->

<!-- ## Presence of onmouseover, iframe, right-click disabling, forms, popups etc.
Except forms all these things are bit shady. So if a website is having any of these they might be trying to hide something or divert your attention.

presence of keywords like : login, password, card details, email etc. in website content and url)
subdomain with legit name / login or secure
presence of long string/ random characters in url
presence of unicode charector in domain to look like legit website
similarity to legitimate domain
domain reputation in public blacklists
domain registrars with loose policies
ip address reputation
ssl certificate validity (self signed / invalid check)
unusual extension (.tk,pw) TLD
non standard url
pop ups
presence of email address in url 
env : phishing-env
 -->

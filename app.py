from flask import Flask, request, render_template, send_file
from io import BytesIO
from bs4 import BeautifulSoup
import requests
import urllib.parse
from urllib.parse import urljoin
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import controller

app = Flask(__name__)
@app.route('/',  methods=['GET','POST'])
def home():
    
    try:
        url = request.form['url']
        result = controller.main(url)
        output = result
    except:
        output = 'NA'

    return render_template('index.html', output=output)


@app.route('/screenshot')
def screenshot():
    try:

        # set up the headless browser
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        driver = webdriver.Chrome(options=options)

        # navigate to the website
        driver.get('https://www.google.com')

        # take a screenshot
        screenshot = driver.get_screenshot_as_png()

        # close the browser
        driver.quit()

        # convert the screenshot to a bytes object
        screenshot_bytes = BytesIO(screenshot)

        # return the screenshot as an image
        return send_file(screenshot_bytes, mimetype='image/png')
    except Exception as e:
        return  f"Error: {e}"

# @app.route('/result', methods=['POST'])
# def result():
#     url = request.form['url']
#     print(url)
#     result = controller.main(url)
#     output = result

#     return render_template('result.html', output=output)


@app.route('/preview/<path:url>')
def preview(url):
    try:
        # url = urllib.parse.unquote(url, encoding='ISO-8859-1')
        url = 'https://' + url
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')

        # inject external resources into HTML
        for link in soup.find_all('link'):
            if link.get('href'):
                link['href'] = urljoin(url, link['href'])
        for script in soup.find_all('script'):
            if script.get('src'):
                script['src'] = urljoin(url, script['src'])
        for img in soup.find_all('img'):
            if img.get('src'):
                img['src'] = urljoin(url, img['src'])

        return render_template('preview.html', content=soup.prettify())
    except Exception as e:
        return  f"Error: {e}"


if __name__ == '__main__':
    app.run(debug=True)
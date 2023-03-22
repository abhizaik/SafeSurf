from flask import Flask, request, render_template
from bs4 import BeautifulSoup
import requests
from urllib.parse import urljoin, quote, unquote
import controller

app = Flask(__name__)
@app.route('/')
def home():
    return render_template('index.html')


@app.route('/result', methods=['POST'])
def result():
    url = request.form['url']
    print(url)
    result = controller.main(url)
    output = result

    return render_template('result.html', output=output)


@app.route('/preview/<path:url>')
def preview(url):
    try:
        url = unquote(url)
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
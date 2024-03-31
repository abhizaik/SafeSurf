from flask import Flask, request, render_template
from bs4 import BeautifulSoup
import requests
from urllib.parse import urljoin
from controller import Controller
import onetimescript
from db import db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///domains.db'
db.init_app(app)
with app.app_context():
    db.create_all() 

controller = Controller()


@app.route('/',  methods=['GET','POST'])
def home():
    
    try:
        url = request.form['url']
        result = controller.main(url)
        output = result
    except:
        output = 'NA'

    return render_template('index.html', output=output)


@app.route('/preview', methods=['POST'])
def preview():
    try:
        url = request.form.get('url')
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')

        # inject external resources into HTML
        for link in soup.find_all('link'):
            if link.get('href'):
                link['href'] = urljoin(url, link['href'])
        
        # Uncomment this if you want to enable script
        # for script in soup.find_all('script'):
        #     if script.get('src'):
        #         script['src'] = urljoin(url, script['src'])

        for img in soup.find_all('img'):
            if img.get('src'):
                img['src'] = urljoin(url, img['src'])

        return render_template('preview.html', content=soup.prettify())
    except Exception as e:
        return  f"Error: {e}"


@app.route('/source-code', methods=['GET','POST'])
def view_source_code():

    try:
        url = request.form.get('url')
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        formatted_html = soup.prettify()
        
        return render_template('source_code.html', formatted_html = formatted_html, url = url)
    
    except Exception as e:
        return  f"Error: {e}"

@app.route('/update-db')
def update_db(): 
    try:
        with app.app_context():
            response = onetimescript.update_db()
            print("Database populated successfully!")
            return response, 200
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return "An error occurred: " + str(e), 500

@app.route('/update-json')
def update_json(): 
    try:
        with app.app_context():
            response = onetimescript.update_json()
            print("JSON updated successfully!")
            return response, 200
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return "An error occurred: " + str(e), 500


if __name__ == '__main__':
    app.debug = True
    app.run()
from flask import Flask, render_template, request
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin  # modified import

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html', links=None)

@app.route('/scan', methods=['POST'])
def scan():
    url = request.form['url']
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        # Use urljoin to combine the base URL with each href
        links = [urljoin(url, a['href']) for a in soup.find_all('a', href=True)]
        return render_template('index.html', links=links)
    except Exception as e:
        return f"An error occurred: {e}"

if __name__ == '__main__':
    app.run(debug=True)

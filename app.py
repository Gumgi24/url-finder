from flask import Flask, render_template, request
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse  # added

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
        links = [urlparse(a['href']).path for a in soup.find_all('a', href=True) if urlparse(a['href']).path]
        return render_template('index.html', links=links)
    except Exception as e:
        return f"An error occurred: {e}"

if __name__ == '__main__':
    app.run(debug=True)

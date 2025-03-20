from flask import Flask, render_template, request
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
from collections import defaultdict
import re

app = Flask(__name__)

def is_valid_url(url):
    regex = re.compile(
        r'^(?:http|https)://'  # http:// or https://
        r'\w+(?:\.\w+)+'
    )
    return re.match(regex, url)

PAGE_SIZE = 5

@app.route('/')
def index():
    return render_template('index.html', domain_groups=None, page=1, total_pages=0, search_query="")

@app.route('/scan', methods=['POST'])
def scan():
    url = request.form['url']
    if not is_valid_url(url):
        return "Invalid URL provided.", 400

    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        links = [urljoin(url, a['href']) for a in soup.find_all('a', href=True)]

        # Group links by domain
        domain_groups = defaultdict(list)
        for link in links:
            domain = urlparse(link).netloc
            domain_groups[domain].append(link)
        domain_groups = dict(domain_groups)

        # Sort domains and paginate
        sorted_domains = sorted(domain_groups.keys())
        page = int(request.args.get('page', 1))
        total_pages = (len(sorted_domains) + PAGE_SIZE - 1) // PAGE_SIZE
        start = (page - 1) * PAGE_SIZE
        end = start + PAGE_SIZE
        paginated_domains = sorted_domains[start:end]
        paginated_groups = {domain: domain_groups[domain] for domain in paginated_domains}

        return render_template('index.html', domain_groups=paginated_groups, page=page, total_pages=total_pages, search_query="")
    except Exception as e:
        return f"An error occurred: {e}"

if __name__ == '__main__':
    app.run(debug=True)

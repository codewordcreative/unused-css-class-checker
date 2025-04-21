import requests
import re
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup

# Set sitemap and site-wide universal CSS locations to compare here
main_sitemap_url = 'https://yourdomain.com/sitemap.xml'
css_url = 'https://yourdomain.com/wp-content/uploads/oxygen/css/universal.css'

# Custom user agent 
headers = {
    'User-Agent': 'csstest'
}

# Sorrynotsorry for suppressing this warning, because it does not matter
from bs4 import XMLParsedAsHTMLWarning
import warnings
warnings.filterwarnings("ignore", category=XMLParsedAsHTMLWarning)

def get_html_classes(html):
    soup = BeautifulSoup(html, 'html.parser')
    all_classes = set()
    for element in soup.find_all(class_=True):
        for cls in element.get('class'):
            all_classes.add(cls.lstrip('.'))
    return all_classes

# Extract class names from the CSS file defined above
def get_css_classes(css_url):
    response = requests.get(css_url, headers=headers)
    if response.status_code == 200:
        matches = re.findall(r'(?<![a-zA-Z0-9_-])(?:\.[a-zA-Z_][a-zA-Z0-9_-]*)(?![a-zA-Z0-9_-])', response.text)
        return set(cls.lstrip('.') for cls in matches)
    else:
        print(f"Failed to fetch CSS file: {css_url}, status code: {response.status_code}")
        return set()

# Extract URLs from sitemap or index defined above
def get_urls(sitemap_url):
    response = requests.get(sitemap_url, headers=headers)
    if response.status_code != 200:
        print(f"Failed to fetch sitemap: {sitemap_url}, status code: {response.status_code}")
        return []

    try:
        root = ET.fromstring(response.content)
        ns = {'sm': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
        urls = [loc.text for loc in root.findall('.//sm:loc', ns)]
        nested_sitemaps = [url for url in urls if url.endswith('.xml')]
        for nested_sitemap in nested_sitemaps:
            urls.extend(get_urls(nested_sitemap))
        return urls
    except ET.ParseError as e:
        print(f"XML parsing error in sitemap {sitemap_url}: {e}")
        return []

all_urls = set()
all_html_classes = set()

# Extract all URLs from the main sitemap (including nested sitemaps)
sitemap_urls = get_urls(main_sitemap_url)

# Track processed URLs
processed_urls = set()

# Crawl URLs and extract classes in HTML (note that JS is NOT checked)
for page_url in sitemap_urls:
    if page_url not in processed_urls:
        print(f"\nCrawling page: {page_url}")
        page_response = requests.get(page_url, headers=headers)
        if page_response.status_code == 200:
            html_classes = get_html_classes(page_response.text)
            all_html_classes.update(html_classes)
            all_urls.add(page_url)
            processed_urls.add(page_url)
        else:
            print(f"  Failed to crawl: {page_url}, status code: {page_response.status_code}")
    else:
        print(f"  Already processed, skipped: {page_url}")

# Extract classes from the site-wide CSS defined above
css_classes = get_css_classes(css_url)

# Compare and reveal possibly unused CSS classes
unused_classes = css_classes - all_html_classes

# Tada
print(f"\n=== Unused CSS classes ({len(unused_classes)} found) ===")
if unused_classes:
    for css_class in sorted(unused_classes):
        print(f".{css_class}")
else:
    print("All CSS classes are used.")

print(f"\n=== Summary ===")
print(f"Total URLs crawled: {len(all_urls)}")
print(f"Total unique CSS classes: {len(css_classes)}")
print(f"Total unique HTML classes found: {len(all_html_classes)}")
print(f"Unused CSS classes: {len(unused_classes)}")

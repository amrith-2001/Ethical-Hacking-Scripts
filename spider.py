#!/usr/bin/env python
import requests
import re
import urlparse

target_url = "http://10.0.2.5/mutillidae/"
target_links = []

def extract_links(url):
    response = requests.get(target_url)
    return re.findall('(?:href=")(.*?)"', response.content)

def crawl(url):
    href_links = extract_links(url)
    for link in href_links:
        link = urlparse.urljoin(url, link)

        if "#" in link:  #in case of multiple links displaying same info
            link = link.split('#')[0]

        if url in link and link not in target_links:
            target_links.append(link)
            print(link)
            crawl(link)

crawl(target_url)


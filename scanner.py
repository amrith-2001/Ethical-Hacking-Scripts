#!/usr/bin/env python

import requests
import re
import urlparse
from bs4 import BeautifulSoup


class Scanner:
    def __init__(self, url, ignore_links):
        self.session = requests.Session()
        self.target_url = url
        self.target_links = []
        self.links_to_ignore = ignore_links

    def extract_links(self, url):
        response = self.session.get(url)
        return re.findall('(?:href=")(.*?)"', response.content)

    def crawl(self, url=None):
        if url == None:
            url = self.target_url
        href_links = self.extract_links(url)
        for link in href_links:
            link = urlparse.urljoin(url, link)

            if "#" in link:  # in case of multiple links displaying same info
                link = link.split('#')[0]

            if self.target_url in link and link not in self.target_links and link not in self.links_to_ignore:
                self.target_links.append(link)
                print(link)
                self.crawl(link)

    def extract_form(self, url):
        response = self.session.get(url)
        parsed_html = BeautifulSoup(response.content, features='lxml')
        return parsed_html.findAll('form')

    def submit_form(self, form, value, url):
        action = form.get('action')
        post_url = urlparse.urljoin(url, action)
        method = form.get('method')

        inputs_list = form.findAll('input')  # since input is a separate html tag
        post_data = {}
        for inputs in inputs_list:
            input_name = inputs.get('name')
            input_type = inputs.get("type")
            input_value = inputs.get("value")
            if input_type == "text":  # that is if it is of type submit ,then do nothing
                input_value = value

            post_data[input_name] = input_value
        if method == "post":  #since all forms may not be of post
            return self.session.post(post_url, data=post_data)
        return self.session.get(post_url, params=post_data)

    def run_scanner(self):
        for link in self.target_links:
            forms = self.extract_form(link)
            for form in forms:
                print("[+] Testing form in " + link)
                is_vulnerable_to_xss = self.test_xss_in_form(form, link)
                if is_vulnerable_to_xss:
                    print("\n\n[***] XSS discovered in " + link + " in the following form")
                    print(form)

            if "=" in link:  #if link sends data to the website i.e get request
                print("[+] Testing " + link)
                is_vulnerable_to_xss = self.test_xss_in_links(link)
                if is_vulnerable_to_xss:
                    print("\n\n[***] XSS discovered in " + link)

    def test_xss_in_form(self, form, url):
        xss_test_script = "<sCript>alert('XSS')</scriPt>"
        response = self.submit_form(form, xss_test_script, url)
        return xss_test_script in response.content

    def test_xss_in_links(self, url):
        xss_test_script = "<sCript>alert('XSS')</scriPt>"
        url = url.replace("=", "=" + xss_test_script)
        response = self.session.get(url)
        return xss_test_script in response.content




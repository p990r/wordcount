from urllib.request import urlopen
from bs4 import BeautifulSoup as bs
import re


class UrlObj:
    def get_page(self):
        try:
            return urlopen(self.url, timeout = 2).read()
        except:
            return None

    @staticmethod
    def parse_html(page):
        try:
            return bs(page, features="html.parser")
        except AttributeError:
            return None

    @staticmethod
    def decode_html(html):
        # kill all script and style elements
        for script in html(["script", "style"]):
            script.extract()  # rip it out
        # get text
        text = html.get_text()
        # break into lines and remove leading and trailing space on each
        lines = (line.strip() for line in text.splitlines())
        # break multi-headlines into a line each
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        # drop blank lines
        text = '\n'.join(chunk for chunk in chunks if chunk)
        return text

    @staticmethod
    def split_words(list):
        words = []
        string_list = re.split('[^a-z]', list)
        for elem in string_list:
            words.append(re.sub('[^a-z]', '', elem))
        return words

    @staticmethod
    def make_words_list(text):
        words = []
        strings = text.lower().split()
        for string in strings:
            words_list = UrlObj.split_words(string)
            for val in words_list:
                words.append(val)
        return words

    def __init__(self, url):
        self.url = url
        self.words_set = set()
        self.page = self.get_page()

        if (self.page):
            self.html = self.parse_html(self.page)
            self.text = self.decode_html(self.html)
            self.words = self.make_words_list(self.text)
            self.words_set = set(self.words)
        else:
            print('Error: ' + url + ' does not exist')
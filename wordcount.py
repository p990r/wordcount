from urllib.request import urlopen
from urllib.error import HTTPError, URLError
from bs4 import BeautifulSoup as bs
import re
import concurrent.futures
import time


def text_to_list(path):
    list = []
    file = open(path, "r")
    for line in file:
        list.append(line)
    file.close()
    return list


def get_page(url):
    try:
        return urlopen(url, timeout = 2).read()
    except (HTTPError, URLError):
        return None


def parse_html(page):
    try:
        return bs(page, features="html.parser")
    except AttributeError:
        return None


def decode_html(page):
    # kill all script and style elements
    for script in page(["script", "style"]):
        script.extract()  # rip it out
    # get text
    text = page.get_text()
    # break into lines and remove leading and trailing space on each
    lines = (line.strip() for line in text.splitlines())
    # break multi-headlines into a line each
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    # drop blank lines
    text = '\n'.join(chunk for chunk in chunks if chunk)
    return text


def page_to_words(page):
    words = []
    html = parse_html(page)
    text = decode_html(html)
    strings = text.lower().split()
    for string in strings:
        string_list = re.split('[^a-z]', string)
        for str in string_list:
            words.append(re.sub('[^a-z]', '', str))
    return words


def make_set(url):
    page = get_page(url)
    if (page):
        words_list = page_to_words(page)
        words_set = set(words_list)
    else:
        print('Error: ' + url + ' does not exist')
        return set()
    return words_set


def main():
    start = time.time()

    path = 'wordcount-urls.txt' # path to url text file
    urls = text_to_list(path)
    union_set = set()

    with concurrent.futures.ProcessPoolExecutor() as executor:
        words_sets = executor.map(make_set, urls)

    words_sets = list(words_sets)
    for words_set in words_sets:
        union_set = set.union(union_set, words_set)

    print('Number of tokens: ' + str(len(union_set)))

    end = time.time()
    print('Time: ' + str(end - start) + ' seconds')

if __name__ == '__main__':
    main()

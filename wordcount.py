import concurrent.futures
import time
import urlObj


def text_to_list(path):
    list = []
    file = open(path, "r")
    for line in file:
        list.append(line)
    file.close()
    return list


def make_set(url):
    obj = urlObj.UrlObj(url)
    return obj.words_set


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

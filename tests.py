"""
This class contains unit testing to graphics functions
"""

import urlObj
import unittest


class MyTest(unittest.TestCase):
    obj1 = urlObj.UrlObj('http://www.wikipedia.org')
    obj2 = urlObj.UrlObj('http://www.wikipedia.org/bhkafjdkhafjdafhjdkafhjkdaefkhyj') # this page shouldn't exist

    def test_get_page(self):
        self.assertEqual(None, self.obj2.page)
        self.assertEqual(self.obj1.page, self.obj1.get_page())

    def test_decode_html(self):
        self.assertEqual(self.obj1.text, self.obj1.decode_html(self.obj1.html))

    def test_split_words(self):
        self.assertEqual(['abc', 'def','hij'], urlObj.UrlObj.split_words('abc5def hij'))

    def test_make_words_list(self):
        self.assertEqual(['', '', '', '', 'abc', 'de', 'xyz', '', ''], urlObj.UrlObj.make_words_list('123 abc1de xyz77'))


if __name__ == '__main__':
    unittest.main()
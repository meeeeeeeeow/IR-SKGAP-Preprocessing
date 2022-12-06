from main import foo
import unittest
from clustering import Clustering
from nltk.stem import PorterStemmer


class BasicTest(unittest.TestCase):
    def test_foo(self):
        assert foo()

    def test_something(self):
        assert True

    def test_clustering(self):
        def Preprocessing(filename):
            # Tokenization
            line = []
            j = 0
            with open('./data/%s' % filename) as f:
                lines = f.readlines()
                for i in lines:
                    line.append([])
                    line[j] = i.split()
                    j += 1

            Punctuation_Marks = '[.,"\'-?:!;`]()'
            Numbers = '0123456789'
            words = []
            for i in range(len(line)):
                for j in range(len(line[i])):
                    for k in line[i][j]:
                        if k in Punctuation_Marks:
                            line[i][j] = line[i][j].replace(k, "")
                    for l in line[i][j]:
                        if l in Numbers:
                            line[i][j] = line[i][j].replace(l, "")

            for i in line:
                for j in range(len(i)):
                    words.append(i[j])
            # Lowercase
            for i in range(len(words)):
                words[i] = words[i].lower()

            # Stem from Porter's algorithm and stop word removal
            stemmer = PorterStemmer()
            singles = [stemmer.stem(word) for word in words]
            # Import the stop word
            stop_word = []
            with open('./NTLK list of English stopwords.txt') as f:
                lines = f.readlines()
                for i in lines:
                    temp = i.split()
                    stop_word.append(temp[0])
            single = singles.copy()
            for i in singles:
                if i in stop_word:
                    single.remove(i)
            extra_remove = ['`', '_', ' ', ""]
            for i in singles:
                if i in extra_remove:
                    single.remove(i)

            return single

        CAs = {'title1': Preprocessing('4.txt'), 'title2': Preprocessing(
            '5.txt'), 'title3': Preprocessing('6.txt')}

        print(Clustering(CAs))
        assert True

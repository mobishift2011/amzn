#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" testing cross-validation and speed for different frameworks

framwork used:

*   sklearn. bayes, svm, knn
*   pattern. bayes, svm, knn
*   nltk

"""
import os
import re
DIRNAME = os.path.dirname(os.path.abspath(__file__)) 
DATAPATH = os.path.join(DIRNAME, 'dataset')

import time
import sklearn
import sklearn.svm
import sklearn.naive_bayes
import sklearn.neighbors
import sklearn.datasets
import pattern
import pattern.vector

class Classifier(object):
    def __init__(self, name):
        self.name = name

    def load_files(self):
        pass

    def classify(self, text):
        pass

    def validate(self):
        pass

words = re.compile(ur'\b\w+\b')
def adjacent_words_tokenizer(doc):
    l = words.findall(doc)
    for i in range(len(l)):
        yield l[i]

class SklearnClassifier(Classifier):
    def __init__(self, clf=None):
        self.name = 'sklearn'
        self.x = None
        self.y = None
        self.clf = {
            'svm':sklearn.svm.LinearSVC(),
            'bayes':sklearn.naive_bayes.MultinomialNB(),
            'knn':sklearn.neighbors.KNeighborsClassifier(5, weights='uniform'),
        }.get(clf, sklearn.svm.LinearSVC())
        self.trained = False
        self.vectorizer = False
        self.target_names = None
        
    def load_files(self):
        files = sklearn.datasets.load_files(DATAPATH)
        self.vectorizer = sklearn.feature_extraction.text.TfidfVectorizer(tokenizer=adjacent_words_tokenizer)
        self.x = self.vectorizer.fit_transform(files.data)
        self.y = files.target
        self.target_names = files.target_names

    def validate(self):
        return sklearn.cross_validation.cross_val_score(self.clf, self.x, self.y, cv=5)         

    def classify(self, text):
        if not self.trained:
            self.trained = True
            self.clf.fit(self.x, self.y)
        
        ret = []
        index = list(self.clf.predict(self.vectorizer.transform([text])))[0]
        return self.target_names[index]

class PatternClassifier(Classifier):
    def __init__(self, clf=None):
        self.name = 'pattern'
        self.clf = {
            'svm':pattern.vector.SVM(),
            'bayes':pattern.vector.Bayes(),
            'knn':pattern.vector.kNN(),
        }.get(clf, pattern.vector.SVM())
        self.corpus = None
    
    def load_files(self):
        self.corpus = pattern.vector.Corpus()
        for p1 in os.listdir(DATAPATH):
            directory = os.path.join(DATAPATH, p1)
            if os.path.isdir(directory):
                for p2 in os.listdir(directory):
                    path = os.path.join(DATAPATH, p1, p2)
                    content = open(path).read()
                    self.clf.train(content,p1)
                    self.corpus.append(pattern.vector.Document(content, type=p1))
    
    def classify(self, text):
        return self.clf.classify(text)

    def validate(self):
        return self.clf.test(self.corpus, d=0.8, folds=5)

class NltkClassifier(Classifier):
    def __init__(self, clf=None):
        self.name = 'nltk'

def test_validation():
    """ testing different package's accurracy, coverage, ... """
    for Clf in [SklearnClassifier, PatternClassifier]:
        for method in ['bayes', 'knn', 'svm']:
            print
            print
            print
            print '='*10, Clf.__name__, method, '='*10
            t1 = time.time()
            c = Clf(method) 
            c.load_files()
            t2 = time.time()
            print 'loading time', t2 - t1
            print 'validatin result', c.validate()
            t3 = time.time()
            print 'validating time', t3 - t2

def main():
    test_validation()
    return
    c = SklearnClassifier('bayes')
    c.load_files()
    s = '''Measurements: shoulder to hemline 36&quot;, sleeve length 25.5&quot;, taken from size S\nAuthentic product'''
    print c.classify(s)

if __name__ == '__main__':
    main()

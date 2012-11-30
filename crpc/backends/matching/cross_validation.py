#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" testing cross-validation and speed for different frameworks

framwork used:

*   sklearn. bayes, svm, knn
*   pattern. bayes, svm, knn
*   nltk

"""
DATAPATH = 'dataset'

import time
import sklearn
import sklearn.svm
import sklearn.naive_bayes
import sklearn.neighbors
import sklearn.datasets
#from pattern.vector import Bayes, SVM, kNN, Document, Corpus

class Classifier(object):
    def __init__(self, name):
        self.name = name

    def load_files(self):
        pass

    def classify(self, text):
        pass

    def validate(self):
        pass

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
        self.vectorizer = sklearn.feature_extraction.text.TfidfVectorizer()
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
            
def test_validation():
    for Clf in [SklearnClassifier]:
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
    #test_validation()
    #return
    c = SklearnClassifier('bayes')
    c.load_files()
    s = '''Measurements: shoulder to hemline 36&quot;, sleeve length 25.5&quot;, taken from size S\nAuthentic product'''
    print c.classify(s)

if __name__ == '__main__':
    main()

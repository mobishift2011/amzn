#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" Department Classifier/Cross Validation

>>> from backends.matching.classifier import Classifier
>>> c = Classifier()
>>> c.load_from_database()
>>> c.classify('this is some text need to be classified')
(u'Women', u'Shoes')

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
import sklearn.metrics
import pattern
import pattern.vector
from pprint import pprint

from models import RawDocument

class Classifier(object):
    def __init__(self, name):
        self.name = name

    def load_files(self):
        pass

    def classify(self, text):
        pass

    def validate(self):
        pass

class TrainSet(object):
    """ a sturcture similar to sklearn's load_files structure """
    def __init__(self):
        self.target_names = []
        self.target = []
        self.data = []


class SklearnClassifier(Classifier):
    """ Wraps sklearn's API to pattern.vector's style
    
    >>> clf = SklearnClassifier(clf='svm') # can be bayes/knn, defaults to svm
    >>> clf.train('big lion', 'lion')
    >>> clf.train('moutain lion', 'lion')
    >>> clf.train('moutain mastiff', 'mastiff')
    >>> clf.train('tibet mastiff', 'mastiff')
    >>> clf.classify('water mastiff')
    mastiff

    """
    def __init__(self, clf=None):
        self.name = 'sklearn'
        self.trainset = TrainSet()
        self.x = None
        self.y = None
        self.clf = {
            'svm':sklearn.svm.LinearSVC(),
            'svm-rbf':sklearn.svm.SVC(),
            'bayes':sklearn.naive_bayes.MultinomialNB(),
            'knn':sklearn.neighbors.KNeighborsClassifier(5, weights='uniform'),
        }.get(clf, sklearn.svm.LinearSVC())
        self.transformed = False
        self.vectorizer = None

    def load_files(self):
        self.trainset = sklearn.datasets.load_files(DATAPATH)
        self.vectorizer = sklearn.feature_extraction.text.TfidfVectorizer()
        self.transformed = False

    def transform(self):
        """ vectorize all and fit the classifier """
        self.x = self.vectorizer.fit_transform(self.trainset.data)
        self.y = self.trainset.target
        self.clf.fit(self.x, self.y)
        self.transformed = True

    def train(self, rawdocument, type, strict=False):
        """ train a document to a type 

        :param rawdocument: a str of document
        :param type: category of the rawdocument, can be string or whatever(?)
        :param strict:  Whether perform similarity check on receive, default to False
                        Enable this is very costly, only enable it when training interactively

        returns True on success or False

        """
        if not self.vectorizer:
            self.vectorizer = sklearn.feature_extraction.text.TfidfVectorizer()

        # we exclude identical training documents
        if strict and len(self.trainset.target_names)>1:
            if self.similar(rawdocument)[0] > 0.95:
                print '==> Warning, document too close to existing documents, ignored'
                print '==>', rawdocument
                print '==>'
                print '==>'
                return False
        
        self.trainset.data.append(rawdocument)

        try:
            index = self.trainset.target_names.index(type)
        except ValueError:
            # not in list
            index = len(self.trainset.target_names) 
            self.trainset.target_names.append(type)
           
        self.trainset.target.append(index) 
        self.transformed = False
        return True

    def validate(self):
        if not self.transformed:
            self.transform()
        return sklearn.cross_validation.cross_val_score(self.clf, self.x, self.y, cv=5)

    def classify(self, text):
        """ provided some raw documentation, return the 'type' it belongs to """
        if not self.transformed:
            try:
                self.transform()
            except ValueError:
                return self.trainset.target_names[0]
        
        ret = []
        index = list(self.clf.predict(self.vectorizer.transform([text])))[0]
        return self.trainset.target_names[int(index)]

    def similarities(self, text):
        """ returns an array of similarities to the given text """
        if not self.transformed:
            self.transform()

        v = self.vectorizer.transform([text])

        # dot production for distance
        cosine_similarities = sklearn.metrics.pairwise.linear_kernel(v, self.x).flatten()
        return cosine_similarities

    def similar(self, text):
        """ return a pair of (SIMILARITY, TEXT) """
        cosine_similarities = self.similarities(text)
        most_similar_doc_index = cosine_similarities.argsort()[-1]
        similarity = cosine_similarities[most_similar_doc_index]
        similar_text = self.trainset.data[most_similar_doc_index]
        return similarity, similar_text

    def similar_top10(self, text):
        cosine_similarities = self.similarities(text)
        top10 = []
        for index in cosine_similarities.argsort()[:-10:-1]:
            top10.append((cosine_similarities[index], self.trainset.data[index]))
        return top10

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

class FavbuyClassifier(object):
    def __init__(self, clf_class=SklearnClassifier, clf_method='svm'):    
        self.clf_class = clf_class
        self.clf_method = clf_method
        self.d0clf = clf_class(clf_method)
        self.d1clf = clf_class(clf_method)
        self.d2clf_dict = {}

    def load_from_database(self):
        for doc in RawDocument.objects():
            self.d0clf.train(doc.content, doc.d0)
            self.d1clf.train(doc.content, doc.d1)
            if not doc.d1 in self.d2clf_dict:
                self.d2clf_dict[doc.d1] = self.clf_class(self.clf_method)
            self.d2clf_dict[doc.d1].train(doc.content, doc.d2)
    
    def train(self, content, type):
        d0, d1, d2 = type
        self.d0clf.train(content, d0)
        self.d1clf.train(content, d1)
        if not d1 in self.d2clf_dict:
            self.d2clf_dict[d1] = self.clf_class(self.clf_method)
        self.d2clf_dict[d1].train(content, d2)
        return True

    def classify(self, content):
        d0 = self.d0clf.classify(content)
        d1 = self.d1clf.classify(content)
        if d1 in self.d2clf_dict:
            d2 = self.d2clf_dict[d1].classify(content)
        else:
            d2 = ""
        return d0, d1, d2

class FavbuyScorer(object):
    def classify(self, content):
        pass

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
    #test_validation()
    #return
    clf = SklearnClassifier()
    #clf.load_files()
    clf.load_from_database()
    pprint(clf.classify('''Material: 67% Polyester 28% Rayon 5% Spandex, Lining: 100% PolyesterApprox. measurements (size 4): sleeve length 24", shoulder to hem 38"Care: Dry cleanOrigin: Imported Fit: This brand runs true to size. To ensure the best fit, we suggest consulting the size chart.
Double-Breasted Long Belted Car Coat
Long car coat; Collarless neck; Topstitch detail; Long sleeves with button cuffs; Epaulet button tabs on shoulders; Double-breasted button front closure; Optional studded belt with chain tassel detail; Button-close front patch pockets; Vented slit at back hem; Fully lined
'''))

if __name__ == '__main__':
    main()

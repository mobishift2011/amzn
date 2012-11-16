'''
Created on 2012-11-6

@author: ethan
'''
from os import listdir, path

AWS_ACCESS_KEY = "AKIAIQC5UD4UWIJTBB2A"
AWS_SECRET_KEY = "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"
IMAGE_S3_BUCKET = 'product.image.favbuy'
IMAGE_ROOT = ''
URL_EXPIRES_IN = 60 * 60 * 24 * 365 * 50

"""
The same as the specific crawling name defined in the crawling folder.
"""
SITES = (
    'bluefly',
    'gilt',
    'hautelook',
    'myhabit',
    'nomorerack',
    'onekingslane',
    'ruelala',
    'zulily',
)
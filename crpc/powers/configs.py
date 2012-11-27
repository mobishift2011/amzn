'''
Created on 2012-11-6

@author: ethan
'''

DEBUG = True

AWS_ACCESS_KEY = "AKIAIQC5UD4UWIJTBB2A"
AWS_SECRET_KEY = "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"
IMAGE_S3_BUCKET = 'favbuy'
IMAGE_ROOT = ''
URL_EXPIRES_IN = 60 * 60 * 24 * 365 * 25    # S3 has an epoch time of 03:14 UTC on Tuesday, 19 January 2038.

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
    'venteprivee'
)

CATALOG_BASE_URL = 'http://localhost:1319/api'
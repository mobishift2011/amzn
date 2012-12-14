'''
Created on 2012-11-6

@author: ethan
'''

DEBUG = True

AWS_ACCESS_KEY 	= "AKIAIQC5UD4UWIJTBB2A"
AWS_SECRET_KEY 	= "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"
S3_IMAGE_BUCKET = 'image_favbuy'
IMAGE_ROOT 		= ''
S3_IMAGE_URL	= 'https://s3.amazonaws.com/{0}'.format(S3_IMAGE_BUCKET)
URL_EXPIRES_IN 	= 60 * 60 * 24 * 365 * 25    # S3 has an epoch time of 03:14 UTC on Tuesday, 19 January 2038.

"""
The same as the specific crawling name defined in the crawling folder.
"""
SITES = (
    'beyondtherack',
    'bluefly',
    'gilt',
    'hautelook',
    'ideeli',
    'myhabit',
    'nomorerack',
    'onekingslane',
    'ruelala',
    'zulily',
    'venteprivee',
    'modnique'
)

IMAGE_SIZE = {
	'Event': (
		{
			'width': 280,
			'height': 280,
		},
		{
			'width': 280,
			'height': 135,
		},
		{
			'width': 244,
			'height': 200,
		},
		{
			'width': 224,
			'height': 0,
		},
		{
			'width': 316,
			'height': 196,
		},
	),
	'Product': (
		{
			'width': 220,
			'height': 300,
			# 'fluid': True	# not fix, but the smaller size should fill the bound
		},
		{
			'width': 50,
			'height': 66,
		},
		{
			'width': 224,
			'height': 0,
		}
	)
}

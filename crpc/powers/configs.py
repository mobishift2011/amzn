'''
Created on 2012-11-6

@author: ethan
'''

DEBUG = True

AWS_ACCESS_KEY 	= "AKIAIQC5UD4UWIJTBB2A"
AWS_SECRET_KEY 	= "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"
S3_IMAGE_BUCKET = 'favbuy-images4'
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
    'modnique',
    'lot18',
    'totsy'
)

IMAGE_SIZE = {
	'Event': (
		{
			'width': 280,
			'height': 280,
            'background-color': '#e5e5e5',
            'thumbnail-policy': 'crop'
		},
		{
			'width': 280,
			'height': 136,
            'background-color': '#e5e5e5',
            'thumbnail-policy': 'crop'
		},
		{
			'width': 244,
			'height': 200,
            'background-color': '#e5e5e5',
            'thumbnail-policy': 'crop'
		},
		{
			'width': 224,
			'height': 0,
            'background-color': '#e5e5e5',
            'thumbnail-policy': 'scale-trim'
		},
		{
			'width': 316,
			'height': 196,
            'background-color': '#d6d6d6',
            'thumbnail-policy': 'crop'
		},
		# For iPhone
		{
			'width': 320,
			'height': 168,
            'background-color': '#e5e5e5',
            'thumbnail-policy': 'crop'
		},
		{
			'width': 156,
			'height': 82,
            'background-color': '#e5e5e5',
            'thumbnail-policy': 'scale-trim'
		},
	),
	'Product': (
		{
			'width': 244,
			'height': 200,
            'background-color': '#e5e5e5',
            'thumbnail-policy': 'scale-trim'
		},
		{
			'width': 50,
			'height': 50,
            'background-color': '#e5e5e5',
            'thumbnail-policy': 'crop'
		},
		{
			'width': 224,
			'height': 0,
            'background-color': '#e5e5e5',
            'thumbnail-policy': 'scale-trim'
		},
		# For iPhone
		{
			'width': 146,
			'height': 0,
            'background-color': '#e5e5e5',
            'thumbnail-policy': 'scale-trim'
		},
		{
			'width': 176,
			'height': 253,
            'background-color': '#e5e5e5',
            'thumbnail-policy': 'crop'
		},
		{
			'width': 320,
			'height': 460,
            'background-color': '#e5e5e5',
            'thumbnail-policy': 'crop'
		},
		{
			'width': 84,
			'height': 106,
            'background-color': '#e5e5e5',
            'thumbnail-policy': 'crop'
		},
	)
}

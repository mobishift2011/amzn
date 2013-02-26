# -*- coding: utf-8 -*-
from admin.models import Brand
import boto
from boto.s3.key import Key
from boto.s3.connection import S3Connection
import json
import os
from os import listdir, path

S3_IMAGE_BUCKET = 'favbuy-brand'
S3_IMAGE_URL	= 'https://s3.amazonaws.com/{0}'.format(S3_IMAGE_BUCKET)
AWS_ACCESS_KEY 	= "AKIAIQC5UD4UWIJTBB2A"
AWS_SECRET_KEY 	= "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"

policy = {
  "Version": "2008-10-17",
  "Statement": [{
    "Sid": "AllowPublicRead",
    "Effect": "Allow",
    "Principal": { "AWS": "*" },
    "Action": ["s3:GetObject"],
    "Resource": ["arn:aws:s3:::{0}/*".format(S3_IMAGE_BUCKET) ]
  }]
}

conn = S3Connection(AWS_ACCESS_KEY, AWS_SECRET_KEY)
bucket = conn.create_bucket(S3_IMAGE_BUCKET)
bucket.set_policy(json.dumps(policy))
key = Key(bucket)

print 'Input dir path:'
ipath = raw_input() or '/home/ethan/projects/brandall'

def upload(name, appendix):
	print 'uploading', name, '...'

	key.key = name
	f_path = path.join(ipath, name+appendix)
	with open(f_path) as f:
		if not key.exists():
			key.set_contents_from_file(f, headers={'Content-Type':'image/png'})
		s3_url = '{0}/{1}'.format(S3_IMAGE_URL, key.key)
	
	return s3_url


def main(path):
	no_match = []
	for image in listdir(path):
		name, appendix = os.path.splitext(image)
		
		brand = Brand.objects(title_edit=name, is_delete=False).first()
		if not brand:
			brand = Brand.objects(title=name, is_delete=False).first()

		if not brand:
			no_match.append(name)
			continue

		url = upload(name, appendix)
		print url, '\n'
		if not brand.images or url not in brand.images:
			brand.images.append(url)
			brand.save()

	print 'no match: ', no_match


if __name__ == '__main__':
	main(ipath)
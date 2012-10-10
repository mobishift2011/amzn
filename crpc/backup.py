#!/usr/bin/env python
# -*- coding: utf-8 -*-
from gevent import monkey
monkey.patch_all()
import gevent.pool

import boto
from boto.s3.key import Key
from boto.s3.connection import S3Connection

import pymongo

import os
import sys
import time
import mock
import tarfile
import traceback
from cStringIO import StringIO
from datetime import datetime, timedelta

DUMP_FILE = '/mnt/dump.tar.gz'
DUMP_DIR = '/mnt/mongodump'
DBPATH = '/var/lib/mongodb'
    
AWS_ACCESS_KEY = "AKIAIQC5UD4UWIJTBB2A"
AWS_SECRET_KEY = "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"
CHUNK_SIZE = 100 * 1024 * 1024

def dumpdb():
    admin = pymongo.Connection().admin

        # lock when we backup
        # admin.command('fsync', 1, lock=1)

        #os.system("tar cvvf {0} {1}".format(DUMP_FILE, DBPATH))
        #os.system("mv {0}/mongod.lock /tmp/mongod.lock".format(DBPATH))
    
        # unlock
        # admin['$cmd'].sys.unlock.find_one()
        
    os.system("mongodump --out {0}".format(DBPATH, DUMP_DIR))
    os.system("tar czvvf {0} {1}".format(DUMP_FILE, DUMP_DIR))

def get_connection():
    return boto.connect_s3(AWS_ACCESS_KEY, AWS_SECRET_KEY)

def upload_part(mp, fname, idx, offset):
    f = open(fname)
    f.seek(offset)
    content = f.read(CHUNK_SIZE)
    f.close()

    success = False
    for x in xrange(3):
        try:
            conn = get_connection()
            bucket = conn.lookup(mp.bucket_name)

            p = boto.s3.multipart.MultiPartUpload(bucket)
            p.id = mp.id
            p.key_name = mp.key_name

            p.upload_part_from_file(StringIO(content), idx+1, replace=True)
            success = True
            break
        except Exception, e:
            print "Error in part upload - %s %s %s" % (fname, idx, offset)
            print traceback.format_exc()

    assert success, "Part failed - %s %s %s" % (fname, idx, offset)

def upload(options):
    conn = get_connection()
    bck = conn.create_bucket(options.bucket)

    pool = gevent.pool.Pool(options.concurrency)

    for fname in options.files:
        if options.path == '.':
            fpath = os.path.basename(fname)
        else:
            fpath = os.path.join(options.path, os.path.basename(fname))

        s = "Putting: %s -> %s/%s ..." % (fname, options.bucket, fpath),
        print "%-80s" % (s),
        sys.stdout.flush()

        start = time.time()

        size = os.stat(fname).st_size
        if size > (CHUNK_SIZE*2) and options.concurrency > 1:
            mp = bck.initiate_multipart_upload(fpath, reduced_redundancy=options.reduced_redundancy)

            greenlets = []
            idx = offset = 0
            while offset < size:
                greenlets.append( pool.spawn(upload_part, mp, fname, idx, offset) )
                idx += 1
                offset += CHUNK_SIZE

            gevent.joinall(greenlets)
            cmp = mp.complete_upload()
        else:
            key = bck.new_key(fpath)
            f = open(fname)
            key.set_contents_from_file(f, reduced_redundancy=options.reduced_redundancy, replace=True)
            f.close()

        size = float(size)/1024/1024
        elapsed = time.time() - start

        print " %6.1f MiB in %.1fs (%d KiB/s)" % (size, elapsed, int(size*1000/elapsed))

def upload2s3():
    conn = S3Connection(AWS_ACCESS_KEY, AWS_SECRET_KEY)

    now = datetime.now()
    sevendaysbefore = now - timedelta(days=7)

    try:
        print 'createing bucket'
        bucket = conn.create_bucket('mongodbdump')

        print 'get key'
        k = Key(bucket)
        k.key = sevendaysbefore.date().isoformat()
        if k.exists():
            print 'delete key', k.key
            k.delete()

        k.key = now.date().isoformat()
        if k.exists():
            print 'delete key', k.key
            k.delete()
        options = mock.Mock()
        options.concurrency = 20
        options.reduced_redundancy = False
        options.bucket = "mongodbdump"
        options.path = "."
        options.files = [ DUMP_FILE ]
        upload(options)
    except Exception, e:
        traceback.print_exc()

if __name__ == '__main__':
    dumpdb()
    upload2s3()

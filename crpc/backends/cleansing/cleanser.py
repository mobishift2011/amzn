#!/usr/bin/env python
# -*- coding: utf-8
import re
from models import Product, Model, Session, engine
from sqlalchemy import func
from datetime import datetime
    
goodcharacter = re.compile('^[0-9a-zA-Z-]+$')

MODEL_BEST          = 0
MODEL_DEFAULT       = -1
MODEL_UNCLASSIFIED  = -999
MODEL_REPEAT        = -888

def extract_models():
    blocksize = 10000
    session = Session()
    count = session.query(func.count(Product.id)).filter_by(level=MODEL_BEST).scalar()
    models = set([])
    for i in range(count/blocksize):
        if i<30:
            continue
        #if i>=30:
        #    break
        print i
        ms = set(( p.model.upper() for p in session.query(Product).filter_by(level=MODEL_BEST).offset(i*blocksize).limit(blocksize) ))
        models |= ms
   
    print 'got exitings'
    exist_models = set((m.model for m in session.query(Model))) 
    print 'set minus'
    models -= exist_models

    print 'inserting new', len(models)
    engine.execute("insert into model (model, updated_at) values (%s, %s)", [(m, datetime.utcnow()) for m in models])
                
def getlevel(model):
    if goodcharacter.match(model):
        return MODEL_BEST
    else:
        return MODEL_UNCLASSIFIED

def cleanse():
    blocksize = 10000
    session = Session()
    count = session.query(func.count(Product.id)).filter_by(level=MODEL_DEFAULT).scalar()
    for i in range(count/blocksize):
        _part_cleanse(i*blocksize, blocksize)

def _part_cleanse(offset, limit):
    print offset, limit
    session = Session()
    for p in session.query(Product).filter_by(level=-1).offset(offset).limit(limit):
        level = getlevel(p.model) 
        if p.level != level:
            print p.model, p.site, p.title, level
            p.level = level
            session.add(p)
    session.commit()

if __name__ == '__main__':
    #cleanse()
    #extract_models()

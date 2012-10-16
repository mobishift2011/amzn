#!/usr/bin/env python
# -*- coding: utf-8 -*-
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Float, Index
from sqlalchemy import UniqueConstraint

from datetime import datetime, timedelta

engine = create_engine('mysql+pymysql://root@localhost:3306/ml')
Base = declarative_base()
Session = sessionmaker(bind=engine)
        
session = Session()


class Product(Base):
    __tablename__ = 'Product'
    id          =   Column(Integer, primary_key=True)
    model       =   Column(String(256), index=True)
    title       =   Column(String(1024))
    site        =   Column(String(32))
    key         =   Column(String(1024))
    UniqueConstraint('site', 'key', name='sitekey')

Index('product_site_key', Product.site, Product.key)

Base.metadata.create_all(engine)

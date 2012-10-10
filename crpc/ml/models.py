#!/usr/bin/env python
# -*- coding: utf-8 -*-
from sqlalchemy import create_engine
engine = create_engine('mysql+pymysql://root:123456@localhost:3306/ml')

from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

from sqlalchemy.orm import sessionmaker
Session = sessionmaker(bind=engine)
        
session = Session()

from datetime import datetime, timedelta

from sqlalchemy import Column, Integer, String, Boolean, DateTime, Float, Index

class Product(Base):
    __tablename__ = 'Product'
    id          =   Column(Integer, primary_key=True)
    model       =   Column(String(32), index=True)
    title       =   Column(String(256))
    price       =   Column(Float)
    site        =   Column(String(32))
    key         =   Column(String(32))
    duplicate   =   Column(Boolean, default=False)

Index('product_site_key', Product.site, Product.key)

Base.metadata.create_all(engine)

#!/usr/bin/env python
# -*- coding: utf-8 -*-
from sqlalchemy import create_engine
engine = create_engine('sqlite:////home/jingchao/Projects/amzn/crpc/status.db')

from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

from sqlalchemy.orm import sessionmaker
Session = sessionmaker(bind=engine)
        
session = Session()

from datetime import datetime, timedelta

from sqlalchemy import Column, Integer, String, Boolean, DateTime
class Stat(Base):
    __tablename__ = 'Stat'

    sid = Column(Integer, primary_key=True)
    crawler = Column(String, nullable=False)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    stopped = Column(Boolean, default=False)
    loops = Column(Integer, default=0)
    errors = Column(Integer, default=0) 
    errors_list = Column(String, default='') # comma sepreated error

    @staticmethod
    def get_or_create(crawler):
        s = session.query(Stat).filter_by(crawler=crawler, stopped=False).first()
        if not s:
            s = Stat(crawler=crawler)
            s.created_at = s.updated_at = datetime.utcnow()
            session.add(s)
            session.commit()
        return s
                
    def incr(self):
        self.updated_at = datetime.utcnow()
        self.loops += 1
        session.add(self)
        session.commit()

    def error(self, message):
        self.udpated_at = datetime.utcnow()
        self.loops += 1 
        self.errors += 1
        l = self.errors_list.split(';;;')[:9]
        l.insert(0, message)
        self.errors_list = ';;;'.join(l)
        session.add(self)
        session.commit()

    def done(self):
        self.stopped = True
        session.commit()

Base.metadata.create_all(engine)

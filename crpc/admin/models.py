from settings import MONGODB_HOST
from backends.monitor.models import Task
from backends.monitor.throttletask import task_broke_completed
from backends.monitor.executor import execute
from backends.monitor.setting import EXPIRE_MINUTES

from mongoengine import *
from datetime import datetime, timedelta

connect(db='admin', host=MONGODB_HOST)

class Brand(Document):
    title           =   StringField(unique=True)
    title_edit      =   StringField()
    title_cn        = StringField(default=u'')
    title_checked   =   BooleanField(default=False)
    alias           =   ListField(StringField(), default=list())
    keywords        =   StringField(default='')
    url             =   StringField(default='')
    url_checked     =   BooleanField(default=False)
    blurb           =   StringField(default='')
    blurb_cn      =   StringField(default=u'')
    icon            =   StringField()
    images          =   ListField(StringField())   
    level           =   IntField(default=0) # luxrious or not 
    dept            =   ListField(StringField(max_length=30))
    is_delete       =   BooleanField(default=False)
    done            =   BooleanField(default=False)
    created_at      =   DateTimeField(default=datetime.now())
 
    meta = {
        'ordering': ['title']
    }
        
    def __unicode__(self):
        return self.title

    def to_json(self):
        return {
            'title'           :   self.title,
            'title_edit'      :   self.title_edit,
            'title_cn'         :    self.title_cn,
            'title_checked'   :   self.title_checked,
            'alias'           :   self.alias,
            'keywords'        :   self.keywords,
            'url'             :   self.url,
            'url_checked'     :   self.url_checked,
            'blurb'           :   self.blurb,
            'blurb_cn'      :   self.blurb_cn,
            'icon'            :   self.icon,
            'images'          :   self.images,
            'level'           :   self.level,
            'dept'            :   self.dept,
            'is_delete'       :   self.is_delete,
            'done'            :   self.done,
            'created_at'      :   str(self.created_at)
        }


def delete_expire_task(expire_minutes=EXPIRE_MINUTES):
    """ delete the expire RUNNING Task, expire_minutes is in settings
        TODO: expire_minutes be set on the web page

    :param expire_minutes: set the expire running task in hours
    """
    expire_datetime = datetime.utcnow() - timedelta(minutes=expire_minutes)
    for t in Task.objects(status=Task.RUNNING, updated_at__lt=expire_datetime):
        t.status = Task.FAILED
        t.ended_at = datetime.utcnow()
        t.save()
        task_broke_completed(t.site, t.method)


class DealSchedule(Document):
    """ schedules info """
    site            =   StringField()
    method          =   StringField()
    description     =   StringField()
    minute          =   StringField()
    hour            =   StringField()
    dayofmonth      =   StringField()
    month           =   StringField()
    dayofweek       =   StringField()
    enabled         =   BooleanField(default=False)

    def get_crontab_arguments(self):
        return "{0} {1} {2} {3} {4}".format(self.minute, self.hour, self.dayofmonth, self.month, self.dayofweek)

    def timematch(self):
        t = datetime.utcnow()
        tsets = self._time_sets()
        return  t.minute in tsets['minute'] and \
                t.hour in tsets['hour'] and \
                t.day in tsets['dayofmonth'] and \
                t.month in tsets['month'] and \
                t.weekday() in tsets['dayofweek']

    def _time_sets(self):
        wholes = {'minute':60, 'hour':24, 'dayofmonth':31, 'month':12, 'dayofweek':7}
        names = ['minute', 'hour', 'dayofmonth', 'month', 'dayofweek']
        for name in names:
            if not getattr(self, name):
                setattr(self, name, "*")
        
        tsets = {} 
        for name in names:
            nsets = set()
            for e in getattr(self, name).split(','):
                if '/' in e:
                    # */3
                    star, div = e.rsplit('/',1)
                    if star != '*':
                        raise ValueError('valid syntax: */n')
                    nsets.update(filter(lambda x:x%int(div)==0, range(0,wholes[name])))
                elif '-' in e:
                    # 1-5
                    f, t = e.split('-')
                    nsets.update(range(int(f),int(t)+1))
                elif e == '*':
                    nsets.update(range(0, wholes[name]+1))
                else:
                    # 7
                    nsets.add(int(e))

            tsets[ name ] = nsets
    
        return tsets

    @staticmethod
    def run():
        while True:
            for s in DealSchedule.objects(enabled=True):
                if s.timematch():
                    execute(s.site, s.method)

            # assume this for loop can be finished in less than one minute
            delete_expire_task()
            gevent.sleep(60 - datetime.utcnow().second)
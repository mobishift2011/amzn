from backends.monitor.ghub import GHub
from backends.monitor.throttletask import can_task_run, task_completed, is_task_already_running
from crawlers.common.routine import new, new_thrice, update, new_category, new_listing, new_product, update_category, update_listing, update_product
from helpers.rpc import get_rpcs
from settings import CRAWLER_PEERS

from functools import partial
import gevent

def execute(site, method):
    """ execute CrawlerServer function

    """
    if can_task_run(site, method):
        job = gevent.spawn(globals()[method], site, get_rpcs(CRAWLER_PEERS), concurrency=10)
        job.rawlink(partial(task_completed, site=site, method=method))
        GHub().extend('tasks', [job])

# Create your tasks here
from __future__ import absolute_import, unicode_literals
from celery import shared_task

from zhspider import crawl2


@shared_task
def crawl_chinasarft():
    print("check and update chinasarft screenplay info")
    crawl2()
    return 0
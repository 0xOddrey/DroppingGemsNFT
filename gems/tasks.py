



from .models import *
from .openai_api import *
import base64
from .build_image import * 
from .save_to_png import *
import datetime
import requests 

# using SendGrid's Python Library
# https://github.com/sendgrid/sendgrid-python
import os
from base.celery import app
from django.views.generic import TemplateView
from django.core import mail
from datetime import datetime, timedelta
from django.template.loader import render_to_string
from django.utils.html import strip_tags
import _datetime
from datetime import datetime
from .models import *
from decouple import config, Csv
from celery import Celery
from django.conf import settings
from celery.schedules import crontab
from celery import shared_task
from datetime import datetime, timedelta
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from .models import *
from decouple import config, Csv
from django.template.loader import get_template

import requests
from base.celery import app


from base.celery import app


@app.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):
    # Calls test('hello') every 10 seconds.
    sender.add_periodic_task(
        
        crontab(minute=1),
        UpdateMeta.s('updating'),
    )

  

@app.task
def UpdateMeta(arg):
    current_datetime = datetime.datetime.now()  
    
    twitter_connection = twitterConnection.objects.all().order_by('last_updated')[0]

    
    md_ref = twitter_connection.meta_data_id
    print(md_ref)
    meta_match = gemsMeta.objects.filter(id=md_ref).first()
    if meta_match:
        final = getTopic(twitter_connection.twitter)
        base_code, _ = get_image(final, 1)
        meta_match.image = base_code
        meta_match.save()
    
        


    twitter_connection.last_updated = current_datetime
    twitter_connection.save()

    url = "https://api.opensea.io/api/v1/asset/0x0B5DdEFf4D54C1B1eE635657C17cF54135e5DB30/8/?force_update=true" % (meta_match.metaID)   
    print(url)   

    headers = {
        "Accept": "application/json",
        "X-API-KEY": "Connection: keep-alive"
    }

    response = requests.request("GET", url, headers=headers)
    return("success")
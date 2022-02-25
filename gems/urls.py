try:
    from django.conf.urls import url
except ImportError:
    from django.urls import re_path as url

from django.conf import settings
if getattr(settings, 'POSTMAN_I18N_URLS', False):
    from django.utils.translation import pgettext_lazy
else:
    def pgettext_lazy(c, m): return m

from django.urls import path, include, re_path
from django.conf.urls import url
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_exempt

from . import views 

urlpatterns = [

    url(r'^$',
        views.Homepage, 
        name='homepage'),

    url(r'^final-mint/(?P<twitterId>[\w\s]+)/',
        views.finalMint, 
        name='final_mint'),

    url(r'^my-gems/(?P<wallet>[\w\s]+)/(?P<twitterId>[\w\s]+)/(?P<twitterRef>[\w\s]+)/',
        views.MyGems, 
        name='my_gems'),

    url(r'^my-gems-anon/(?P<reveal>[\w\s]+)/(?P<tokenId>[\w\s]+)/(?P<wallet>[\w\s]+)/(?P<twitterId>[\w\s]+)/(?P<twitterRef>[\w\s]+)/',
        views.MakeAnon, 
        name='my_gems_anon'),

    url(r'^my-gems-reset/(?P<tokenId>[\w\s]+)/(?P<wallet>[\w\s]+)/(?P<twitterId>[\w\s]+)/(?P<twitterRef>[\w\s]+)/',
        views.GemReset, 
        name='my_gems_reset'),

    url(r'^mint/',
        views.Mint, 
        name='mint'),

    url(r'^gem-preview/(?P<tokenId>[\w\s]+)/',
        views.GemPreview, 
        name='gem_preview'),


    url(r'^learn-more/',
        views.LearnMore, 
        name='learn_more'),

    url(r'^about-us/',
        views.AboutUs, 
        name='about_us'),

    url(r'^api/(?P<tokenId>[\w\s]+)/?(?:\.json)',
        views.MetaDataApi, 
        name='metadata_api'),

    url(r'^api/(?P<tokenId>[\w-]+)',
        views.MetaDataApi, 
        name='metadata_api'),

    path(
        "auth/twitter/redirect/",
        views.TwitterAuthRedirectEndpoint.as_view(),
        name="twitter-login-redirect",
    ),
    path(
        "complete/twitter/",
        views.TwitterCallbackEndpoint.as_view(),
        name="twitter-login-callback",
    ),
    path('is-authenticated', views.IsAuthenticated.as_view())

]
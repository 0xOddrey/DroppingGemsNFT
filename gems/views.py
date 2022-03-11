from django.shortcuts import render
from rest_framework import serializers, viewsets
from .serializers import AttributeSerializer
from .models import *
from PIL.Image import new
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View, FormView, TemplateView, DetailView, ListView
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm, AdminPasswordChangeForm
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.views.generic.edit import FormMixin
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
from django.conf import settings
from django.core.files import File
import datetime
import base64
import json 
import random
import base64
from io import BytesIO
from .openai_api import *
import base64
from .build_image import * 
from .save_to_png import *
from django.core.files import File
import boto3
import urllib.request
import requests
from django.core.files.base import ContentFile
from os.path import basename
from .tasks import *
from requests_oauthlib import OAuth1
from urllib.parse import urlencode
from rest_framework.views import APIView
from django.http.response import  HttpResponseRedirect
from requests_oauthlib import OAuth1
from requests_oauthlib import OAuth1Session
from requests_oauthlib import requests
from .utils import is_twitter_authenticated, update_or_create_user_token, get_user_tokens
from web3 import Web3
from .gemsContract import *



w3 = Web3(Web3.HTTPProvider('https://eth-mainnet.alchemyapi.io/v2/nFzmfPoiMWnPgTBNZWU9JGmkWSAeoVIt'))

# Create your views here.
#Homepage Landing Page
def Homepage(request):

    first_gem =  None 
    example_gems = []
    example_tweeters = ["JoshuaOgundu", "chriscantino", "ArlanWasHere", "0xOddrey", "OneBandwagonFan", "CPGclub"]
    for person in example_tweeters:
        p_index = example_tweeters.index(person)
        if p_index == 0:
            ci = random.randint(0, 4)
            final = getTopic(person)
            base_code, svg_code = get_image(final, ci)
            first_gem = str("@" + person), base_code
        else: 
            ci = random.randint(0, 4)
            final = getTopic(person)
            base_code, svg_code = get_image(final, ci)
            result = str("@" + person), base_code
            example_gems.append(result)
    

    
    return render(request, "homepage.html", {"example_gems": example_gems, 'first_gem': first_gem})

def Mint(request):
    current_gas = w3.eth.gas_price
    gem_contract = get_gem_contract()
    current_count = gem_contract.functions.totalSupply().call()
    return render(request, "mint.html", {"current_count": int(current_count), "current_gas":current_gas})

def finalMint(request, twitterId):

    return render(request, "mint.html", {})



def MyGems(request, wallet, twitterId, twitterRef):
    gems = []
    new_twitter_connection = []
    assigned = True
    if "none" not in twitterId:
        new_twitter_connection = twitterConnection.objects.filter(id=twitterId, twitter_ref=twitterRef).first()
        if new_twitter_connection:
            if new_twitter_connection.meta_data:
                pass
            else:
                assigned = False
    

    if "none" not in wallet:
        gem_contract = get_gem_contract()
        addy = Web3.toChecksumAddress(wallet)
        
        ownership = gem_contract.functions.tokensOfOwner(addy).call()
        
        for tokenId in ownership:
            meta_match, created = gemsMeta.objects.get_or_create(metaID=tokenId)
            if created:
                meta_match.name = "Gem #%s" % (tokenId)
                meta_match.description = "A unique gem based on your tweets"
                meta_match.background = random.randint(0, 4)
                meta_match.save()

            twitter_connection = twitterConnection.objects.filter(meta_data=meta_match).first()
            if twitter_connection:
                final = getTopic(twitter_connection.twitter)
                base_code, _ = get_image(final, int(meta_match.background))
            else:
                if new_twitter_connection and assigned == False:
                    new_twitter_connection.meta_data = meta_match
                    new_twitter_connection.save()
                    meta_match.name = "@%s Gem" % (new_twitter_connection.twitter)
                    meta_match.is_anon = False
                    twitter_connection = new_twitter_connection
                    final = getTopic(new_twitter_connection.twitter)
                    base_code, _ = get_image(final, int(meta_match.background))
                    assigned = True 
                else:
                    final = getTopic('_none_')
                    base_code, _ = get_image(final, int(meta_match.background))


            meta_match.image = base_code
            meta_match.save()
            
            result = meta_match, twitter_connection
            gems.append(result)

    return render(request, "mygems.html", {"gems": gems, "twitterRef": twitterRef, "wallet_addy": wallet, 'new_twitter_connection': new_twitter_connection, 'twitterId': twitterId})


def MakeAnon(request, reveal, tokenId, wallet, twitterId, twitterRef):
    reveal = int(reveal)
    if reveal == 1:
        meta_match = gemsMeta.objects.filter(metaID=tokenId).first()
        meta_match.name = "Gem #%s" % (tokenId)
        meta_match.is_anon = True
        meta_match.save()
    else:
        meta_match = gemsMeta.objects.filter(metaID=tokenId).first()
        twitt_conn = twitterConnection.objects.filter(meta_data=meta_match).first()
        meta_match.name = "@%s Gem" % (twitt_conn.twitter)
        meta_match.is_anon = False
        meta_match.save()

    return redirect('my_gems', wallet=wallet, twitterId=twitterId, twitterRef=twitterRef)


def GemReset(request, tokenId, wallet, twitterId, twitterRef):
    meta_match = gemsMeta.objects.filter(metaID=tokenId).first()
    twitt_conn = twitterConnection.objects.filter(meta_data=meta_match).first()
    twitt_conn.delete()
    
    meta_match.name = "Gem #%s" % (tokenId)
    meta_match.is_anon = True
    meta_match.save()

    return redirect('my_gems', wallet=wallet, twitterId='none', twitterRef='none')

def LearnMore(request):
    
    return render(request, "learn-more.html", {})


def GemPreview(request, tokenId):
    meta_match = gemsMeta.objects.filter(metaID=tokenId).first()

    if meta_match:
        twitter_connection = twitterConnection.objects.filter(meta_data=meta_match).first()
        if twitter_connection:
            final, tn, subject, polar = getFullTopic(twitter_connection.twitter)
            base_code, svg_code = get_image(final, int(meta_match.background))
            results = save_to_png(svg_code, twitter_connection.twitter)

            f = open(results, 'rb')
            meta_match.image_file = File(f)
            meta_match.save()
            
        else:
            final, tn, subject, polar = getFullTopic('_none_')
            base_code, _ = get_image(final, int(meta_match.background))

        
        try:
            meta_match.image = base_code
            meta_match.save()
            url = "https://api.opensea.io/api/v1/asset/0x0B5DdEFf4D54C1B1eE635657C17cF54135e5DB30/%s/?force_update=true" % (meta_match.metaID)   
    
            headers = {
                "Accept": "application/json",
                "X-API-KEY": "Connection: keep-alive"
            }

            response = requests.request("GET", url, headers=headers)
        except:
            pass
    
        return render(request, "gem-preview.html", {"tokenId": tokenId, "meta_match": meta_match, "final": final, "tn": tn, "subject": int(subject), "polar": int(polar)})
    else:
        return render(request, "404.html")

def AboutUs(request):
    example_gems = []
    example_tweeters = ["0xoddrey", "AnnaShimuni", "Vii__Tat", "zahna_montana"]
    jobs = ["Developer", "Product Design", "Art Director", "Community Manager"]
    for person in example_tweeters:
        index = example_tweeters.index(person)
        final = getTopic(person)
        ci = random.randint(0, 4)
        base_code, svg_code = get_image(final, ci)
        result = str("@" + person), jobs[index], base_code
        example_gems.append(result)
    
    return render(request, "about-us.html", {'example_gems': example_gems})

def MetaDataApi(request,  tokenId):
    if request.method == "GET":
        meta_match = gemsMeta.objects.filter(metaID=tokenId).first()
        
        if meta_match is None:
            meta_match, created = gemsMeta.objects.get_or_create(metaID=tokenId)
            if created:
                meta_match.name = "Gem #%s" % (tokenId)
                meta_match.description = "A unique gem based on your tweets"
                meta_match.background = random.randint(0, 4)
            final = getTopic('_none_')
            base_code, _ = get_image(final, int(meta_match.background))
            meta_match.image = base_code
            meta_match.save()

        twitter_connection = twitterConnection.objects.filter(meta_data=meta_match).first()

        try:
            if twitter_connection:
                final = getTopic(twitter_connection.twitter)
                base_code, _ = get_image(final, int(meta_match.background))
            else:
                final = getTopic('_none_')
                base_code, _ = get_image(final, int(meta_match.background))

            meta_match.image = base_code
            meta_match.save()
        except:
            pass
        
        
        return JsonResponse(AttributeSerializer(meta_match).data)


class TwitterAuthRedirectEndpoint(APIView):
    def get(self, request, *args, **kwargs):
        try:
                oauth = OAuth1(
                    client_key= config('consumer_key2'),
                    client_secret= config('consumer_secret2'),
                )
                #Step one: obtaining request token
                request_token_url = "https://api.twitter.com/oauth/request_token"
                data = urlencode({
                    "oauth_callback": config('REDIRECT_URI') 
                })
                
                response = requests.post(request_token_url, auth=oauth, data=data)
                response.raise_for_status()
                response_split = response.text.split("&")
                oauth_token = response_split[0].split("=")[1]
                oauth_token_secret = response_split[1].split("=")[1]
                
                #Step two: redirecting user to Twitter
                twitter_redirect_url = (
                    f"https://api.twitter.com/oauth/authenticate?oauth_token={oauth_token}"
                )
                return HttpResponseRedirect(twitter_redirect_url)
        except ConnectionError:
            html = "<html><body>You have no internet connection</body></html>"
            return HttpResponse(html, status=403)
        except Exception as ex:
            html="<html><body>Something went wrong. Try Again</body></html>"
            print(ex)
            return HttpResponse(html, status=403)




class TwitterCallbackEndpoint(APIView):
    def get(self, request, *args, **kwargs):
        try:
            oauth_token = request.query_params.get("oauth_token")
            oauth_verifier = request.query_params.get("oauth_verifier")
            oauth = OAuth1(
                client_key= config('consumer_key2'),
                client_secret = config('consumer_secret2'),
                resource_owner_key=oauth_token,
                verifier=oauth_verifier,
            )
            res = requests.post(
                f"https://api.twitter.com/oauth/access_token", auth=oauth
            )
            res_split = res.text.split("&")
            oauth_token=res_split[0].split("=")[1]
            oauth_secret=res_split[1].split("=")[1]
            user_id = res_split[2].split("=")[1] if len(res_split) > 2 else None
            user_name = res_split[3].split("=")[1] if len(res_split) > 3 else None 
            if not request.session.exists(request.session.session_key):
                request.session.create()
            update_or_create_user_token(request.session.session_key, oauth_token,
            oauth_secret, user_id, user_name)
            twitter_match, _ = twitterConnection.objects.get_or_create(user_id=user_id, twitter=user_name)
            ##
            twitt_ref = twitter_match.twitter_ref
            redirect_url="https://www.gemsnft.co/my-gems/none/%s/%s/" % (twitter_match.id, twitt_ref)
            return HttpResponseRedirect(redirect_url)
        except ConnectionError:
            return HttpResponse(
                "<html><body>You have no internet connection</body></html>", status=403
            )
        except Exception as ex:
            print(ex)
            return HttpResponse(
                "<html><body>Something went wrong.Try again.</body></html>", status=403
            )

class IsAuthenticated(APIView):
    def get(self, request, *args, **kwargs):
        is_authenticated = is_twitter_authenticated(
            self.request.session.session_key)
        return Response({'status': is_authenticated}, status=status.HTTP_200_OK)
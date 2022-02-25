

import random
from .models import *

def assignMetaData(tokenId):
    meta_match, created = gemsMeta.objects.get_or_create(metaID=tokenId)

    meta_match.name = "Gem #%s" % (tokenId)
    meta_match.description = "A unique gem based on your tweets"
    if meta_match.background is None: 
        meta_match.background = random.randint(0, 4)
        meta_match.save()

    twitter_connection = twitterConnection.objects.filter(meta_data=meta_match).first()

    
    if twitter_connection:
        final = getTopic(twitter_connection.twitter)
        base_code, svg_code = get_image(final, int(meta_match.background))
        title = '%s-%s-gems.svg' %(twitter_connection.twitter, tokenId)
        new_image = open(title, 'w').write(svg_code)
        s_image = open(title, 'rb')
        filename = basename(title)
        meta_match.image = base_code
        s_image.close()
    else:
        final = getTopic('_none_')
        base_code, svg_code = get_image(final)
        title = '%s-%s-gems.svg' %(final, tokenId)
        new_image = open(title, 'w').write(svg_code)
        s_image = open(title, 'rb')
        filename = basename(title)
        meta_match.image = base_code

    meta_match.save()



def updateMetaData(tokenId):
    meta_match, created = gemsMeta.objects.get_or_create(metaID=tokenId)

        meta_match.name = "Gem #%s" % (tokenId)
        meta_match.description = "A unique gem based on your tweets"
        if meta_match.background is None: 
            meta_match.background = random.randint(0, 4)
            meta_match.save()

        twitter_connection = twitterConnection.objects.filter(meta_data=meta_match).first()

        
        if twitter_connection:
            final = getTopic(twitter_connection.twitter)
            base_code, svg_code = get_image(final, int(meta_match.background))
            title = '%s-%s-gems.svg' %(twitter_connection.twitter, tokenId)
            new_image = open(title, 'w').write(svg_code)
            s_image = open(title, 'rb')
            filename = basename(title)
            meta_match.image = base_code
            s_image.close()
        else:
            final = getTopic('_none_')
            base_code, svg_code = get_image(final)
            title = '%s-%s-gems.svg' %(final, tokenId)
            new_image = open(title, 'w').write(svg_code)
            s_image = open(title, 'rb')
            filename = basename(title)
            meta_match.image = base_code

        meta_match.save()
from cairosvg import svg2png, svg2svg
import re
import base64
from PIL import Image
import io
from .models import *
import boto3
from decouple import config, Csv

import numpy as np



def save_as_base(base_code, username):
    new_data = base_code.replace('data:image/svg+xml;base64,', '')
    data = new_data.replace(' ', '+')
    print(data)
    imgdata = base64.b64decode(data)
    filename = 'some_image.png'  # I assume you have a way of picking unique filenames
    with open(filename, 'wb') as f:
            f.write(imgdata)
        
    

def save_to_png(svg_code, username):
    file_name = str("gems/static/images/" + username + "-output.png")

    image_ceated = svg2png(bytestring=svg_code, write_to=file_name)
    return(file_name)

    

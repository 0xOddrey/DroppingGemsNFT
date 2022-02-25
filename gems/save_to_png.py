from cairosvg import svg2png
import re
import base64
from PIL import Image
import io
from .models import *
import boto3
from decouple import config, Csv

def save_as_base(svg_code, username):
    image = base64.b64decode(svg_code)       
    fileName = 'test.jpeg'

    imagePath = ("test.jpeg")
    img = Image.open(io.BytesIO(image))
    img.save(imagePath, 'jpeg')



def save_as_PNG(svg_code, username):
    file_name = str(username + "-output.png")
    svg_code = re.sub('(\\s+|\\n)', ' ', svg_code)
    svg_code = svg_code.replace('\\n', '')
    image_ceated = svg2png(bytestring=svg_code,write_to=file_name)
  
    return(file_name)
    
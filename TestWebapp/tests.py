from django.test import TestCase

# Create your tests here.
'''
import os
from PIL import Image
filename = os.listdir("static/BingPicture/")
new_dir = "static/smallimage/"
size_m = 35
size_n = 35
  
for img in filename:
  image = Image.open("static/BingPicture/" + img)
  image_size = image.resize((size_m, size_n),Image.ANTIALIAS)
  image_size.save(new_dir + img)
'''
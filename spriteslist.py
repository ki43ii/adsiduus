from sprites import *
import os

sprites = {}

for filename in os.listdir("allsprites"):
    filepath = os.path.join("allsprites", filename)
    if os.path.isfile(filepath):
        key = os.path.splitext(filename)[0]
        sprites[key] = image_to_ascii(filepath)

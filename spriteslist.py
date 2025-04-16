from sprites import *

sprites = {
""
}
import os
print("sprites = {")
for filename in os.listdir("allsprites"):
    filepath = os.path.join("allsprites", filename)
    if os.path.isfile(filepath):
        print(filename + ":\n" + image_to_ascii(filepath) + ",")
print("}")

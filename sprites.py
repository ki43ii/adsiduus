from numpy import array
from PIL import Image

ASCII_CHARS = "@%#*+=-:. "

def convertToAscii(image_path, new_width=80):
    img = Image.open(image_path).convert("RGB")
    width, height = img.size
    aspect_ratio = height / width
    new_height = int(new_width * aspect_ratio * 0.55)
    img = img.resize((new_width, new_height))

    pixels = array(img)
    ascii_str = ""

    for row in pixels:
        for r, g, b in row:
                brightness = (int(r) + int(g) + int(b)) / 3
                char = ASCII_CHARS[brightness // 32]
                ascii_str += f"\033[38;2;{r};{g};{b}m{char}"
        ascii_str += "\033[0m\n"

    return ascii_str

# tested with print(convertToAscii(r'shockedpikachu.png'))

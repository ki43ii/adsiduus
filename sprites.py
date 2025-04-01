from PIL import Image
from numpy import array

ASCII_CHARS = "@%#*+=-:. "

# MEGA IMPORTANT. THIS FUNCTION DOES THE ASCII FOR YOU
# INSTRUCTIONS: GET THE SOURCE IMAGE (remove backgrounds)
# THEN USE THE FUNCTION AS SO 

# sprites = {"thing" : image_to_ascii(r"sprites\thing.png", yourresolution)}

def image_to_ascii(image_path, new_width=80):
    img = Image.open(image_path).convert("RGB")
    width, height = img.size
    aspect_ratio = height / width
    new_height = int(new_width * aspect_ratio * 0.55)
    img = img.resize((new_width, new_height))

    pixels = array(img)
    ascii_str = ""

    for row in pixels:
        for r, g, b in row:

            brightness = (int(r) + int(g) + int(b)) // 3  # Get grayscale brightness
            char = ASCII_CHARS[brightness // 32]  # Map brightness to ASCII char
            ascii_str += f"\033[38;2;{r};{g};{b}m{char}"  # ANSI escape color
        ascii_str += "\033[0m\n"  # Reset color at end of line

    return ascii_str  # ✅ Returns the colored ASCII string

sprites = {"barbarian" : None}

print(image_to_ascii("allsprites/bg.png"), 20)

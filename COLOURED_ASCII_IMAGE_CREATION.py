from PIL import Image
from rich.console import Console
from rich.text import Text
import numpy as np

console = Console()

# ASCII characters from dark to light
ASCII_CHARS = "@%#*+=-:. "

def image_to_colored_ascii(image_path, new_width=80):
    img = Image.open(image_path).convert("RGB")  # Open image in RGB mode
    width, height = img.size
    aspect_ratio = height / width
    new_height = int(new_width * aspect_ratio * 0.55)  # Adjust for terminal aspect ratio
    img = img.resize((new_width, new_height))

    pixels = np.array(img)
    text = Text()

    for row in pixels:
        for r, g, b in row:
            brightness = int((r + g + b) / 3)  # Get grayscale brightness
            char = ASCII_CHARS[brightness // 32]  # Map brightness to ASCII char
            text.append(char, style=f"rgb({r},{g},{b})")  # Set color

        text.append("\n")  # New line for each row

    console.print(text)

# Run the function with your image
image_to_colored_ascii("your_image.png")


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

import re

ANSI_PATTERN = re.compile(r'\x1b\[[0-9;]*m')

def split_ansi_line(line, width=80):
    result = []
    i = 0
    current_color = ''
    while i < len(line) and len(result) < width:
        if line[i] == '\x1b':
            match = ANSI_PATTERN.match(line, i)
            if match:
                current_color = match.group()
                i = match.end()
                continue
        result.append(current_color + line[i])
        i += 1
    while len(result) < width:
        result.append(' ')
    return result[:width]


def overlayer(img1, img2, box):
    width, height = 80, 40

    # Convert base image into ANSI-safe canvas
    base_lines = img1.splitlines()
    while len(base_lines) < height:
        base_lines.append('')  # pad bottom
    base_lines = base_lines[:height]
    canvas = [split_ansi_line(line) for line in base_lines]

    # Convert overlay image
    overlay_lines = img2.splitlines()
    overlay_cells = [split_ansi_line(line) for line in overlay_lines]

    box_x, box_y = box  # Now Y=0 is the TOP row

    for row_offset, line_cells in enumerate(overlay_cells):
        canvas_y = box_y + row_offset
        if 0 <= canvas_y < height:
            for col_offset, cell in enumerate(line_cells):
                canvas_x = box_x + col_offset
                if 0 <= canvas_x < width:
                    if cell.strip():  # only paste non-blank
                        canvas[canvas_y][canvas_x] = cell

    return '\n'.join(''.join(row) for row in canvas)

sprites = {"barbarian" : None}  # to be completed

print(image_to_ascii("allsprites/bg.png", 20))

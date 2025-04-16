from PIL import Image
from numpy import array
import re
import os

FULL_BLOCK = "█"  # Assuming this is defined
SPACE = " "  # Space for transparent/black pixels

def image_to_ascii(image_path):
    img = Image.open(image_path).convert("RGBA")  # Use RGBA to get alpha for transparency
    width, height = img.size

    pixels = array(img)
    ascii_str = ""

    # Optionally skip rows to squash vertical size if terminal font is tall
    row_step = 1  # Change to 2 if your terminal font is tall

    for y in range(0, height, row_step):
        for r, g, b, a in pixels[y]:  # RGBA values, with 'a' being the alpha (transparency)
            brightness = (r + g + b) / 3  # Average brightness of the pixel
            if brightness == 0 or a == 0:  # Fully transparent or black pixels
                ascii_str += SPACE
            else:
                ascii_str += f"\033[38;2;{r};{g};{b}m{FULL_BLOCK}"
        ascii_str += "\033[0m\n"

    return ascii_str

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

def create_scene(bg, enemies: list, player, weapon):
    
    enemy_shuffled = shuffle(enemies)
    scene = bg
    box = None  # will figure out later
    for enemy in enemies:
        scene = overlayer(scene, enemy, box)

    scene = overlayer(scene, player)
    scene = overlayer(scene, weapon)

    return scene


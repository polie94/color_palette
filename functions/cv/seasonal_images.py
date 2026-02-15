from transformers import pipeline
from PIL import Image, ImageDraw
import torch
import operator
import numpy as np

def get_mask(img:Image) -> Image:
    pipe = pipeline("image-segmentation")
    results = pipe(img)
    getter = operator.itemgetter("label")
    result = next((result for result in results if getter(result) == "person"), None)
    mask = result["mask"]

    return mask

def create_palette(color_palet:dict)->Image:
    # Image size
    width, height = 800, 600
    # Number of colors
    num_colors = len(color_palet)

    # Create a blank image
    img = Image.new("RGB", (width, height), "#FFFFFF")  # white background
    draw = ImageDraw.Draw(img)

    # Calculate block height
    block_height = height // num_colors

    # Draw color blocks
    for i, color in enumerate(color_palet):
        top = i * block_height
        bottom = (i + 1) * block_height
        draw.rectangle([0, top, width, bottom], fill=color)

    # Optional: draw white lines between blocks for separation
    for i in range(1, num_colors):
        y = i * block_height
        draw.line([0, y, width, y], fill="#FFFFFF", width=4)

    return img

def prepare_output(img:Image, palette:Image, mask:Image) -> Image:

    img = img.resize(mask.size)
    palette = palette.resize(mask.size)
    mask_array = np.array(mask)
    mask_pil = Image.fromarray(mask_array, mode="L")
    palette.paste(img, (0, 0), mask_pil)

    return  palette 
    








from transformers import pipeline
from PIL import Image, ImageDraw
import torch
import operator
import numpy as np

from functions.cv.color_palettes import *

class ImagePrep():
    def __init__(self, img:Image):
        self.image = img
        self.season_palettes = SEASONAL_PALETTES
        self.subseason_palletes = SUBSEASONAL_PALETTES

    @staticmethod
    def _run_segmentation(img) -> dict:
        pipe = pipeline("image-segmentation")
        results = pipe(img)
        return results
        
    def _get_mask(self) -> Image:
        results = self._run_segmentation(self.image)
        getter = operator.itemgetter("label")
        result = next((result for result in results if getter(result) == "person"), None)
        mask = result["mask"]
        mask_array = np.array(mask)
        mask_pil = Image.fromarray(mask_array, mode="L")

        return mask_pil

    def _create_palette_bg(self, color_palette:dict) -> Image:
        # Image size
        width, height = 800, 600
        # Number of colors
        num_colors = len(color_palette)

        # Create a blank image
        img = Image.new("RGB", (width, height), "#FFFFFF")
        draw = ImageDraw.Draw(img)

        # Calculate block height
        block_height = height // num_colors

        # Draw color blocks
        for i, color in enumerate(color_palette):
            top = i * block_height
            bottom = (i + 1) * block_height
            draw.rectangle([0, top, width, bottom], fill=color)

        # Draw white lines between blocks for separation
        for i in range(1, num_colors):
            y = i * block_height
            draw.line([0, y, width, y], fill="#FFFFFF", width=4)

        return img

    def prepare_output(self) -> Image:

        mask = self._get_mask()
        img = self.image.resize(mask.size)
        for cp_name, cp in self.season_palettes.items():
            palette = self._create_palette_bg(cp)
            palette = palette.resize(mask.size)
            palette.paste(img, (0, 0), mask)
            palette.save(f"seasonales_output/{cp_name}.jpg")
        for cp_name, cp in self.subseason_palletes.items():
            palette = self._create_palette_bg(cp)
            palette = palette.resize(mask.size)
            palette.paste(img, (0, 0), mask)
            palette.save(f"subseasonales_output/{cp_name}.jpg")        









# -*- coding: utf-8 -*-
# !/usr/bin/env python3

import pathlib
from PIL import Image, ImageDraw, ImageColor, ImageFont

def watermark_image(image_obj, watermark_text):
        # load a standard gray color
        gray_color = ImageColor.getcolor('gray', 'RGB')

        # load a font object
        font_path = (pathlib.Path('..') / 'fonts' / 'Arvo-Bold.ttf').resolve()
        font = ImageFont.truetype(str(font_path), 100)

        # the  watermark is a new image with the same size of the source image
        # and added alpha channel.
        watermark = Image.new("RGBA", image_obj.size)

        # Then we draw on that new image via an ImageDraw instance: we
        # add text wiht a specific font and a surrounding rectangle, both gray
        drawing = ImageDraw.ImageDraw(watermark, "RGBA")
        drawing.text((150, 350), watermark_text, fill=gray_color, font=font)
        drawing.rectangle([(100, 320), (1150, 500)], outline=gray_color)

        # Turn the watermark image to grayscale. Then we use an alpha filter
        # to make drawings a little bit transparent
        grayscale_watermark = watermark.convert("L")
        watermark.putalpha(grayscale_watermark)

        # We then paste the watermark on the source image
        image_obj.paste(watermark, None, watermark)

        return image_obj


if __name__ == '__main__':
    # load source image
    src_img_path = (pathlib.Path('..') / 'images' / 'tiger.jpg').resolve()
    with Image.open(str(src_img_path)) as img:

        # call the magic!
        watermarked_img = watermark_image(img, 'MY WATERMARK')

        # create target image and save
        watermarked_img_path = pathlib.Path('watermarked.jpg')
        watermarked_img_path.touch()
        watermarked_img.save(str(watermarked_img_path.resolve()))

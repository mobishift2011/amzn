#!/usr/bin/env python
from PIL import Image, ImageChops

def trim(im, padding=5):
    """
    trim image, leave padding width
    """
    bg = Image.new(im.mode, im.size, im.getpixel((0,0)))
    diff = ImageChops.difference(im, bg)
    diff = ImageChops.add(diff, diff, 2.0, -100)
    bbox = diff.getbbox()
    obbox = im.getbbox()
    x0,y0 = max(bbox[0]-padding, obbox[0]), max(bbox[1]-padding, obbox[1])
    x1,y1 = min(bbox[2]+padding, obbox[2]), min(bbox[3]+padding, obbox[3])
    return im.crop((x0,y0,x1,y1))

def scale(im, size, method=Image.ANTIALIAS, centering=(0.5,0.7), bgcolor='white'):
    """
    resize 'image' to 'max_size' keeping the aspect ratio 
    and place it in center of backgoundcolor 'max_size' image 
    """
    im_aspect = 1. * im.size[0] / im.size[1]
    out_aspect = 1. * size[0] / size[1]
    if im_aspect >= out_aspect:
        scaled = im.resize((size[0], int(round(size[0]/im_aspect))), method)
    else:
        scaled = im.resize((int(round(size[1]*im_aspect)), size[1]), method)

    offset = (int((size[0] - scaled.size[0])*centering[0]), int((size[1] - scaled.size[1])*centering[1]))
    try:
        back = Image.new(im.mode, size, bgcolor)
    except TypeError:
        if im.mode != "RGB":
            im = im.convert("RGB")
        back = Image.new(im.mode, size, bgcolor)
    back.paste(scaled, offset)
    return back

def crop(im, size, method=Image.ANTIALIAS, centering=0.5):
    """
    resize 'image' to size, keeping the aspect ratio
    and drop the unecessary part of image, leaving only topleft part
    """
    im_aspect = 1. * im.size[0] / im.size[1]
    out_aspect = 1. * size[0] / size[1]
    if im_aspect >= out_aspect:
        w, h = im.size[1]*out_aspect, im.size[1]
        d = im.size[0] - w
        croped = im.crop((int(d*centering), 0, int(w+d*centering), h))
    else:
        w, h = im.size[0], im.size[0]/out_aspect,
        d = im.size[1] - h
        croped = im.crop((0, int(d*(1-centering)), w, int(h+d*(1-centering))))
    croped.thumbnail(size, method)
    return croped

if __name__ == '__main__':
    pass


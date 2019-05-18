from PIL import Image
import os, sys

def fix_size(fn, desired_w=224, desired_h=224, fill_color=(0, 0, 0, 255)):
    """Edited from https://stackoverflow.com/questions/44231209/resize-rectangular-image-to-square-keeping-ratio-and-fill-background-with-black"""
    im = Image.open(fn)
    x, y = im.size

    desired_ratio = desired_w / desired_h

    w = max(desired_w, x)
    h = int(w / desired_ratio)
    if h < y:
        h = y
        w = int(h * desired_ratio)

    new_im = Image.new('RGB', (w, h), fill_color)
    new_im.paste(im, ((w - x) // 2, (h - y) // 2))
    return new_im.resize((desired_w, desired_h))

if __name__ == '__main__':
    path = sys.argv[1]
    img = fix_size(path)
    img.save('tmp.jpg')
    img.show()
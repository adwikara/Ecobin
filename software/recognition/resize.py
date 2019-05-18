from PIL import Image
import os, sys

def make_square(im, min_size=224, fill_color=(0, 0, 0, 0)):
    x, y = im.size
    size = max(min_size, x, y)
    new_im = Image.new('RGBA', (size, size), fill_color)
    new_im.paste(im, int(((size - x) / 2), int((size - y) / 2)))
    return new_im

def fix_size(fn, desired_w=224, desired_h=224, fill_color=(0, 0, 0, 255)):
    im = Image.open(fn)
    x, y = im.size
    if x==224 and y==224:
        return
    desired_ratio = desired_w / desired_h

    w = max(desired_w, x)
    h = int(w / desired_ratio)
    if h < y:
        h = y
        w = int(h * desired_ratio)

    new_im = Image.new('RGB', (w, h), fill_color)
    new_im.paste(im, ((w - x) // 2, (h - y) // 2))
    return new_im.resize((desired_w, desired_h))

def resize(path):
    if os.path.isfile(path+ ".DS_Store"):
        os.remove(path+ ".DS_Store")
    dirs = os.listdir( path )
    for item in dirs:
        if os.path.isfile(path+item):
            # im = Image.open(path+item)
            # rgb_im = im.convert('RGB')
            f,e = os.path.splitext(path+item)
            imResize = fix_size(path+item)
            if imResize==None: 
                continue
            # imResize = rgb_im.resize((224,224), Image.ANTIALIAS)
            imResize.save(f + '_resized.jpg', 'JPEG', quality=90)
            os.remove(path+item)

def main():
    path = sys.argv[1]
    resize(path)

if __name__ == "__main__":
    # execute only if run as a script
    main()
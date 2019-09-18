from PIL import Image
from PIL import ExifTags
imgName = '291c0ee32e0df140e7f7b1627ddcb2a36f83aff9b3ae671439bf7e345af264e7.jpg'
img = Image.open(imgName)
print(img.format)

try:
    for orientation in ExifTags.TAGS.keys():
        if ExifTags.TAGS[orientation] == 'Orientation':
            break
    exif = dict(img._getexif().items())

    if exif[orientation] == 3:
        img = img.transpose(Image.ROTATE_180)
    elif exif[orientation] == 6:
        img = img.transpose(Image.ROTATE_270)
    elif exif[orientation] == 8:
        img = img.transpose(Image.ROTATE_90)

except (AttributeError, KeyError, IndexError):
    # cases: image don't have getexif
    pass

size = img.size

width = size[0]
height = size[1]

if width > 1028 or height > 1028:
    factor = 1
    if height > width:
        factor = 1028 / height
    else:
        factor = 1028 / width

    size = (int(width * factor), int(height * factor))

img = img.resize(size, Image.BILINEAR)

img.save('resize_' + imgName)

img.close()
import base64
from PIL import Image
from io import BytesIO
from PIL import ExifTags
import time
from GladFood import settings

MAX_SIZE = 500

# imgBase64 = imgBase64.split(',')
def resize(imgBase64):
    random = str(time.time())
    im = Image.open(BytesIO(base64.b64decode(imgBase64)))
    im_format = im.format
    random = random + str(time.time())
    # im = Image.open('image.jpg')
    # print(str(im.format).lower())
    # print(f"data:image/{str(im.format).lower()};base64,{imgBase64}")

    

    # print(base64.b64encode(im)[:10])
    try:
        for orientation in ExifTags.TAGS.keys():
            if ExifTags.TAGS[orientation] == 'Orientation':
                break
        exif = dict(im._getexif().items())

        if exif[orientation] == 3:
            im = im.transpose(Image.ROTATE_180)
        elif exif[orientation] == 6:
            im = im.transpose(Image.ROTATE_270)
        elif exif[orientation] == 8:
            im = im.transpose(Image.ROTATE_90)

    except (AttributeError, KeyError, IndexError):
        # cases: image don't have getexif
        pass

    size = im.size

    width = int(size[0])
    height = int(size[1])

    if width > MAX_SIZE or height > MAX_SIZE:
        factor = 1
        if height > width:
            factor = MAX_SIZE / height
        else:
            factor = MAX_SIZE / width

        size = (int(width * factor), int(height * factor))

    im = im.resize(size, Image.BILINEAR)
    random = random + str(time.time())
    # im_name = str(time.time()) + imgBase64[1] + imgBase64[-1] + '.' + im_format
    # im.save(im_name, format=im_format)
    # with open(im_name, "rb") as img_file:
    #     img_base64_resize = base64.b64encode(img_file.read()).decode("utf-8")


    # img_base64_resize = base64.b64encode(im.tobytes()).decode("utf-8")

    # buffered = BytesIO()
    # im.save(buffered, format=im_format)
    # img_base64_resize = base64.b64encode(buffered.getvalue()).decode("utf-8")
    # return f"data:image/{str(im_format).lower()};base64,{img_base64_resize}"

    im_name = random + str(time.time()) + imgBase64[1] + imgBase64[-1] + '.' + im_format
    im.save(settings.MEDIA_ROOT + '/' + im_name, format=im_format)
    return settings.MEDIA_URL + im_name

# im.save(imgBase64[0])
# data:image/png;base64,


# im = Image.open('image.jpg')
# print(base64.b64encode(im)[:10])
# imgBase64Test = "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";
# print(resize(imgBase64Test))

from PIL import Image, ImageChops, ImageEnhance
import sys, os.path
import cv2


def ELA(in_filename, out_filename):

    im = Image.open(in_filename)

    im.save("ela.jpg", 'JPEG', quality=95)
    resaved_im = Image.open("ela.jpg")

    ela_im = ImageChops.difference(im, resaved_im)
    extrema = ela_im.getextrema()
    max_diff = max([ex[1] for ex in extrema])
    scale = 255.0/max_diff
    print scale
    ela_im = ImageEnhance.Brightness(ela_im).enhance(scale*2)
    print "Maximum diffrence was %d" % (max_diff)

    ela_im.save(out_filename)


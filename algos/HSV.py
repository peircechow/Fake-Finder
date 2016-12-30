import time, numpy, sys, os
from PIL import Image
from matplotlib import colors
import cv2

Image.MAX_IMAGE_PIXELS = None #disable resolution limit

def gen_bboxs(pil_img,sqrt_num):
    """ Generate list of tuples with coordinates of bboxs.
        img is Image object from PIL module
        sqrt_num is squared number of bboxs you want to have
        bbox_tuple = (left, upper, right, lower )"""

    width=pil_img.size[0]
    height=pil_img.size[1]

    x = divmod(width, sqrt_num)[0]
    y = divmod(height, sqrt_num)[0]

    widths = [(0, x)]
    for n in range(sqrt_num-2):
        z=widths[-1][-1]
        widths.append((z, z+x))
    widths.append((widths[-1][-1], width))

    heights = [(0,y)]
    for n in range(sqrt_num-2):
        z=heights[-1][-1]
        heights.append((z, z+y))
    heights.append((heights[-1][-1], height))
        
    bboxs=[]
    for num1 in range(sqrt_num):
        for num2 in range(sqrt_num):
            bboxs.append((widths[num2][0], heights[num1][0], widths[num2][1], heights[num1][1]))

    return bboxs

def YCbCr_to_RGB(arr):
    """ Converts YCbCr colorspace to RGB color space.
        *arr* is numpy array. Conversion formula assumes that YCbCr have the
        full 8-bit range of 0-255. Result is float"""
    
    # check length of the last dimension (should be 3 --> i.e. 3 channels)
    if arr.shape[-1] != 3:
        raise ValueError("Last dimension of input array must be 3; "
                         "shape {shp} was found.".format(shp=arr.shape))
    # assure that array is int (not e.g. uint8)
    Y=arr[:,:,0].astype(int)
    Cb=arr[:,:,1].astype(int)
    Cr=arr[:,:,2].astype(int)
    
    r = Y + (1.402 * (Cr-128))
    g = Y + (-0.344136 * (Cb-128)) + (-0.714136 *(Cr-128))
    b = Y + (1.772 * (Cb-128))

    return numpy.concatenate([aux[..., numpy.newaxis] for aux in [r,g,b]], axis=2)


def HSV(in_pth, out_pth):

    t0 = time.time()
    img = Image.open(in_pth)
    height, width = (img.size[0],img.size[1])
    t1 = time.time()
    print 'Image loaded in %.2f seconds' % (t1-t0)

    #Check image mode (RGB or YCbCr)
    mode = img.getbands()

    #Split image
    bboxs = gen_bboxs(img,50)
    small_imgs = [img.crop(bbox) for bbox in bboxs]
    t2 = time.time()
    del img
    print "Image splited in %.2f seconds\n" % (t2-t1)

    #Process images
    i=1
    part_count=len(small_imgs)
    small_hsv=[]
    for small in small_imgs:
        if mode == ('R', 'G', 'B'):
            rgb = numpy.array(small)/255.0
        elif mode == ('Y', 'Cb', 'Cr'):
            ycbcr= numpy.array(small)
            rgb = YCbCr_to_RGB(ycbcr)/255.0
        else:
            raise TypeError("Unsupported image colorspace! Must be RGB or YCbCr; "
                         "{mode} was found.".format(mode=mode))
    
        hsv=colors.rgb_to_hsv(rgb)
        small_hsv.append(Image.fromarray(numpy.uint8(hsv*255.0)))
        i+=1
        progress=divmod((i*100.0)/part_count, 10)
        if progress[1]==0:
            print "Processing image parts... %s"%(progress[0]*10)+r'%'
    del small_imgs, small
    t3=time.time()
    print 'Processing completed in %.2f seconds \n'%(t3-t2)


    #Merge image (RGB is HSV)
    new_img = Image.new('RGB', (height, width))
    i=0
    for small in small_hsv:
        new_img.paste(small, bboxs[i])
        i+=1
    t4=time.time()
    del small_hsv#, small
    print 'Image merged in %.2f seconds' % (t4-t3)

    #Save new image
    print 'Saving converted image...'
    
    new_img.save(out_pth)

    #cv2.imwrite("HSV.jpg",new_img)
    del new_img
    t5=time.time()
    print 'Image saved in %.2f seconds\n'%(t5-t4)


    #Overall time
    tn=time.time()
    print 'Overall time of processing: %.2f seconds' % (tn-t0)
    



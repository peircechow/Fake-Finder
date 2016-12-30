import numpy as np
import pywt
import cv2    


def w2d(in_pth, out_pth, mode='haar', level=1):
    #Datatype conversions
    #convert to grayscale
    img = cv2.imread(in_pth)
    imArray = cv2.cvtColor( img,cv2.COLOR_RGB2GRAY )
    #convert to float
    imArray =  np.float32(imArray)   
    imArray /= 255;
    # compute coefficients 
    coeffs=pywt.wavedec2(imArray, mode, level=level)

    #Process Coefficients
    coeffs_H=list(coeffs)  
    coeffs_H[0] *= 0;  

    # reconstruction
    imArray_H=pywt.waverec2(coeffs_H, mode);
    imArray_H *= 255;
    imArray_H = np.uint8(imArray_H)

    cv2.imwrite(out_pth,imArray_H)
    # return imArray_H # returns the image
    #Display result
    # #cv2.imwrite("%s_wavelet"%img,imArray_H)
    # cv2.imshow('image',imArray_H)
    
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

#  w2d("test5.jpg",'db1',5)

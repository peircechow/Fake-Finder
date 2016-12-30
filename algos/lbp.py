import copy #have to test this out first
import cv2


def thresholded(center, pixels):
    out = []
    for a in pixels:
        if a >= center:
            out.append(1)
        else:
            out.append(0)
    return out


def get_pixel_else_0(l, idx, idy, default=0):
    try:
        return l[idx,idy]
    except IndexError:
        return default


def LBP(in_filename, out_filename):
    img = cv2.imread(in_filename, 0)
    transformed_img = copy.copy(img)

    for x in range(0, len(img)):
        for y in range(0, len(img[0])):
            center        = img[x,y]
            top_left      = get_pixel_else_0(img, x-1, y-1)
            top_up        = get_pixel_else_0(img, x, y-1)
            top_right     = get_pixel_else_0(img, x+1, y-1)
            right         = get_pixel_else_0(img, x+1, y )
            left          = get_pixel_else_0(img, x-1, y )
            bottom_left   = get_pixel_else_0(img, x-1, y+1)
            bottom_right  = get_pixel_else_0(img, x+1, y+1)
            bottom_down   = get_pixel_else_0(img, x,   y+1 )

            values = thresholded(center, [top_left, top_up, top_right, right, bottom_right,
                                          bottom_down, bottom_left, left])

            weights = [1, 2, 4, 8, 16, 32, 64, 128]
            res = 0
            for a in range(0, len(values)):
                res += weights[a] * values[a]

            transformed_img.itemset((x,y), res)

        print x
    cv2.imwrite(out_filename, transformed_img)
    return img

#cv2.imwrite("%s_LBP.jpg"%file_name, transformed_img)
# cv2.imshow('image_%s'%file_name, img)
# cv2.imshow('thresholded image_%s'%file_name, transformed_img)
#
# hist,bins = np.histogram(img.flatten(),256,[0,256])
#
# cdf = hist.cumsum()
# cdf_normalized = cdf * hist.max()/ cdf.max()
# cv2.waitKey(0)

# plt.plot(cdf_normalized, color = 'b')
# plt.hist(transformed_img.flatten(),256,[0,256], color = 'r')
# plt.xlim([0,256])
# plt.legend(('cdf','histogram'), loc = 'upper left')
# plt.show()



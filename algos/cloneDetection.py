# SIFT kpMatching in one image
import cv2  # more or less done, just need to install correct version of cv2 to get SIFT()
import numpy as np
import drawMatches as dm
import time


class Image:
    def __init__(self, img, status):  # stores the image and give the number of matches1 (<40) matches2 (<50)
        self.img = img
        self.status = status

    def get_img(self):
        return self.img

    def get_status(self):
        return self.status


def sift_method(img):
    sift = cv2.SIFT()  # note that this SIFT()can be found on 2.4.6.1. download 2.4.13

    # find the keypoints and descriptors with SIFT
    kp, des = sift.detectAndCompute(img, None)

    print "No of keypoints:", len(des)
    # print("Number of kp1 is", len(kp1))
    matchPair = dm.BFMatcherWithin(des, kp)  # unsorted, returns an array of Pair objects, with distance, kp1, and kp2
    print "Keypoints Matched. Sorting Keypoints..."
    matchPair = sorted(matchPair, key=lambda x: x.distance)
    print "Keypoints sorted"

    return matchPair


def brief_method(img):
    # Initiate STAR detector
    star = cv2.FeatureDetector_create("STAR")

    # Initiate BRIEF extractor
    brief = cv2.DescriptorExtractor_create("BRIEF")

    # find the keypoints with STAR
    kp = star.detect(img, None)

    # compute the descriptors with BRIEF
    kp, des = brief.compute(img, kp)

    if len(kp) < 900:
        return False  # so that we can do on SIFT

    print "No of keypoints:", len(des)
    # print("Number of kp1 is", len(kp1))
    matchPair = dm.BFMatcherWithin(des, kp)  # unsorted, returns an array of Pair objects, with distance, kp1, and kp2
    print "Keypoints Matched. Sorting Keypoints..."
    matchPair = sorted(matchPair, key=lambda x: x.distance)
    print "Keypoints sorted"

    return matchPair


# cv2.imwrite("%s_SIFTmatch(within).jpg" %file_name,img3)

def cloneDetection(in_filename, out_filename, T1 = 50):  # returns an image and the status
    img1 = cv2.imread(in_filename)
    # Threshold
    T2 = 60
    T3 = 80

    i = 0
    j = 0
    k = 0

    start = time.time()
    matchPair = brief_method(img1)
    method = "BREIF"
    if matchPair is False:
        matchPair = sift_method(img1)
        method = "SIFT"
    end = time.time()
    print "Time taken to draw matches" , end - start
    print "%s is used." % method
    print "no. of Keypoints", len(matchPair)

    for m in matchPair:
        if m.distance > T1:
            break
        i += 1

    for n in matchPair:
        if n.distance > T2:
            break
        j += 1

    print "No. of matches under euclidean distance of %s is %s" % (str(T1), str(i))
    if i >= 10:  # many many matches and i>10
        img3 = dm.drawMatchesWithin(img1, matchPair[:j])
        statement = "This is definitely a tampered image"

    elif 2 < i < 10:
        img3 = dm.drawMatchesWithin(img1, matchPair[:j])
        statement = 'This may be a tampered image'

    else:  # i==0
        img3 = dm.drawMatchesWithin(img1, matchPair[:i])
        statement = "Copy-move image tampering is not detected"

    print statement

    cv2.imwrite(out_filename, img3)
    img_obj = Image(img3, statement)
    status = img_obj.status
    return status

# file_name = "test"
# img1 = cv2.imread('%s.jpg' % file_name, 0)  # queryImage
# cloneDetection(img1)

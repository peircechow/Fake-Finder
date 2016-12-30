import numpy as np
import cv2
import random

class Pair:
    def __init__(self,dist,kp1Pt,kp2Pt): # just need to know the corrdinates by linking the points there
        self.distance = dist
        self.kp1Pt = kp1Pt
        self.kp2Pt = kp2Pt

    def getDistance(self):
        return self.distance

    def getKp1(self):
        return self.kp1Pt

    def getKp2(self):
        return self.kp2Pt


def BFMatcherWithin(des, kp): # O(n!) :(
    #cauculating eucledian distance
    
    matches = []

    for i in range(len(des)-1):
        kp_index = i
        des1 = des[i] # [18.0,0.0,.....,0.0,17.0]
        desOthers = des[i+1:] #
        minDist = 9999999999999999999999999999
        for d in desOthers: # going through each of the second des
            
            kp_index += 1
            total = 0
           
            for j in range(len(des[i])): # going through each vector dimension
                total += float(int(des1[j]) - int(d[j])) **(2) # sqrt of (x1-x2)^2 + ..............
            total = total ** (0.5)
                #print(total), "Curr total"
            if total < minDist: # or if total == 0
                minDist = total
                kp1Pt = kp[i].pt
                kp2Pt = kp[kp_index].pt
                # print (total), "@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@"
            if total == 0 or total == 0.0:
                break
        # so before moving on to the next element in des, I have to set these first
        try:
            p = Pair(minDist, kp1Pt, kp2Pt)
            matches.append(p)

        except:
            pass


    return matches




def drawMatchesWithin(img, matches):
    """
    drawing matches within an image, to match kp of SIFT/SURF
    """

    #  img = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)
    
    # For each pair of points we have between both images
    # draw circles, then connect a line between them
    for mat in matches:
        color1=random.randint(0,255)
        color2=random.randint(0,255)
        color3=random.randint(0,255)
        (x1,y1) = mat.kp1Pt
        (x2,y2) = mat.kp2Pt

        # Draw a small circle at both co-ordinates
        # radius 4
        # colour blue
        # thickness = 1
        #PEIRCE EDITED VERSION: randomise the colour
        
        cv2.circle(img, (int(x1),int(y1)), 4, (color1, color2, color3), 1)   
        cv2.circle(img, (int(x2),int(y2)), 4, (color1, color2, color3), 1)
        
        # Draw a line in between the two points
        # thickness = 1
        
        cv2.line(img, (int(x1),int(y1)), (int(x2),int(y2)), (color1, color2, color3), 1)


    # Show the image
    #cv2.imshow('Matched Features', out)
    #cv2.waitKey(0)
    

    # Also return the image if you'd like a copy
    return img


def drawMatches2(img1, kp1, matches):

    rows1 = img1.shape[0]
    cols1 = img1.shape[1]

    out = img1


    # draw circles, then connect a line between them
    for mat in matches:
        color1 = random.randint(0, 255)
        color2 = random.randint(0, 255)
        color3 = random.randint(0, 255)
        # Get the matching keypoints for each of the images
        img1_idx = mat.queryIdx
        img2_idx = mat.trainIdx

        # x - columns
        # y - rows
        print "mat.queryIdx is:", img1_idx, type(img1_idx)
        print "mat.trainIdx is:", img2_idx, type(img2_idx)
        (x1, y1) = kp1[img1_idx].pt
        (x2, y2) = kp2[img2_idx].pt

        # Draw a small circle at both co-ordinates
        # radius 4
        # colour blue
        # thickness = 1
        # PEIRCE EDITED VERSION: randomise the colour

        cv2.circle(out, (int(x1), int(y1)), 4, (color1, color2, color3), 1)
        cv2.circle(out, (int(x2), int(y2)), 4, (color1, color2, color3), 1)
        print("mat:", mat)
        print (int(x2) + cols1, int(y2))
        # cv2.drawKeypoints(out,kp1,flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
        # Draw a line in between the two points
        # thickness = 1
        # colour blue
        cv2.line(out, (int(x1), int(y1)), (int(x2) + cols1, int(y2)), (color1, color2, color3), 1)


    # Also return the image if you'd like a copy
    return out
    

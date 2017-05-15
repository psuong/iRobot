import numpy as np
import cv2
import sys
import os
import tesserocr
from PIL import Image
"""Do not use this, it is way too slow"""
#PLAN: Use some text region detector to find regions of interest, feed to tesseract
#to perform OCR


def captch_ex(img):
    

    img_final = img
    img2gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret, mask = cv2.threshold(img2gray, 180, 255, cv2.THRESH_BINARY)
    image_final = cv2.bitwise_and(img2gray, img2gray, mask=mask)
    ret, new_img = cv2.threshold(image_final, 180, 255, cv2.THRESH_BINARY)  # for black text , cv.THRESH_BINARY_INV
    '''
            line  8 to 12  : Remove noisy portion
    '''
    kernel = cv2.getStructuringElement(cv2.MORPH_CROSS, (3,
                                                         3))  # to manipulate the orientation of dilution , large x means                                 horizonatally dilating  more, large y means vertically dilating more
    dilated = cv2.dilate(new_img, kernel, iterations=9)  # dilate , more the iteration more the dilation


    #contours, hierarchy = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)  # get contours

    image, contours, hierarchy = cv2.findContours(dilated,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)  # cv3.x.x

    for contour in contours:
        # get rectangle bounding contour
        [x, y, w, h] = cv2.boundingRect(contour)

        # Don't plot small false positives that aren't text
        if (w < 80 and h < 80) or (w > 120 and h > 120):
            continue

        # draw rectangle around contour on original image
        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 255), 2)

        #you can crop image and send to OCR  , false detected will return no text :)
        cropped = Image.fromarray(img_final[y :y +  h , x : x + w])

        #s = file_name + '/crop_' + str(index) + '.jpg'
        #cv2.imwrite(s , cropped)
        #index = index + 1
        print("Test")



    # write original image with added contours to disk
    cv2.imshow('captcha_result', img)
    cv2.waitKey(10)


def frame_process(img):

    # for visualization
    vis      = img.copy()


    # Extract channels to be processed individually
    channels = cv2.text.computeNMChannels(img)
    # Append negative channels to detect ER- (bright regions over dark background)
    cn = len(channels)-1
    for c in range(0,cn):
      channels.append((255-channels[c]))

    # Apply the default cascade classifier to each independent channel (could be done in parallel)
    print("Extracting Class Specific Extremal Regions from "+str(len(channels))+" channels ...")
    print("    (...) this may take a while (...)")
    for channel in channels:

      erc1 = cv2.text.loadClassifierNM1(pathname + '/trained_classifierNM1.xml')
      er1 = cv2.text.createERFilterNM1(erc1,16,0.00015,0.13,0.2,True,0.1)

      erc2 = cv2.text.loadClassifierNM2(pathname + '/trained_classifierNM2.xml')
      er2 = cv2.text.createERFilterNM2(erc2,0.5)

      regions = cv2.text.detectRegions(channel,er1,er2)

      if regions:
          rects = cv2.text.erGrouping(img,channel,[r.tolist() for r in regions])
      #rects = cv2.text.erGrouping(img,gray,[x.tolist() for x in regions], cv2.text.ERGROUPING_ORIENTATION_ANY,'../../GSoC2014/opencv_contrib/modules/text/samples/trained_classifier_erGrouping.xml',0.5)

      #Visualization
      for r in range(0,np.shape(rects)[0]):
        rect = rects[r]
        cv2.rectangle(vis, (rect[0],rect[1]), (rect[0]+rect[2],rect[1]+rect[3]), (0, 0, 0), 2)
        cv2.rectangle(vis, (rect[0],rect[1]), (rect[0]+rect[2],rect[1]+rect[3]), (255, 255, 255), 1)


    #Visualization
    cv2.imshow("Text detection result", vis)
    


cap = cv2.VideoCapture("http://192.168.43.1:8080/video")


while(cap.isOpened()):

    ret, frame = cap.read()
    captch_ex(frame[:, 120:])
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

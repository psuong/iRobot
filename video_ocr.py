import numpy as np
import cv2
import sys
import os

"""Do not use this, it is way too slow"""
#PLAN: Use some text region detector to find regions of interest, feed to tesseract
#to perform OCR

pathname = os.path.dirname(os.path.abspath(sys.argv[0]))

erc1 = cv2.text.loadClassifierNM1(pathname + '/trained_classifierNM1.xml')
erc2 = cv2.text.loadClassifierNM2(pathname + '/trained_classifierNM2.xml')



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


cap = cv2.VideoCapture("curved_roads.mp4")
print("Hello!")

while(cap.isOpened()):
    print("Hello!!")
    ret, frame = cap.read()
    frame_process(frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

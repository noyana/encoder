# import the necessary packages
from __future__ import print_function
from imutils.object_detection import non_max_suppression
from imutils import paths
import numpy as np
import argparse
import imutils
import cv2
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--images", required=True, help="path to images directory")
args = vars(ap.parse_args())
# initialize the HOG descriptor/person detector
hog = cv2.HOGDescriptor()
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())
# loop over the image paths
imagePaths = list(paths.list_images(args["images"]))
for imagePath in imagePaths:
    # load the image and resize it to (1) reduce detection time
    # and (2) improve detection accuracy
    imagefile = cv2.imread(imagePath)

    # Initializing the HOG person
    # detector
    hog = cv2.HOGDescriptor()
    hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

    # Reading the Image
    image = cv2.imread(imagefile)

    # Resizing the Image
    image = imutils.resize(image,
                           width=min(400, image.shape[1]))

    # Detecting all the regions in the
    # Image that has a pedestrians inside it
    (regions, _) = hog.detectMultiScale(image,
                                        winStride=(4, 4),
                                        padding=(4, 4),
                                        scale=1.05)

    # Drawing the regions in the Image
    for (x, y, w, h) in regions:
        cv2.rectangle(image, (x, y),
                      (x + w, y + h),
                      (0, 0, 255), 2)

    # Showing the output Image
    cv2.imshow("Image", image)
    cv2.waitKey(0)

    cv2.destroyAllWindows()

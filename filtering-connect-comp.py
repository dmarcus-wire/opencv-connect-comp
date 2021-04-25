# USAGE
# pythong filtering-connect-comp.py -i license_plate.png

# import necessary packages
import numpy as np
import argparse
import cv2

# construct the argument parse
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True,
                help="path to input image")
ap.add_argument("-c","--connectivity", type=int, default=4,
                help="connectivity for connected component analysis")
args = vars(ap.parse_args())

# load the input image from disk
# convert to grayscale
# threshold it
image = cv2.imread(args["image"])
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
thresh = cv2.threshold(gray, 0, 255,
                       cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]

# apply connected components analysis to the thresholded image
output = cv2.connectedComponentsWithStats(
    thresh, args["connectivity"], cv2.CV_32S)
(numLabels, labels, stats, centroids) = output

# init a output mask to store all (and just) the characters parsed from the plate
# same spatial dimensions as grayscale
mask = np.zeros(gray.shape, dtype="uint8")

# loop over the number of unique connected components,
# skip over the first label as it is background
# if i == 0  its the background, just start when i == 1
for i in range(1, numLabels):
    # extract the connected components statistics for the current label
    x = stats[i, cv2.CC_STAT_LEFT]
    y = stats[i, cv2.CC_STAT_TOP]
    w = stats[i, cv2.CC_STAT_WIDTH]
    h = stats[i, cv2.CC_STAT_HEIGHT]
    area = stats[i, cv2.CC_STAT_AREA]

    # for each connected component drew the mask with waitkey call and print each stat variables
    # record w, h, area and determined the values for the keepW/H/A below
    # print(x, y, h, area)
    # componentMask = (labels == i).astype("uint8") * 255
    # cv2.imshow("Mask", mask)
    # cv2.waitKey(0)

    # filter the components
    # ensure the w, h, and area are all neither too small or too big
    keepWidth = w > 10 and w < 50 # original 5 and 50
    keepHeight = h > 45 and h < 65
    keepArea = area > 500 and area < 1500

    # ensure the connected component we are examining passes for all 3 tests
    if all((keepWidth, keepHeight, keepArea)):
        # construct a mask for the current connected components
        # take the bitwise OR with the mask
        print("[INFO] keeping connected component {}".format(i))
        componentMask = (labels == i).astype("uint8") * 255
        mask = cv2.bitwise_or(mask, componentMask) # add the compnentmask to the character mask

# show the original image
cv2.imshow("Image", image)
# show the mask for the plate characters
cv2.imshow("Characters", mask)
cv2.waitKey(0)

# you can then pass into a character recognition model
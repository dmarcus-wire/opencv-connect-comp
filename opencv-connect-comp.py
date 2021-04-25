# USAGE
# python opencv-connect-comp

# thresholding
# foreground = white = 255
# background = black = 0
# extract just the pixels that are connected

# import necessary packages
import argparse
import cv2

#SETUP
# construct the argument parser
ap = argparse.ArgumentParser()
ap.add_argument("-i","--image", required=True,
                help="path to input image")
# 4 connectivity is good for most
ap.add_argument("-c","--connectivity", type=int, default=4,
                help="connectivity for connected component analysis")
args = vars(ap.parse_args())

#DATA_PRE_PROCESSING
# load the input image from disk, convert it to grayscale and threshold it
image = cv2.imread(args["image"]) # load image from disk
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) # convert to grayscale
thresh = cv2.threshold(gray, 0, 255, # use OTSU (Otsu's method) autothresholding to segment foreground from background
                       cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]

# show input grayscale of the license play
cv2.imshow("Gray", gray)
# applied thresholding foreground = white, background = black
cv2.imshow("Thresh", thresh)
cv2.waitKey(0)

# apply connected component analysis to threshold image
# opencv has 4 connected component analysis
# withStats is the most used and recommended
# 3 params: binary image = threshold; connectivity type; datatype 32-bit short CV_32S
# numLabels = total unique labels; labels = NxN integer map from thresh image; stats = startingX,Y, H and W, center X and Y coordinate
output = cv2.connectedComponentsWithStats(
    thresh, args["connectivity"], cv2.CV_32S) # binary thresh image, connectivity command, datatype CV_32S
(numLabels, labels, stats, centroids) = output # total # of unique labels, stats incl. bounding box, centroids/center of each component

# loop over the number of unique connected component labels
# id = 0 is the background, so we want to check and verify its the background
# typically you wouldnt process this
for i in range(0, numLabels):
    # if this is the first component then we examine the *background*
    if i == 0:
        text = "examing component {}/{} (background".format(
            i + 1, numLabels)

# otherwise, we are examining an actual connected component
    else:
        text = "examining component {}/{}".format( i + 1, numLabels)

    # print a status message update for the current connected component
    print("[INFO] {}".format(text))

    # extract the connected component statistics and centroid for current label
    x = stats[i, cv2.CC_STAT_LEFT] # starting x
    y = stats[i, cv2.CC_STAT_TOP] # starting y
    w = stats[i, cv2.CC_STAT_WIDTH]
    h = stats[i, cv2.CC_STAT_HEIGHT]
    area = stats[i, cv2.CC_STAT_AREA]
    (cX, cY) = centroids[i]

    # clone the original image see we can draw on it
    # then draw a bounding box around the connected component
    # along with a circle corresponding to the centroid
    output = image.copy()
    cv2.rectangle(output, (x, y), (x + w, y + h), (0, 255, 0), 3) # draw bounding box from the starting x, y, add the w and h,
    cv2.circle(output, (int(cX), int(cY)), 4, (0, 0, 255), -1) # visualize the centroid with a circle

    # construct a mask for the current connected component
    # labels is an NxN matrix the same as the input image and multiple by 255
    # finding a pixel in the labels array that have the current connected component ID
    componentMask = (labels == i).astype("uint8") * 255

    # show the output image and connected components
    cv2.imshow("Output", output)
    cv2.imshow("Connected Components", componentMask)
    cv2.waitKey(0)
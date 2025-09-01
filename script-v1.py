
import cv2 as cv
import sys
i=0
img = cv.imread(cv.samples.findFile("starry_night.png"))

if img is None:
    sys.exit("Could not read the image.")

cv.imshow("Display window", img)
k = cv.waitKey(0)

if k == ord("s"):
    cv.imwrite(f"starry_night({i}).jpg", img)
    print("File was Saved")
from __future__ import print_function, division
from color_interpolation import color_interpolate_map
import cv2
import numpy as np

color_map = {
    0.0: (255, 0, 0),
    0.2: (255, 255, 255),
    0.5: (255, 255, 255),
    0.8: (0, 200, 255),
    1.0: (0, 0, 255)
}


def nothing(x):
    pass

cv2.namedWindow("Test")
cv2.createTrackbar("Temp", "Test", 0, 45, nothing)

image = np.zeros((500, 500, 3), dtype=np.uint8)

while True:
    image[:, :, :] = 0
    image[:, :, 1] = 255

    k = cv2.waitKey(1) & 0xFF
    if k == 27:
        break

    temp = cv2.getTrackbarPos("Temp", "Test")

    color = color_interpolate_map(color_map, temp / 45)

    image[:, :] = color

    temp -= 10
    cv2.putText(image, "Temp: " + str(temp) + "C", (20, 20), cv2.FONT_HERSHEY_PLAIN, 1.5, (0, 0, 0))

    cv2.imshow("Test", image)
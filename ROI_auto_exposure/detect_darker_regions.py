import cv2
import numpy as np

# Load the image in grayscale
img = cv2.imread('demo.jpg', cv2.IMREAD_GRAYSCALE)

# Find the pixel with the lowest intensity value
min_intensity = np.min(img)
min_intensity_loc = np.argwhere(img == min_intensity)[0]

# Print the location of the darkest spot
print('Darkest spot:', min_intensity_loc)

# Expand the darkest region by creating a mask with a threshold value
ret, mask = cv2.threshold(img, min_intensity + 10, 255, cv2.THRESH_BINARY)

# Apply morphological operations to the mask to fill in small gaps and remove noise
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5,5))
mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

# Find the contours of the mask
contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Draw the contours on the original image
img_contours = cv2.drawContours(img, contours, -1, (0,255,0), 2)

# Display the results
cv2.imshow('Original', img)
cv2.imshow('Mask', mask)
cv2.imshow('Contours', img_contours)
cv2.waitKey(0)
cv2.destroyAllWindows()

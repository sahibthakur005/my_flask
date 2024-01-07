import cv2
import numpy as np

# Load the image
image = cv2.imread(r'C:\Users\adesh\Desktop\imgex\bg\imgbg4.jpg')

# Define text and its style
text = "unnu Ai"
font = cv2.FONT_HERSHEY_SIMPLEX
font_scale = 1
font_thickness = 2
text_color = (0, 255, 255)  # Yellow color in BGR format

# Get text size
text_size = cv2.getTextSize(text, font, font_scale, font_thickness)[0]

# Position the text at the bottom right corner with a margin of 10 pixels
text_x = image.shape[1] - text_size[0] - 10
text_y = image.shape[0] - 10

# Overlay text on the image
cv2.putText(image, text, (text_x, text_y), font, font_scale, text_color, font_thickness)

# Display the image with the overlaid text
cv2.imshow('Styled Text on Image', image)
cv2.waitKey(0)
cv2.destroyAllWindows()
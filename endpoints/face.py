import cv2

# Load the two images
img1 = cv2.imread(r'C:\Users\adesh\Desktop\imgex\ejjx.jpg')
img2 = cv2.imread(r'C:\Users\adesh\Desktop\imgex\ejjx.jpg')

# Load the face detection model (e.g., Haar Cascade or a DNN-based face detector)
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

# Detect faces in both images
faces_img1 = face_cascade.detectMultiScale(img1, scaleFactor=1.1, minNeighbors=5)
faces_img2 = face_cascade.detectMultiScale(img2, scaleFactor=1.1, minNeighbors=5)

if len(faces_img1) > 0 and len(faces_img2) > 0:
    # Assume only one face in each image for simplicity (you might need to handle multiple faces)
    x1, y1, w1, h1 = faces_img1[0]
    x2, y2, w2, h2 = faces_img2[0]

    # Extract regions of interest (ROIs) for specific facial features (e.g., lips, hair)
    # Crop and copy color from img1 to img2
    # Replace this with code to extract and copy specific facial features' colors

    # Example: Copy the face from img1 to img2
    face_img1 = img1[y1:y1+h1, x1:x1+w1]
    img2[y2:y2+h2, x2:x2+w2] = face_img1

    # Save the modified img2 with transferred facial features' colors
    cv2.imwrite('img2_with_features.jpg', img2)
else:
    print("No faces detected in one or both images.")
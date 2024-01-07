from flask import Flask, request, jsonify, Blueprint
import base64
import os
import cv2
import tempfile
import rembg
import numpy as np
from PIL import Image
from io import BytesIO
from werkzeug.datastructures import FileStorage


bp = Blueprint('sketch', __name__)


@bp.route('/sketch', methods=['POST'])
def upload_image():
    if 'image' not in request.files:
        return jsonify({'message': 'No file part in the request'}), 400
    

    image_file = request.files['image']
    img3 = request.form['description']
    if image_file.filename == '':
        return jsonify({'message': 'No selected file'}), 400
    



    nparr = np.frombuffer(image_file.read(), np.uint8)
    image2 = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    img1 = rembg.remove(image2)
    #img2 = cv2.imread(img3)








# Read the image
    image = img1
#cv2.imread(r'C:\Users\adesh\Desktop\imgex\imm1.jpg')

# Convert the image to grayscale
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Invert the grayscale image
    inverted_gray_image = 255 - gray_image

# Apply Gaussian Blur
    blurred_image = cv2.GaussianBlur(inverted_gray_image, (33, 33), 0)

# Invert the blurred image
    inverted_blurred_image = 255 - blurred_image

# Create the pencil sketch by blending the grayscale image with the inverted blurred image
    pencil_sketch = cv2.divide(gray_image, inverted_blurred_image, scale=256.0)

    #os.remove(temp_file_path)




    # Define text and its style
    image = pencil_sketch
    text = "unnu Ai app"
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 1
    font_thickness = 2
    text_color = (255, 255, 255)  # Yellow color in BGR format

# Get text size
    text_size = cv2.getTextSize(text, font, font_scale, font_thickness)[0]

# Position the text at the bottom right corner with a margin of 10 pixels
    text_x = image.shape[1] - text_size[0] - 10
    text_y = image.shape[0] - 10

# Overlay text on the image
    cv2.putText(image, text, (text_x, text_y), font, font_scale, text_color, font_thickness)
    #os.remove(temp_file_path)




    retval, buffer = cv2.imencode('.png', image)

    img_str_bytes = base64.b64encode(buffer)
    image_byte_array = img_str_bytes.decode("utf-8")


    # Construct the response with message and byte array
    response_data = {
        'message': 'Image uploaded successfully as byte array',
        'image_byte_array': image_byte_array if image_byte_array else None
    }
 
    return jsonify(response_data), 200





if __name__ == '__main__':
    bp.run(debug=False)



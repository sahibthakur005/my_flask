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

bp = Blueprint('newbg5', __name__)

def process_image_chunks(file_storage):
    chunk_size = 4096 * 4096 # set chunk size
    output = BytesIO()
    while True:
        chunk = file_storage.read(chunk_size)
        if not chunk:
            break
        processed_chunk = rembg.remove(chunk)
        output.write(processed_chunk)
        return output.getvalue()

@bp.route('/newbg5', methods=['POST'])
def upload_image():
    if 'image' not in request.files:
        return jsonify({'message': 'No file part in the request'}), 400

    image_file = request.files['image']
    img3 = request.form['description']
    img4 = request.form['string1']
    if image_file.filename == '':
        return jsonify({'message': 'No selected file'}), 400

    

    # Resize img1 to match the dimensions of img2
   
#end  
    
   
    nparr = np.frombuffer(image_file.read(), np.uint8)
    image2 = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    img1 = rembg.remove(image2)
    img2 = cv2.imread(img3)
    
    # Resize img1 to 100x100
    
# Resize img1 to any specified size (e.g., 100x100)
    new_width = 400
    new_height = 400
    img1_resized = cv2.resize(img1, (new_width, new_height))

# Get the dimensions of img2
    height_img2, width_img2 = img2.shape[:2]

# Create a blank canvas of the size of img2
    composite = np.zeros((height_img2, width_img2, 3), dtype=np.uint8)

# Overlay img2 (background) on the composite canvas
    composite[:height_img2, :width_img2] = img2

# Calculate the position for img1 dynamically
    x_offset = 0
    #width_img2 - img1_resized.shape[1]  # Adjust if needed
    y_offset = height_img2 - img1_resized.shape[0]  # Adjust if needed

# Adjust the region in composite to match img1_resized shape
    composite_region = composite[y_offset:y_offset+img1_resized.shape[0], x_offset:x_offset+img1_resized.shape[1]]

# Ensure both shapes match or resize the region to match img1_resized
    if composite_region.shape[:2] != img1_resized.shape[:2]:
     composite_region = cv2.resize(composite_region, (img1_resized.shape[1], img1_resized.shape[0]))

# Blend img1 onto the composite canvas using alpha blending
    for c in range(3):
     composite[y_offset:y_offset+img1_resized.shape[0], x_offset:x_offset+img1_resized.shape[1], c] = \
        img1_resized[..., c] * (img1_resized[..., 3] / 255.0) + \
        composite_region[..., c] * (1.0 - img1_resized[..., 3] / 255.0)
     

     # Define text and its style
     image = composite
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
    #second text.....begin
     # Define text and its style
    
   # Assuming 'image' contains the image data

    text = img4
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 1
    font_thickness = 2
    text_color = (0, 255, 255)  # Yellow color in BGR format
    rect_color = (100, 0, 0)  # Blue color in BGR format

# Get text size
    text_size, _ = cv2.getTextSize(text, font, font_scale, font_thickness)

# Position the text at the bottom left corner with a margin of 10 pixels
    text_x = 10  # 10 pixels from the left edge
    text_y = image.shape[0] - 10  # 10 pixels from the bottom edge

# Position for the rectangle to cover the text
    rect_x = text_x - 5  # Add some padding to the text
    rect_y = text_y - text_size[1] - 5  # Adjust for text height and padding

# Draw a filled rectangle as the background for the text
    cv2.rectangle(image, (rect_x, rect_y), (text_x + text_size[0] + 5, text_y + 5), rect_color, -1)  # -1 thickness for filled rectangle

# Overlay text on the image
    cv2.putText(image, text, (text_x, text_y), font, font_scale, text_color, font_thickness)
    #os.remove(temp_file_path)
     




    retval, buffer = cv2.imencode('.png', image)
    img_str_bytes = base64.b64encode(buffer)
    image_byte_array = img_str_bytes.decode("utf-8")

    

     



    response_data = {
        'message': 'Images overlayed successfully as byte array',
        'image_byte_array': image_byte_array if image_byte_array else None
    }
 
    
    return jsonify(response_data), 200

if __name__ == '__main__':
    bp.run(debug=False)
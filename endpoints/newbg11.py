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


bp = Blueprint('newbg11', __name__)

#img2 = cv2.imread(r'C:\Users\adesh\Documents\GitHub\my_flask\endpoints\image\img2.jpg')  # Replace 

def process_image_chunks(file_storage):
    chunk_size = 4096 * 4096 #set chunk size
    output = BytesIO()
    while True:
        chunk = file_storage.read(chunk_size)
        if not chunk:
            break
        processed_chunk = rembg.remove(chunk)
        output.write(processed_chunk)
        return output.getvalue()
 




@bp.route('/newbg11', methods=['POST'])
def upload_image():
    if 'image' not in request.files:
        return jsonify({'message': 'No file part in the request'}), 400
    

    image_file = request.files['image']
    img3 = request.form['description']
    if image_file.filename == '':
        return jsonify({'message': 'No selected file'}), 400

    # Convert image file to byte array
    # using rembg
    #input_image = Image.open(file)
    #input_array = np.array(input_image)
    #output_array = rembg.remove(input_array)
    #output_image = Image.fromarray(output_array)
    #buffered = BytesIO()
    #output_image.save(buffered, format='JPEG')
    #img_str_bytes = base64.b64encode(buffered.getvalue())
    #image_file = file

    nparr = np.frombuffer(image_file.read(), np.uint8)
    image2 = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    img1 = rembg.remove(image2)
    img2 = cv2.imread(img3)
    
    #img1 = output_image
    #cv process begin
    #img1 = cv2.imread(r'C:\Users\adesh\Documents\GitHub\my_flask\endpoints\image\img1.jpg', cv2.IMREAD_UNCHANGED)  # Replace 'path_to_img1.png' with the actual path
     # Replace 'path_to_img2.png' with the actual path

# Ensure both images have the same dimensions
    img2 = cv2.resize(img2, (img1.shape[1], img1.shape[0]))

# Check if the foreground image has an alpha channel
    if img1.shape[-1] == 4:
      b, g, r, alpha = cv2.split(img1)

    # Normalize alpha channel to range 0-1
    alpha = alpha / 255.0

    # Convert alpha channel to 3-channel format
    alpha = cv2.merge((alpha, alpha, alpha))

    # Resize alpha channel to match image dimensions
    alpha = cv2.resize(alpha, (img1.shape[1], img1.shape[0]))

    # Calculate the weighted sum of the foreground and background images
    foreground = cv2.multiply(alpha, img1[:, :, :3].astype(float))
    background = cv2.multiply(1.0 - alpha, img2.astype(float))

    # Convert the result back to uint8
    result = cv2.convertScaleAbs(cv2.add(foreground, background))
    # Define text and its style
    image = result
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













    #input_array = file.read()
    #output_array = rembg.remove(input_array)
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

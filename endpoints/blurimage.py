from flask import Flask, request, jsonify, Blueprint
import base64
from rembg import remove
import os
import cv2
import tempfile
import rembg
import numpy as np
from PIL import Image
from io import BytesIO
from werkzeug.datastructures import FileStorage


bp = Blueprint('blurimage', __name__)

#img2 = cv2.imread(r'C:\Users\adesh\Documents\GitHub\my_flask\endpoints\image\img2.jpg')  # Replace 

def process_image_chunks(file_storage):
    chunk_size = 4096 * 4096 #set chunk size
    output = BytesIO()
    while True:
        chunk = file_storage.read(chunk_size)
        if not chunk:
            break
        processed_chunk = chunk
        output.write(processed_chunk)
        return output.getvalue()
 




@bp.route('/blurimage', methods=['POST'])
def upload_image():
    if 'image' not in request.files:
        return jsonify({'message': 'No file part in the request'}), 400
    

    image_file = request.files['image']
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

    file_storage = FileStorage(image_file)

    output_image = process_image_chunks(file_storage)
    
    temp_file_path = tempfile.NamedTemporaryFile(suffix='.png', delete=False).name
    with open(temp_file_path, 'wb') as temp_file:
        temp_file.write(output_image)
    
       
    original_img = cv2.imread(temp_file_path)

    #cv2 code start....
    # Load the original image
#original_img = cv2.imread(r'C:\xampp\htdocs\imageuploader\uploads\imgr1.jpg')

# Store the original image's shape for later use
    height, width, _ = original_img.shape

# Extract foreground using Rembg
    output = remove(cv2.imencode('.png', original_img)[1].tobytes())

    nparr = np.frombuffer(output, np.uint8)
    img_foreground = cv2.imdecode(nparr, cv2.IMREAD_UNCHANGED)

# Create a mask from the alpha channel of the foreground image
    alpha = img_foreground[:, :, 3]

# Resize the alpha channel to match the original image's size
    alpha_resized = cv2.resize(alpha, (width, height))

# Normalize the alpha channel to be between 0 and 1
    alpha_resized = alpha_resized / 255.0

# Remove alpha channel to blend properly
    img_foreground = img_foreground[:, :, :3]

# Resize the foreground to match the original image's size
    img_foreground_resized = cv2.resize(img_foreground, (width, height))

# Blur the background of the original image
    blurred_background = cv2.GaussianBlur(original_img, (195, 195), 0)  # Adjust the blur kernel size as needed

# Blend the foreground and blurred background using bitwise operations
    mask = np.repeat(np.expand_dims(alpha_resized, axis=2), 3, axis=2)
    result = np.uint8(img_foreground_resized * mask + blurred_background * (1 - mask))

# Replace the original image's region with the blended image
    original_img = result
    os.remove(temp_file_path)

    cv2.imwrite(r'C:\Users\adesh\Desktop\imgex\enu.jpg', original_img)

# Display the result
    cv2.imshow('Blurred Background with Foreground', original_img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    #cv2 code end...
    retval, buffer = cv2.imencode('.png', original_img)

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

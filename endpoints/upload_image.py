from flask import Flask, request, jsonify, Blueprint
import base64
import rembg
import numpy as np
from PIL import Image
from io import BytesIO
from werkzeug.datastructures import FileStorage


bp = Blueprint('upload_image', __name__)

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
 




@bp.route('/upload_image', methods=['POST'])
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





    #input_array = file.read()
    #output_array = rembg.remove(input_array)

    img_str_bytes = base64.b64encode(output_image)
    image_byte_array = img_str_bytes.decode("utf-8")


    # Construct the response with message and byte array
    response_data = {
        'message': 'Image uploaded successfully as byte array',
        'image_byte_array': image_byte_array if image_byte_array else None
    }

    return jsonify(response_data), 200

if __name__ == '__main__':
    bp.run(debug=False) 

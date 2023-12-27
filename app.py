from flask import Flask
from endpoints import endpoint1, endpoint2, upload_image, newbg, blurimage

app = Flask(__name__)
#register blueprint for endpoint
app.register_blueprint(endpoint1.bp)
#app.register_blueprint(endpoint2.bp)
app.register_blueprint(upload_image.bp)
app.register_blueprint(newbg.bp)
app.register_blueprint(blurimage.bp)

if __name__ == "__main__":
    app.run(host='0.0.0.0')
from flask import Flask
from endpoints import  upload_image, blurimage
from endpoints import newbg, newbg2, newbg3, newbg4, newbg5, newbg6, newbg7, newbg8, newbg9, newbg10
from endpoints import newbg11, newbg12, newbg13, newbg14, newbg15, newbg16, newbg17, newbg18, newbg19

app = Flask(__name__)
#register blueprint for endpoint
#app.register_blueprint(endpoint2.bp)
app.register_blueprint(upload_image.bp)
app.register_blueprint(blurimage.bp)
app.register_blueprint(newbg.bp)
app.register_blueprint(newbg2.bp)
app.register_blueprint(newbg3.bp)
app.register_blueprint(newbg4.bp)
app.register_blueprint(newbg5.bp)
app.register_blueprint(newbg6.bp)
app.register_blueprint(newbg7.bp)
app.register_blueprint(newbg8.bp)
app.register_blueprint(newbg9.bp)
app.register_blueprint(newbg10.bp)
app.register_blueprint(newbg11.bp)
app.register_blueprint(newbg12.bp)
app.register_blueprint(newbg13.bp)
app.register_blueprint(newbg14.bp)
app.register_blueprint(newbg15.bp)
app.register_blueprint(newbg16.bp)
app.register_blueprint(newbg17.bp)
app.register_blueprint(newbg18.bp)
app.register_blueprint(newbg19.bp)

#app.register_blueprint(sketch.bp)


if __name__ == "__main__":
    app.run(host='0.0.0.0')
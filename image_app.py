from flask import Flask
from flask import render_template
from flask import request, redirect, url_for
from werkzeug.utils import secure_filename
import cv2 # temporary sol
from algos import cloneDetection as cd, ela, HSV, wavelets, lbp

app = Flask(__name__)



@app.route("/about")
def hello(name=None):
    return render_template('about.html')


# UPLOAD_FOLDER = 'uploads/'
ALLOWED_EXTENSIONS = set(['png','jpg','jpeg'])
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
JPEG = set(['jpg','jpeg'])

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def is_jpeg(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in JPEG


@app.route('/upload', methods=['GET', 'POST'])
@app.route('/', methods=['GET', 'POST'])
def upload_file():  #upload and check the file
    if request.method == 'POST':
        f = request.files['the_file'] # gets input image
        print (f), "type of f", type(f)
        method = request.form['method']
        print method
        if allowed_file(f.filename): #if file is a valid format, then do the processing
            # if method == something then do the appropriate image processing
            # process the image, then call the image together with the status
            in_pth = 'uploads/' + secure_filename(f.filename)
            f.save(in_pth)

            #  img_in = cv2.imread('uploads/' + secure_filename(f.filename))
            img_out = ''
            status = ''
            out_filename = f.filename.rsplit('.', 1)[0] \
                       + '_' + method + '.' \
                       + f.filename.rsplit('.', 1)[1].lower()
            out_pth = "static/images/" + out_filename  # name of output image
                                                                # depending on method chosen image.jpg -> image_ela.jpg
            print out_pth
            # cv2.imwrite(out_file, img_in)
            if method == "hsv": # note that HSV .py file uses PIL, so cannot use cv2.imread
                status = "Image is converted to HSV"
                HSV.HSV(in_pth, out_pth)
                pass
            elif method == "ela":
                status = "Error level analysis performed on this image"
                ela.ELA(in_pth, out_pth)

            elif method == "lbp":
                status = "Local Binary Patterns of this image"
                lbp.LBP(in_pth, out_pth)
                pass
            elif method == "dwt":  #
                status = "Discrete Wavelet Transform on this image"
                img_out = wavelets.w2d(in_pth, out_pth)
            elif method == "cd":  # returns the image and the status of the output
                status = cd.cloneDetection(in_pth, out_pth)  # returns an image and a status

            else:
                status = "This is an invalid image"
                pass  # we can return an error page

            # save image then load
            print "f.filename: ", f.filename
            print "secure_filename(f.filename)", secure_filename(f.filename)
            # cv2.imwrite("static/images/" + out_filename, img_out) #I think I should write this in the functions itself
            # out_filename = "galaxy.jpg"
            img_src = url_for('static', filename='images/%s' % out_filename) # no problem with this
            # return html that will display the image and the status
            return render_template("output.html", img_src=img_src, status = status)
            # return "Image: %s <br> Method: %s <br> %s" % (f.filename, method, str(img_in))

    return render_template("upload_new.html")

if __name__ == '__main__':
    app.run(port=5004)

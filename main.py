from unicodedata import name
import cv2
import numpy as np
from app import app
from flask import request, jsonify
from werkzeug.utils import secure_filename
from math import ceil
import pytesseract as pyt
from method_fund_boxes import convert_img_to_array as cita
from flask_cors import CORS

ALLOWED_EXTENSIONS = set(['jfif','txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def hello_world():
    return 'Hello World!'
       
@app.route('/cedula/file-upload/', methods=['POST'])
def upload_file():
	# check if the post request has the file part
    if 'file' not in request.files:
        resp = jsonify({'message' : 'No file part in the request'})
        resp.status_code = 400
        return resp
    file = request.files['file']
    if file.filename == '':
        resp = jsonify({'message' : 'No file selected for uploading'})
        resp.status_code = 400
        return resp
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        # file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        #im = image_from_buffer(filename)
        #gray  = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        filestr = file.read()
        npimg = np.fromstring(filestr, np.uint8)
        #npimg = numpy.fromstring(filestr, numpy.uint8)
        img = cv2.imdecode(npimg,cv2.IMREAD_COLOR)
        imageRGB = cv2.cvtColor(img , cv2.COLOR_BGR2RGB)
        #img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        #img_rgb = Image.frombytes('RGB', img_cv.shape[:2], img_cv, 'raw', 'BGR', 0, 0)
        #print(img)
        info = cita(imageRGB)
        
        #np.savetxt("datos.csv",img, delimiter=",")
        
        information = info[0]
        image_info = info[1]
        keys = info[2]

        names = keys[:,6]
        coordinates = keys[:,0:4]

        dir_info = {}
        i=0
        for i in range(len(information)):
            dir_info[names[i]] = {'text_ocr': information[i], 'x0': coordinates[i][0], 'x1': coordinates[i][2], 'y0': coordinates[i][1], 'y1': coordinates[i][3]}


        resp = jsonify({'information_cedulas':dir_info, 'Information_img': {'height': image_info[1], 'width': image_info[0]}})
        resp.status_code = 201
        return resp
    else:
        resp = jsonify({'message' : 'Allowed file types are txt, pdf, png, jpg, jpeg, gif'})
        resp.status_code = 400
        return resp
   



if __name__ == "__main__":
	app.run( host='0.0.0.0')

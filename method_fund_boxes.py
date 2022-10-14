from math import ceil
import pytesseract as pyt
import torch
from matplotlib import image, pyplot as plt
from PIL import Image


def ocr(bbox):
    # Lectura de los datos con Pytesseract
    im = bbox
    print(type(bbox))
    custom_oem_psm_config = r'--oem 1 --psm 6'
    text = pyt.image_to_string(im, lang='spa', config=custom_oem_psm_config)
    text = text.strip('\n\x0c')
    text = text.replace('\n', ' ')
    text = text.replace(' -', '-')
    text = text.replace('- ', '')
    text = text.replace('&L ', '')
    text = text.replace('Aa', '')
    print('Informacion de la fila: ' + text)
    return text



def convert_img_to_array(img):
    # Toma la imagen desde el webservice

    model = torch.hub.load('ultralytics/yolov5', 'custom',
                           path='best.pt', device='cpu')
    results = model(img)
    results = results.pandas().xyxy[0]
    
    m = results.to_numpy() #Transformar la matrix panda a numpy
    m = m[m[:, 5].argsort()]
    print(m)
    information = []

    y, x = img.shape[:2]
    shape = [x, y]
    print('Tamaño de la imagen', str(x), str(y))

    for i in range(len(m)):
        xmin = m[i, 0]
        ymin = m[i, 1]
        xmax = m[i, 2]
        ymax = m[i, 3]

        x0 = int(xmin)
        y0 = int(ymin)

        x1 = int(xmax)
        y1 = int(ymax)

        
        cortado = img[y0:y1 , x0:x1]
        
        cut = ocr(cortado)

        information.append(cut)

    print('Informacion general\n')
    return information, shape, m

if __name__ == "__main__":
    convert_img_to_array()

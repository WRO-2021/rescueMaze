import subprocess
from PIL import Image
import pytesseract
import numpy as np
import cv2

#con subprocess chiamo un comando bash, funziona solo sul raspberry che usavo
#poi pulisco un po' l'immagine e la analizzo, ho fatto copia-incolla da un sito per questo
#per farlo ci ho messo un bel po', soprattutto per fare una foto, visto che hanno aggiornato al nuovo debian e le vecchie librerie non funzionano

foto =subprocess.Popen(["libcamera-jpeg", "-o", "pyFoto.jpg" ,"-n" ,"--tuning-file","/usr/share/libcamera/ipa/raspberrypi/imx219_noir.json"])
foto.wait()
#print(foto.stdout)

pyFoto = 'pyFoto.jpg'
img= np.array(Image.open(pyFoto))


norm_img = np.zeros((img.shape[0], img.shape[1]))
img = cv2.normalize(img, norm_img, 0, 255, cv2.NORM_MINMAX)
img = cv2.threshold(img, 100, 255, cv2.THRESH_BINARY)[1]
img = cv2.GaussianBlur(img, (1, 1), 0)

text = pytesseract.image_to_string(img)

print(text)

import numpy as np
from PIL import Image

def process_pic():
    #Load the image
    image = Image.open("rawTrash.jpg")
    sample = image

    #Setup the dimensions to crop
    (hor, ver) = sample.size #Default picture from PiCam is 16:9 Aspect Ratio
    
    #3:2 Aspect Ratio
    area = (400,0,1640,960)

    #Crop the image based on the dimensions
    cropped = sample.crop(area)
    
    #Resize for backend, and save image
    cropped.resize((224,224), Image.ANTIALIAS).save("trash.jpg")


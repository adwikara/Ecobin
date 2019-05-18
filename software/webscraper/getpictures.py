import os
#https://github.com/hardikvasa/google-images-download
object = '"metal cans"'
number_pics = str(100)

cmd = "python google_images_download.py" + " -k " + object + " -l " + number_pics
print(cmd)

os.system(cmd)
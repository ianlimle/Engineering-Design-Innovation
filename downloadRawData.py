# -*- coding: utf-8 -*-
"""
Created on Wed Jan 16 17:40:46 2019

@author: Ian
"""

from PIL import Image
import urllib.request
import subprocess
import requests
import os

def get_file(url, local_filename):
    attempts = 0
    while attempts < 3:
        try:
            r = requests.get(url)
            with open(local_filename, 'wb') as f:  
                    f.write(r.content)
            f.close()
            img = Image.open(local_filename)

            break
        except:
            attempts += 1
            print("Attempt#" + str(attempts) + " - Failed to read from "+url)

    try:
        img = Image.open(local_filename)
        img.verify()
        
    except Exception as e:
        print(e)
        print(local_filename + " corrupted..deleting it..")
        subprocess.run(['rm', local_filename])

    return

pic_num = 1
if not os.path.exists('fish'):
    os.mkdir('fish')
    
with open("fish_raw.txt", "r") as txtfile:
    urls= txtfile.readlines()
    for url in urls:         
        get_file(url, "fish/"+str(pic_num)+".jpg")
        #img = cv2.imread("fish/"+str(pic_num)+".jpg",cv2.IMREAD_COLOR)
        # should be larger than samples / pos pic (so we can place our image on it)
        #resized_image = cv2.resize(img, (100,100))
        #cv2.imwrite("fish/"+str(pic_num)+".jpg",img)
        pic_num += 1
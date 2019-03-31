# ----------------------------------------------------------------------------------
# MIT License
#
# Copyright(c) Microsoft Corporation. All rights reserved.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# ----------------------------------------------------------------------------------
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.



import os, uuid, sys
from azure.storage.blob import BlockBlobService, PublicAccess
import os
import pygame, sys
import cognitive_face as CF
import requests
from io import BytesIO
from PIL import Image, ImageDraw

from pygame.locals import *
import pygame.camera

width = 640
height = 480

KEY = "c0ea04f0997447e8b83dcef3eca688cd"
CF.Key.set(KEY)
BASE_URL = 'https://westeurope.api.cognitive.microsoft.com/face/v1.0'  # Replace with your regional Base URL
CF.BaseUrl.set(BASE_URL)

def getRectangle(faceDictionary):
    rect = faceDictionary['faceRectangle']
    left = rect['left']
    top = rect['top']
    bottom = left + rect['height']
    right = top + rect['width']
    return ((left, top), (bottom, right))

def send_intruder_email(num_of_faces):

    gmail_user = 'ema.p25@gmail.com'
    gmail_password = 'vec132525'

    sent_from = gmail_user
    to = ['nikolaaleksic44@gmail.com']
    subject = 'Intruder Alert!'
    body = 'There\'s someone in the room! Camera sees %d people'%num_of_faces

    email_text = """Subject: %s\ %s""" % (subject, body)

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.login(gmail_user, gmail_password)
        # ...send emails
        server.sendmail(sent_from, to, email_text)
        server.close()

        print 'Email sent!'
    except:
        print 'Something went wrong...'

# ---------------------------------------------------------------------------------------------------------
# Method that creates a test file in the 'Documents' folder.
# This sample application creates a test file, uploads the test file to the Blob storage,
# lists the blobs in the container, and downloads the file with a new name.
# ---------------------------------------------------------------------------------------------------------
# Documentation References:
# Associated Article - https://docs.microsoft.com/en-us/azure/storage/blobs/storage-quickstart-blobs-python
# What is a Storage Account - http://azure.microsoft.com/en-us/documentation/articles/storage-whatis-account/
# Getting Started with Blobs-https://docs.microsoft.com/en-us/azure/storage/blobs/storage-python-how-to-use-blob-storage
# Blob Service Concepts - http://msdn.microsoft.com/en-us/library/dd179376.aspx
# Blob Service REST API - http://msdn.microsoft.com/en-us/library/dd135733.aspx
# ----------------------------------------------------------------------------------------------------------

#initialise pygame   
os.environ["SDL_VIDEODRIVER"] = "dummy"
pygame.init()
pygame.camera.init()
cam = pygame.camera.Camera("/dev/video0",(width,height))
cam.start()
cnt = 0

#setup window
windowSurfaceObj = pygame.display.set_mode((width,height),1,16)
pygame.display.set_caption('Camera')

while cnt < 5:
    try:
        # Create the BlockBlockService that is used to call the Blob service for the storage account
        block_blob_service = BlockBlobService(account_name='csb61e6613152abx4a5dxbd0', account_key='glQnTM179qQcEckkbAgOBw6PmcMrFA/BkqoOu7g2RS2TilooNHHOnLP3rpIWtJpzd8YbS37+KX4rdTJIIkoxWg==')

        # Create a container called 'quickstartblobs'.
        container_name ='quickstartblobs'
        block_blob_service.create_container(container_name)

        # Set the permission so the blobs are public.
        block_blob_service.set_container_acl(container_name, public_access=PublicAccess.Container)

        # Create a file in Documents to test the upload and download.
        #take a picture
        image = cam.get_image()
        catSurfaceObj = image
        windowSurfaceObj.blit(catSurfaceObj,(0,0))

        local_file_name = "mi"+str(cnt)+".jpg"
        pygame.image.save(windowSurfaceObj,'mi'+str(cnt)+'.jpg')
        cnt += 1
        local_path=os.path.abspath(os.path.curdir)
        full_path_to_file = os.path.join(local_path, local_file_name)

	img_url = full_path_to_file
	faces = CF.face.detect(img_url, attributes='age')
	if(len(faces) > 0 and cnt % 5 == 0):
		send_intruder_email(len(faces))
	#Download the image from the url
	#response = requests.get(img_url)
	img = Image.open(full_path_to_file)

	#For each face returned use the face rectangle and draw a red box.
	draw = ImageDraw.Draw(img)
	for face in faces:
    		draw.rectangle(getRectangle(face), outline='red')
    		#print(face)

	#Display the image in the users default image browser.
	img.save(full_path_to_file)

        print("Temp file = " + full_path_to_file)
        print("\nUploading to Blob storage as blob" + local_file_name)

        # Upload the created file, use local_file_name for the blob name
        block_blob_service.create_blob_from_path(container_name, local_file_name, full_path_to_file)

    except Exception as e:
        print(e)

cam.stop()




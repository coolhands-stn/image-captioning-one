from PIL import Image
from os.path import join, dirname, realpath
from glob import glob

import streamlit as st
import numpy as np
# import tensorflow as tf
import numpy as np

import os
import cv2
import imutils

# Loading images to frontend
def load_image(image_file):
	img = Image.open(image_file)
	return img

st.text("Stany Ganyani R204442S")

# User search query
search_query = st.text_input("enter object to query", "search query",key="search_query" )

# Allow user to upload video
video = st.file_uploader(label="upload video", type="mp4", key="video_upload_file")

# Continue only if video is uploaded successfully
if(video is not None):
    # Notify user
    st.text("video has been uploaded")
    # Gather video meta data
    file_details = {"filename":video.name, "filetype":video.type,
                    "filesize":video.size}
    # Show on ui
    st.write(file_details)
    # save video
    with open(video.name, "wb") as f:
        f.write(video.getbuffer())
    # Notify user
    st.success("file saved")

    # Show video on ui 
    video_file = open(file_details['filename'], 'rb')
    video_bytes = video_file.read()
    st.video(video_bytes)

    st.write('uploaded video right now')

    # Create frames for the video and save 
    def create_frames():
        images_array = []
        cap = cv2.VideoCapture(video.name)
        index = 0

        while True:
            ret, frame = cap.read()
            if ret == False:
                cap.release()
                break
            if frame is None:
                break
            else:
                if index == 0:
                    images_array.append(frame)
                    cv2.imwrite(f"frames/{index}.jpeg", frame)

                else:
                    if index % 10 == 0:
                        images_array.append(frame)
                    cv2.imwrite(f"frames/{index}.jpeg", frame)

            index += 1
        return np.array(images_array)
    

    # Create frames
    # create_frames()
    images_array = create_frames()

    # Continue only if frames have been successfully created 
    if len(images_array) > 0:
        frame_paths = glob(f"frames/*.jpeg")
        for path in frame_paths:
            st.image(load_image(path),width=250)
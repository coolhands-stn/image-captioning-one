import streamlit as st 
from PIL import Image
from os.path import join, dirname, realpath
from glob import glob
import numpy as np
import os
import cv2,imutils

from transformers import GPT2TokenizerFast, ViTImageProcessor, VisionEncoderDecoderModel

st.text("IMAGE CAPTIONING : Stany Ganyani R204442S")

# Frames path
FRAMES = join(dirname(realpath(__file__)), "frames")

def load_image(image_file):
	img = Image.open(image_file)
	return img

#  upload video
video = st.file_uploader(label="upload video", type="mp4", key="video_upload_file")

# Continue only if video is uploaded successfully
if(video is not None):
    # Remove pre-existing FRAMES dir
    if os.path.exists(FRAMES):
        frame_paths = glob(f"frames/*.jpeg")
        # Remove every file
        for path in frame_paths:
            os.remove(path)
        os.rmdir(FRAMES)
        st.write('Removed pre-exisiting frames dir')
	    
    # Notify user
    st.text("Video has been uploaded")
    # Gather video meta data
    file_details = {
        "filename":video.name, 
        "filetype":video.type,
        "filesize":video.size
    }
    # Show on ui
    st.write(file_details)
    # save video
    with open(video.name, "wb") as f:
        f.write(video.getbuffer())
    
    st.success("Video saved")

    video_file = open(file_details['filename'], 'rb')
    video_bytes = video_file.read()
    st.video(video_bytes)

    def create_frames():

        # Create frames directory
        os.makedirs(FRAMES)

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

    # Invoke Function to create frames
    images_array = create_frames()

    # Continue only if frames have been successfully created 
    # if len(images_array) > 0:
    #     frame_paths = glob(f"frames/*.jpeg")
    #     for path in frame_paths:
    #         st.image(load_image(path), width=250)

    def generate_caption(image_path):
        # Loading the model and it's helper components
        model_raw = VisionEncoderDecoderModel.from_pretrained("nlpconnect/vit-gpt2-image-captioning")
        image_processor = ViTImageProcessor.from_pretrained("nlpconnect/vit-gpt2-image-captioning")
        tokenizer = GPT2TokenizerFast.from_pretrained("nlpconnect/vit-gpt2-image-captioning")

        image = Image.open(image_path)
        pixel_values   = image_processor(image, return_tensors ="pt").pixel_values

        generated_ids  = model_raw.generate(
            pixel_values,
            do_sample=True,
            max_new_tokens = 30,
            top_k=5
        )
        generated_text = tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]
        st.write(generated_text)

    
    if len(images_array) > 0:
        frame_paths = glob(f"frames/*.jpeg")
        for path in frame_paths:
            caption = generate_caption(path)
            st.image(load_image(path), caption=caption, width=250)
            # break


import streamlit as st
from transformers import AutoModel
import numpy as np
from PIL import Image
import torch
import os
def read_image_as_np_array(image_path):
    with open(image_path, "rb") as file:
        image = Image.open(file).convert("L").convert("RGB")
        image = np.array(image)
    return image

def load_model():
    model = AutoModel.from_pretrained("ragavsachdeva/magi", trust_remote_code=True).cuda()
    return model
uploaded_file = st.file_uploader("Choose an image...", type="jpg")
if uploaded_file is not None:
    image = read_image_as_np_array(uploaded_file)
model = load_model()
with torch.no_grad():
    results = model.predict_detections_and_associations([image])
    text_bboxes_for_all_images = [x["texts"] for x in results]
    ocr_results = model.predict_ocr([image], text_bboxes_for_all_images)
    st.write(ocr_results)

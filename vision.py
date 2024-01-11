# Q&A Chatbot
#from langchain.llms import OpenAI

from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.

import streamlit as st
import os
import pathlib
import textwrap
from PIL import Image
from uuid import uuid4


import google.generativeai as genai


os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

## Function to load OpenAI model and get respones

def get_gemini_response(input_text,image,prompt):
    # Validate inputs
    if not input_text or not image or not prompt:
        raise ValueError("All parameters must be provided and non-empty")

    # Load the model
    model = genai.GenerativeModel('gemini-pro-vision')

    # Ensure the image parameter is a list and has at least one item
    if not isinstance(image, list) or len(image) == 0:
        raise ValueError("Image parameter must be a list with at least one item")

    # Generate content
    try:
        response = model.generate_content([input_text, image[0],prompt])
    except Exception as e:
        print(f"An error occurred while generating content: {e}")
        return None

    # Return the generated text
    return response.text

def input_image_setup(uploaded_file):
    # Check if a file has been uploaded
    if uploaded_file is not None:
        # Read the file into bytes
        bytes_data = uploaded_file.getvalue()

        image_parts = [
            {
                "mime_type": uploaded_file.type,  # Get the mime type of the uploaded file
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")


##initialize our streamlit app

st.set_page_config(page_title="Gemini Image Demo")

st.header("Gemini Application")
input=st.text_input("Input Prompt: ",key="input")
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
image=""   
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image.", use_column_width=True)


submit=st.button("Tell me about the image")

input_prompt = """
               You are an expert in understanding image.
               You will receive input images
               and you need to extract the exact text from the image
               """

## If ask button is clicked



import requests
from uuid import uuid4

def translate_text(text):
    key = "f3a47cba04864b638e74f100019a703b"
    endpoint = "https://api.cognitive.microsofttranslator.com"
    location = "southeastasia"

    try:
        response = requests.post(
            f"{endpoint}/translate",
            json=[{"text": text}],
            headers={
                "Ocp-Apim-Subscription-Key": key,
                "Ocp-Apim-Subscription-Region": location,
                "Content-type": "application/json",
                "X-ClientTraceId": str(uuid4()),
            },
            params={
                "api-version": "3.0",
                "fromLang": "en",
                "to": "or"
            }
        )
        
        response.raise_for_status()  # Raise an error for unsuccessful responses

        result = response.json()
        return result[0]['translations'][0]['text']
    except requests.exceptions.RequestException as e:
        print(f"Translation error: {e}")


if submit:
    image_data = input_image_setup(uploaded_file)
    response=get_gemini_response(input_prompt,image_data,input)
    st.subheader("The Response is")


    
    st.write(translate_text(response))
